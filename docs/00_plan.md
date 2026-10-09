# 00 — Project plan

**Objective:** Test whether vessel context (type, size, manoeuvring regime) improves 5/10/20-minute trajectory
prediction over transparent kinematic baselines, using 18 days of real Danish AIS (19 Sep – 6 Oct 2026).

**Application:** NTNU PhD (AI for ship traffic monitoring) asks for a CV and cover letter only.
Plan: **apply Fri 16 Oct 2026** with a public repo and a preliminary summary linked from both documents.
After that, keep building towards the interview (deeper results plus a live demo).

## Phase 1: Application-ready (9–16 Oct)

| Day | Kiran (research owner) | Claude (engineering) |
|---|---|---|
| Fri 9 ✅ | Repo, 18-day dataset, frozen split | Pipeline, quality, baselines on 359k windows |
| Fri 9 eve / Sat 10 | Read R1–R4, fill literature matrix | Regime-support figures (turn-rate and speed distributions, turn hotspots) |
| Sat 10 | **Define manoeuvring regimes** | E0 gap-threshold sensitivity, paired CV-vs-CTRV CI, CTRV failure diagnosis |
| Sun 11 | Draft H1–H3, cover letter v1 | Implement regimes, baselines by regime and ship type |
| Mon 12 | **Freeze hypotheses** (commit), CV project entry | Gradient-boosting predictor (motion-only) |
| Tue 13 | Review results, decide headline | **Context ablation with GBM**: motion-only vs + ship type/size |
| Wed 14 | Write the preliminary summary (Claude drafts figures and tables) | Figures, README polish |
| Thu 15 | Final cover letter + CV with repo link | Remove the proposal from git history, make the repo public, final checks |
| **Fri 16** | **Submit application** | — |

**The preliminary summary (1–2 pages, `paper/preliminary_summary.md`/PDF) contains:** problem, data and quality
numbers, method, split, validation results (baselines, regime breakdown, GBM context ablation), what's next.
All numbers are labelled *validation, preliminary*. The test set stays locked.

## Phase 2: Interview-ready (17 Oct onwards)

| Window | Work |
|---|---|
| 17–21 Oct | GRU (motion-only vs + context), 3 seeds, uncertainty output |
| 22–24 Oct | Synthetic anomaly benchmark (speed, turn, route-offset, residual signals) |
| ~25 Oct | **One-time test-set run** after the protocol is final; numbers frozen |
| 26–30 Oct | V1 report (6–10 pages), figure set |
| Nov | Demo for the interview: historical playback map, predicted vs actual tracks, anomaly overlays |
| On interview call | Prepare a 10-minute walkthrough: question → data → why the baselines → results → limits → PhD direction |

## Fallback
If something slips before 16 Oct, apply with data quality + baselines + the regime analysis. That is already an honest,
complete piece of work. The application does not wait for the learned model.
