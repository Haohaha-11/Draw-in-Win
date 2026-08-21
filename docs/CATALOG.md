# Visualization catalog

This catalog maps the principal chart families to representative scripts, data expectations, and retained outputs. It is intentionally curated: every source file remains available under `collections/`, while this page highlights the most useful starting points.

## Scientific charts

Location: [`collections/scientific-charts`](../collections/scientific-charts)

| Family | Representative script | Data | Typical output |
|---|---|---|---|
| 3D grouped bars | `3d_grouped_bar_chart.py` | Embedded | PNG, PDF, SVG |
| 3D strategy comparison | `3d_grouped_comparison_chart.py` | Embedded | PNG, PDF |
| Correlation heatmap | `correlation_heatmap.py` | Embedded matrix | PNG |
| Mixed matrix/hexagon | `mixed_correlation_matrix.py` | Bundled `Spearman_2.csv` | PNG, SVG |
| Grouped bars with error | `grouped_bar_with_error.py` | Embedded | PNG, PDF, SVG |
| Grouped chord diagram | `grouped_chord_diagram.py` | Bundled centrality and Spearman data | PNG, SVG, CSV |
| Resilience trajectory | `resilience_trajectory_plot.py` | Embedded | PNG, SVG |
| Scientific composite panel | `scientific_combined_plot.py` | Synthetic | PNG, SVG |
| SDG strategy comparison | `strategy_comparison_plot.py` | External scenario text files | PNG, SVG |
| Static vs dynamic weights | `static_vs_dynamic_weights_plot.py` | External scenario text files | PNG, SVG |
| R mixed correlation charts | `mixed_correlation_heatmap.R`, `mixed_correlation_hexagon.R` | Correlation table | R graphics device |

## Experimental charts

Location: [`collections/experimental-charts`](../collections/experimental-charts)

| Family | Representative script | Notes |
|---|---|---|
| XGBoost + SHAP | `xgb_shap.py`, `xgb_shap_2.py` | Generates or uses simulated data; heaviest dependencies |
| Core–periphery network | `hexin_bianyuan.py`, `hexin_bianyuan_2.py` | Network-based structural layouts |
| Polar bubble/radar | `leida_qipao.py`, `qipao_leida.py`, `polar_coverage_chart.py` | Multivariate radial encodings |
| Rose charts | `meigui.py`, `meigui_2.py` | Ranked radial categories |
| Smooth radial chart | `smooth_radial_chart.py` | Self-contained radial interpolation |
| Regression panels | `huiguinihe.py`, `xianxingnihe.py` | Regression and diagnostic presentation |
| Correlation/quadrant views | `xiangguanxing.py`, `xiangxian.py` | Relationship and quadrant analysis |
| 3D waterfalls | `3d_pubu.py`, `3d_pubu_2.py` | Layered 3D trend surfaces |
| Chord and yield experiments | `fenzuhexian.py`, `yunyu.py` | Grouped chord and yield-oriented designs |

## Sports analytics

Location: [`collections/sports-analytics`](../collections/sports-analytics)

| Family | Representative script | Bundled data/output location |
|---|---|---|
| Revenue composition | `donut_chart.py` | `Components/` |
| Roster flow | `sankey_chart.py` | `Components/` |
| Player radar | `Rank/player_radar_chart.py` | `Rank/` |
| Ranking rose chart | `rank.py` | `Rank/` |
| Ranking bar chart | `rank_bar.py` | `Rank/` |
| Monte Carlo raincloud | `monte.py` | `monte_carlo/` and root output |
| 3D waterfall | `3d_pubu_*.py` | Root CSVs and SVG/PNG outputs |
| 3D grouped bars | `3d_bar_W*.py` | `wpc.csv` |
| Ribbon/petal encodings | `tiaodai.py`, `huaban.py` | Root outputs |

## Sensitivity analysis

Location: [`collections/sensitivity-analysis`](../collections/sensitivity-analysis)

The three `omega_sensitivity_plot*.py` variants compare W, P, and C trajectories across multiple omega values. Five bundled `wpc_timeseries_omega*.csv` files support direct reproduction. Each variant retains PDF, PNG, and SVG exports.

## Model studies

Location: [`collections/model-studies`](../collections/model-studies)

- `dynamic-ranking/` contains baseline and scenario-specific candidate ranking charts plus dynamic/static state tables.
- `investment-and-popularity/` contains cash-flow and investment/popularity scatter plots, popularity comparisons, and four policy scenarios.
- `season-and-recovery/` contains season decision comparisons and multi-season recovery trajectories.

## SDG systems

Location: [`collections/sdg-systems`](../collections/sdg-systems)

This collection is primarily a data and modeling dependency for visualizations elsewhere in the repository:

- `data/` — raw, score, rank, and Spearman matrices.
- `dynamic-weights/` — parameter fitting and Excel conversion utilities.
- `network-and-prior/` — network construction, centrality calculations, and SDG label mapping.

## Choosing an export format

| Format | Best use | Trade-off |
|---|---|---|
| PNG | README previews, slides, raster-first reports | Not ideal for large-scale editing |
| SVG | Web, Illustrator/Inkscape editing, reusable labels | Some journal workflows need conversion |
| PDF | Papers, LaTeX, print | Harder to edit element-by-element |

For new work, export SVG plus a 300-DPI PNG preview. Add PDF when the target publication or typesetting workflow benefits from it.
