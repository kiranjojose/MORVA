"""The V4 decision script applies the draft rules exactly (scripts/v4_decide.py)."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from v4_decide import DEV_SCENARIOS, RULES, decide  # noqa: E402


def _ci(mean, lo, hi):
    return {"mean": mean, "ci95_lo": lo, "ci95_hi": hi}


def _gbm(e=(-300, -350, -250), c=(800, 600, 1000), h_e=(3, -20, 25)):
    return {"paired": {"E_fairway - A_motion": {"err_20min_m": _ci(*e), "fde_m": _ci(*e)},
                       "C_location - A_motion": {"err_20min_m": _ci(*c), "fde_m": _ci(*c)},
                       "H_wind_current - E_fairway": {"err_20min_m": _ci(*h_e), "fde_m": _ci(*h_e)}}}


def _intervals(c80=0.80, c90=0.90):
    return {"intervals": {"0.8": {h: {"coverage": c80} for h in ("20", "60")},
                          "0.9": {h: {"coverage": c90} for h in ("20", "60")}}}


def _deviation(gap=(0.25, 0.20, 0.30), control_fa=0.05):
    res = {sc: {"model_minus_rule": {"0.05": {r: {"20": _ci(*gap)} for r in RULES}}} for sc in DEV_SCENARIOS}
    res["none"] = {"model_box": {"0.05": {"per_horizon": {"20": {"false_alarm_rate": control_fa}}}}}
    return {"results": res}


def _write(root, name, summary, stamp="20261201T000000Z"):
    d = root / "runs" / f"{stamp}_{name}"
    d.mkdir(parents=True)
    (d / "summary.json").write_text(json.dumps(summary))


def _all_runs(root, transfer_gbm=None, home_gbm=None, local=(0.80, 0.90), deviation=None):
    for r in ("oslofjord", "skagen"):
        _write(root, f"gbm_transfer_test_{r}", transfer_gbm or _gbm())
        _write(root, f"intervals_E_fairway_transfer_test_{r}_localcal", _intervals(*local))
    _write(root, "gbm_test", home_gbm or _gbm())
    _write(root, "intervals_E_fairway_test", _intervals())
    _write(root, "deviation_E_fairway_test", deviation or _deviation())


def test_all_hypotheses_supported_with_the_planned_number_of_checks(tmp_path):
    _all_runs(tmp_path)
    h = decide(tmp_path, "test")["hypotheses"]
    assert {k: v["outcome"] for k, v in h.items()} == {f"V4-H{i}": "supported" for i in range(1, 6)}
    assert [len(h[f"V4-H{i}"]["checks"]) for i in range(1, 6)] == [4, 4, 12, 19, 1]


def test_ci_bounds_decide_not_means(tmp_path):
    _all_runs(tmp_path, transfer_gbm=_gbm(e=(-300, -600, 0.0), c=(800, -1, 1600)),
              deviation=_deviation(gap=(0.25, 0.0, 0.5)))
    h = decide(tmp_path, "test")["hypotheses"]
    assert all(h[k]["outcome"] == "not supported" for k in ("V4-H1", "V4-H2", "V4-H4"))


@pytest.mark.parametrize("h_e, expected", [((0, -149, 149), "supported"), ((0, -151, 20), "not supported"),
                                           ((100, 40, 150), "not supported")])
def test_equivalence_needs_the_whole_ci_inside_the_margin(tmp_path, h_e, expected):
    _all_runs(tmp_path, home_gbm=_gbm(h_e=h_e))
    assert decide(tmp_path, "test")["hypotheses"]["V4-H5"]["outcome"] == expected


@pytest.mark.parametrize("fa, expected", [(0.04, "supported"), (0.06, "supported"), (0.039, "not supported"),
                                          (0.061, "not supported")])
def test_control_false_alarm_band_is_inclusive(tmp_path, fa, expected):
    _all_runs(tmp_path, deviation=_deviation(control_fa=fa))
    assert decide(tmp_path, "test")["hypotheses"]["V4-H4"]["outcome"] == expected


def test_missing_runs_leave_hypotheses_undecided_and_reruns_are_refused(tmp_path):
    _all_runs(tmp_path)
    (tmp_path / "runs" / "20261201T000000Z_intervals_E_fairway_transfer_test_skagen_localcal" / "summary.json").unlink()
    assert decide(tmp_path, "test")["hypotheses"]["V4-H3"]["outcome"].startswith("undecided")
    _write(tmp_path, "gbm_test", _gbm(), stamp="20261202T000000Z")
    with pytest.raises(SystemExit):
        decide(tmp_path, "test")
