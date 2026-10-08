"""Derivation tests. Run with:  python -m pytest -q"""
import math

from src.analyze import derived_properties, quality_flags, oil_water_summary
from src.data import load_comparison, load_retort


def test_comparison_table_has_expected_properties():
    comp = load_comparison()
    for prop in ("mud_weight", "dial_reading_300rpm", "dial_reading_600rpm",
                 "gel_strength_10sec", "gel_strength_10min", "filtrate_volume", "mud_cake_thickness"):
        assert prop in comp.index


def test_pv_yp_from_dial_readings():
    d = derived_properties()
    assert d.loc["plastic_viscosity_cP", "biodiesel_mud"] == 75
    assert d.loc["yield_point_lb100ft2", "biodiesel_mud"] == 10
    assert d.loc["plastic_viscosity_cP", "diesel_mud"] == 17
    assert d.loc["yield_point_lb100ft2", "diesel_mud"] == 13


def test_flow_index_matches_api_two_point_formula():
    d = derived_properties()
    assert math.isclose(d.loc["power_law_n_two_point", "biodiesel_mud"], 3.32 * math.log10(160 / 85), rel_tol=1e-9)
    assert d.loc["power_law_n_two_point", "biodiesel_mud"] > d.loc["power_law_n_two_point", "diesel_mud"]


def test_gel_flags_fire_for_both_muds():
    q = quality_flags()
    flagged = q[q["flag"] & q["check"].str.startswith("10 s gel should not exceed")]
    assert set(flagged["mud"]) == {"biodiesel_mud", "diesel_mud"}


def test_retort_volumes_fill_the_chamber():
    r = load_retort()
    assert abs(r["oil_ml"] + r["water_ml"] + r["solids_ml"] - r["chamber_volume_ml"]) < 1e-9


def test_oil_water_ratios_sum_to_100():
    o = oil_water_summary()
    assert ((o["oil_percent"] + o["water_percent"]) - 100).abs().max() < 1e-9
