import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

# 设置字体为Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.serif'] = ['Times New Roman']

# 数据（从表格中提取）- Seattle和Las Vegas的数值已交换
categories = ['Seattle', 'Las Vegas', 'Mexico City', 'Seattle', 'Las Vegas', 'Mexico City', 'Seattle', 'Las Vegas', 'Mexico City']

# B列数据 (Loss amount) - Seattle和Las Vegas的数值已交换
b_values = [27.14, 22.11, 24.82, 7.84, 2.42, 4.65, -0.7, -2.7, 9.65]
b_errors = [1, 1, 1, 0.5, 0.2, 0.4, 0, 0.1, 0.5]  # C列的误差

# D列数据 (Diversion fl) - Seattle和Las Vegas的数值已交换
d_values = [23.74, 14.87, 6.04, 2.67, 13.47, 0.65, 2.17, 11.87, 0.4]
d_errors = [1, 1, 0.4, 0.2, 1, 0, 0.2, 1, 0]  # E列的误差

# 分组定义
group1 = [0, 1, 2]  # S1, L1, M1
group2 = [3, 4, 5]  # S2, L2, M2
group3 = [6, 7, 8]  # S3, L3, M3

# 创建图形
fig, ax = plt.subplots(figsize=(10, 6))

# 设置柱子宽度和位置
bar_width = 0.233  # 原来的2/3
x = np.arange(len(categories))

# 颜色设置
color_a = '#f1e5c7'  # 柱子颜色1 - Popularity Depreciation
color_b = '#7a4d1e'  # 柱子颜色2 - Diverted Flow

# 绘制柱状图
bars1 = ax.bar(x - bar_width/2, b_values, bar_width,
               label='Popularity Depreciation', color=color_a, alpha=1)

bars2 = ax.bar(x + bar_width/2, d_values, bar_width,
               label='Diverted Flow', color=color_b, alpha=1)

# 添加分组背景色
group_colors = ['#b5bf91', '#97a958', '#75805d']  # 背景颜色
group_labels = ['Static', 'Dynamic', 'Adaptive']
groups = [group1, group2, group3]

# 创建背景色块和收集图例元素
from matplotlib.patches import Patch
legend_elements = []

for i, (group, color, label) in enumerate(zip(groups, group_colors, group_labels)):
    x_start = group[0] - 0.5
    x_end = group[-1] + 0.5
    ax.axvspan(x_start, x_end, alpha=1, color=color, zorder=0)

    # 添加到图例
    legend_elements.append(Patch(facecolor=color, alpha=1, label=label))

# 设置坐标轴
ax.set_ylabel('Percentage (%)', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=12)
ax.set_ylim(-5, 30)

# 添加网格
ax.grid(True, axis='y', alpha=0.3, linestyle='--', linewidth=0.8)
ax.set_axisbelow(True)

# 添加图例（包含柱子和背景）
legend_elements.insert(0, Patch(facecolor=color_a, alpha=1, label='Popularity Depreciation'))
legend_elements.insert(1, Patch(facecolor=color_b, alpha=1, label='Diverted Flow'))

ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.12),
         fontsize=12, frameon=False, ncol=5)

# 添加右侧y轴（百分比）
ax2 = ax.twinx()
ax2.set_ylim(ax.get_ylim())
ax2.set_ylabel('Percentage (%)', fontsize=14)

# 调整布局
plt.tight_layout()

# 保存图片
plt.savefig('grouped_bar_with_error.png', dpi=300, bbox_inches='tight')
plt.savefig('grouped_bar_with_error.pdf', bbox_inches='tight')
plt.savefig('grouped_bar_with_error.svg', bbox_inches='tight')

print("图表已保存:")
print("- grouped_bar_with_error.png")
print("- grouped_bar_with_error.pdf")
print("- grouped_bar_with_error.svg")

plt.show()
