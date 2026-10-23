"""The V3 split and regions are fixed before validation analysis (docs/00_plan.md, "V3"); these tests guard them."""

from datetime import datetime, timedelta

from morva.config import load_config

DATA = load_config("configs/v3/data.yaml")
EXP = load_config("configs/v3/experiment.yaml")
BLOCKS = ("train_start", "train_end", "val_end", "calib_end", "test_end")


def _cal(name):
    return {k: datetime.fromisoformat(v) for k, v in EXP["split"]["calendars"][name].items()}


def test_v3_blocks_are_ordered_and_have_the_planned_lengths():
    for name in ("dk2026", "us2025"):
        c = _cal(name)
        assert [c[k] for k in BLOCKS] == sorted(c[k] for k in BLOCKS)
        days = [(c[b] - c[a]).days for a, b in zip(BLOCKS, BLOCKS[1:], strict=False)]
        assert days == [18, 5, 4, 14], name  # train 19 Sep-6 Oct, val 7-11, calib 12-15, test 16-29 Oct


def test_v3_test_periods_match_the_plan():
    dk, us = _cal("dk2026"), _cal("us2025")
    assert (dk["calib_end"], dk["test_end"] - timedelta(days=1)) == (datetime(2026, 10, 16), datetime(2026, 10, 29))
    assert (us["calib_end"], us["test_end"] - timedelta(days=1)) == (datetime(2025, 10, 16), datetime(2025, 10, 29))
    # Same calendar dates in both years
    assert all((dk[k].month, dk[k].day) == (us[k].month, us[k].day) for k in BLOCKS)


def test_v3_regions_use_known_sources_and_calendars_and_do_not_overlap():
    regions = [DATA["aoi"], *DATA["transfer_aois"]]
    names = [r["name"] for r in regions]
    assert len(set(names)) == len(names)
    assert {"great_belt_oresund", "bornholm", "skagen", "salish_sea", "houston"} == set(names)
    for r in regions:
        assert r["source"] in DATA["sources"] and r["calendar"] in EXP["split"]["calendars"]
        assert r["lat_min"] < r["lat_max"] and r["lon_min"] < r["lon_max"]
    for i, a in enumerate(regions):
        for b in regions[i + 1:]:
            disjoint = (a["lat_max"] <= b["lat_min"] or b["lat_max"] <= a["lat_min"]
                        or a["lon_max"] <= b["lon_min"] or b["lon_max"] <= a["lon_min"])
            assert disjoint, (a["name"], b["name"])
    assert DATA["aoi"]["source"] == "dma"  # models are trained in the Danish home area only


def test_v3_task_and_outputs_are_separate_from_v2():
    w = EXP["windows"]
    assert (w["obs_steps"], w["future_steps"], w["step_s"]) == (20, 60, 60)
    assert max(w["horizons_min"]) == w["future_steps"] * w["step_s"] // 60
    assert EXP["results_dir"] == "results/v3" and DATA["paths"]["processed"].startswith("data/v3/")
    # The default (V2) configuration is untouched
    v2 = load_config("configs/experiment.yaml")
    assert v2["results_dir"] == "results/v2" and v2["windows"]["future_steps"] == 20
    assert v2["split"]["test_end"] == "2026-10-16T00:00:00"
