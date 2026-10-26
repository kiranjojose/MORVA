"""Apply the frozen V3 decision rules (docs/05_protocol.md, frozen in 126dda2) to saved run summaries.

Written before any V3 test result existed. It only reads `<results>/runs/*/summary.json`; it fits nothing and changes
nothing. For the test split it requires exactly one run per command (the single test pass) and refuses otherwise.

    uv run python scripts/v3_decide.py results/v3 --split test            # the confirmatory decision
    uv run python scripts/v3_decide.py results/v3 --split val --latest    # check against validation (reruns exist)
"""

import argparse
import glob
import json
from pathlib import Path

TOLERANCE = 0.03                    # V3-H3 and V3-H4: within +-3 percentage points of nominal
LEVELS = ("0.8", "0.9")
HORIZONS = ("20", "60")             # minutes; 60 is the final horizon (FDE)
LOCAL_REGIONS = ("bornholm", "skagen", "salish_sea")
PRIMARY_REGION = "salish_sea"


def load(results: Path, name: str, latest: bool) -> tuple[dict | None, str | None]:
    """The run summary whose folder ends in `_{name}`; with latest=False exactly one must exist."""
    runs = sorted(glob.glob(str(results / "runs" / f"*_{name}" / "summary.json")))
    if not runs:
        return None, None
    if len(runs) > 1 and not latest:
        raise SystemExit(f"{len(runs)} runs match '{name}'; the test pass allows exactly one (use --latest only "
                         "for validation checks)")
    return json.loads(Path(runs[-1]).read_text()), Path(runs[-1]).parent.name


def paired(summary: dict, comparison: str, horizon: str) -> dict:
    metric = "fde_m" if horizon == "60" else f"err_{horizon}min_m"
    return summary["paired"][comparison][metric]


def decide(results: Path, split: str, latest: bool = False) -> dict:
    """Outcome of V3-H1 to V3-H4. Each check records its value, the rule and whether it passes. A hypothesis is
    'supported' only if every check passes, 'not supported' if any fails, and 'undecided' if a run is missing."""
    transfer = f"transfer_{split}"
    out = {"split": split, "runs": {}, "hypotheses": {}}

    def hyp(name, checks, missing):
        if missing:
            outcome = "undecided (missing runs: " + ", ".join(missing) + ")"
        else:
            outcome = "supported" if all(c["pass"] for c in checks) else "not supported"
        out["hypotheses"][name] = {"outcome": outcome, "checks": checks}

    gbm, run = load(results, f"gbm_{transfer}_{PRIMARY_REGION}", latest)
    out["runs"]["gbm_salish_sea"] = run
    for name, comparison, rule in (("V3-H1", "E_fairway - A_motion", "upper < 0"),
                                   ("V3-H2", "C_location - A_motion", "lower > 0")):
        checks = []
        if gbm:
            for h in HORIZONS:
                x = paired(gbm, comparison, h)
                ok = x["ci95_hi"] < 0 if rule == "upper < 0" else x["ci95_lo"] > 0
                checks.append({"check": f"{comparison} at {h} min, 95% CI {rule}", "mean": x["mean"],
                               "ci95_lo": x["ci95_lo"], "ci95_hi": x["ci95_hi"], "pass": bool(ok)})
        hyp(name, checks, [] if gbm else [f"gbm_{transfer}_{PRIMARY_REGION}"])

    def coverage_checks(names):
        checks, missing = [], []
        for label, name in names:
            r, run = load(results, f"intervals_E_fairway_{name}", latest)
            out["runs"][f"intervals_{label}"] = run
            if r is None:
                missing.append(f"intervals_E_fairway_{name}")
                continue
            for lvl in LEVELS:
                for h in HORIZONS:
                    c = r["intervals"][lvl][h]["coverage"]
                    checks.append({"check": f"{label}: {float(lvl):.0%} box at {h} min within ±3 points",
                                   "coverage": c, "nominal": float(lvl),
                                   "pass": bool(round(abs(c - float(lvl)), 9) <= TOLERANCE)})
        return checks, missing

    checks, missing = coverage_checks([(r, f"{transfer}_{r}_localcal") for r in LOCAL_REGIONS])
    hyp("V3-H3", checks, missing)
    checks, missing = coverage_checks([("home", split)])
    hyp("V3-H4", checks, missing)
    return out


def num(x: float) -> str:
    """Signed metres with a true minus sign, as in the docs."""
    return f"{x:+,.0f}".replace("-", "\u2212")


def to_markdown(d: dict) -> str:
    lines = [f"# V3 decision ({d['split']})", "", "Runs: " + ", ".join(f"`{v}`" for v in d["runs"].values() if v),
             "", "| Hypothesis | Outcome |", "|---|---|"]
    lines += [f"| {k} | **{v['outcome']}** |" for k, v in d["hypotheses"].items()]
    for k, v in d["hypotheses"].items():
        lines += ["", f"## {k}", "", "| Check | Value | Pass |", "|---|---|---|"]
        for c in v["checks"]:
            if "coverage" in c:
                val = f"{c['coverage']:.1%} (nominal {c['nominal']:.0%})"
            else:
                val = f"{num(c['mean'])} m ({num(c['ci95_lo'])} to {num(c['ci95_hi'])})"
            lines.append(f"| {c['check']} | {val} | {'yes' if c['pass'] else 'NO'} |")
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("results", type=Path, help="results directory, e.g. results/v3")
    ap.add_argument("--split", default="test", choices=["val", "test"])
    ap.add_argument("--latest", action="store_true", help="use the latest of several runs (validation checks only)")
    ap.add_argument("--write", type=Path, help="also write the markdown and a .json next to it")
    args = ap.parse_args(argv)
    if args.split == "test" and args.latest:
        raise SystemExit("--latest is not allowed for the test split: the test pass has exactly one run per command")
    d = decide(args.results, args.split, args.latest)
    md = to_markdown(d)
    print(md)
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(md)
        args.write.with_suffix(".json").write_text(json.dumps(d, indent=2) + "\n")


if __name__ == "__main__":
    main()
