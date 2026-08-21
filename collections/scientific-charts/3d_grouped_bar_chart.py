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
    plt.rcParams['font.family'] = 'Times New Roman'

# 数据定义
categories = ['BJ', 'SH', 'JS', 'AH', 'FJ', 'GD', 'GX', 'HN', 'SX', 'XZ', 'GS', 'QH']

# 示例数据（百分比）
data_A = [52, 70, 42, 63, 84, 70, 95, 68, 70, 60, 18, 68]
data_B = [62, 73, 48, 58, 95, 85, 88, 68, 88, 95, 23, 85]

# 误差数据
error_A = [3, 4, 5, 4, 3, 5, 4, 3, 4, 5, 2, 4]
error_B = [4, 3, 4, 5, 3, 4, 5, 4, 3, 4, 3, 5]

# 分组定义
groups = {
    'Group1': (0, 4, '#FFF9E6'),  # 淡黄色
    'Group2': (4, 8, '#E8F5E9'),  # 淡绿色
    'Group3': (8, 12, '#E3F2FD')  # 淡蓝色
}

# 创建图形
fig = plt.figure(figsize=(16, 10), dpi=300)
ax = fig.add_subplot(111, projection='3d')

# 设置柱子参数
x_pos = np.arange(len(categories))
width = 0.35
depth = 0.5

# 柱子颜色（马卡龙色系）
color_A = '#A8D8EA'  # 浅蓝色
color_B = '#B8E6B8'  # 浅绿色

# 绘制柱子
bars_A = []
bars_B = []

for i, (cat, val_A, val_B, err_A, err_B) in enumerate(zip(categories, data_A, data_B, error_A, error_B)):
    # A柱子
    bar_A = ax.bar3d(i - width/2, 0, 0, width, depth, val_A,
                     color=color_A, alpha=0.9, edgecolor='white', linewidth=1.5, shade=True)
    bars_A.append(bar_A)

    # B柱子
    bar_B = ax.bar3d(i + width/2, 0, 0, width, depth, val_B,
                     color=color_B, alpha=0.9, edgecolor='white', linewidth=1.5, shade=True)
    bars_B.append(bar_B)

    # 绘制误差棒
    ax.plot([i - width/2 + width/2, i - width/2 + width/2],
            [depth/2, depth/2],
            [val_A - err_A, val_A + err_A],
            'k-', linewidth=2, zorder=10)
    ax.plot([i + width/2 + width/2, i + width/2 + width/2],
            [depth/2, depth/2],
            [val_B - err_B, val_B + err_B],
            'k-', linewidth=2, zorder=10)

# 添加背景色块
for group_name, (start, end, color) in groups.items():
    # 创建背景平面
    xx = np.array([start - 0.5, end - 0.5, end - 0.5, start - 0.5])
    yy = np.array([-0.2, -0.2, depth + 0.2, depth + 0.2])
    zz = np.array([0, 0, 0, 0])

    verts = [list(zip(xx, yy, zz))]
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    poly = Poly3DCollection(verts, alpha=0.3, facecolor=color, edgecolor='none')
    ax.add_collection3d(poly)

    # 添加组标签
    mid_pos = (start + end) / 2 - 0.5
    ax.text(mid_pos, depth + 0.8, 105, group_name,
            fontsize=16, fontweight='bold', ha='center',
            color={'Group1': '#F4A460', 'Group2': '#66BB6A', 'Group3': '#42A5F5'}[group_name])

# 设置坐标轴
ax.set_xlabel('Categories', fontsize=14, labelpad=10)
ax.set_ylabel('', fontsize=14)
ax.set_zlabel('Percentage (%)', fontsize=14, labelpad=10)

# 设置x轴刻度
ax.set_xticks(x_pos)
ax.set_xticklabels(categories, fontsize=12)

# 设置z轴范围和刻度
ax.set_zlim(0, 110)
ax.set_zticks(np.arange(0, 101, 20))
ax.set_zticklabels([f'{i}%' for i in range(0, 101, 20)], fontsize=11)

# 添加网格线
ax.grid(True, linestyle='--', alpha=0.3, color='gray')

# 设置视角
ax.view_init(elev=20, azim=45)

# 添加图例
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=color_A, edgecolor='white', label='A', alpha=0.9),
    Patch(facecolor=color_B, edgecolor='white', label='B', alpha=0.9)
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=13, framealpha=0.9)

# 设置背景
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor('lightgray')
ax.yaxis.pane.set_edgecolor('lightgray')
ax.zaxis.pane.set_edgecolor('lightgray')

# 调整布局
plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

# 保存图片
plt.savefig('3d_grouped_bar_chart.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('3d_grouped_bar_chart.pdf', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('3d_grouped_bar_chart.svg', dpi=300, bbox_inches='tight', facecolor='white')

print("高分辨率3D柱状图已生成！")
print("- PNG格式: 3d_grouped_bar_chart.png")
print("- PDF格式: 3d_grouped_bar_chart.pdf")
print("- SVG格式: 3d_grouped_bar_chart.svg")

plt.show()
