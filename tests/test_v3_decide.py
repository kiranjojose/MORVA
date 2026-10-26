"""The V3 decision script applies the frozen rules exactly (scripts/v3_decide.py)."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from v3_decide import decide  # noqa: E402


def _ci(mean, lo, hi):
    return {"mean": mean, "ci95_lo": lo, "ci95_hi": hi}


def _gbm(e20, e60, c20, c60):
    return {"paired": {"E_fairway - A_motion": {"err_20min_m": e20, "fde_m": e60},
                       "C_location - A_motion": {"err_20min_m": c20, "fde_m": c60}}}


def _intervals(c80, c90):
    return {"intervals": {"0.8": {h: {"coverage": c80} for h in ("20", "60")},
                          "0.9": {h: {"coverage": c90} for h in ("20", "60")}}}


def _write(root, name, summary, stamp="20261101T000000Z"):
    d = root / "runs" / f"{stamp}_{name}"
    d.mkdir(parents=True)
    (d / "summary.json").write_text(json.dumps(summary))


def _all_runs(root, gbm=None, local=(0.80, 0.90), home=(0.80, 0.90)):
    _write(root, "gbm_transfer_test_salish_sea",
           gbm or _gbm(_ci(-400, -450, -350), _ci(-1200, -1350, -1000), _ci(1100, 900, 1300), _ci(6000, 5000, 7000)))
    for r in ("bornholm", "skagen", "salish_sea"):
        _write(root, f"intervals_E_fairway_transfer_test_{r}_localcal", _intervals(*local))
    _write(root, "intervals_E_fairway_test", _intervals(*home))


def test_all_hypotheses_supported(tmp_path):
    _all_runs(tmp_path)
    h = decide(tmp_path, "test")["hypotheses"]
    assert {k: v["outcome"] for k, v in h.items()} == {k: "supported" for k in ("V3-H1", "V3-H2", "V3-H3", "V3-H4")}
    assert len(h["V3-H3"]["checks"]) == 12 and len(h["V3-H4"]["checks"]) == 4


def test_ci_rules_need_the_bound_not_the_mean(tmp_path):
    # E better on average but CI touches zero at 20 min; C worse on average but CI crosses zero at 60 min
    _all_runs(tmp_path, gbm=_gbm(_ci(-400, -800, 0.0), _ci(-1200, -1350, -1000), _ci(1100, 900, 1300),
                                 _ci(6000, -10, 9000)))
    h = decide(tmp_path, "test")["hypotheses"]
    assert h["V3-H1"]["outcome"] == "not supported" and h["V3-H2"]["outcome"] == "not supported"


@pytest.mark.parametrize("c80, expected", [(0.77, "supported"), (0.83, "supported"), (0.769, "not supported"),
                                           (0.831, "not supported")])
def test_coverage_tolerance_is_three_points_inclusive(tmp_path, c80, expected):
    _all_runs(tmp_path, local=(c80, 0.90))
    assert decide(tmp_path, "test")["hypotheses"]["V3-H3"]["outcome"] == expected


def test_missing_run_leaves_hypothesis_undecided(tmp_path):
    _all_runs(tmp_path)
    for f in (tmp_path / "runs").glob("*_intervals_E_fairway_transfer_test_skagen_localcal"):
        (f / "summary.json").unlink()
        f.rmdir()
    assert decide(tmp_path, "test")["hypotheses"]["V3-H3"]["outcome"].startswith("undecided")


def test_more_than_one_run_is_refused_for_the_test_split(tmp_path):
    _all_runs(tmp_path)
    _write(tmp_path, "intervals_E_fairway_test", _intervals(0.8, 0.9), stamp="20261102T000000Z")
    with pytest.raises(SystemExit):
        decide(tmp_path, "test")
    assert decide(tmp_path, "test", latest=True)["hypotheses"]["V3-H4"]["outcome"] == "supported"
