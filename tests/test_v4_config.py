"""The V4 split and region roles are fixed before validation analysis (docs/00_plan.md, "V4"); tests guard them."""

from datetime import datetime, timedelta

from morva.config import load_config

DATA = load_config("configs/v4/data.yaml")
EXP = load_config("configs/v4/experiment.yaml")
V3 = load_config("configs/v3/experiment.yaml")
BLOCKS = ("train_start", "train_end", "val_end", "calib_end", "test_end")


def _cal(cfg, name):
    return {k: datetime.fromisoformat(v) for k, v in cfg["split"]["calendars"][name].items()}


def test_v4_blocks_are_ordered_and_have_the_planned_lengths():
    for name, lengths in (("no2026", [18, 5, 4, 14]), ("dk2026b", [41, 5, 4, 14])):
        c = _cal(EXP, name)
        assert [c[k] for k in BLOCKS] == sorted(c[k] for k in BLOCKS)
        assert [(c[b] - c[a]).days for a, b in zip(BLOCKS, BLOCKS[1:], strict=False)] == lengths, name


def test_skagen_is_evaluated_only_on_days_after_the_spent_v3_periods():
    spent_end = _cal(V3, "dk2026")["test_end"]
    skagen = _cal(EXP, "dk2026b")
    assert skagen["train_end"] == spent_end  # spent days only build the flow map
    assert skagen["test_end"] - timedelta(days=1) == datetime(2026, 11, 21)


def test_v4_regions_use_known_sources_and_calendars_and_do_not_overlap():
    regions = [DATA["aoi"], *DATA["transfer_aois"]]
    assert [r["name"] for r in regions] == ["west_coast", "oslofjord", "skagen"]
    for r in regions:
        assert r["source"] in DATA["sources"] and r["calendar"] in EXP["split"]["calendars"]
        assert r["lat_min"] < r["lat_max"] and r["lon_min"] < r["lon_max"]
    for i, a in enumerate(regions):
        for b in regions[i + 1:]:
            disjoint = (a["lat_max"] <= b["lat_min"] or b["lat_max"] <= a["lat_min"]
                        or a["lon_max"] <= b["lon_min"] or b["lon_max"] <= a["lon_min"])
            assert disjoint, (a["name"], b["name"])
    assert DATA["aoi"]["source"] == "kystverket"  # models are trained in Norwegian waters only


def test_v4_task_and_outputs_are_separate_from_v3():
    assert EXP["windows"] == V3["windows"]
    assert EXP["results_dir"] == "results/v4" and DATA["paths"]["processed"].startswith("data/v4/")
    assert not any("vessel" in sets for sets in EXP["gbm"]["feature_sets"].values())  # no static data in HAIS
