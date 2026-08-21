# Draw-in-Win

**面向数学建模、科研论文与数据分析的高质量可视化代码集。**

[English README](README.md) · [图表目录](docs/CATALOG.md) · [复现说明](docs/REPRODUCIBILITY.md) · [贡献指南](CONTRIBUTING.md)

Draw-in-Win 是从真实数学建模研究项目中整理出的科研绘图库，现收录 **69 个 Python 脚本、2 个 R 脚本、配套示例数据，以及 130 个保留的 PNG/SVG/PDF 图表文件**。仓库重点覆盖相关性分析、网络关系、极坐标可视化、三维图、参数敏感性、模型对比、体育运营分析与可解释机器学习。

整理过程中保留了原图的论文级导出能力，同时完成了主题归档、确定重复项清理、机器绝对路径替换、商业字体文件排除和自动质量检查。原始代码目录没有被修改。

## 分类示例

六个顶层分类现在都提供一张代表性预览和一个可以直接运行的入口脚本。

| 通用科研图 | 实验性图表 |
|:--:|:--:|
| ![论文风格多模型雷达图](collections/scientific-charts/paper_style_multi_radar.png) | ![核心—边缘网络](collections/experimental-charts/core_periphery_network.png) |
| **论文风格多模型雷达图**<br>[查看脚本](collections/scientific-charts/paper_style_multi_radar.py) · `python collections/scientific-charts/paper_style_multi_radar.py` | **核心—边缘网络**<br>[查看脚本](collections/experimental-charts/hexin_bianyuan.py) · `python collections/experimental-charts/hexin_bianyuan.py` |

| 体育分析 | 敏感性分析 |
|:--:|:--:|
| ![球员对比雷达图](collections/sports-analytics/Rank/player_radar_chart.png) | ![Omega 参数敏感性曲线](collections/sensitivity-analysis/omega_sensitivity_W.png) |
| **球员对比雷达图**<br>[查看脚本](collections/sports-analytics/Rank/player_radar_chart.py) · `python collections/sports-analytics/Rank/player_radar_chart.py` | **Omega 参数敏感性曲线**<br>[查看脚本](collections/sensitivity-analysis/omega_sensitivity_plot.py) · `python collections/sensitivity-analysis/omega_sensitivity_plot.py` |

| 模型研究 | SDG 系统 |
|:--:|:--:|
| ![赛季策略对比](collections/model-studies/season-and-recovery/season_comparison_bar.png) | ![SDG 得分演化热图](collections/sdg-systems/sdg_score_evolution.png) |
| **赛季策略对比**<br>[查看脚本](collections/model-studies/season-and-recovery/season_comparison_bar.py) · `python collections/model-studies/season-and-recovery/season_comparison_bar.py` | **SDG 得分演化**<br>[查看脚本](collections/sdg-systems/sdg_score_evolution.py) · `python collections/sdg-systems/sdg_score_evolution.py` |

四联雷达图根据栅格参考图复现了版式与视觉风格。脚本已明确注明其中的基准数组为视觉反推占位值；如需进行定量比较，应替换为实验原始数据。

更多预览见 [`docs/assets/gallery`](docs/assets/gallery)，其他历史输出保留在对应脚本旁边。

## 完整图表图库

下面展示全部 **54 个不重复的保留预览**：`collections/` 下的每一张 PNG、3 个只有 SVG 的独立图，以及 3 张只存在于精选图库中的有效成品。完全相同的重复拷贝只展示一次。点击预览可打开原始尺寸；如有对应 SVG/PDF，它们仍保留在生成脚本旁边。

### 通用科研图——13 张

| 论文风格多模型雷达图 | 组合科研图 |
|:--:|:--:|
| [![论文风格多模型雷达图](collections/scientific-charts/paper_style_multi_radar.png)](collections/scientific-charts/paper_style_multi_radar.png) | [![组合科研图](collections/scientific-charts/scientific_combined_plot.png)](collections/scientific-charts/scientific_combined_plot.png) |
| **带误差线的分组柱状图** | **分组弦图** |
| [![带误差线的分组柱状图](collections/scientific-charts/grouped_bar_with_error.png)](collections/scientific-charts/grouped_bar_with_error.png) | [![分组弦图](collections/scientific-charts/grouped_chord_diagram.png)](collections/scientific-charts/grouped_chord_diagram.png) |
| **弦图独立图例** | **混合相关性矩阵** |
| [![弦图独立图例](collections/scientific-charts/chord_diagram_legend.png)](collections/scientific-charts/chord_diagram_legend.png) | [![混合相关性矩阵](collections/scientific-charts/mixed_correlation_matrix.png)](collections/scientific-charts/mixed_correlation_matrix.png) |
| **韧性轨迹图** | **SDG 最终得分对比** |
| [![韧性轨迹图](collections/scientific-charts/resilience_trajectory_plot.png)](collections/scientific-charts/resilience_trajectory_plot.png) | [![SDG 最终得分对比](collections/scientific-charts/sdg_final_scores_plot.png)](collections/scientific-charts/sdg_final_scores_plot.png) |
| **静态与动态权重对比** | **静态与动态权重图例** |
| [![静态与动态权重对比](collections/scientific-charts/static_vs_dynamic_weights_plot.png)](collections/scientific-charts/static_vs_dynamic_weights_plot.png) | [![静态与动态权重图例](collections/scientific-charts/static_vs_dynamic_legend.png)](collections/scientific-charts/static_vs_dynamic_legend.png) |
| **策略对比图** | **三维分组柱状图** |
| [![策略对比图](collections/scientific-charts/strategy_comparison_plot.png)](collections/scientific-charts/strategy_comparison_plot.png) | [![三维分组柱状图](docs/assets/gallery/3d-grouped-bar-chart.png)](docs/assets/gallery/3d-grouped-bar-chart.png) |
| **六边形相关性热图** | |
| [![六边形相关性热图](docs/assets/gallery/correlation-heatmap-hexagon.png)](docs/assets/gallery/correlation-heatmap-hexagon.png) | |

### 实验性图表——13 张

| 回归与密度诊断组合图 | 核心—边缘网络 |
|:--:|:--:|
| [![回归与密度诊断组合图](collections/experimental-charts/40.png)](collections/experimental-charts/40.png) | [![核心—边缘网络](collections/experimental-charts/core_periphery_network.png)](collections/experimental-charts/core_periphery_network.png) |
| **极坐标气泡图** | **Mantel 相关性热图** |
| [![极坐标气泡图](collections/experimental-charts/grain_polar_bubble.png)](collections/experimental-charts/grain_polar_bubble.png) | [![Mantel 相关性热图](collections/experimental-charts/mantel_heatmap.png)](collections/experimental-charts/mantel_heatmap.png) |
| **三维分组瀑布图** | **嵌套覆盖关系图** |
| [![三维分组瀑布图](collections/experimental-charts/output.png)](collections/experimental-charts/output.png) | [![嵌套覆盖关系图](collections/experimental-charts/recreated_chart.png)](collections/experimental-charts/recreated_chart.png) |
| **平滑径向图 v2** | **平滑径向图** |
| [![平滑径向图 v2](collections/experimental-charts/smooth_radial_chart_v2_1.png)](collections/experimental-charts/smooth_radial_chart_v2_1.png) | [![平滑径向图](collections/experimental-charts/smooth_radial_chart.png)](collections/experimental-charts/smooth_radial_chart.png) |
| **平滑光谱图** | **光谱图** |
| [![平滑光谱图](collections/experimental-charts/spectral_plot_smooth.png)](collections/experimental-charts/spectral_plot_smooth.png) | [![光谱图](collections/experimental-charts/spectral_plot.png)](collections/experimental-charts/spectral_plot.png) |
| **XGBoost 与 SHAP 分析** | **粮食产量图** |
| [![XGBoost 与 SHAP 分析](docs/assets/gallery/xgb-shap-analysis.png)](docs/assets/gallery/xgb-shap-analysis.png) | [![粮食产量图](collections/experimental-charts/grain_yield_chart.svg)](collections/experimental-charts/grain_yield_chart.svg) |
| **线性拟合诊断图** | |
| [![线性拟合诊断图](collections/experimental-charts/xianxingnihe.svg)](collections/experimental-charts/xianxingnihe.svg) | |

### 体育分析——16 张

| 三维分组柱状图 W | 三维实心分组柱状图 |
|:--:|:--:|
| [![三维分组柱状图 W](collections/sports-analytics/3d_bar_W_output.png)](collections/sports-analytics/3d_bar_W_output.png) | [![三维实心分组柱状图](collections/sports-analytics/3d_bar_W_solid_output.png)](collections/sports-analytics/3d_bar_W_solid_output.png) |
| **三维分组柱状图 v2** | **三维分组柱状图 SVG 变体** |
| [![三维分组柱状图 v2](collections/sports-analytics/3d_bar_W_v2_output.png)](collections/sports-analytics/3d_bar_W_v2_output.png) | [![三维分组柱状图 SVG 变体](collections/sports-analytics/3d_bar_W_output_1.svg)](collections/sports-analytics/3d_bar_W_output_1.svg) |
| **三维瀑布图 W 变体 2** | **三维瀑布图 C** |
| [![三维瀑布图 W 变体 2](collections/sports-analytics/3d_waterfall_2_W.png)](collections/sports-analytics/3d_waterfall_2_W.png) | [![三维瀑布图 C](collections/sports-analytics/3d_waterfall_C.png)](collections/sports-analytics/3d_waterfall_C.png) |
| **三维瀑布图 P** | **三维瀑布图 W** |
| [![三维瀑布图 P](collections/sports-analytics/3d_waterfall_P.png)](collections/sports-analytics/3d_waterfall_P.png) | [![三维瀑布图 W](collections/sports-analytics/3d_waterfall_W.png)](collections/sports-analytics/3d_waterfall_W.png) |
| **收入构成环形图** | **阵容流动桑基图** |
| [![收入构成环形图](collections/sports-analytics/Components/lakers_revenue_donut.png)](collections/sports-analytics/Components/lakers_revenue_donut.png) | [![阵容流动桑基图](collections/sports-analytics/Components/lakers_sankey.png)](collections/sports-analytics/Components/lakers_sankey.png) |
| **蒙特卡洛雨云图** | **球员排名花瓣图** |
| [![蒙特卡洛雨云图](collections/sports-analytics/monte_carlo_raincloud.png)](collections/sports-analytics/monte_carlo_raincloud.png) | [![球员排名花瓣图](collections/sports-analytics/player_ranking_petal.png)](collections/sports-analytics/player_ranking_petal.png) |
| **球员 Delta-V 排名图** | **球员排名玫瑰图** |
| [![球员 Delta-V 排名图](collections/sports-analytics/Rank/lakers_deltaV_bar_chart.png)](collections/sports-analytics/Rank/lakers_deltaV_bar_chart.png) | [![球员排名玫瑰图](collections/sports-analytics/Rank/lakers_ranking_rose_chart.png)](collections/sports-analytics/Rank/lakers_ranking_rose_chart.png) |
| **球员对比雷达图** | **带状编码图** |
| [![球员对比雷达图](collections/sports-analytics/Rank/player_radar_chart.png)](collections/sports-analytics/Rank/player_radar_chart.png) | [![带状编码图](collections/sports-analytics/tiaodai_output.png)](collections/sports-analytics/tiaodai_output.png) |

### 敏感性分析——3 张

| Omega 敏感性 W | Omega 敏感性 P |
|:--:|:--:|
| [![Omega 敏感性 W](collections/sensitivity-analysis/omega_sensitivity_W.png)](collections/sensitivity-analysis/omega_sensitivity_W.png) | [![Omega 敏感性 P](collections/sensitivity-analysis/omega_sensitivity_P.png)](collections/sensitivity-analysis/omega_sensitivity_P.png) |
| **Omega 敏感性 C** | |
| [![Omega 敏感性 C](collections/sensitivity-analysis/omega_sensitivity_C.png)](collections/sensitivity-analysis/omega_sensitivity_C.png) | |

### 模型研究——8 张

| 基准候选排名 | Case-B 候选排名 |
|:--:|:--:|
| [![基准候选排名](collections/model-studies/dynamic-ranking/Dynamic/baseline_candidate_rank_bar.png)](collections/model-studies/dynamic-ranking/Dynamic/baseline_candidate_rank_bar.png) | [![Case-B 候选排名](collections/model-studies/dynamic-ranking/Dynamic/case_b_candidate_rank_bar.png)](collections/model-studies/dynamic-ranking/Dynamic/case_b_candidate_rank_bar.png) |
| **现金流散点图** | **投资—热度散点图** |
| [![现金流散点图](collections/model-studies/investment-and-popularity/Model_4新/cash_flow_scatter.png)](collections/model-studies/investment-and-popularity/Model_4新/cash_flow_scatter.png) | [![投资—热度散点图](collections/model-studies/investment-and-popularity/Model_4新/investment_pop_scatter.png)](collections/model-studies/investment-and-popularity/Model_4新/investment_pop_scatter.png) |
| **热度策略对比** | **热度构成饼图** |
| [![热度策略对比](collections/model-studies/investment-and-popularity/pop_comparison.png)](collections/model-studies/investment-and-popularity/pop_comparison.png) | [![热度构成饼图](collections/model-studies/investment-and-popularity/pop_pie_chart.png)](collections/model-studies/investment-and-popularity/pop_pie_chart.png) |
| **赛季策略对比** | **多赛季恢复轨迹** |
| [![赛季策略对比](collections/model-studies/season-and-recovery/season_comparison_bar.png)](collections/model-studies/season-and-recovery/season_comparison_bar.png) | [![多赛季恢复轨迹](collections/model-studies/season-and-recovery/v_recovery_plot.png)](collections/model-studies/season-and-recovery/v_recovery_plot.png) |

### SDG 系统——1 张

| SDG 得分演化 | |
|:--:|:--:|
| [![SDG 得分演化](collections/sdg-systems/sdg_score_evolution.png)](collections/sdg-systems/sdg_score_evolution.png) | |

## 内容结构

| 主题集合 | 主要内容 |
|---|---|
| [`scientific-charts`](collections/scientific-charts) | 相关性矩阵、弦图、多模型雷达图、组合科研图、SDG 策略对比和三维图 |
| [`experimental-charts`](collections/experimental-charts) | 极坐标气泡、雷达图、玫瑰图、回归拟合、核心—边缘网络、XGBoost/SHAP |
| [`sports-analytics`](collections/sports-analytics) | 球员排名、阵容流动、收入构成、蒙特卡洛分析和三维瀑布图 |
| [`sensitivity-analysis`](collections/sensitivity-analysis) | 不同参数配置下的敏感性比较 |
| [`model-studies`](collections/model-studies) | 动态排名、投资—热度关系、赛季决策和恢复过程 |
| [`sdg-systems`](collections/sdg-systems) | SDG 得分演化、动态权重、网络中心性、Spearman 数据与模型辅助代码 |

更细的“图表类型—代码—数据—输出格式”对应关系见[图表目录](docs/CATALOG.md)。

## 快速开始

```bash
git clone https://github.com/Haohaha-11/Draw-in-Win.git
cd Draw-in-Win
python -m venv .venv
```

Windows PowerShell：

```powershell
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

运行本次新增、且不依赖外部数据的四联雷达图示例：

```bash
python collections/scientific-charts/paper_style_multi_radar.py
```

脚本会在同一目录导出 PNG、SVG 和 PDF。也可以运行组合科研图示例：

```bash
python collections/scientific-charts/scientific_combined_plot.py
```

运行包含配套数据的赛季对比示例：

```bash
cd collections/model-studies/season-and-recovery
python season_comparison_bar.py
```

R 语言示例还需要安装 `tidyverse`、`ggplot2` 和 `reshape2`。

## 可复现性分级

仓库中的代码分为三类：

1. **完全自包含**：脚本内部生成数据，安装依赖后即可运行。
2. **仓库数据驱动**：CSV/XLSX 数据与脚本一并保留。
3. **外部数据模板**：原项目输入数据不在旧代码目录中；原有本机绝对路径已经改成清晰的仓库相对路径，并在文档中写明预期文件结构。

具体说明见[复现指南](docs/REPRODUCIBILITY.md)。部分历史脚本通过语法检查并不代表其专用研究数据已经包含在仓库内。

## 输出与排版

- PNG：通常以 300 DPI 输出，适合报告、幻灯片和快速预览。
- SVG：适合在 Illustrator、Inkscape 或网页环境中继续编辑。
- PDF：适合论文排版和 LaTeX 工作流。

历史脚本一般将图表输出到脚本所在的 collection。仓库同时保留了代表性成品，便于不运行模型就能查看设计效果。

## 字体与跨平台兼容

旧项目曾直接引用本机的 Times New Roman 字体文件。为了避免商业字体再分发风险，新仓库不包含相关 TTF/ZIP 文件，并统一使用 Matplotlib 自带的 **DejaVu Serif** 作为可移植回退字体。如本机已合法安装 Times New Roman，可按投稿规范自行切换 `font.family`。

## 质量检查

```bash
python tools/check_repository.py
```

该检查会验证所有 Python 文件的语法、必需文档、README 图像链接、商业字体文件、疑似密钥和机器专用绝对路径。相同检查也会在 GitHub Actions 中运行。

## 数据安全说明

- 加载自定义 CSV/XLSX 前，请先确认列名和量纲与脚本预期一致。
- Pickle/joblib 文件在反序列化时可能执行代码，只应加载可信来源的 `.pkl` 文件。
- HTML 示例依赖第三方 CDN，离线环境下可能无法完整显示。
- 绘图代码不需要 API Key、访问令牌或其他账号凭证。

## 贡献与引用

新增图表时，请避免硬编码绝对路径，附带小型、可公开的数据样例，并至少提交一张代表性预览。完整要求见[贡献指南](CONTRIBUTING.md)。

引用格式可使用：

```bibtex
@software{draw_in_win,
  author  = {Haohaha-11},
  title   = {Draw-in-Win: Scientific Visualization Recipes for Mathematical Modeling},
  year    = {2026},
  url     = {https://github.com/Haohaha-11/Draw-in-Win}
}
```

## 许可证

仓库目前尚未选择开源许可证。在正式添加许可证文件之前，代码和图表资产默认为**保留所有权利**；第三方依赖及 CDN 资源分别遵循其自身许可证。
