# visualisation-lib

A project organised with the [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/) layout.

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
