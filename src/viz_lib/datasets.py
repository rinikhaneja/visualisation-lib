"""Access to the sample datasets bundled inside the package."""

from __future__ import annotations

from importlib import resources

import pandas as pd

_PKG = "viz_lib.data"


def _resolve(name: str) -> str:
    return name if name.endswith(".csv") else name + ".csv"


def available() -> list[str]:
    """Return the names (without ``.csv``) of the bundled datasets."""
    return sorted(
        r.name[:-4]
        for r in resources.files(_PKG).iterdir()
        if r.name.endswith(".csv")
    )


def load(name: str) -> "pd.DataFrame":
    """Load a bundled dataset by name (``.csv`` optional) into a DataFrame."""
    fname = _resolve(name)
    try:
        with resources.files(_PKG).joinpath(fname).open("r", encoding="utf-8") as fh:
            return pd.read_csv(fh)
    except (FileNotFoundError, ModuleNotFoundError):
        raise FileNotFoundError(
            f"no bundled dataset {name!r}; available: {', '.join(available())}"
        )


def path(name: str):
    """Return a context manager yielding a real filesystem path to the CSV."""
    return resources.as_file(resources.files(_PKG).joinpath(_resolve(name)))
