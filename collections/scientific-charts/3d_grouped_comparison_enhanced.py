import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import Rectangle

# 设置字体
try:
    font_path = font_manager.findfont('DejaVu Serif')
    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
except:
    plt.rcParams['font.family'] = 'serif'

# 数据
categories = ['S1', 'L1', 'M1', 'S2', 'L2', 'M2', 'S3', 'L3', 'M3']
b_scores = np.array([22.11, 27.14, 24.82, 2.42, 7.84, 4.65, -2.7, -0.7, 9.65])
d_scores = np.array([14.87, 23.74, 6.04, 13.47, 2.67, 0.65, 11.87, 2.17, 0.4])

# 模拟误差（根据表格中的E列数据）
b_errors = np.array([1, 1, 0.4, 0.2, 0.5, 0.4, 0.1, 0, 0.5]) * 3  # 放大误差以便可见
d_errors = np.array([1, 1, 0.4, 1, 0.2, 0, 1, 0.2, 0]) * 3

# 创建图形
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(111, projection='3d')

# 设置位置参数
n_categories = len(categories)
x_pos = np.arange(n_categories)
y_pos_b = np.zeros(n_categories)
y_pos_d = np.ones(n_categories) * 1.2

# 柱子参数
width = 0.35
depth = 0.35

# 颜色设置（参考图的颜色）
color_b = '#6BA3D4'  # 蓝色
color_d = '#7FCD91'  # 绿色

# 绘制B组柱状图（只绘制正值）
for i in range(n_categories):
    if b_scores[i] > 0:
        ax.bar3d(x_pos[i] - width/2, y_pos_b[i] - depth/2, 0,
                width, depth, b_scores[i],
                color=color_b, alpha=0.85, edgecolor='white', linewidth=1)

        # 添加误差线（简化版）
        if b_errors[i] > 0:
            ax.plot([x_pos[i], x_pos[i]],
                   [y_pos_b[i], y_pos_b[i]],
                   [b_scores[i], b_scores[i] + b_errors[i]],
                   'k-', linewidth=1.5)

# 绘制D组柱状图
for i in range(n_categories):
    if d_scores[i] > 0:
        ax.bar3d(x_pos[i] - width/2, y_pos_d[i] - depth/2, 0,
                width, depth, d_scores[i],
                color=color_d, alpha=0.85, edgecolor='white', linewidth=1)

        # 添加误差线
        if d_errors[i] > 0:
            ax.plot([x_pos[i], x_pos[i]],
                   [y_pos_d[i], y_pos_d[i]],
                   [d_scores[i], d_scores[i] + d_errors[i]],
                   'k-', linewidth=1.5)

# 设置坐标轴标签
ax.set_xlabel('\nCategories', fontsize=13, fontweight='bold')
ax.set_ylabel('\nMetrics', fontsize=13, fontweight='bold')
ax.set_zlabel('Percentage (%)', fontsize=13, fontweight='bold')

# 设置x轴刻度
ax.set_xticks(x_pos)
ax.set_xticklabels(categories, fontsize=11)

# 设置y轴刻度
ax.set_yticks([0, 1.2])
ax.set_yticklabels(['B', 'D'], fontsize=11)

# 设置z轴范围和刻度
ax.set_zlim(0, 100)
ax.set_zticks(np.arange(0, 101, 20))

# 调整视角（类似参考图）
ax.view_init(elev=18, azim=50)

# 设置背景颜色
ax.xaxis.pane.fill = True
ax.yaxis.pane.fill = True
ax.zaxis.pane.fill = True
ax.xaxis.pane.set_facecolor('#F5F5F5')
ax.yaxis.pane.set_facecolor('#F5F5F5')
ax.zaxis.pane.set_facecolor('#FFFFFF')

# 添加网格
ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

# 添加分组背景标签
# Group1 (黄色背景)
ax.text(1.0, -0.8, 90, 'Group1', fontsize=13, fontweight='bold',
        color='#DAA520', ha='center',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#FFFACD', alpha=0.8, edgecolor='none'))

# Group2 (绿色背景)
ax.text(4.0, -0.8, 90, 'Group2', fontsize=13, fontweight='bold',
        color='#2E8B57', ha='center',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#E8F5E9', alpha=0.8, edgecolor='none'))

# Group3 (蓝色背景)
ax.text(7.0, -0.8, 90, 'Group3', fontsize=13, fontweight='bold',
        color='#4682B4', ha='center',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#E3F2FD', alpha=0.8, edgecolor='none'))

# 添加图例
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=color_b, edgecolor='white', label='B (Loss amount)', alpha=0.85),
    Patch(facecolor=color_d, edgecolor='white', label='D (Diversion fl)', alpha=0.85)
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=11, framealpha=0.9)

# 设置标题
ax.set_title('Comparison of B and D Scores Across Categories',
             fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('3d_grouped_comparison_enhanced.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('3d_grouped_comparison_enhanced.pdf', bbox_inches='tight', facecolor='white')
plt.show()

print("增强版图表已保存")
print("- 3d_grouped_comparison_enhanced.png")
print("- 3d_grouped_comparison_enhanced.pdf")
