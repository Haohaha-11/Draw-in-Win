"""
静态权重 vs 动态权重对比图：两种策略在2036年各SDG上的得分对比
主图：各SDG的最终得分折线图
插图：实现目标的个数（≥90分）
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR / 'data' / 'sdg-strategies'

# 设置Times New Roman字体
font_path = fm.findfont('DejaVu Serif')
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = font_prop.get_name()
fm.fontManager.addfont(font_path)

# 1. 读取数据函数
def parse_sdg_predictions(file_path):
    """
    解析SDG预测文件，提取每年每个SDG的得分
    返回：字典 {year: {sdg_num: score}}
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 存储数据：{year: {sdg_num: score}}
    data = {}
    current_sdg = None

    for line in lines:
        line = line.strip()

        # 匹配SDG编号行
        sdg_match = re.match(r'SDG\s+(\d+):', line)
        if sdg_match:
            current_sdg = int(sdg_match.group(1))
            continue

        # 匹配年份和得分行
        year_match = re.match(r'(\d{4})年:\s+([\d.]+)', line)
        if year_match and current_sdg is not None:
            year = int(year_match.group(1))
            score = float(year_match.group(2))

            if year not in data:
                data[year] = {}
            data[year][current_sdg] = score

    return data

# 2. 读取两个策略的数据
print("正在读取数据...")
static_data = parse_sdg_predictions(DATA_DIR / 'centralities' / 'SDG_predictions_2025_2036.txt')
dynamic_data = parse_sdg_predictions(DATA_DIR / 'dynamic' / 'SDG_predictions_2036.txt')

# 3. 提取2036年各SDG的得分
final_year = 2036
sdg_numbers = list(range(1, 18))  # SDG 1-17

static_final = [static_data[final_year][sdg] for sdg in sdg_numbers]
dynamic_final = [dynamic_data[final_year][sdg] for sdg in sdg_numbers]

print(f"\n{final_year}年各SDG得分已提取")

# 4. 计算每个策略的最高值和最低值
static_max = max(static_final)
static_min = min(static_final)
dynamic_max = max(dynamic_final)
dynamic_min = min(dynamic_final)

print(f"\n各策略得分范围：")
print(f"  Static Weights: 最高 {static_max:.2f}, 最低 {static_min:.2f}")
print(f"  Dynamic Weights: 最高 {dynamic_max:.2f}, 最低 {dynamic_min:.2f}")

# 5. 定义配色方案
colors = {
    'static': '#d6e7f1',      # 浅蓝色
    'dynamic': '#fdd29a'      # 浅橙色
}

# 6. 创建主图
fig, ax = plt.subplots(figsize=(12, 6))

# 绘制两条折线（带标记）
ax.plot(sdg_numbers, static_final,
        linestyle='--', marker='s', markersize=7,
        color=colors['static'], markerfacecolor=colors['static'],
        markeredgecolor='black', markeredgewidth=0.5,
        linewidth=2.5, label='Static Weights', zorder=3)

ax.plot(sdg_numbers, dynamic_final,
        linestyle='--', marker='o', markersize=7,
        color=colors['dynamic'], markerfacecolor=colors['dynamic'],
        markeredgecolor='black', markeredgewidth=0.5,
        linewidth=2.5, label='Dynamic Weights', zorder=3)

# 添加90分阈值线
threshold = 90
ax.axhline(y=threshold, color='red', linestyle=':', linewidth=2,
           label=f'Threshold ({threshold})', alpha=0.7, zorder=2)

# 7. 设置主图样式
# 坐标轴标签
ax.set_xlabel('SDG Number', fontsize=16, fontweight='bold', fontproperties=font_prop)
ax.set_ylabel('Final Score (2036)', fontsize=16, fontweight='bold', fontproperties=font_prop)

# 设置坐标轴范围
ax.set_xlim(0.5, 17.5)
ax.set_xticks(sdg_numbers)
ax.set_xticklabels([str(i) for i in sdg_numbers])

# 纵坐标范围
all_scores = static_final + dynamic_final
y_min = min(all_scores) - 10
y_max = max(all_scores) + 5
ax.set_ylim(y_min, y_max)

# 刻度朝内
ax.tick_params(axis='both', which='major', direction='in',
               labelsize=12, width=1.5, length=6)
ax.tick_params(axis='both', which='minor', direction='in',
               width=1, length=3)

# 加粗边框
for spine in ax.spines.values():
    spine.set_linewidth(1.5)

# 添加网格
ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5, axis='y')

# 添加图例（放在左下角）
legend = ax.legend(loc='lower left', fontsize=10, frameon=True,
                   fancybox=False, shadow=False, prop=font_prop,
                   framealpha=0.95, ncol=2)
legend.get_frame().set_linewidth(1.5)

# 8. 创建插图（中间偏左下方的柱状图）- 显示最高值和最低值
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# 使用bbox_to_anchor精确定位到中间偏左下方
ax_inset = inset_axes(ax, width="50%", height="56%",
                      loc='center',
                      bbox_to_anchor=(0.15, 0.05, 0.5, 0.56),
                      bbox_transform=ax.transAxes)

# 插图数据：最高值和最低值
categories = ['Static\nWeights', 'Dynamic\nWeights']
max_values = [static_max, dynamic_max]
min_values = [static_min, dynamic_min]

# 设置柱子位置
x = np.arange(len(categories))
width = 0.35  # 柱子宽度

# 绘制最高值和最低值的柱状图
bars_max = ax_inset.bar(x - width/2, max_values, width,
                        label='Max Score',
                        color=colors['static'],
                        edgecolor='black', linewidth=1.5,
                        hatch='////', alpha=0.8)

bars_min = ax_inset.bar(x + width/2, min_values, width,
                        label='Min Score',
                        color=colors['dynamic'],
                        edgecolor='black', linewidth=1.5,
                        hatch='\\\\\\\\', alpha=0.8)

# 在柱子上方标注数值
for i, val in enumerate(max_values):
    ax_inset.text(i - width/2, val + 1, f'{val:.1f}',
                  ha='center', va='bottom',
                  fontsize=11, fontweight='bold',
                  fontproperties=font_prop)

for i, val in enumerate(min_values):
    ax_inset.text(i + width/2, val + 1, f'{val:.1f}',
                  ha='center', va='bottom',
                  fontsize=11, fontweight='bold',
                  fontproperties=font_prop)

# 设置插图样式
ax_inset.set_ylabel('Score', fontsize=13, fontweight='bold',
                    fontproperties=font_prop)
ax_inset.set_title('Max & Min Scores (2036)', fontsize=12,
                   fontproperties=font_prop, pad=8)
ax_inset.set_xticks(x)
ax_inset.set_xticklabels(categories, fontproperties=font_prop, fontsize=11)
ax_inset.tick_params(axis='both', labelsize=10, direction='in', width=1.5, length=5)

# 不在插图内添加图例，将单独生成

# 移除插图的右边框和上边框
ax_inset.spines['right'].set_visible(False)
ax_inset.spines['top'].set_visible(False)

# 加粗插图的左边框和下边框
ax_inset.spines['left'].set_linewidth(1.5)
ax_inset.spines['bottom'].set_linewidth(1.5)

# 设置y轴范围
y_range = max(max_values) - min(min_values)
ax_inset.set_ylim(min(min_values) - y_range * 0.1, max(max_values) + y_range * 0.15)

# 设置插图背景为白色
ax_inset.patch.set_facecolor('white')
ax_inset.patch.set_alpha(1.0)

# 9. 调整布局并保存
plt.tight_layout()

# 保存为SVG和PNG格式
output_svg = SCRIPT_DIR / 'static_vs_dynamic_weights_plot.svg'
output_png = SCRIPT_DIR / 'static_vs_dynamic_weights_plot.png'

plt.savefig(output_svg, format='svg', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig(output_png, format='png', dpi=300, bbox_inches='tight', facecolor='white')

print(f"\n图表已保存：")
print(f"  SVG: {output_svg}")
print(f"  PNG: {output_png}")

# 10. 单独生成柱状图图例
fig_legend, ax_legend = plt.subplots(figsize=(4, 2))
ax_legend.axis('off')

# 创建图例元素
from matplotlib.patches import Rectangle
legend_elements = [
    Rectangle((0, 0), 1, 1, fc=colors['static'], ec='black',
              linewidth=1.5, hatch='////', alpha=0.8, label='Max Score'),
    Rectangle((0, 0), 1, 1, fc=colors['dynamic'], ec='black',
              linewidth=1.5, hatch='\\\\\\\\', alpha=0.8, label='Min Score')
]

legend = ax_legend.legend(handles=legend_elements, loc='center',
                         fontsize=12, frameon=True,
                         fancybox=False, shadow=False, prop=font_prop,
                         ncol=2)
legend.get_frame().set_linewidth(1.5)

# 保存图例
legend_svg = SCRIPT_DIR / 'static_vs_dynamic_legend.svg'
legend_png = SCRIPT_DIR / 'static_vs_dynamic_legend.png'
fig_legend.savefig(legend_svg, format='svg', dpi=300, bbox_inches='tight', facecolor='white')
fig_legend.savefig(legend_png, format='png', dpi=300, bbox_inches='tight', facecolor='white')

print(f"\n图例已单独保存：")
print(f"  SVG: {legend_svg}")
print(f"  PNG: {legend_png}")

plt.close(fig_legend)

# 打印详细统计
print(f"\n{final_year}年各SDG得分对比：")
print(f"{'SDG':<5} {'Static':<10} {'Dynamic':<10} {'Difference':<10}")
print("-" * 40)
for i, sdg in enumerate(sdg_numbers):
    diff = dynamic_final[i] - static_final[i]
    print(f"{sdg:<5} {static_final[i]:<10.2f} {dynamic_final[i]:<10.2f} {diff:+10.2f}")

print(f"\n平均得分：")
print(f"  Static Weights: {np.mean(static_final):.2f}")
print(f"  Dynamic Weights: {np.mean(dynamic_final):.2f}")
print(f"  提升: {np.mean(dynamic_final) - np.mean(static_final):+.2f}")

plt.show()
