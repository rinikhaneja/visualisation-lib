# visualisation-lib

A small, importable plotting library, organised with the
[Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/) layout.

- **Install name** (pip / PyPI): `viz-lib`
- **Import name** (in Python): `viz_lib`

(As with any package, the install name uses a hyphen and the import name uses
an underscore — `pip install viz-lib`, then `import viz_lib`.)

## Install

```bash
# from a local checkout (editable, for development)
pip install -e .

# once published
pip install viz-lib
```

## Use

```python
import pandas as pd
import viz_lib as viz

df = pd.read_csv("data.csv")
viz.ranked_bar(df, category="country", value="co2_per_capita")
```

Public API: `ranked_bar`, `split_panel_line`, `stacked_area`, plus the shared
`theme` helpers (`apply_theme`, `series_color`, `smog_color`, `PALETTE`, `SMOG`).

### Bundled datasets

Sample CSVs ship **inside** the package (`viz_lib/data/`) and are read with
`importlib.resources`, so they load whether you run from a checkout or an
installed wheel:

```python
import viz_lib
viz_lib.datasets.available()          # ['co2_per_capita', 'us_co2_by_fuel', ...]
df = viz_lib.load_dataset("us_co2_by_fuel")
```

## Plots

Plot functions live in `src/viz_lib/`. They share one contract: tidy data plus
role keywords, an optional `ax` for composition, and a returned matplotlib
object. A single theme (`viz_lib.theme`) gives every plot one identity using a
validated, colorblind-safe palette.

### `split_panel_line`

Draws one metric across several series split into panels, each with its own
y-scale — the honest way to show series whose magnitudes differ by 10×+ without
a misread-prone log axis.

```python
from viz_lib import split_panel_line

fig = split_panel_line(
    x=years,
    series={"Qatar": [...], "United States": [...], "India": [...]},
    panels={
        "Oil exporters":  ["Qatar", "Kuwait"],
        "Major economies": ["United States", "India"],
    },
    x_label="Year",
    y_label="Tonnes CO₂ per capita",
)
fig.savefig("reports/figures/co2_split_panel.png", dpi=150, bbox_inches="tight")
```

See `notebooks/example_split_panel.py` for a runnable example.

### `ranked_bar`

A sorted horizontal bar chart for comparing a value across items (the
Evergreen Chart Chooser's pick for ranking with long labels). Built to the
Data Viz Checklist: sorted by value, direct labels, no gridlines/border, a
takeaway title, and a CO₂-themed "smog" color ramp (darker = more emissions)
that stays legible in black & white and for colorblind readers.

```python
import pandas as pd
from viz_lib import ranked_bar

df = pd.read_csv("data/raw/co2_per_capita.csv")
df = df[df["Year"] == 2024]

fig = ranked_bar(
    df, category="Entity", value="CO₂ emissions per capita",
    reference=4.7, reference_label="World average",
    title="A few small, oil-rich nations emit the most CO₂ per person",
    subtitle="Tonnes of CO₂ per person, 2024",
)
```

`compare="<earlier-column>"` adds a ▲/▼ change tag per bar; pass the same
`vmax` to two charts to share one honest color scale. See
`notebooks/co2_bars.py` for the two-group CO₂ example.

## Project structure

```
├── data/               # raw, interim, processed, external
├── notebooks/          # exploration only
├── src/                # imported modules
├── models/             # trained artifacts
├── reports/figures/    # graphics for write-ups
├── docs/               # mkdocs site
└── pyproject.toml      # project metadata
```

| Path               | Purpose                                             |
| ------------------ | --------------------------------------------------- |
| `data/`            | Raw, interim, processed, and external data.         |
| `notebooks/`       | Jupyter notebooks for exploration only.             |
| `src/`             | Reusable, importable Python modules.                |
| `models/`          | Trained and serialized model artifacts.             |
| `reports/figures/` | Graphics generated for write-ups and reporting.     |
| `docs/`            | MkDocs documentation site.                          |
| `pyproject.toml`   | Project metadata and build configuration.           |
