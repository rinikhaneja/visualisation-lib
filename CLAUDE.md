# CLAUDE.md

Guidance for working in this repository.

## What this is

`viz_lib` is a small, importable Python plotting library (built on matplotlib +
pandas) plus a few scripts that use it to draw CO₂-emissions charts. It follows
the [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/)
layout.

- **Install name** (pip/PyPI): `viz-lib`
- **Import name** (in code): `viz_lib`

## Common commands

```bash
pip install -e .                      # editable install (dev)
python -m build                       # build a wheel into dist/ (bundles the CSVs)
python notebooks/co2_bars.py          # render graphs 1 & 2 -> reports/figures/
python notebooks/us_co2_hero.py       # render graph 3 (hero) -> reports/figures/
```

Rendering headlessly: prefix with `MPLBACKEND=Agg`.

## Layout

```
src/viz_lib/            # THE LIBRARY (importable, shipped in the wheel)
  __init__.py           #   public API (see __all__)
  theme.py              #   apply_theme, series_color, smog_color, PALETTE, SMOG
  bar.py                #   ranked_bar
  area.py               #   stacked_area
  datasets.py           #   load  (exposed as viz_lib.load_dataset)
  data/                 #   bundled sample CSVs (a sub-package; needs its __init__.py)
notebooks/              # SCRIPTS that USE the library (not part of the package)
  co2_bars.py           #   two ranked bar charts
  us_co2_hero.py        #   US CO₂-by-fuel stacked area
reports/figures/        # generated PNGs (gitignored)
data/{raw,interim,...}  # Cookiecutter data dirs (contents gitignored)
```

Keep the distinction: `src/viz_lib/` is the reusable library; `notebooks/` holds
example scripts that import it. Do not move scripts into `src/viz_lib/`.

## Public API

`ranked_bar`, `stacked_area`, `load_dataset`, `datasets`, plus the theme helpers
`apply_theme`, `series_color`, `smog_color`, `PALETTE`, `SMOG`. (Load via
`viz_lib.datasets.load(name)` / `viz_lib.load_dataset(name)`.)

## Bundled datasets

CSVs live in `src/viz_lib/data/` and are read with `importlib.resources` (not
relative paths), so they load from a checkout or an installed wheel:

```python
import viz_lib
df = viz_lib.load_dataset("us_co2_by_fuel")   # or "co2_per_capita"
```

To add a dataset: drop the CSV in `src/viz_lib/data/` (it ships automatically via
`[tool.setuptools.package-data]` in pyproject.toml).

## Conventions for plot functions

Every plot function:
- takes a tidy pandas **DataFrame** plus role keywords (`category`, `value`,
  `x`, `series`, …);
- calls `apply_theme()` first;
- accepts an optional `ax=` so it composes into larger figures;
- returns the matplotlib **Figure**;
- only calls `fig.tight_layout()` when it created the figure (`owns_fig`).

Style choices (Evergreen Data Viz Checklist): bars sorted by value, direct value
labels, muted/absent gridlines and spines, a takeaway title. Colors come from
`theme.py` — the categorical `PALETTE` (via `series_color`, cycles past 8) and
the sequential "smog" ramp (`smog_color`, used by `ranked_bar`).

## Notes

- The code has been deliberately trimmed for size (currently ~294 .py lines).
  Docstrings are one line; there are no blank lines inside functions and one
  blank line between top-level defs. Preserve that style when editing.
- `datasets.py` intentionally exposes only `load` (the earlier `available`/`path`
  helpers were removed as unused).
- The Colab notebook (`notebooks/us_carbon_story_github.ipynb`) installs the
  library from GitHub (`@main`) and draws the two charts; regenerate it if the
  library changes (its builder lives in the session scratchpad, not the repo).
- Removed charts remain retrievable from git history (e.g. the by-source
  `stacked_bar` chart is in commit `24b3a59`).
