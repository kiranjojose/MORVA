"""Draw the V3 test summary figure from saved run summaries (post-test reporting only).

Reads the single locked test pass in `<results>/runs/` (exactly one run per command, as in v3_decide) and plots values
already reported in docs/06_results.md: paired E - A error differences at 20 and 60 minutes, and 60-minute coverage of
model E's 80% and 90% boxes under home and local calibration. It fits and recomputes nothing.

    uv run python scripts/v3_figure.py results/v3 results/v3/figures/v3_summary_test.png
"""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from v3_decide import load  # noqa: E402

REGIONS = [("Home", None), ("Bornholm", "bornholm"), ("Skagen", "skagen"), ("Salish Sea", "salish_sea"),
           ("Houston", "houston")]
BASE, LIGHT, ACCENT, INK, MUTED = "#2a78d6", "#9cc3ef", "#eb6834", "#0b0b0b", "#52514e"


def run(results: Path, name: str) -> dict:
    summary, _ = load(results, name, latest=False)
    if summary is None:
        raise SystemExit(f"missing run: {name}")
    return summary


def interval(x: dict) -> tuple[float, list[list[float]]]:
    return x["mean"], [[x["mean"] - x["ci95_lo"]], [x["ci95_hi"] - x["mean"]]]


def style(ax, title: str, xlabel: str) -> None:
    ax.set_title(title, fontsize=10, color=INK, loc="left")
    ax.set_xlabel(xlabel, fontsize=8, color=MUTED)
    ax.grid(axis="x", alpha=0.25)
    ax.tick_params(axis="x", labelsize=8, colors=MUTED)
    ax.tick_params(axis="y", length=0)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)


def figure(results: Path, out: Path) -> Path:
    y = np.arange(len(REGIONS))[::-1].astype(float)
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.4), sharey=True, gridspec_kw={"width_ratios": [1.4, 1, 1]})

    ax = axes[0]
    for (_, r), yi in zip(REGIONS, y, strict=True):
        paired = run(results, "gbm_test" if r is None else f"gbm_transfer_test_{r}")["paired"]["E_fairway - A_motion"]
        for metric, dy, colour in (("err_20min_m", 0.15, LIGHT), ("fde_m", -0.15, BASE)):
            mean, err = interval(paired[metric])
            ax.errorbar(mean, yi + dy, xerr=err, fmt="o", ms=4, color=colour, ecolor=colour, elinewidth=1.2,
                        capsize=2)
    ax.axvline(0, color=MUTED, lw=1)
    ax.plot([], [], "o", color=LIGHT, label="20 min")
    ax.plot([], [], "o", color=BASE, label="60 min")
    ax.legend(fontsize=8, frameon=False, loc="lower left")
    ax.set_yticks(y, [name for name, _ in REGIONS], fontsize=9)
    style(ax, "A. Fairway context vs motion only", "E − A mean error (m), 95% CI; left of 0 = E better")

    for ax, level, letter in ((axes[1], "0.8", "B"), (axes[2], "0.9", "C")):
        nominal = float(level)
        ax.axvspan(nominal - 0.03, nominal + 0.03, color=MUTED, alpha=0.12, lw=0)
        ax.axvline(nominal, color=MUTED, lw=1)
        for (_, r), yi in zip(REGIONS, y, strict=True):
            names = [("home", "intervals_E_fairway_test" if r is None else f"intervals_E_fairway_transfer_test_{r}")]
            if r is not None:
                names.append(("local", f"intervals_E_fairway_transfer_test_{r}_localcal"))
            for calibration, name in names:
                x = run(results, name)["intervals"][level]["60"]
                mean, err = interval({"mean": x["coverage"], "ci95_lo": x["ci95_lo"], "ci95_hi": x["ci95_hi"]})
                colour, dy = (ACCENT, 0.15) if calibration == "home" else (BASE, -0.15)
                ax.errorbar(mean, yi + (dy if r is not None else 0), xerr=err, fmt="o", ms=4, color=colour,
                            ecolor=colour, elinewidth=1.2, capsize=2)
        ax.set_xlim(0.35, 1.0)
        ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
        style(ax, f"{letter}. Coverage of {nominal:.0%} boxes at 60 min",
              f"Share inside box; band = {nominal:.0%} ± 3 points")
    axes[1].plot([], [], "o", color=ACCENT, label="home calibration")
    axes[1].plot([], [], "o", color=BASE, label="local calibration")
    axes[1].legend(fontsize=8, frameon=False, loc="upper left")

    fig.suptitle("V3 locked test (16–29 Oct): models trained on the Danish home area only", fontsize=11, x=0.01,
                 ha="left", color=INK)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=200)
    plt.close(fig)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("results", type=Path)
    ap.add_argument("out", type=Path)
    args = ap.parse_args(argv)
    print("wrote", figure(args.results, args.out))


if __name__ == "__main__":
    main()
