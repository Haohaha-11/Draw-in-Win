# Draw-in-Win

**Publication-ready scientific visualization recipes for modeling, correlation analysis, networks, sensitivity studies, and sports analytics.**

[简体中文](README.zh-CN.md) · [Visualization catalog](docs/CATALOG.md) · [Reproducibility guide](docs/REPRODUCIBILITY.md) · [Contributing](CONTRIBUTING.md)

![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![R supported](https://img.shields.io/badge/R-supported-276DC3?logo=r&logoColor=white)
![Repository checks](https://github.com/Haohaha-11/Draw-in-Win/actions/workflows/quality.yml/badge.svg)
![Figures](https://img.shields.io/badge/figure%20artifacts-124-7A5AF8)

Draw-in-Win is a curated collection of research visualization code developed around mathematical modeling projects. It brings together 67 Python scripts, 2 R scripts, bundled example datasets, and 124 retained figure artifacts in a structure designed for discovery, reuse, and paper-ready export.

The repository preserves the visual language of the original research work—high-resolution PNG previews, editable SVG figures, and vector PDF outputs—while removing duplicate copies, machine-specific paths, editor caches, and redistributable commercial font files.

## Gallery

| Scientific composite | Network structure |
|:--:|:--:|
| ![Scientific composite plot](docs/assets/gallery/scientific-combined-plot.png) | ![Grouped chord diagram](docs/assets/gallery/chord-diagram.png) |
| **Multi-panel scientific comparison** | **Grouped SDG chord diagram** |

| Multivariate structure | Three-dimensional comparison |
|:--:|:--:|
| ![Hexagonal correlation heatmap](docs/assets/gallery/correlation-heatmap-hexagon.png) | ![3D grouped bar chart](docs/assets/gallery/3d-grouped-bar-chart.png) |
| **Mixed hexagonal correlation map** | **3D grouped comparison chart** |

| Simulation and uncertainty | Flow and composition |
|:--:|:--:|
| ![Monte Carlo raincloud plot](docs/assets/gallery/monte-carlo-raincloud.png) | ![Sankey diagram](docs/assets/gallery/sankey-diagram.png) |
| **Monte Carlo raincloud distribution** | **Sankey flow diagram** |

![Scenario recovery trajectory](docs/assets/gallery/recovery-trajectory.png)

More previews are available in [`docs/assets/gallery`](docs/assets/gallery) and beside the scripts that generated them.

## What is included

| Collection | Focus | Code | Retained outputs |
|---|---|---:|---:|
| [`scientific-charts`](collections/scientific-charts) | Correlation matrices, chord diagrams, 3D comparisons, resilience and SDG strategy plots | 15 Python + 2 R | 21 |
| [`experimental-charts`](collections/experimental-charts) | Polar bubbles, radial layouts, regression panels, core–periphery graphs, XGBoost/SHAP | 19 Python | 21 |
| [`sports-analytics`](collections/sports-analytics) | Player rankings, roster flows, revenue composition, Monte Carlo and 3D waterfalls | 16 Python | 39 |
| [`sensitivity-analysis`](collections/sensitivity-analysis) | Parameter sweeps and comparative sensitivity curves | 3 Python | 9 |
| [`model-studies`](collections/model-studies) | Dynamic ranking, investment/popularity scenarios, season and recovery comparisons | 9 Python | 24 |
| [`sdg-systems`](collections/sdg-systems) | Dynamic weights, network centrality, Spearman inputs, and supporting model code | 5 Python | Data/model support |

See the [visualization catalog](docs/CATALOG.md) for chart families, representative scripts, input requirements, and expected output formats.

## Repository layout

```text
Draw-in-Win/
├── collections/
│   ├── experimental-charts/       # exploratory and advanced chart designs
│   ├── model-studies/
│   │   ├── dynamic-ranking/
│   │   ├── investment-and-popularity/
│   │   └── season-and-recovery/
│   ├── scientific-charts/         # general scientific figure recipes
│   ├── sdg-systems/               # SDG network/model inputs and utilities
│   ├── sensitivity-analysis/
│   └── sports-analytics/
├── docs/
│   ├── assets/gallery/             # normalized README previews
│   ├── CATALOG.md
│   └── REPRODUCIBILITY.md
├── tools/check_repository.py       # dependency-free repository health check
├── CONTRIBUTING.md
├── README.zh-CN.md
└── requirements.txt
```

Data is intentionally kept near the scripts that consume it. This minimizes hidden coupling and makes each collection easier to inspect independently.

## Quick start

### 1. Clone and create an environment

```bash
git clone https://github.com/Haohaha-11/Draw-in-Win.git
cd Draw-in-Win
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Or on macOS/Linux:

```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The full requirements file includes the heavier machine-learning stack used by the SHAP examples. If you only want Matplotlib-based figures, install `numpy pandas matplotlib scipy seaborn networkx openpyxl` first and add optional packages as needed.

The two R examples require `tidyverse`, `ggplot2`, and `reshape2`.

### 3. Run a self-contained example

```bash
python collections/scientific-charts/scientific_combined_plot.py
```

This example uses generated data and writes SVG and PNG files beside the script. For scripts using bundled data, run them from their collection directory unless the script already resolves paths from `__file__`:

```bash
cd collections/model-studies/season-and-recovery
python season_comparison_bar.py
```

## Reproducibility levels

The collection contains three kinds of recipes:

1. **Self-contained** — synthetic or embedded data; runs after dependencies are installed.
2. **Bundled-data** — reads CSV/XLSX assets committed beside the script.
3. **External-data template** — retained research code whose original input was not part of the source archive. Machine-specific paths have been replaced with documented repository-relative locations.

The exact conventions and missing-input layout are documented in the [reproducibility guide](docs/REPRODUCIBILITY.md). A script being syntactically valid does not imply that its domain-specific external dataset is included.

## Output conventions

Most recipes export one or more of the following:

- **PNG** at 300 DPI for previews, reports, and slides.
- **SVG** for editable vector artwork and web use.
- **PDF** for publication workflows and LaTeX documents.

The historical scripts generally write outputs beside themselves. Existing generated artifacts are retained so that visual designs can be evaluated without rerunning every model. When adapting a recipe, prefer `pathlib.Path(__file__).resolve().parent` for both input and output paths.

## Fonts and portability

The original project used Times New Roman font binaries from a local machine. Those files are deliberately not distributed here. Normalized scripts use Matplotlib's bundled **DejaVu Serif**, providing a redistributable and cross-platform fallback. You may set `font.family` to Times New Roman locally if your system installation and publication requirements permit it.

## Data and model safety

- CSV and XLSX files are ordinary tabular inputs; inspect their schemas before substituting your own data.
- Pickle/joblib model files can execute code during deserialization. Only load the bundled `.pkl` artifacts if you trust this repository and never load untrusted replacements.
- The HTML demos use third-party CDN resources and therefore need a network connection when opened.
- No API keys, credentials, or personal access tokens are required by the visualization scripts.

## Quality checks

Run the dependency-free health check before contributing:

```bash
python tools/check_repository.py
```

It verifies Python syntax, required documentation, gallery links, prohibited redistributable font files, and accidental machine-specific absolute paths. GitHub Actions runs the same check on pushes and pull requests.

## Project history

This repository is a curated and deduplicated presentation of an internal mathematical-modeling visualization workspace. Original topic clusters were reorganized into descriptive collections; exact duplicate nested copies, build caches, editor metadata, and proprietary font binaries were excluded. The source workspace is not modified by this curation process.

## Contributing

Contributions that improve portability, accessibility, visual consistency, or reproducibility are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. In particular, keep input data small and documented, avoid absolute paths, and commit at least one representative preview for a new chart family.

## Citation

If this collection supports your research or teaching, cite the repository:

```bibtex
@software{draw_in_win,
  author  = {Haohaha-11},
  title   = {Draw-in-Win: Scientific Visualization Recipes for Mathematical Modeling},
  year    = {2026},
  url     = {https://github.com/Haohaha-11/Draw-in-Win}
}
```

## License

No open-source license has been selected for this repository yet. Unless a license file is added, the code and assets remain **all rights reserved**. Third-party libraries and CDN resources retain their own licenses.
