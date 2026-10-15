# VesselMind

**Context-aware vessel behaviour modelling from historical AIS: reproducible baselines, prediction and anomaly analysis.**

> **Status:** V1 research prototype (started 9 Oct 2026). Hypotheses frozen 11 Oct; single post-freeze test run done.
> Everything in this repository is historical research playback. It is not a real-time or safety-certified system.

---

## ⚠️ Before making this repository public (delete this whole section when done)

The repo is **private** until every box below is ticked. Items marked **(Kiran)** need your own words or judgement;
items marked **(Claude)** are mechanical and wait only for your go-ahead.

**Remove private material**
- [ ] **(Claude, needs your OK)** Remove `docs/proposal/` (proposal .docx + .pdf) from the working tree **and from git
      history** (it is in the first commit, `39e810d`). This rewrites every commit hash and needs a force push.
      Commit hashes quoted in the docs (`f1b61da`, `e80e7aa`, `2ae4ece` …) must be updated afterwards.
- [ ] **(Kiran)** Decide whether `docs/00_plan.md` (application timeline) and `docs/09_open_questions.md` stay public.
      Removing them is fine; editing them to a neutral "project plan" is also fine.

**Replace scaffolding with your own words**
- [ ] **(Kiran)** `paper/preliminary_summary.md`: rewrite every section, then delete the
      "OUTLINE, written by Claude as scaffolding" banner at the top.
- [ ] **(Kiran)** `docs/01_problem.md`: rewrite the motivation paragraph (the `TODO (Kiran)` note).
- [ ] **(Kiran)** `docs/02_literature.md`: check every claim against the paper itself, then remove the
      "UNVERIFIED DRAFT" status line. If there is no time, leave the banner in; an honest "unverified" beats a wrong citation.

**Fix stale or incomplete facts**
- [ ] **(Kiran)** `docs/03_data_card.md`: fill the two `TODO`s: the DMA licence / terms of use (with the date you
      checked) and the frozen area of interest.
- [ ] **(Claude)** `docs/06_results.md`: the header still says the test split is locked; add the test results.
- [ ] **(Kiran)** Choose a licence (MIT is the usual choice for research code) so others may reuse it, and Claude
      adds `LICENSE`. Data is not redistributed, so the DMA terms only need to be cited.

**Final checks**
- [ ] **(Claude)** Fresh clone into an empty folder → `uv sync` → `uv run pytest` → `make smoke` all pass.
- [ ] **(Claude)** Scan tracked files for local paths, emails and secrets (last scan, 15 Oct: none found; all commits
      use the GitHub no-reply address).
- [ ] **(Kiran)** Read this README top to bottom as if you were the hiring committee.
- [ ] **(Kiran)** Flip visibility on GitHub (Settings → General → Danger zone → Change visibility), then open the repo
      logged out to check the link in the CV and cover letter works.
- [ ] Delete this section and commit.

---

## Research question

Does vessel and geographic context improve 5–20-minute trajectory prediction beyond transparent kinematic and
motion-only learned baselines, in which manoeuvring regimes, and does the gain transfer to unseen vessels and unseen
waters?

See [docs/01_problem.md](docs/01_problem.md) and [docs/05_protocol.md](docs/05_protocol.md).

## Data

Danish Maritime Authority historical AIS, 19 Sep – 6 Oct 2026 (18 days), Great Belt / Øresund / southern Kattegat,
Class A only: 63.3 M rows → 359,738 prediction windows (20-min history → 20-min forecast) from 1,971 vessels.
Whole-day time split: train 19–30 Sep, validation 1–3 Oct, test 4–6 Oct. See [docs/03_data_card.md](docs/03_data_card.md).

## Results (test split, single run after the hypothesis freeze)

![Error at 20 minutes for each model in three settings](results/figures/generalisation_test.png)

Mean final displacement error at 20 minutes (FDE@20, metres), 57,068 test windows:

| Model | In-area | Unseen vessels | Unseen waters |
|---|---|---|---|
| Constant velocity (CV) | 1,554 | 1,554 | 1,554 |
| A: motion only | 1,267 | 1,429 | 1,465 |
| B: + vessel attributes | 1,128 | 1,367 | 1,442 |
| C: + location | 863 | 1,165 | 2,592 |
| D: all | **831 (−47%)** | 1,140 (−27%) | 1,918 (+23%) |

1. **Kinematic refinements do not beat constant velocity.** CTRV is worse (+467 m); damped CTRV and a Kalman filter
   converge to CV. Turns in these waters are short, so the latest reported state beats extrapolating history.
2. **Motion-only learning helps most where kinematics fail**, especially in combined turning-and-speed-change manoeuvres.
3. **Location context gives the largest in-area gain**, in every manoeuvring regime and under every threshold choice.
4. **But it is memorised geography.** The gain survives on vessels never seen in training, yet **reverses in waters
   never seen in training** (+1,127 m vs motion-only). Raw coordinates do not transfer.

| Hypothesis (frozen 11 Oct) | Test outcome |
|---|---|
| H1 Motion-only learning beats CV, most in non-steady regimes | Supported |
| H2 Vessel context helps beyond motion | Supported in-area; weak for unseen vessels; absent in unseen waters |
| H3 Geographic context > vessel context when turning | Supported |
| H4 Geographic gain shrinks in unseen areas but stays positive | **Rejected** |
| H4b Raw-coordinate context does not transfer (drafted after validation) | Supported |

Validation and test agree within ~25 m on every headline number. Full tables: [docs/06_results.md](docs/06_results.md)
and [results/tables/](results/tables/). Limitations: [docs/07_limitations.md](docs/07_limitations.md).
Preliminary write-up: [paper/preliminary_summary.md](paper/preliminary_summary.md).

**What this motivates:** transferable representations of navigational context (fairway geometry, traffic-flow fields,
bathymetry) that work in waters without training data.

## Quick start

```bash
uv sync                                   # Python 3.12 environment
uv run pytest                             # unit tests
make smoke                                # full pipeline on SYNTHETIC data (isolated workspace)
```

Real data (Danish Maritime Authority historical AIS):

```bash
# 1. Download the daily files into data/raw/ (see data/README.md), then:
uv run vesselmind manifest data/raw/aisdk-YYYY-MM-DD.zip --notes "..."
make pipeline                             # ingest -> clean -> windows -> baselines (validation split)
uv run vesselmind gbm                     # learned residual model + context ablation (validation)
```

## Pipeline

```
raw zip/CSV (immutable, checksummed manifest)
  -> ingest:    AOI + Class A filter, schema cast          data/interim/*.parquet
  -> clean:     sentinels -> null, quality flags, segments  data/processed/tracks.parquet, vessels.parquet
  -> windows:   1-min resampling, 20-min history / 20-min future, gap-safe windows, time-block split
  -> models:    persistence, CV, CTRV, damped CTRV, CV Kalman; gradient-boosted residual on CV (feature sets A–D)
  -> evaluate:  one shared evaluator: ADE/FDE, per-horizon error, paired comparisons, vessel-grouped bootstrap CIs
  -> generalise: vessel-held-out (with same-size control), spatially held-out (4 longitude bands), regime breakdown
```

## Repository layout

| Path | Contents |
|---|---|
| `src/vesselmind/` | `ingestion/ quality/ trajectories/ features/ models/ anomaly/ evaluation/ viz/`, `cli.py` |
| `configs/` | `data.yaml` (source, AOI, quality, segmentation), `experiment.yaml` (windows, split, baselines) |
| `data/` | `raw/ interim/ processed/` (git-ignored), `manifests/` (committed provenance) |
| `docs/` | problem, literature, data card, methods, protocol, results, limitations, research log |
| `paper/` | preliminary research summary |
| `results/` | `tables/`, `figures/`, `runs/<timestamp>/summary.json` |
| `tests/` | unit tests for geodesy, quality flags, segmentation, windows, split and metrics |

## Principles

- Raw data is never modified. Suspicious points are flagged, not silently deleted.
- Splits are by time block. No window crosses a split boundary, and transforms are fit on training data only.
- The test split is locked (`--confirm-test`) and was run once, after hypotheses were frozen.
- Negative results are reported (H4 was rejected). Synthetic anomaly labels are always labelled as synthetic.

## Acknowledgement of tools

Implementation was assisted by an AI coding assistant (Claude). Research questions, protocol decisions,
interpretation and writing are the author's own.
