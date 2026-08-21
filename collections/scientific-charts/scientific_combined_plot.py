"""
科研风格组合图表：主图（Sigmoid折线散点图）+ 插图（柱状图）
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import Rectangle
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

# 设置Times New Roman字体
font_path = fm.findfont('DejaVu Serif')
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = font_prop.get_name()
fm.fontManager.addfont(font_path)

# 1. 生成模拟数据
x = np.linspace(-40, 60, 200)

# Sigmoid函数：y = 1 / (1 + exp(k*(x - x0)))
def sigmoid(x, x0, k):
    """
    x0: 中心点（下降的中心位置）
    k: 陡峭度（越大越陡）
    """
    return 1 / (1 + np.exp(k * (x - x0)))

# 生成4组数据（不同的下降位置和陡峭度）
y1 = sigmoid(x, x0=10, k=0.15)  # 在x=10左右急剧下降
y2 = sigmoid(x, x0=15, k=0.12)  # 在x=15左右下降，稍缓
y3 = sigmoid(x, x0=20, k=0.09)  # 在x=20左右下降，更缓
y4 = sigmoid(x, x0=25, k=0.07)  # 在x=25左右下降，最平缓

# 添加少量噪声使数据更真实
np.random.seed(42)
y1 += np.random.normal(0, 0.02, len(x))
y2 += np.random.normal(0, 0.02, len(x))
y3 += np.random.normal(0, 0.02, len(x))
y4 += np.random.normal(0, 0.02, len(x))

# 限制y值在0-1范围内
y1 = np.clip(y1, 0, 1)
y2 = np.clip(y2, 0, 1)
y3 = np.clip(y3, 0, 1)
y4 = np.clip(y4, 0, 1)

# 2. 定义配色方案
colors = {
    'series1': '#d6e7f1',
    'series2': '#fdd29a',
    'series3': '#fbb5ae',
    'series4': '#fff6de'
}

# 3. 创建主图
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制4条折线（带标记）
# 每隔10个点显示一个标记，避免过于密集
marker_interval = 15

ax.plot(x[::marker_interval], y1[::marker_interval],
        linestyle='--', marker='s', markersize=8,
        color=colors['series1'], markerfacecolor=colors['series1'],
        markeredgecolor='black', markeredgewidth=0.5,
        linewidth=2, label='Label 1', zorder=3)

ax.plot(x[::marker_interval], y2[::marker_interval],
        linestyle='--', marker='o', markersize=8,
        color=colors['series2'], markerfacecolor=colors['series2'],
        markeredgecolor='black', markeredgewidth=0.5,
        linewidth=2, label='Label 2', zorder=3)

ax.plot(x[::marker_interval], y3[::marker_interval],
        linestyle='--', marker='^', markersize=8,
        color=colors['series3'], markerfacecolor=colors['series3'],
        markeredgecolor='black', markeredgewidth=0.5,
        linewidth=2, label='Label 3', zorder=3)

ax.plot(x[::marker_interval], y4[::marker_interval],
        linestyle='--', marker='v', markersize=8,
        color=colors['series4'], markerfacecolor=colors['series4'],
        markeredgecolor='black', markeredgewidth=0.5,
        linewidth=2, label='Label 4', zorder=3)

# 4. 设置主图样式
# 坐标轴标签
ax.set_xlabel('Time', fontsize=16, fontweight='bold', fontproperties=font_prop)
ax.set_ylabel('YYY', fontsize=16, fontweight='bold', fontproperties=font_prop)

# 设置坐标轴范围
ax.set_xlim(-40, 60)
ax.set_ylim(0.0, 1.0)

# 刻度朝内
ax.tick_params(axis='both', which='major', direction='in',
               labelsize=12, width=1.5, length=6)
ax.tick_params(axis='both', which='minor', direction='in',
               width=1, length=3)

# 加粗边框
for spine in ax.spines.values():
    spine.set_linewidth(1.5)

# 添加网格（可选，使图表更专业）
ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)

# 添加图例（移到左侧，避免与插图重叠）
legend = ax.legend(loc='upper left', fontsize=11, frameon=True,
                   fancybox=False, shadow=False, prop=font_prop)
legend.get_frame().set_linewidth(1.5)

# 5. 创建插图（右上角的柱状图）
# 使用 inset_axes 创建插图，调整位置到右上角
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# 位置参数：[left, bottom, width, height] 在主图坐标系中的相对位置
ax_inset = inset_axes(ax, width="35%", height="35%",
                      loc='upper right',
                      bbox_to_anchor=(0, 0, 1, 1),
                      bbox_transform=ax.transAxes,
                      borderpad=2)

# 插图数据
categories = [1, 2, 3, 4]
values = [25, 61, 43, 35]
bar_colors = [colors['series1'], colors['series2'],
              colors['series3'], colors['series4']]

# 绘制柱状图
bars = ax_inset.bar(categories, values, color=bar_colors,
                    edgecolor='black', linewidth=1,
                    hatch='////', alpha=0.8)

# 在柱子上方标注数值
for i, (cat, val) in enumerate(zip(categories, values)):
    ax_inset.text(cat, val + 2, str(val),
                  ha='center', va='bottom',
                  fontsize=10, fontweight='bold',
                  fontproperties=font_prop)

# 设置插图样式
ax_inset.set_xlabel('Category', fontsize=9, fontweight='bold',
                    fontproperties=font_prop)
ax_inset.set_ylabel('BB (mm)', fontsize=9, fontweight='bold',
                    fontproperties=font_prop)
ax_inset.set_xticks(categories)
ax_inset.set_xticklabels(['1', '2', '3', '4'], fontproperties=font_prop)
ax_inset.tick_params(axis='both', labelsize=8, direction='in')

# 移除插图的右边框和上边框
ax_inset.spines['right'].set_visible(False)
ax_inset.spines['top'].set_visible(False)

# 加粗插图的左边框和下边框
ax_inset.spines['left'].set_linewidth(1.5)
ax_inset.spines['bottom'].set_linewidth(1.5)

# 设置y轴范围（留出空间显示数值标注）
ax_inset.set_ylim(0, max(values) * 1.15)

# 设置插图背景为白色，确保不透明
ax_inset.patch.set_facecolor('white')
ax_inset.patch.set_alpha(1.0)

# 6. 调整布局并保存
plt.tight_layout()

# 保存为SVG和PNG格式
output_svg = SCRIPT_DIR / 'scientific_combined_plot.svg'
output_png = SCRIPT_DIR / 'scientific_combined_plot.png'

plt.savefig(output_svg, format='svg', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig(output_png, format='png', dpi=300, bbox_inches='tight', facecolor='white')

print(f"图表已保存：")
print(f"  SVG: {output_svg}")
print(f"  PNG: {output_png}")

plt.show()
