"""Derived properties and data-quality flags. Run from the repository root:  python -m src.analyze"""
import math

import pandas as pd

from . import config as C
from .data import load_comparison, load_recipe, load_retort


def derived_properties(comp: pd.DataFrame | None = None) -> pd.DataFrame:
    """Calculate PV, YP, ratios and power-law indices from the 300/600 rpm dial readings."""
    comp = load_comparison() if comp is None else comp
    rows = {}
    for mud in C.MUDS:
        d300 = float(comp.loc["dial_reading_300rpm", mud])
        d600 = float(comp.loc["dial_reading_600rpm", mud])
        pv = d600 - d300
        yp = d300 - pv
        n = 3.32 * math.log10(d600 / d300)
        k = d300 / (C.RPM300_SHEAR_RATE ** n)
        rows[mud] = {
            "plastic_viscosity_cP": pv,
            "yield_point_lb100ft2": yp,
            "yp_over_pv": yp / pv,
            "apparent_viscosity_cP": d600 / 2.0,
            "power_law_n_two_point": n,
            "power_law_K_lb_s_n_100ft2": k,
        }
    return pd.DataFrame(rows)


def quality_flags(comp: pd.DataFrame | None = None) -> pd.DataFrame:
    """Plausibility checks on the recorded values. Each row is one check on one mud."""
    comp = load_comparison() if comp is None else comp
    out = []
    for mud in C.MUDS:
        g10s = float(comp.loc["gel_strength_10sec", mud])
        g10m = float(comp.loc["gel_strength_10min", mud])
        d300 = float(comp.loc["dial_reading_300rpm", mud])
        out.append({"mud": mud, "check": "10 s gel should not exceed 10 min gel",
                    "values": f"10 s = {g10s:g}, 10 min = {g10m:g}", "flag": g10s > g10m})
        out.append({"mud": mud, "check": "gel strength should not exceed the 300 rpm dial reading (3 rpm gel readings are normally far lower)",
                    "values": f"10 s gel = {g10s:g}, 300 rpm dial = {d300:g}", "flag": g10s > d300})
    fl = float(comp.loc["filtrate_volume", "diesel_mud"])
    out.append({"mud": "diesel_mud", "check": "zero filtrate: test conditions and mud recipe must be recorded to interpret",
                "values": f"filtrate = {fl:g} mL", "flag": fl == 0})
    return pd.DataFrame(out)


def oil_water_summary() -> pd.DataFrame:
    """Compare the biodiesel recipe's oil:water ratio with the retort result and the recommended ratio."""
    rec = load_recipe().set_index("constituent")
    oil, water = rec.loc["Base oil (biodiesel)", "amount"], rec.loc["Water", "amount"]
    ret = load_retort()
    r_oil, r_water, r_solids = ret["oil_ml"], ret["water_ml"], ret["solids_ml"]
    chamber = ret["chamber_volume_ml"]
    return pd.DataFrame([
        {"source": "recipe (biodiesel mud)", "oil_percent": 100 * oil / (oil + water), "water_percent": 100 * water / (oil + water), "solids_vol_percent": None},
        {"source": "retort (sample NOT confirmed as biodiesel mud)", "oil_percent": 100 * r_oil / (r_oil + r_water), "water_percent": 100 * r_water / (r_oil + r_water), "solids_vol_percent": 100 * r_solids / chamber},
        {"source": "recommended for 11-14 ppg (source-report table)", "oil_percent": C.RECOMMENDED_OIL_PERCENT_11_14_PPG, "water_percent": 100 - C.RECOMMENDED_OIL_PERCENT_11_14_PPG, "solids_vol_percent": None},
    ])


def main() -> None:
    C.TABLE_DIR.mkdir(parents=True, exist_ok=True)
    d = derived_properties()
    d.round(3).to_csv(C.TABLE_DIR / "derived_properties.csv")
    q = quality_flags()
    q.to_csv(C.TABLE_DIR / "data_quality_flags.csv", index=False)
    o = oil_water_summary()
    o.round(2).to_csv(C.TABLE_DIR / "oil_water_summary.csv", index=False)
    print(d.round(3).to_string()); print(); print(q.to_string(index=False)); print(); print(o.round(2).to_string(index=False))


if __name__ == "__main__":
    main()
