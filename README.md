# visualisation-lib

A project organised with the [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/) layout.

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
