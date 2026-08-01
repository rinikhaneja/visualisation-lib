"""Access to the sample datasets bundled inside the package."""
from __future__ import annotations
from importlib import resources
import pandas as pd
_PKG = "viz_lib.data"

def load(name: str) -> "pd.DataFrame":
    """Load a bundled dataset by name (.csv optional) into a DataFrame."""
    fname = name if name.endswith(".csv") else name + ".csv"
    with resources.files(_PKG).joinpath(fname).open("r", encoding="utf-8") as fh:
        return pd.read_csv(fh)
