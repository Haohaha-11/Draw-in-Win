"""
候选球员排名花瓣状雷达图
从D/Rank/候选球星信息汇总.csv读取数据并绘制
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os

# 字体和样式设置
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

# =========================================================================================
# ====================================== 颜色库 =========================================
# =========================================================================================
color_schemes = {
    1: ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F', '#EDC948',
        '#B07AA1', '#FF9DA7', '#9C755F', '#BAB0AC', '#D37295', '#B59A4A',
        '#34657F', '#A34E79'],
}
color_scheme = 1

# =========================================================================================
# ====================================== 绘图函数 ========================================
# =========================================================================================
def create_petal_plot(labels, values, color_list):
    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(polar=True))
    num_vars = len(labels)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles = np.array(angles) + (np.pi / 2 - angles[0])

    for i in range(num_vars):
        angle = angles[i]
        value = values[i]
        color = color_list[i]

        num_points_petal = 100
        r_points = np.linspace(0, value, num_points_petal)
        base_width = (2 * np.pi / num_vars)
        max_angular_width = base_width * 0.25
        delta_theta = max_angular_width * np.sin(np.pi * r_points / value)

        thetas1 = angle + delta_theta
        radii1 = r_points
        thetas2 = angle - delta_theta[::-1]
        radii2 = r_points[::-1]

        # 绘制花瓣
        ax.fill(np.concatenate([thetas1, thetas2]),
                np.concatenate([radii1, radii2]),
                color=color,
                alpha=0.7,
                edgecolor=color,
                linewidth=1.5)

    ax.grid(False)
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.spines['polar'].set_visible(False)

    max_val = max(values) * 1.4  # 增大范围，从1.2改为1.4
    ax.set_ylim(0, max_val)

    # 绘制参考圆
    ax.plot(np.linspace(0, 2 * np.pi, 100),
            np.full(100, max_val * 0.6),  # 调整参考圆位置
            color='gray',
            linestyle='-',
            linewidth=1.5,
            zorder=0)

    ax.plot(np.linspace(0, 2 * np.pi, 100),
            np.full(100, max_val * 0.2),
            color='gray',
            linestyle='--',
            linewidth=1.0,
            zorder=0)

    ax.plot(np.linspace(0, 2 * np.pi, 100),
            np.full(100, max_val * 0.4),
            color='gray',
            linestyle='--',
            linewidth=1.0,
            zorder=0)

    # 添加球员名称标注
    for i, (angle, label, color) in enumerate(zip(angles, labels, color_list)):
        rotation = np.rad2deg(angle)
        if angle >= np.pi / 2 and angle < 3 * np.pi / 2:
            alignment = "center"
            rotation += 270
        else:
            alignment = "center"
            rotation += 270

        ax.text(
            angle,
            max_val * 0.75,  # 调整文字位置，从0.85改为0.75
            label,
            size=14,  # 增大字体，从12改为14
            color=color,
            ha=alignment,
            va="center",
            rotation=rotation,
            rotation_mode="anchor",
            weight='bold'
        )

    return fig, ax

# =========================================================================================
# ====================================== 执行部分 ========================================
# =========================================================================================
if __name__ == '__main__':
    # 读取数据
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, 'Rank', '候选球星信息汇总.csv')

    df = pd.read_csv(data_path)

    # 按Value_Increase降序排序
    df = df.sort_values('Value_Increase', ascending=False)

    # 提取球员名称和Value_Increase
    labels = df['Player_ID'].tolist()
    raw_values = df['Value_Increase'].tolist()

    # 数据变换：使用平方根变换压缩差距
    transformed_values = [np.sqrt(max(0, v)) for v in raw_values]

    # Min-Max归一化到0.3-1.0范围（确保最小值也有可见的花瓣）
    min_val = min(transformed_values)
    max_val = max(transformed_values)

    if max_val > min_val:
        values = [0.3 + 0.7 * (v - min_val) / (max_val - min_val) for v in transformed_values]
    else:
        values = [0.5] * len(transformed_values)

    print(f"Loaded {len(labels)} players")
    print(f"Top player: {labels[0]}")
    print(f"  Raw value: {raw_values[0]:.2f}")
    print(f"  Transformed value: {values[0]:.3f}")
    print(f"Last player: {labels[-1]}")
    print(f"  Raw value: {raw_values[-1]:.2f}")
    print(f"  Transformed value: {values[-1]:.3f}")

    # 提取配色方案
    palette_colors = color_schemes[color_scheme]
    num_colors = len(palette_colors)

    # 根据标签数量，循环使用调色板中的颜色
    final_colors = [palette_colors[i % num_colors] for i in range(len(labels))]

    # 调用函数进行绘图
    fig, ax = create_petal_plot(labels, values, final_colors)

    # 保存图片
    output_png = os.path.join(script_dir, 'player_ranking_petal.png')
    output_svg = os.path.join(script_dir, 'player_ranking_petal.svg')
    output_pdf = os.path.join(script_dir, 'player_ranking_petal.pdf')

    plt.savefig(output_png, dpi=300, bbox_inches='tight')
    print(f"\nPNG saved to: {output_png}")

    plt.savefig(output_svg, format='svg', dpi=300, bbox_inches='tight')
    print(f"SVG saved to: {output_svg}")

    plt.savefig(output_pdf, format='pdf', bbox_inches='tight')
    print(f"PDF saved to: {output_pdf}")

    plt.show()
