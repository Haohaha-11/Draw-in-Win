"""
策略对比图：三种策略（Ours, Random, Average）的SDG平均得分对比
主图：时间序列折线图
插图：2036年最终得分柱状图
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
    返回：字典 {year: [sdg1_score, sdg2_score, ..., sdg17_score]}
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

# 2. 读取三个策略的数据
print("正在读取数据...")
ours_data = parse_sdg_predictions(DATA_DIR / 'centralities' / 'SDG_predictions_2025_2036.txt')
random_data = parse_sdg_predictions(DATA_DIR / 'random' / 'SDG_predictions_2025_2036.txt')
average_data = parse_sdg_predictions(DATA_DIR / 'average' / 'SDG_predictions_2025_2036.txt')

# 3. 计算每年的平均得分
years = sorted(ours_data.keys())
print(f"年份范围: {years[0]} - {years[-1]}")

ours_avg = []
random_avg = []
average_avg = []

for year in years:
    # 计算该年17个SDG的平均得分
    ours_scores = [ours_data[year][sdg] for sdg in range(1, 18)]
    random_scores = [random_data[year][sdg] for sdg in range(1, 18)]
    average_scores = [average_data[year][sdg] for sdg in range(1, 18)]

    ours_avg.append(np.mean(ours_scores))
    random_avg.append(np.mean(random_scores))
    average_avg.append(np.mean(average_scores))

print(f"\n各策略平均得分范围:")
print(f"  Ours: {min(ours_avg):.2f} - {max(ours_avg):.2f}")
print(f"  Random: {min(random_avg):.2f} - {max(random_avg):.2f}")
print(f"  Average: {min(average_avg):.2f} - {max(average_avg):.2f}")

# 4. 定义配色方案（使用之前的颜色）
colors = {
    'ours': '#d6e7f1',      # 浅蓝色
    'random': '#fdd29a',    # 浅橙色
    'average': '#fbb5ae'    # 浅粉色
}

# 5. 创建主图
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制三条折线（带标记）
marker_interval = 1  # 每个年份都显示标记

ax.plot(years[::marker_interval], ours_avg[::marker_interval],
        linestyle='--', marker='s', markersize=7,
        color=colors['ours'], markerfacecolor=colors['ours'],
        markeredgecolor='black', markeredgewidth=0.5,
        linewidth=2.5, label='Ours', zorder=3)

ax.plot(years[::marker_interval], random_avg[::marker_interval],
        linestyle='--', marker='o', markersize=7,
        color=colors['random'], markerfacecolor=colors['random'],
        markeredgecolor='black', markeredgewidth=0.5,
        linewidth=2.5, label='Random', zorder=3)

ax.plot(years[::marker_interval], average_avg[::marker_interval],
        linestyle='--', marker='^', markersize=7,
        color=colors['average'], markerfacecolor=colors['average'],
        markeredgecolor='black', markeredgewidth=0.5,
        linewidth=2.5, label='Average', zorder=3)

# 6. 设置主图样式
# 坐标轴标签
ax.set_xlabel('Year', fontsize=16, fontweight='bold', fontproperties=font_prop)
ax.set_ylabel('Average SDG Score', fontsize=16, fontweight='bold', fontproperties=font_prop)

# 设置坐标轴范围
ax.set_xlim(years[0] - 0.5, years[-1] + 0.5)
# 增大下方空间，减少上方空间
y_min = min(min(ours_avg), min(random_avg), min(average_avg)) - 8
y_max = max(max(ours_avg), max(random_avg), max(average_avg)) + 3
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
ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)

# 添加图例（放在左上角）
legend = ax.legend(loc='upper left', fontsize=10, frameon=True,
                   fancybox=False, shadow=False, prop=font_prop,
                   framealpha=0.95)
legend.get_frame().set_linewidth(1.5)

# 7. 创建插图（右下角的柱状图）- 显示2036年的最终得分
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

ax_inset = inset_axes(ax, width="30%", height="30%",
                      loc='lower right',
                      bbox_to_anchor=(0, 0, 1, 1),
                      bbox_transform=ax.transAxes,
                      borderpad=2)

# 插图数据：2036年的平均得分
categories = ['Ours', 'Random', 'Average']
final_scores = [ours_avg[-1], random_avg[-1], average_avg[-1]]
bar_colors = [colors['ours'], colors['random'], colors['average']]

# 绘制柱状图
x_pos = np.arange(len(categories))
bars = ax_inset.bar(x_pos, final_scores, color=bar_colors,
                    edgecolor='black', linewidth=1,
                    hatch='////', alpha=0.8, width=0.6)

# 在柱子上方标注数值
for i, (cat, score) in enumerate(zip(categories, final_scores)):
    ax_inset.text(i, score + 0.5, f'{score:.1f}',
                  ha='center', va='bottom',
                  fontsize=9, fontweight='bold',
                  fontproperties=font_prop)

# 设置插图样式
ax_inset.set_ylabel('Final Score (2036)', fontsize=9, fontweight='bold',
                    fontproperties=font_prop)
ax_inset.set_xticks(x_pos)
ax_inset.set_xticklabels(categories, fontproperties=font_prop, fontsize=8, rotation=15)
ax_inset.tick_params(axis='both', labelsize=8, direction='in')

# 移除插图的右边框和上边框
ax_inset.spines['right'].set_visible(False)
ax_inset.spines['top'].set_visible(False)

# 加粗插图的左边框和下边框
ax_inset.spines['left'].set_linewidth(1.5)
ax_inset.spines['bottom'].set_linewidth(1.5)

# 设置y轴范围
ax_inset.set_ylim(min(final_scores) - 5, max(final_scores) + 3)

# 设置插图背景为白色
ax_inset.patch.set_facecolor('white')
ax_inset.patch.set_alpha(1.0)

# 8. 调整布局并保存
plt.tight_layout()

# 保存为SVG和PNG格式
output_svg = SCRIPT_DIR / 'strategy_comparison_plot.svg'
output_png = SCRIPT_DIR / 'strategy_comparison_plot.png'

plt.savefig(output_svg, format='svg', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig(output_png, format='png', dpi=300, bbox_inches='tight', facecolor='white')

print(f"\n图表已保存：")
print(f"  SVG: {output_svg}")
print(f"  PNG: {output_png}")

# 打印统计信息
print(f"\n2036年最终平均得分：")
print(f"  Ours: {ours_avg[-1]:.2f}")
print(f"  Random: {random_avg[-1]:.2f}")
print(f"  Average: {average_avg[-1]:.2f}")
print(f"\nOurs策略相比Random提升: {ours_avg[-1] - random_avg[-1]:.2f}")
print(f"Ours策略相比Average提升: {ours_avg[-1] - average_avg[-1]:.2f}")

plt.show()
