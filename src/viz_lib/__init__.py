"""viz_lib — a small, consistent plotting library."""

from .theme import PALETTE, SMOG, apply_theme, series_color, smog_color
from .bar import ranked_bar, stacked_bar
from .area import stacked_area
from . import datasets
from .datasets import load as load_dataset

__all__ = [
    "PALETTE",
    "SMOG",
    "apply_theme",
    "series_color",
    "smog_color",
    "ranked_bar",
    "stacked_bar",
    "stacked_area",
    "datasets",
    "load_dataset",
]
