import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Wedge
from matplotlib.patches import Patch
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['font.size'] = 12

# 读取湖人现役球员排名数据
df = pd.read_csv('Rank/xianyi_rank.csv')

# 配色方案（反转顺序，从深到浅）
color_palette = ['#3E236D', '#573388', '#2D5191', '#3B89C0', '#3AA09D',
                 '#4FB38E', '#8BC34A', '#B2D963', '#CDEB80', '#F0F4C3']


def draw_rose_chart(ax, fig, data, colors, legend_labels, center_text="Lakers"):
    """绘制玫瑰图"""

    min_radius_actual = 0.4  # 最小半径
    max_radius_actual = 1.1  # 最大半径
    inner_radius = 0.15  # 中心圆的半径

    # 为所有数据生成等间隔的半径值
    radii_steps = np.linspace(min_radius_actual, max_radius_actual, len(data))
    sorted_indices = np.argsort(data)  # 获取数据排序后的索引,从小到大
    radii = np.empty_like(radii_steps)
    radii[sorted_indices] = radii_steps  # 数据越大，半径越大

    # 将所有相关数据打包并排序
    combined = sorted(
        zip(data, radii, colors, legend_labels),
        key=lambda x: x[0],
        reverse=True
    )
    data_sorted, radii_sorted, colors_sorted, legend_labels_sorted = zip(*combined)

    center = (0, 0)  # 圆心坐标

    ax.set_aspect('equal')
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.axis('off')

    text_positions = []
    text_values = []
    text_colors = []
    text_labels = []

    # 绘制完整的360度玫瑰图
    total_angle = 360
    start_angle = 90  # 从顶部开始，逆时针方向

    for i, (value, radius_outer, color, legend_label) in enumerate(
            zip(data_sorted, radii_sorted, colors_sorted, legend_labels_sorted)):
        angle_width = total_angle / len(data)
        end_angle = start_angle + angle_width  # 改为加法，实现逆时针

        # 创建扇形（添加透明度alpha=0.75）并直接添加到ax
        wedge = Wedge(center, radius_outer, start_angle, end_angle,  # 交换start和end的位置
                      width=radius_outer - inner_radius, facecolor=color, edgecolor='white',
                      lw=1.5, alpha=0.75)
        ax.add_patch(wedge)

        # 计算标签位置
        mid_angle = (start_angle + end_angle) / 2
        mid_angle_rad = np.deg2rad(mid_angle)
        label_radius = (radius_outer + inner_radius) / 2
        x = label_radius * np.cos(mid_angle_rad)
        y = label_radius * np.sin(mid_angle_rad)
        text_positions.append((x, y))
        text_values.append(value)
        text_labels.append(legend_label)
        # 根据数值大小调整文字颜色以确保可读性
        text_colors.append('black' if value < 15 else 'white')
        start_angle = end_angle

    # 绘制中心圆
    centre_circle = plt.Circle(center, inner_radius, fc='white', edgecolor='white', lw=1.5)
    ax.add_artist(centre_circle)

    # 添加中心文本
    ax.text(0, 0, center_text,
            ha='center', va='center',
            fontsize=16, fontweight='bold',
            fontname='Times New Roman')

    # 添加分数标签
    for i, (x, y) in enumerate(text_positions):
        angle_deg = np.rad2deg(np.arctan2(y, x))
        if 90 < angle_deg < 270:
            angle_deg += 180

        # 特殊处理LeBron James，使用黑色
        color = 'black' if text_labels[i] == 'LeBron James' else text_colors[i]

        ax.text(x, y, f'{text_values[i]:.2f}',
                ha='center', va='center',
                color=color,
                fontsize=10,
                rotation=angle_deg,
                rotation_mode='anchor')

    # 准备图例
    legend_handles = []
    legend_labels_plot = []
    for i, label in enumerate(legend_labels_sorted):
        legend_handles.append(Patch(facecolor=colors_sorted[i], edgecolor='black', label=label))
        legend_labels_plot.append(label)

    # 添加图例
    fig.legend(handles=legend_handles,
               labels=legend_labels_plot,
               loc='lower center',
               ncol=5,
               fontsize=11,
               bbox_to_anchor=(0.5, 0.05),
               frameon=False,
               handletextpad=0.5,
               columnspacing=1.0)


# 提取数据
player_names = df['player_id'].tolist()
total_scores = (df['Total_Score'] * 10000).tolist()  # 乘以10000

# 创建图表
fig, ax = plt.subplots(1, 1, figsize=(12, 10))

# 绘制玫瑰图
draw_rose_chart(
    ax,
    fig,
    total_scores,
    color_palette,
    player_names,
    center_text="Lakers\nRanking"
)

plt.tight_layout()
plt.savefig('Rank/lakers_ranking_rose_chart.png', dpi=300, bbox_inches='tight')
plt.savefig('Rank/lakers_ranking_rose_chart.pdf', bbox_inches='tight')
plt.savefig('Rank/lakers_ranking_rose_chart.svg', bbox_inches='tight')
plt.show()

print("玫瑰图已生成并保存！")
