import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib import font_manager
import matplotlib
import os

# Load Times New Roman font
script_dir = os.path.dirname(os.path.abspath(__file__))
font_path = font_manager.findfont('DejaVu Serif')
times_font = font_manager.FontProperties(fname=font_path)

# Set style
plt.rcParams['font.family'] = times_font.get_name()
plt.rcParams['font.size'] = 10

# 自定义颜色方案
CUSTOM_COLORS = ['#16058b', '#6200aa', '#9e169d', '#cc4a74', '#eb7852', '#fcb431']

def plot_3d_bar_chart(df, custom_colors):
    """
    绘制3D柱状图

    参数:
        df: DataFrame，包含 'X', 'Y', 'Z' 列
        custom_colors: 自定义颜色列表
    """
    # 创建一个图形(figure)对象，并设置其大小
    fig = plt.figure(figsize=(12, 10))
    # 在图形中添加一个三维坐标系(axes)
    ax = fig.add_subplot(111, projection='3d')

    xpos = df['X'].values  # 获取'X'列的所有值作为每个柱子的x坐标
    ypos = df['Y'].values  # 获取'Y'列的所有值作为每个柱子的y坐标
    zpos = 0  # 设置所有柱子都从 z=0 的高度开始绘制
    dx = np.ones_like(xpos) * 0.4  # 创建一个和xpos形状相同、元素全为0.4的数组，作为柱子的宽度
    dy = np.ones_like(ypos) * 0.4  # 创建一个和ypos形状相同、元素全为0.4的数组，作为柱子的深度
    dz = df['Z'].values  # 获取'Z'列的所有值作为每个柱子的高度

    # 使用双色方案 - 顶端20%带颜色，底部80%浅色
    from matplotlib import cm
    import matplotlib.colors as mcolors

    # 先绘制底部80%的浅色部分
    for i, (x, y, z) in enumerate(zip(xpos, ypos, dz)):
        policy_idx = int(y)
        base_color = CUSTOM_COLORS[policy_idx % len(custom_colors)]
        # 将hex颜色转换为RGB
        rgb = tuple(int(base_color.lstrip('#')[j:j+2], 16)/255 for j in (0, 2, 4))

        # 底部80%使用很浅的颜色（接近白色）
        light_rgb = tuple(0.95 - 0.05 * c for c in rgb)  # 非常浅的颜色
        bottom_height = z * 0.8

        # 绘制底部（无边框，透明度0.2）
        ax.bar3d(x, y, 0, dx[i], dy[i], bottom_height,
                color=light_rgb, alpha=0.2, edgecolor='none', linewidth=0)

        # 顶部20%使用策略的原始颜色（无边框）
        top_height = z * 0.2
        ax.bar3d(x, y, bottom_height, dx[i], dy[i], top_height,
                color=rgb, alpha=0.56, edgecolor='none', linewidth=0)

    # 设置轴标签 - 不设置标签，与3d_pubu_P.py保持一致
    # ax.set_xlabel('Season', labelpad=8, fontsize=14, fontproperties=times_font)
    # ax.set_ylabel('Policy', labelpad=8, fontsize=14, fontproperties=times_font)
    # ax.set_zlabel('W Score', labelpad=8, fontsize=14, fontproperties=times_font)

    # 加粗坐标轴主线 - 移除此设置，与3d_pubu_P.py保持一致
    # ax.xaxis._axinfo["axisline"]['linewidth'] = 2
    # ax.yaxis._axinfo["axisline"]['linewidth'] = 2
    # ax.zaxis._axinfo["axisline"]['linewidth'] = 2

    # 设置刻度参数 - 移除此设置，与3d_pubu_P.py保持一致
    # ax.tick_params(axis='x', direction='out', pad=2, labelsize=12)
    # ax.tick_params(axis='y', direction='out', pad=2, labelsize=11)
    # ax.tick_params(axis='z', direction='out', pad=2, labelsize=12)

    # 设置X轴和Z轴只显示整数刻度
    from matplotlib.ticker import MaxNLocator, MultipleLocator
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    # Z轴设置刻度间隔为0.25
    ax.zaxis.set_major_locator(MultipleLocator(0.25))

    # 设置背景颜色 - 移除此设置，与3d_pubu_P.py保持一致
    # pane_color = 'white'
    # ax.xaxis.pane.set_facecolor(pane_color)
    # ax.yaxis.pane.set_facecolor(pane_color)
    # ax.zaxis.pane.set_facecolor(pane_color)

    # 设置观察视角
    ax.view_init(elev=25, azim=-45)

    # 设置坐标轴范围 - 确保柱子不会溢出
    margin_x = 0.5
    margin_y = 0.2
    ax.set_xlim(df['X'].min() - margin_x, df['X'].max() + margin_x + 0.4)
    ax.set_ylim(df['Y'].min() - margin_y, df['Y'].max() + margin_y + 0.4)
    ax.set_zlim(0, df['Z'].max() * 1.15)

    # 显示背景网格线 - 移除此设置，与3d_pubu_P.py保持一致
    # ax.grid(True, alpha=0.3)

    plt.tight_layout()

    return fig, ax

# 主程序
if __name__ == "__main__":
    # 从wpc.csv读取数据
    data_path = os.path.join(script_dir, 'wpc.csv')
    df_raw = pd.read_csv(data_path)

    # 策略名称映射
    policy_name_mapping = {
        'Model(MPC)': 'Ours',
        'Baseline-Zero': 'Laissez-faire',
        'Baseline-MaxXL': 'Aggressive',
        'Baseline-Random': 'Random',
        'Baseline-Random2': 'Random2',
        'Baseline-Random3': 'Random3'
    }

    # 获取唯一的策略并按照指定顺序排列
    policy_order = ['Model(MPC)', 'Baseline-Zero', 'Baseline-MaxXL',
                    'Baseline-Random', 'Baseline-Random2', 'Baseline-Random3']
    policies = [p for p in policy_order if p in df_raw['policy'].values]

    # 准备3D柱状图数据
    data_list = []
    for i, policy in enumerate(policies):
        policy_data = df_raw[df_raw['policy'] == policy].sort_values('season')
        for _, row in policy_data.iterrows():
            data_list.append({
                'X': row['season'] - 0.2,  # Season作为X轴，向左偏移使柱子居中
                'Y': i + 0.3,  # 策略索引作为Y轴，向上偏移使柱子居中
                'Z': row['W']  # W值作为Z轴（柱子高度）
            })

    # 创建DataFrame
    df = pd.DataFrame(data_list)

    # 调用函数来创建绘图
    fig, ax = plot_3d_bar_chart(df, CUSTOM_COLORS)

    # 设置Y轴刻度标签为策略名称
    policy_display_names = [policy_name_mapping.get(p, p) for p in policies]
    # 设置Y轴刻度位置为整数，并调整位置使其与柱子对齐
    y_tick_positions = [i + 0.5 for i in range(len(policies))]
    ax.set_yticks(y_tick_positions)
    ax.set_yticklabels(policy_display_names, fontsize=13,fontproperties=times_font)

    # 创建图例
    legend_patches = []
    for i, policy_name in enumerate(policy_display_names):
        color = CUSTOM_COLORS[i % len(CUSTOM_COLORS)]
        legend_patches.append(plt.Rectangle((0, 0), 1, 1, color=color, alpha=0.56))

    ax.legend(legend_patches, policy_display_names,
              loc='upper left',
              fontsize=13,
              frameon=True,
              shadow=False,
              fancybox=True,
              framealpha=0.8,
              prop=times_font)

    # 保存图片
    output_png = os.path.join(script_dir, '3d_bar_W_output.png')
    output_svg = os.path.join(script_dir, '3d_bar_W_output_1.svg')

    plt.savefig(output_svg, format='svg', dpi=300, bbox_inches='tight')
    print(f"W indicator 3D Bar Chart saved as '{output_svg}'")

    plt.savefig(output_png, format='png', dpi=300, bbox_inches='tight')
    print(f"Preview PNG also saved as '{output_png}'")

    plt.show()
