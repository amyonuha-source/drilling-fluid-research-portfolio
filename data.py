"""Data loading for the comparison study."""
import pandas as pd

from .config import DATA_RAW


def load_comparison() -> pd.DataFrame:
    """Rows = properties, columns = biodiesel_mud, diesel_mud, unit."""
    return pd.read_csv(DATA_RAW / "mud_comparison_sep2023.csv").set_index("property")


def load_recipe() -> pd.DataFrame:
    return pd.read_csv(DATA_RAW / "biodiesel_mud_recipe_sep2023.csv")


def load_retort() -> pd.Series:
    return pd.read_csv(DATA_RAW / "retort_sample_unassigned.csv").iloc[0]
