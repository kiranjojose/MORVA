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
