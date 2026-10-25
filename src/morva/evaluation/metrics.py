"""Prediction metrics and vessel-grouped uncertainty.

ADE: mean geodesic error over all forecast steps. FDE: error at the final step.
Confidence intervals bootstrap over VESSELS (not windows), because windows from the same
vessel are strongly correlated; resampling windows would give falsely narrow intervals.
"""

import numpy as np

from morva.geo import haversine_m


def step_errors_m(pred: np.ndarray, true: np.ndarray) -> np.ndarray:
    """[n, H, 2] lat/lon arrays -> [n, H] errors in metres."""
    return haversine_m(pred[..., 0], pred[..., 1], true[..., 0], true[..., 1])


def per_sample_metrics(err: np.ndarray, step_s: int, horizons_min: list[int]) -> dict[str, np.ndarray]:
    out = {"ade_m": err.mean(axis=1), "fde_m": err[:, -1]}
    for h in horizons_min:
        k = int(h * 60 / step_s) - 1
        if 0 <= k < err.shape[1]:
            out[f"err_{h}min_m"] = err[:, k]
    return out


def grouped_bootstrap(values, groups, n_boot=1000, seed=0, alpha=0.05) -> tuple[float, float, float]:
    """Mean with a percentile CI from resampling whole groups (vessels) with replacement."""
    values, groups = np.asarray(values, float), np.asarray(groups)
    uniq, inv = np.unique(groups, return_inverse=True)
    sums = np.bincount(inv, weights=values)
    counts = np.bincount(inv).astype(float)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(uniq), size=(n_boot, len(uniq)))
    boot = sums[idx].sum(axis=1) / counts[idx].sum(axis=1)
    lo, hi = np.quantile(boot, [alpha / 2, 1 - alpha / 2])
    return float(values.mean()), float(lo), float(hi)


def summarize(metric: np.ndarray, groups, n_boot=1000, seed=0) -> dict:
    mean, lo, hi = grouped_bootstrap(metric, groups, n_boot, seed)
    return {
        "mean": mean, "ci95_lo": lo, "ci95_hi": hi,
        "median": float(np.median(metric)), "p90": float(np.quantile(metric, 0.9)),
        "n_samples": int(len(metric)), "n_vessels": int(len(np.unique(groups))),
    }


def paired_summaries(per_b: dict[str, np.ndarray], per_a: dict[str, np.ndarray], groups, n_boot=1000,
                     seed=0) -> dict[str, dict]:
    """Paired difference b - a on identical windows for every metric both share (ADE, final error and the error
    at each reported horizon), each with a vessel-grouped bootstrap CI. Negative = b better."""
    return {mk: summarize(per_b[mk] - per_a[mk], groups, n_boot, seed) for mk in per_b if mk in per_a}
