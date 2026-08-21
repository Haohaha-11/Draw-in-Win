import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Wedge
from matplotlib.collections import PatchCollection
from matplotlib.patches import Patch
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['font.size'] = 12

color_palettes = {
    1: {
        'top': ['#3E236D', '#573388', '#2D5191', '#3B89C0', '#3AA09D', '#4FB38E', '#8BC34A', '#B2D963', '#CDEB80', '#F0F4C3', '#FFF9C4'],
        'bottom': ['#FDEFB2', '#F9C647', '#F28F3B', '#ED6A3A', '#D73A49', '#C2185B', '#8E24AA', '#512DA8', '#1976D2', '#004D40']
    },
}

selected_palette_index = 1  # 要使用的配色方案
current_palette = color_palettes[selected_palette_index]  # 获取当前配色方案


def draw_separated_rose_chart(ax, fig, data_top, colors_top, legend_labels_top,
                               data_bottom, colors_bottom, legend_labels_bottom, center_text="MRYR"):
    # 合并上下半区的数据，形成完整的360度圆
    all_data = list(data_top) + list(data_bottom)
    all_colors = list(colors_top) + list(colors_bottom)
    all_labels = [f'{v}%' for v in all_data]
    all_legend_labels = list(legend_labels_top) + list(legend_labels_bottom)

    min_radius_actual = 0.4  # 最小半径
    max_radius_actual = 1.1  # 最大半径
    inner_radius = 0.15  # 中心圆的半径

    # 为所有数据生成等间隔的半径值
    radii_steps = np.linspace(min_radius_actual, max_radius_actual, len(all_data))
    sorted_indices = np.argsort(all_data)  # 获取数据排序后的索引,从小到大
    radii = np.empty_like(radii_steps)
    radii[sorted_indices] = radii_steps[::-1]  # 将半径值按数据大小反向赋给扇区，数据越大，半径越小

    # 将所有相关数据打包并排序
    combined = sorted(
        zip(all_data, radii, all_colors, all_labels, all_legend_labels),
        key=lambda x: x[0],
        reverse=True
    )
    data_sorted, radii_sorted, colors_sorted, labels_sorted, legend_labels_sorted = zip(*combined)

    center = (0, 0)  # 圆心坐标

    ax.set_aspect('equal')
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.axis('off')

    patches_list = []
    text_positions = []
    text_labels_for_plot = []
    text_colors = []

    # 绘制完整的360度玫瑰图
    total_angle = 360
    start_angle = 90  # 从顶部开始

    for i, (value, radius_outer, color, label, legend_label) in enumerate(
            zip(data_sorted, radii_sorted, colors_sorted, labels_sorted, legend_labels_sorted)):
        angle_width = total_angle / len(all_data)
        end_angle = start_angle - angle_width

        # 创建扇形
        wedge = Wedge(center, radius_outer, end_angle, start_angle,
                      width=radius_outer - inner_radius, facecolor=color, edgecolor='white', lw=1.5)
        patches_list.append(wedge)

        # 计算标签位置
        mid_angle = (start_angle + end_angle) / 2
        mid_angle_rad = np.deg2rad(mid_angle)
        label_radius = (radius_outer + inner_radius) / 2
        x = label_radius * np.cos(mid_angle_rad)
        y = label_radius * np.sin(mid_angle_rad)
        text_positions.append((x, y))
        text_labels_for_plot.append(label)
        text_colors.append('white' if value > 5 else 'black')
        start_angle = end_angle

    # 将所有扇区添加到坐标轴上
    ax.add_collection(PatchCollection(patches_list, match_original=True))

    # 绘制中心圆
    centre_circle = plt.Circle(center, inner_radius, fc='white', edgecolor='white', lw=1.5)
    ax.add_artist(centre_circle)

    # 添加中心文本
    ax.text(0, 0, center_text,
            ha='center', va='center',
            fontsize=16, fontweight='bold',
            fontname='Times New Roman')

    # 添加百分比标签
    for i, (x, y) in enumerate(text_positions):
        angle_deg = np.rad2deg(np.arctan2(y, x))
        if 90 < angle_deg < 270:
            angle_deg += 180

        ax.text(x, y, text_labels_for_plot[i],
                ha='center', va='center',
                color=text_colors[i],
                fontsize=10,
                rotation=angle_deg,
                rotation_mode='anchor')

    # 准备图例
    legend_handles = []
    legend_labels_plot = []
    for i, label in enumerate(legend_labels_sorted):
        legend_handles.append(Patch(facecolor=colors_sorted[i], edgecolor='black', label=label))
        legend_labels_plot.append(label)

    # 添加图例（分两行显示）
    # 上半部分图例（前11个）
    fig.legend(handles=legend_handles[:11],
               labels=legend_labels_plot[:11],
               loc='lower center',
               ncol=11,
               fontsize=14,
               bbox_to_anchor=(0.5, 0.62),
               frameon=False,
               handletextpad=0.5,
               columnspacing=1.0)
    # 下半部分图例（后10个）
    fig.legend(handles=legend_handles[11:],
               labels=legend_labels_plot[11:],
               loc='lower center',
               ncol=10,
               fontsize=14,
               bbox_to_anchor=(0.5, 0.32),
               frameon=False,
               handletextpad=0.5,
               columnspacing=1.0)


# 图1数据
data_top_1 = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 1.5]  # 上半区的数据
legend_labels_top_1 = ['RE', 'FVC', 'SM', 'T', 'HR', 'P', 'LAI', 'NPP', 'R', 'SPEI', 'PM2.5']  # 上半区的图例标签
data_bottom_1 = [29.5, 13.2, 2.5, 1.8, 1.6, 9.7, 8.4, 7.7, 7.3, 6.4]  # 下半区的数据
legend_labels_bottom_1 = ['FE', 'NLAI', 'URA', 'UP', 'FP', 'PD', 'UPS', 'PGR', 'NLI', 'GDPC']  # 下半区的图例标签
# 从选择的配色方案中获取颜色
colors_top_1 = current_palette['top']  # 上半区颜色列表
colors_bottom_1 = current_palette['bottom']  # 下半区颜色列表

# 图2数据
data_top_2 = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 1.5]
legend_labels_top_2 = ['RE', 'FVC', 'SM', 'T', 'HR', 'P', 'LAI', 'NPP', 'R', 'SPEI', 'PM2.5']
data_bottom_2 = [29.5, 13.2, 2.5, 1.8, 1.6, 9.7, 8.4, 7.7, 7.3, 6.4]
legend_labels_bottom_2 = ['FE', 'NLAI', 'URA', 'UP', 'FP', 'PD', 'UPS', 'PGR', 'NLI', 'GDPC']
colors_top_2 = current_palette['top']
colors_bottom_2 = current_palette['bottom']

# 图3的数据
data_top_3 = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 1.5]
legend_labels_top_3 = ['RE', 'FVC', 'SM', 'T', 'HR', 'P', 'LAI', 'NPP', 'R', 'SPEI', 'PM2.5']
data_bottom_3 = [29.5, 13.2, 2.5, 1.8, 1.6, 9.7, 8.4, 7.7, 7.3, 6.4]
legend_labels_bottom_3 = ['FE', 'NLAI', 'URA', 'UP', 'FP', 'PD', 'UPS', 'PGR', 'NLI', 'GDPC']
colors_top_3 = current_palette['top']
colors_bottom_3 = current_palette['bottom']

# 创建子图布局
fig, axes = plt.subplots(1, 3, figsize=(16, 10))

# 调用绘图函数
draw_separated_rose_chart(
    axes[0],  # 子图
    fig,  # 总画布
    data_top_1,  # 数据
    colors_top_1,  # 颜色
    legend_labels_top_1,  # 标签
    # 下半区
    data_bottom_1,  # 数据
    colors_bottom_1,  # 颜色
    legend_labels_bottom_1,  # 标签
    center_text="URYR")  # 中心文本

draw_separated_rose_chart(
    axes[1],
    fig,
    data_top_2,
    colors_top_2,
    legend_labels_top_2,
    data_bottom_2,
    colors_bottom_2,
    legend_labels_bottom_2,
    center_text="MRYR")

draw_separated_rose_chart(
    axes[2],
    fig,
    data_top_3,
    colors_top_3,
    legend_labels_top_3,
    data_bottom_3,
    colors_bottom_3,
    legend_labels_bottom_3,
    center_text="LRYR")

plt.tight_layout()
plt.show()
