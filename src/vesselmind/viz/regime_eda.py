"""Exploratory figures to support the manoeuvring-regime definition (past-only quantities).

Turn rate for a window = NET course change (sum of signed COG steps) over the last `lookback`
steps of its history, in deg/min. The net form cancels COG jitter; mean |dCOG| was tried first and
mostly measured sensor noise (median ~5 deg/min at 1-5 kn). Cross-checked against course derived
from positions only (agreement 31% vs 34.5% of 10-15 kn windows above 1 deg/min).
Figures use TRAIN + VAL windows only; the test split is never touched.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import polars as pl  # noqa: E402


def past_turn_rate_deg_min(hist: np.ndarray, step_s: int, lookback: int = 10) -> np.ndarray:
    cog = hist[:, -(lookback + 1):, 3]
    d = (np.diff(cog, axis=1) + 180) % 360 - 180
    return np.abs(np.nansum(d, axis=1)) / (lookback * step_s / 60)


def past_speed_change_kn(hist: np.ndarray, lookback: int = 10) -> np.ndarray:
    return hist[:, -1, 2] - hist[:, -(lookback + 1), 2]


TURN_BINS = [0, 0.5, 1, 2, 5, 10, np.inf]


def regime_eda(hist, meta: pl.DataFrame, per_sample: pl.DataFrame | None, step_s: int, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    keep = meta["split"].is_in(["train", "val"]).to_numpy()
    hist, meta = hist[keep], meta.filter(pl.col("split").is_in(["train", "val"]))
    tr = past_turn_rate_deg_min(hist, step_s)
    dv = past_speed_change_kn(hist)
    meta = meta.with_columns(turn_deg_min=tr, dsog_kn=dv, sog_kn=hist[:, -1, 2],
                             lat=hist[:, -1, 0], lon=hist[:, -1, 1])
    summary = {}

    # 1. Turn-rate distribution
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.hist(np.clip(tr[~np.isnan(tr)], 0, 20), bins=200, color="#3b6ea5")
    ax.set_yscale("log")
    for t in (1, 2, 5):
        frac = float(np.nanmean(tr > t))
        summary[f"frac_turn_gt_{t}_deg_min"] = round(frac, 4)
        ax.axvline(t, ls="--", color="k", lw=0.8)
        ax.text(t, ax.get_ylim()[1] * 0.3, f" >{t}°/min: {frac:.1%}", fontsize=8)
    ax.set_xlabel("Past 10-min net course change rate (°/min, clipped at 20)")
    ax.set_ylabel("Windows (log)")
    ax.set_title("Turn-rate distribution, train+val windows")
    fig.tight_layout()
    fig.savefig(out_dir / "regime_turn_rate_hist.png", dpi=150)
    plt.close(fig)

    # 2. Where turns happen
    fig, ax = plt.subplots(figsize=(8, 7))
    straight = meta.filter(pl.col("turn_deg_min") <= 1).sample(fraction=0.2, seed=0)
    turning = meta.filter(pl.col("turn_deg_min") > 2)
    ax.scatter(straight["lon"], straight["lat"], s=0.2, c="#bbbbbb", label="≤1°/min (20% sample)")
    sc = ax.scatter(turning["lon"], turning["lat"], s=0.6, c=np.clip(turning["turn_deg_min"], 2, 10),
                    cmap="plasma", label=">2°/min")
    fig.colorbar(sc, ax=ax, label="turn rate (°/min)")
    ax.set_aspect(1 / np.cos(np.radians(55.5)))
    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Latitude (°N)")
    ax.set_title("Where vessels turn (window anchor positions, train+val)")
    ax.legend(loc="lower left", markerscale=10, fontsize=8)
    fig.tight_layout()
    fig.savefig(out_dir / "regime_turn_hotspots.png", dpi=150)
    plt.close(fig)

    # 3. Speed by ship type
    types = meta.drop_nulls("ship_type").group_by("ship_type").len().sort("len", descending=True).head(9)["ship_type"]
    data = [meta.filter(pl.col("ship_type") == t)["sog_kn"].drop_nans().drop_nulls().to_numpy() for t in types]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.boxplot(data, showfliers=False)
    ax.set_xticks(range(1, len(types) + 1), [f"{t}\n(n={len(d):,})" for t, d in zip(types, data, strict=True)],
                  fontsize=7)
    ax.set_ylabel("SOG at anchor (kn)")
    ax.set_title("Speed by ship type (moving windows, train+val)")
    fig.tight_layout()
    fig.savefig(out_dir / "regime_speed_by_type.png", dpi=150)
    plt.close(fig)

    # 4. Baseline error by past turn rate (validation run)
    if per_sample is not None:
        val = meta.filter(pl.col("split") == "val").select("sample_id", "turn_deg_min")
        df = per_sample.join(val, on="sample_id").with_columns(
            turn_bin=pl.col("turn_deg_min").cut(TURN_BINS[1:-1], left_closed=True)
        )
        tab = (df.group_by("turn_bin", "model").agg(fde=pl.col("fde_m").mean(), n=pl.len())
               .pivot(on="model", index="turn_bin", values="fde").sort("turn_bin"))
        counts = df.filter(pl.col("model") == "cv").group_by("turn_bin").len().sort("turn_bin")
        tab = tab.join(counts, on="turn_bin")
        summary["fde_by_turn_bin_val"] = tab.with_columns(pl.col("turn_bin").cast(pl.String)).to_dicts()
        fig, ax = plt.subplots(figsize=(7, 4.5))
        labels = tab["turn_bin"].cast(pl.String).to_list()
        x = np.arange(len(labels))
        for k, m in enumerate(["cv", "ctrv"]):
            ax.bar(x + (k - 0.5) * 0.4, tab[m], width=0.4, label=m)
        ax.set_xticks(x, [f"{lab}\n(n={n:,})" for lab, n in zip(labels, tab["len"], strict=True)], fontsize=7)
        ax.set_xlabel("Past turn rate bin (°/min)")
        ax.set_ylabel("Mean FDE at 20 min (m)")
        ax.set_title("Baseline error by past turn rate (validation)")
        ax.legend()
        fig.tight_layout()
        fig.savefig(out_dir / "regime_fde_by_turn_rate.png", dpi=150)
        plt.close(fig)
    return summary
