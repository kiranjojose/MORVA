"""Static figures for the report (Matplotlib, saved to results/figures)."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import polars as pl  # noqa: E402


def plot_tracks(tracks: pl.DataFrame, out: Path, title: str, max_segments: int = 300) -> Path:
    fig, ax = plt.subplots(figsize=(8, 7))
    seg_ids = tracks["segment_id"].unique().sort()[:max_segments]
    for _, g in tracks.filter(pl.col("segment_id").is_in(seg_ids.implode())).group_by("segment_id"):
        g = g.sort("t")
        ax.plot(g["lon"], g["lat"], lw=0.6, alpha=0.7)
    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Latitude (°N)")
    ax.set_aspect(1 / np.cos(np.radians(tracks["lat"].mean())))
    ax.set_title(f"{title}\n{tracks['t'].min():%Y-%m-%d %H:%M} – {tracks['t'].max():%Y-%m-%d %H:%M} UTC, "
                 f"{len(seg_ids)} segments shown")
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def plot_error_vs_horizon(step_errors: dict[str, np.ndarray], step_s: int, out: Path, title: str) -> Path:
    """step_errors: model -> [n, H] metres. Plots mean and 90th percentile per lead time."""
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for name, err in step_errors.items():
        lead = np.arange(1, err.shape[1] + 1) * step_s / 60
        (line,) = ax.plot(lead, err.mean(axis=0), label=f"{name} (mean)")
        ax.plot(lead, np.quantile(err, 0.9, axis=0), ls="--", color=line.get_color(), alpha=0.6,
                label=f"{name} (p90)")
    ax.set_xlabel("Forecast lead time (min)")
    ax.set_ylabel("Position error (m)")
    ax.set_title(title)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def plot_generalisation_panels(panels: dict[str, dict], out: Path, title: str) -> Path:
    """Small multiples (shared x scale) of FDE@20 per learned model, one panel per evaluation setting.

    panels: setting -> {"cv": summary, "A_motion": summary, ...} where summary has mean / ci95_lo / ci95_hi.
    CV is drawn as a dashed reference line; location-based models (C) are highlighted.
    """
    models = [("A_motion", "A  motion"), ("B_vessel", "B  + vessel"), ("C_location", "C  + location"),
              ("D_all", "D  all")]
    base, highlight, ink, muted = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e"
    xmax = max(s[m]["ci95_hi"] for s in panels.values() for m, _ in models) * 1.18
    fig, axes = plt.subplots(1, len(panels), figsize=(11, 3.4), sharex=True, sharey=True)
    for ax, (setting, s) in zip(axes, panels.items(), strict=True):
        y = np.arange(len(models))[::-1]
        for yi, (m, _) in zip(y, models, strict=True):
            v = s[m]
            color = highlight if m == "C_location" else base
            ax.barh(yi, v["mean"], height=0.62, color=color)
            ax.errorbar(v["mean"], yi, xerr=[[v["mean"] - v["ci95_lo"]], [v["ci95_hi"] - v["mean"]]],
                        fmt="none", ecolor=ink, elinewidth=1, capsize=2)
            ax.text(v["ci95_hi"] + xmax * 0.015, yi, f"{v['mean']:,.0f}", va="center", fontsize=8, color=ink)
        cv = s["cv"]["mean"]
        ax.axvline(cv, color=muted, ls="--", lw=1.2)
        ax.text(cv, len(models) - 0.35, f" CV {cv:,.0f}", fontsize=8, color=muted, va="bottom")
        ax.set_title(setting, fontsize=10, color=ink, loc="left")
        ax.set_yticks(y, [lab for _, lab in models], fontsize=9)
        ax.set_xlim(0, xmax)
        ax.set_ylim(-0.6, len(models) - 0.1)
        ax.grid(axis="x", alpha=0.25)
        ax.tick_params(axis="x", labelsize=8, colors=muted)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.set_xlabel("Mean FDE at 20 min (m), 95% CI", fontsize=8, color=muted)
    fig.suptitle(title, fontsize=11, x=0.01, ha="left", color=ink)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=200)
    plt.close(fig)
    return out
