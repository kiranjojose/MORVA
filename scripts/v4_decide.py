"""Apply the V4 decision rules (docs/05_protocol.md, "V4 hypotheses") to saved run summaries.

Written on 6 Nov 2026, before the V4 freeze and before any V4 test data existed. If the rules change at the freeze,
this script changes with them in the same commit. It only reads `<results>/runs/*/summary.json`; it fits nothing and
changes nothing. For the test split it requires exactly one run per command (the single test pass) and refuses
otherwise.

    uv run python scripts/v4_decide.py results/v4 --split test            # the confirmatory decision
    uv run python scripts/v4_decide.py results/v4 --split val --latest    # check against validation (reruns exist)
"""

import argparse
import glob
import json
from pathlib import Path

TOLERANCE = 0.03                    # V4-H3: within +-3 percentage points of nominal
LEVELS = ("0.8", "0.9")
HORIZONS = ("20", "60")             # minutes; 60 is the final horizon (FDE)
TRANSFER_REGIONS = ("oslofjord", "skagen")
ALPHA = "0.05"                      # V4-H4
DEV_HORIZON = "20"                  # V4-H4: minutes (= knot steps at one-minute resolution)
DEV_SCENARIOS = ("turn_30", "turn_60", "turn_90", "stop", "slow_50pct", "fast_150pct")
RULES = ("cv_distance", "turn", "speed")
CONTROL = ("none", 0.04, 0.06)      # V4-H4: the unchanged copy is flagged at 5% +- 1 point
EQUIVALENCE_M = 150.0               # V4-H5: the 95% CI of H - E at 60 min lies inside +-150 m


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
    """Outcome of V4-H1 to V4-H5. Each check records its value, the rule and whether it passes. A hypothesis is
    'supported' only if every check passes, 'not supported' if any fails, and 'undecided' if a run is missing."""
    transfer = f"transfer_{split}"
    out = {"split": split, "runs": {}, "hypotheses": {}}

    def hyp(name, checks, missing):
        if missing:
            outcome = "undecided (missing runs: " + ", ".join(missing) + ")"
        else:
            outcome = "supported" if all(c["pass"] for c in checks) else "not supported"
        out["hypotheses"][name] = {"outcome": outcome, "checks": checks}

    gbm = {}
    for r in TRANSFER_REGIONS:
        gbm[r], out["runs"][f"gbm_{r}"] = load(results, f"gbm_{transfer}_{r}", latest)
    for name, comparison, rule in (("V4-H1", "E_fairway - A_motion", "upper < 0"),
                                   ("V4-H2", "C_location - A_motion", "lower > 0")):
        checks, missing = [], []
        for r in TRANSFER_REGIONS:
            if gbm[r] is None:
                missing.append(f"gbm_{transfer}_{r}")
                continue
            for h in HORIZONS:
                x = paired(gbm[r], comparison, h)
                ok = x["ci95_hi"] < 0 if rule == "upper < 0" else x["ci95_lo"] > 0
                checks.append({"check": f"{r}: {comparison} at {h} min, 95% CI {rule}", "mean": x["mean"],
                               "ci95_lo": x["ci95_lo"], "ci95_hi": x["ci95_hi"], "pass": bool(ok)})
        hyp(name, checks, missing)

    checks, missing = [], []
    for label, name in [("home", split), *[(r, f"{transfer}_{r}_localcal") for r in TRANSFER_REGIONS]]:
        iv, out["runs"][f"intervals_{label}"] = load(results, f"intervals_E_fairway_{name}", latest)
        if iv is None:
            missing.append(f"intervals_E_fairway_{name}")
            continue
        for lvl in LEVELS:
            for h in HORIZONS:
                c = iv["intervals"][lvl][h]["coverage"]
                checks.append({"check": f"{label}: {float(lvl):.0%} box at {h} min within ±3 points",
                               "coverage": c, "nominal": float(lvl),
                               "pass": bool(round(abs(c - float(lvl)), 9) <= TOLERANCE)})
    hyp("V4-H3", checks, missing)

    dev, out["runs"]["deviation_home"] = load(results, f"deviation_E_fairway_{split}", latest)
    checks = []
    if dev:
        res = dev["results"]
        for sc in DEV_SCENARIOS:
            for rule in RULES:
                x = res[sc]["model_minus_rule"][ALPHA][rule][DEV_HORIZON]
                checks.append({"check": f"{sc}: model − {rule} detection at {DEV_HORIZON} min, 95% CI lower > 0",
                               "rate_gap": x["mean"], "ci95_lo": x["ci95_lo"], "ci95_hi": x["ci95_hi"],
                               "pass": bool(x["ci95_lo"] > 0)})
        name, lo, hi = CONTROL
        fa = res[name]["model_box"][ALPHA]["per_horizon"][DEV_HORIZON]["false_alarm_rate"]
        checks.append({"check": f"control: model false alarms at {DEV_HORIZON} min within {lo:.0%}–{hi:.0%}",
                       "rate": fa, "pass": bool(lo <= fa <= hi)})
    hyp("V4-H4", checks, [] if dev else [f"deviation_E_fairway_{split}"])

    home, out["runs"]["gbm_home"] = load(results, f"gbm_{split}", latest)
    checks = []
    if home:
        x = paired(home, "H_wind_current - E_fairway", "60")
        checks.append({"check": f"home: H_wind_current − E_fairway at 60 min, 95% CI inside ±{EQUIVALENCE_M:.0f} m",
                       "mean": x["mean"], "ci95_lo": x["ci95_lo"], "ci95_hi": x["ci95_hi"],
                       "pass": bool(-EQUIVALENCE_M < x["ci95_lo"] and x["ci95_hi"] < EQUIVALENCE_M)})
    hyp("V4-H5", checks, [] if home else [f"gbm_{split}"])
    return out


def num(x: float) -> str:
    """Signed metres with a true minus sign, as in the docs."""
    return f"{x:+,.0f}".replace("-", "−")


def pts(x: float) -> str:
    return f"{100 * x:+.1f}".replace("-", "−")


def to_markdown(d: dict) -> str:
    lines = [f"# V4 decision ({d['split']})", "", "Runs: " + ", ".join(f"`{v}`" for v in d["runs"].values() if v),
             "", "| Hypothesis | Outcome |", "|---|---|"]
    lines += [f"| {k} | **{v['outcome']}** |" for k, v in d["hypotheses"].items()]
    for k, v in d["hypotheses"].items():
        lines += ["", f"## {k}", "", "| Check | Value | Pass |", "|---|---|---|"]
        for c in v["checks"]:
            if "coverage" in c:
                val = f"{c['coverage']:.1%} (nominal {c['nominal']:.0%})"
            elif "rate_gap" in c:
                val = f"{pts(c['rate_gap'])} points ({pts(c['ci95_lo'])} to {pts(c['ci95_hi'])})"
            elif "rate" in c:
                val = f"{c['rate']:.1%}"
            else:
                val = f"{num(c['mean'])} m ({num(c['ci95_lo'])} to {num(c['ci95_hi'])})"
            lines.append(f"| {c['check']} | {val} | {'yes' if c['pass'] else 'NO'} |")
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("results", type=Path, help="results directory, e.g. results/v4")
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
