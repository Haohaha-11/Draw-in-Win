import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import font_manager

# 设置字体
try:
    font_path = font_manager.findfont('DejaVu Serif')
    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
except:
    plt.rcParams['font.family'] = 'serif'

# 数据
categories = ['S1', 'L1', 'M1', 'S2', 'L2', 'M2', 'S3', 'L3', 'M3']
b_scores = [22.11, 27.14, 24.82, 2.42, 7.84, 4.65, -2.7, -0.7, 9.65]
d_scores = [14.87, 23.74, 6.04, 13.47, 2.67, 0.65, 11.87, 2.17, 0.4]

# 创建图形
fig = plt.figure(figsize=(14, 8))
ax = fig.add_subplot(111, projection='3d')

# 设置位置参数
n_categories = len(categories)
x_pos = np.arange(n_categories)
y_pos_b = np.zeros(n_categories)  # B组的y位置
y_pos_d = np.ones(n_categories)   # D组的y位置

# 柱子宽度和深度
width = 0.4
depth = 0.4

# 颜色设置
color_b = '#87CEEB'  # 浅蓝色
color_d = '#90EE90'  # 浅绿色

# 绘制B组柱状图
for i in range(n_categories):
    if b_scores[i] >= 0:
        ax.bar3d(x_pos[i] - width/2, y_pos_b[i] - depth/2, 0,
                width, depth, b_scores[i],
                color=color_b, alpha=0.8, edgecolor='black', linewidth=0.5)

# 绘制D组柱状图
for i in range(n_categories):
    if d_scores[i] >= 0:
        ax.bar3d(x_pos[i] - width/2, y_pos_d[i] - depth/2, 0,
                width, depth, d_scores[i],
                color=color_d, alpha=0.8, edgecolor='black', linewidth=0.5)

# 添加分组背景区域标注
group1_range = (0, 2.5)
group2_range = (3, 5.5)
group3_range = (6, 8.5)

# 设置坐标轴
ax.set_xlabel('Categories', fontsize=12, labelpad=10)
ax.set_ylabel('Groups', fontsize=12, labelpad=10)
ax.set_zlabel('Percentage (%)', fontsize=12, labelpad=10)

# 设置x轴刻度
ax.set_xticks(x_pos)
ax.set_xticklabels(categories, fontsize=10)

# 设置y轴刻度
ax.set_yticks([0, 1])
ax.set_yticklabels(['B (Loss amount)', 'D (Diversion fl)'], fontsize=10)

# 设置z轴范围
ax.set_zlim(0, 100)

# 调整视角
ax.view_init(elev=20, azim=45)

# 添加网格
ax.grid(True, alpha=0.3)

# 添加分组标签（在图上方添加文本）
ax.text(1.0, -0.5, 85, 'Group1', fontsize=12, color='#FFD700',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFFACD', alpha=0.7))
ax.text(4.0, -0.5, 85, 'Group2', fontsize=12, color='#90EE90',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#F0FFF0', alpha=0.7))
ax.text(7.0, -0.5, 85, 'Group3', fontsize=12, color='#87CEEB',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#E0F6FF', alpha=0.7))

# 添加图例
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=color_b, edgecolor='black', label='B (Loss amount)'),
    Patch(facecolor=color_d, edgecolor='black', label='D (Diversion fl)')
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=10)

plt.tight_layout()
plt.savefig('3d_grouped_comparison_chart.png', dpi=300, bbox_inches='tight')
plt.savefig('3d_grouped_comparison_chart.pdf', bbox_inches='tight')
plt.show()

print("图表已保存为 3d_grouped_comparison_chart.png 和 .pdf")
