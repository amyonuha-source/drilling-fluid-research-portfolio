"""Paths, labels and reference values for the biodiesel vs diesel mud comparison."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
RESULTS = ROOT / "results"
FIG_DIR = RESULTS / "figures"
TABLE_DIR = RESULTS / "tables"

MUDS = ("biodiesel_mud", "diesel_mud")
LABELS = {"biodiesel_mud": "Biodiesel-based mud", "diesel_mud": "Diesel-based mud"}
COLOURS = {"biodiesel_mud": "#009E73", "diesel_mud": "#0072B2"}   # Okabe-Ito, colour-blind safe

# Standard-viscometer constant for the power-law consistency index (511 s^-1 at 300 rpm).
RPM300_SHEAR_RATE = 511.0

# Oil/water ratio recommended for each mud-density band, copied from the table in the source
# report (it is labelled "API lowest recommended oil-water ratio for mud densities").
# Only the 11-14 ppg row is used here.
RECOMMENDED_OIL_PERCENT_11_14_PPG = 70.0
