# Reproducibility guide

Draw-in-Win preserves research visualization recipes at different stages of maturity. This document makes those differences explicit so that a missing domain dataset is not confused with a code defect.

## Level A — self-contained recipes

These scripts generate or embed their own data and are the fastest way to explore the visual designs:

- `collections/scientific-charts/scientific_combined_plot.py`
- `collections/scientific-charts/resilience_trajectory_plot.py`
- `collections/scientific-charts/3d_grouped_bar_chart.py`
- `collections/scientific-charts/grouped_bar_with_error.py`
- `collections/scientific-charts/adaptive_stage_empirical_study.py`
- `collections/scientific-charts/progressive_stage_empirical_study.py`
- `collections/scientific-charts/efficiency_studies.py`
- `collections/scientific-charts/stage_ablation_studies.py`
- `collections/scientific-charts/pruning_layer_schedule.py`
- `collections/experimental-charts/smooth_radial_chart.py`
- `collections/experimental-charts/xgb_shap_2.py` (computationally heavier)

The paper-reference scripts are self-contained and deterministic, but their embedded values were transcribed or visually reconstructed from raster references. They reproduce figure designs and should not be treated as the source experiments' measurements. Replace the documented arrays, checkpoints, sequences, and analytic surface before making quantitative claims.

## Level B — bundled-data recipes

These collections retain the relevant CSV/XLSX inputs:

- `collections/sensitivity-analysis/`
- `collections/model-studies/dynamic-ranking/`
- `collections/model-studies/investment-and-popularity/`
- `collections/model-studies/season-and-recovery/`
- `collections/sports-analytics/`
- the correlation/network workflows using `collections/sdg-systems/data/`

Some historical scripts still assume they are launched from their own collection directory. If a relative path cannot be found, change into that directory before running the script.

## Level C — external-data templates

The original source archive referenced SDG prediction text files stored outside the code directory. The machine-specific paths have been normalized to:

```text
collections/scientific-charts/data/sdg-strategies/
├── average/SDG_predictions_2025_2036.txt
├── centralities/SDG_predictions_2025_2036.txt
├── dynamic/SDG_predictions_2036.txt
└── random/SDG_predictions_2025_2036.txt
```

The expected text format contains SDG section headers and annual values, for example:

```text
SDG 1:
2025年: 82.31
2026年: 83.04
```

These external scenario files were not present in the source workspace and are therefore not fabricated here. Add authorized copies at the documented locations to run:

- `sdg_final_scores_plot.py`
- `strategy_comparison_plot.py`
- `static_vs_dynamic_weights_plot.py`

## Working directory

Newly normalized scripts use `pathlib.Path(__file__)` for critical inputs and outputs. Older recipes may use short paths such as `Rank/...` or `Components/...`; run those from `collections/sports-analytics` so their local data folders resolve correctly.

## Fonts

Commercial Times New Roman font binaries from the original machine are excluded. Scripts that explicitly loaded those files now use Matplotlib's bundled DejaVu Serif. This makes headless and Linux rendering more predictable while retaining a serif publication style.

## Determinism

Many synthetic examples set a NumPy or Python random seed. Model fitting, parallel grid search, library version differences, and platform font rendering can still introduce small changes. Treat retained figures as design references rather than byte-for-byte golden files.

## Validation scope

`python tools/check_repository.py` performs static validation only. It compiles every Python source file in memory and checks repository invariants, but it does not install dependencies, train models, or execute every chart. Representative runtime tests should be performed in a clean virtual environment before a tagged release.
