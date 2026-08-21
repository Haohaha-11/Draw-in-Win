"""
SDG最终得分对比图：三种策略在2036年各SDG上的得分对比
主图：各SDG的最终得分柱状图/折线图
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

# 2. 读取三个策略的数据
print("正在读取数据...")
ours_data = parse_sdg_predictions(DATA_DIR / 'centralities' / 'SDG_predictions_2025_2036.txt')
random_data = parse_sdg_predictions(DATA_DIR / 'random' / 'SDG_predictions_2025_2036.txt')
average_data = parse_sdg_predictions(DATA_DIR / 'average' / 'SDG_predictions_2025_2036.txt')

# 3. 提取2036年各SDG的得分
final_year = 2036
sdg_numbers = list(range(1, 18))  # SDG 1-17

ours_final = [ours_data[final_year][sdg] for sdg in sdg_numbers]
random_final = [random_data[final_year][sdg] for sdg in sdg_numbers]
average_final = [average_data[final_year][sdg] for sdg in sdg_numbers]

print(f"\n{final_year}年各SDG得分已提取")

# 4. 计算实现目标的个数（≥90分）
threshold = 90
ours_achieved = sum(1 for score in ours_final if score >= threshold)
random_achieved = sum(1 for score in random_final if score >= threshold)
average_achieved = sum(1 for score in average_final if score >= threshold)

print(f"\n实现目标个数（≥{threshold}分）：")
print(f"  Ours: {ours_achieved}/17")
print(f"  Random: {random_achieved}/17")
print(f"  Average: {average_achieved}/17")

# 5. 定义配色方案
colors = {
    'ours': '#d6e7f1',      # 浅蓝色
    'random': '#fdd29a',    # 浅橙色
    'average': '#fbb5ae'    # 浅粉色
}

# 6. 创建主图
fig, ax = plt.subplots(figsize=(12, 6))

# 绘制三条折线（带标记）
ax.plot(sdg_numbers, ours_final,
        linestyle='--', marker='s', markersize=7,
        color=colors['ours'], markerfacecolor=colors['ours'],
        markeredgecolor='black', markeredgewidth=0.5,
        linewidth=2.5, label='Ours', zorder=3)

ax.plot(sdg_numbers, random_final,
        linestyle='--', marker='o', markersize=7,
        color=colors['random'], markerfacecolor=colors['random'],
        markeredgecolor='black', markeredgewidth=0.5,
        linewidth=2.5, label='Random', zorder=3)

ax.plot(sdg_numbers, average_final,
        linestyle='--', marker='^', markersize=7,
        color=colors['average'], markerfacecolor=colors['average'],
        markeredgecolor='black', markeredgewidth=0.5,
        linewidth=2.5, label='Average', zorder=3)

# 添加90分阈值线
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
all_scores = ours_final + random_final + average_final
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

# 8. 创建插图（中间下方的柱状图）- 显示实现目标的个数
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# 使用bbox_to_anchor精确定位到中间偏左下方，增大尺寸为原来的两倍
# [x, y, width, height] 相对于主图的位置
ax_inset = inset_axes(ax, width="50%", height="56%",
                      loc='center',
                      bbox_to_anchor=(0.15, 0.05, 0.5, 0.56),
                      bbox_transform=ax.transAxes)

# 插图数据：实现目标的个数
categories = ['Ours', 'Random', 'Average']
achieved_counts = [ours_achieved, random_achieved, average_achieved]
bar_colors = [colors['ours'], colors['random'], colors['average']]

# 绘制柱状图
x_pos = np.arange(len(categories))
bars = ax_inset.bar(x_pos, achieved_counts, color=bar_colors,
                    edgecolor='black', linewidth=1.5,
                    hatch='////', alpha=0.8, width=0.6)

# 在柱子上方标注数值
for i, (cat, count) in enumerate(zip(categories, achieved_counts)):
    ax_inset.text(i, count + 0.5, str(count),
                  ha='center', va='bottom',
                  fontsize=14, fontweight='bold',
                  fontproperties=font_prop)

# 设置插图样式
ax_inset.set_ylabel('Achieved SDGs', fontsize=13, fontweight='bold',
                    fontproperties=font_prop)
ax_inset.set_title(f'(Score ≥ {threshold})', fontsize=12,
                   fontproperties=font_prop, pad=8)
ax_inset.set_xticks(x_pos)
ax_inset.set_xticklabels(categories, fontproperties=font_prop, fontsize=12, rotation=15)
ax_inset.tick_params(axis='both', labelsize=11, direction='in', width=1.5, length=5)

# 移除插图的右边框和上边框
ax_inset.spines['right'].set_visible(False)
ax_inset.spines['top'].set_visible(False)

# 加粗插图的左边框和下边框
ax_inset.spines['left'].set_linewidth(1.5)
ax_inset.spines['bottom'].set_linewidth(1.5)

# 设置y轴范围
ax_inset.set_ylim(0, 17 + 1)
ax_inset.set_yticks([0, 5, 10, 15])

# 设置插图背景为白色
ax_inset.patch.set_facecolor('white')
ax_inset.patch.set_alpha(1.0)

# 9. 调整布局并保存
plt.tight_layout()

# 保存为SVG和PNG格式
output_svg = SCRIPT_DIR / 'sdg_final_scores_plot.svg'
output_png = SCRIPT_DIR / 'sdg_final_scores_plot.png'

plt.savefig(output_svg, format='svg', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig(output_png, format='png', dpi=300, bbox_inches='tight', facecolor='white')

print(f"\n图表已保存：")
print(f"  SVG: {output_svg}")
print(f"  PNG: {output_png}")

# 打印详细统计
print(f"\n{final_year}年各SDG得分对比：")
print(f"{'SDG':<5} {'Ours':<8} {'Random':<8} {'Average':<8}")
print("-" * 35)
for i, sdg in enumerate(sdg_numbers):
    print(f"{sdg:<5} {ours_final[i]:<8.2f} {random_final[i]:<8.2f} {average_final[i]:<8.2f}")

plt.show()
