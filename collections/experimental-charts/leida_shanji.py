"""
平滑曲线雷达图（山脊图）生成器
=====================================

这个脚本使用正态分布（高斯分布）创建平滑的"山脊"效果的极坐标图。

使用方法：
---------
1. 修改下面"数据输入区域"中的参数
2. 运行脚本：python leida_shanji.py
3. 图表将保存为 PNG 和 SVG 格式

参数说明：
---------
- categories: 轴的名称列表（顺时针排列）
- data_sets: 每一层的数据值（必须与 categories 长度一致）
- base_radii: 每层的基础半径（Total > Train > Test）
- sigma: 山脊宽度（0.1-0.2）
- height_scale: 山脊高度（0.08-0.15）
- color_schemes: 配色方案

作者：Kiro AI Assistant
日期：2026-01-29
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import matplotlib.patches as mpatches
import matplotlib
from matplotlib import font_manager

# 设置字体
font_path = font_manager.findfont('DejaVu Serif')
try:
    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
except:
    plt.rcParams['font.family'] = 'Times New Roman'

# PDF 输出设置
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

################################################################################
# 数据输入区域 - 在这里修改你的数据
################################################################################

# 颜色库（可以添加多个配色方案）
color_schemes = [
    {
        'name': 'Scheme_1',
        'palette': {'Total': '#003f5c', 'Train': '#ff6361', 'Test': '#ffa600'}
    },
]

# 每个轴的名称标注（顺时针设置）
# 注意：类别数量必须与下面的数据点数量一致
categories = ['性能', '稳定性', '可扩展性', '安全性', '易用性', '文档', '社区', '成本']
num_vars = len(categories)

# 每一层山脊图的数值（单位：百分比）
# 注意：每个列表的长度必须与 categories 的长度一致
data_sets = {
    'Total': [85.2, 78.5, 92.3, 88.7, 75.4, 82.1, 90.5, 68.9],
    'Train': [82.1, 75.2, 88.6, 85.3, 72.8, 78.5, 87.2, 65.4],
    'Test': [78.5, 70.8, 82.4, 80.1, 68.3, 73.9, 82.7, 60.2]
}

# 每一层山脊图的基础半径（控制每层的大小）
# Total（最外层）> Train（中间层）> Test（最内层）
base_radii = {'Total': 90, 'Train': 55, 'Test': 20}

# 正态分布参数（控制山脊的形状）
sigma = 0.14  # 标准差，数值越大山脊越宽（建议范围：0.1-0.2）
height_scale = 0.12  # 缩放因子，数值越大山脊越高（建议范围：0.08-0.15）

################################################################################
# 数据输入区域结束 - 下面的代码无需修改
################################################################################

# 使用颜色库里的每一种颜色来进行绘图
for index, scheme in enumerate(color_schemes):
    current_colors = scheme['palette']
    print(f"正在生成第 {index + 1}/{len(color_schemes)} 张图: 使用 '{scheme['name']}' 配色")

    # 创建极坐标图
    fig, ax = plt.subplots(
        figsize=(12, 12),
        subplot_kw=dict(polar=True)
    )
    fig.set_facecolor('white')

    # 生成每个类别在极坐标图上的角度（弧度制）
    angles = np.linspace(
        np.pi / 2,  # 起始点：90°（正上方）
        -1.5 * np.pi,  # 结束点：-270°
        num_vars,
        endpoint=False
    )

    # 定义绘图的层次顺序（数值越大越靠上）
    layer_order = {'Total': 0, 'Train': 1, 'Test': 2}

    # 绘制每一层山脊图
    for name in ['Total', 'Train', 'Test']:
        base_radius = base_radii[name]
        data = data_sets[name]
        color = current_colors[name]
        z = layer_order[name]

        # 为每个数据点绘制一个山脊
        for i, value in enumerate(data):
            mu_angle = angles[i]  # 山脊的中心角度

            # 生成山脊的角度范围（从中心向两侧延伸 3.5 个标准差）
            hump_angles = np.linspace(
                mu_angle - 3.5 * sigma,
                mu_angle + 3.5 * sigma,
                100
            )

            # 使用正态分布计算山脊的高度
            pdf_values = norm.pdf(
                hump_angles,
                loc=mu_angle,
                scale=sigma
            )

            # 计算山脊外轮廓的半径
            hump_radii = base_radius + value * pdf_values * height_scale

            # 山脊内边缘的半径（基础半径）
            inner_radii = np.full_like(hump_angles, base_radius)

            # 填充山脊
            ax.fill_between(
                hump_angles,
                inner_radii,
                hump_radii,
                color=color,
                zorder=z
            )

    # 添加每个山脊的数值标签
    for name in ['Total', 'Train', 'Test']:
        base_radius = base_radii[name]
        data = data_sets[name]

        for i, value in enumerate(data):
            mu_angle = angles[i]

            # 计算山脊峰值的半径
            peak_radius = base_radius + value * norm.pdf(mu_angle, mu_angle, sigma) * height_scale

            # 计算文字旋转角度
            angle_deg = (np.rad2deg(mu_angle) + 360) % 360
            rotation = angle_deg - 90

            # 调整旋转角度，使文字始终可读
            while rotation < -90:
                rotation += 180
            while rotation > 90:
                rotation -= 180
            if 180 < angle_deg < 360:
                rotation += 180

            # 添加数值标签
            ax.text(
                mu_angle, peak_radius + 3.5,
                f'{value:.1f}%',
                ha='center', va='center',
                fontsize=9,
                fontfamily='Times New Roman',
                fontweight='bold',
                rotation=rotation
            )

    # 绘制径向引导线
    max_radius_for_lines = 120
    line_start_radius = base_radii['Test']

    for angle in angles:
        ax.plot(
            [angle, angle],
            [line_start_radius, max_radius_for_lines],
            color='gray',
            linestyle='--',
            linewidth=0.8,
            zorder=-1
        )

    # 添加类别标签
    label_radius_category = 128

    for angle, label in zip(angles, categories):
        ax.text(
            angle, label_radius_category, label,
            ha='center', va='center',
            fontsize=14,
            fontfamily='Times New Roman',
            rotation=0
        )

    # 调整图表样式
    ax.set_ylim(0, 140)
    ax.spines['polar'].set_visible(False)
    ax.grid(False)
    ax.set_yticklabels([])
    ax.set_xticks([])

    # 创建图例
    legend_colors = [current_colors['Test'], current_colors['Train'], current_colors['Total']]
    legend_labels = ['Test', 'Train', 'Total']
    patches = [
        mpatches.Patch(color=color, label=label)
        for color, label in zip(legend_colors, legend_labels)
    ]

    fig.legend(
        handles=patches,
        loc='center left',
        bbox_to_anchor=(0.8, 0.65),
        frameon=True,
        fontsize=12,
        labelspacing=1.2,
        prop={'family': 'Times New Roman'}
    )

    # 调整布局
    fig.tight_layout(pad=3)
    plt.subplots_adjust(left=0.05, right=0.8, top=0.95, bottom=0.15)

    # 保存结果
    save_path_png = f'smooth_radial_chart_v2_{index + 1}.png'
    save_path_svg = f'smooth_radial_chart_v2_{index + 1}.svg'

    plt.savefig(save_path_png, dpi=300, bbox_inches='tight')
    plt.savefig(save_path_svg, format='svg', bbox_inches='tight')

    print(f"图表已保存: {save_path_png} 和 {save_path_svg}")

    plt.show()
    plt.close(fig)

print("所有图表生成完成！")
