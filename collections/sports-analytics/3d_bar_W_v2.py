import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import os

# --- 1. 环境与字体配置 ---
script_dir = os.path.dirname(os.path.abspath(__file__))
# Use Matplotlib's bundled DejaVu Serif for portable rendering.
font_path = font_manager.findfont('DejaVu Serif')

# 创建不同字号的字体对象，解决 fontsize 不生效的问题
font_small = font_manager.FontProperties(fname=font_path, size=9)
font_reg = font_manager.FontProperties(fname=font_path, size=12)
font_large = font_manager.FontProperties(fname=font_path, size=11)

# 设置全局基础样式
plt.rcParams['font.family'] = font_reg.get_name()
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 自定义颜色方案
CUSTOM_COLORS = ['#16058b', '#6200aa', '#9e169d', '#cc4a74', '#eb7852', '#fcb431']

def plot_3d_bar_chart(df, custom_colors):
    """绘制3D柱状图"""
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    xpos = df['X'].values
    ypos = df['Y'].values
    dx = np.ones_like(xpos) * 0.4
    dy = np.ones_like(ypos) * 0.4
    dz = df['Z'].values

    # 绘制双色柱体
    for i, (x, y, z) in enumerate(zip(xpos, ypos, dz)):
        policy_idx = int(y)
        base_color = custom_colors[policy_idx % len(custom_colors)]

        # 将hex转换为RGB
        rgb = tuple(int(base_color.lstrip('#')[j:j+2], 16)/255 for j in (0, 2, 4))

        # 底部80%：浅色透明
        light_rgb = tuple(min(1.0, 0.9 + 0.1 * c) for c in rgb) # 稍微亮化的背景色
        bottom_height = z * 0.8
        ax.bar3d(x, y, 0, dx[i], dy[i], bottom_height,
                color=light_rgb, alpha=0.2, edgecolor='none')

        # 顶部20%：原色
        top_height = z * 0.2
        ax.bar3d(x, y, bottom_height, dx[i], dy[i], top_height,
                color=base_color, alpha=0.7, edgecolor='none')

    # 设置观察视角
    ax.view_init(elev=25, azim=-45)

    # 设置刻度定位
    from matplotlib.ticker import MaxNLocator, MultipleLocator
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.zaxis.set_major_locator(MultipleLocator(0.25))

    # 设置范围
    margin = 0.5
    ax.set_xlim(df['X'].min() - margin, df['X'].max() + margin)
    ax.set_ylim(df['Y'].min() - margin, df['Y'].max() + margin)
    ax.set_zlim(0, df['Z'].max() * 1.1)

    return fig, ax

if __name__ == "__main__":
    # --- 2. 数据处理 ---
    data_path = os.path.join(script_dir, 'wpc.csv')
    if not os.path.exists(data_path):
        # 模拟数据以供演示（如果文件不存在）
        df_raw = pd.DataFrame({
            'policy': ['Model(MPC)', 'Baseline-Zero', 'Baseline-MaxXL']*4,
            'season': [1,1,1,2,2,2,3,3,3,4,4,4],
            'W': np.random.rand(12)
        })
    else:
        df_raw = pd.read_csv(data_path)

    policy_name_mapping = {
        'Model(MPC)': 'Ours',
        'Baseline-Zero': 'Laissez-faire',
        'Baseline-MaxXL': 'Aggressive',
        'Baseline-Random': 'Random',
        'Baseline-Random2': 'Random2',
        'Baseline-Random3': 'Random3'
    }

    policy_order = ['Model(MPC)', 'Baseline-Zero', 'Baseline-MaxXL',
                    'Baseline-Random', 'Baseline-Random2', 'Baseline-Random3']
    policies = [p for p in policy_order if p in df_raw['policy'].values]

    data_list = []
    for i, policy in enumerate(policies):
        policy_data = df_raw[df_raw['policy'] == policy].sort_values('season')
        for _, row in policy_data.iterrows():
            data_list.append({
                'X': row['season'],
                'Y': i,
                'Z': row['W']
            })

    df = pd.DataFrame(data_list)

    # --- 3. 绘图与字体应用 ---
    fig, ax = plot_3d_bar_chart(df, CUSTOM_COLORS)

    # 设置 Y 轴标签 - 显式应用 font_large (11pt)
    policy_display_names = [policy_name_mapping.get(p, p) for p in policies]
    ax.set_yticks(range(len(policies)))
    ax.set_yticklabels(policy_display_names, fontproperties=font_large)

    # 隐藏 X 和 Z 轴标签
    ax.set_xlabel('')
    ax.set_zlabel('')

    # 创建图例 - 使用 font_reg (10pt)
    legend_patches = []
    for i, policy_name in enumerate(policy_display_names):
        color = CUSTOM_COLORS[i % len(CUSTOM_COLORS)]
        legend_patches.append(plt.Rectangle((0, 0), 1, 1, color=color, alpha=0.7))

    ax.legend(legend_patches, policy_display_names,
              loc='upper left',
              prop=font_reg,  # 这里的 prop 会决定图例字号
              frameon=True,
              fancybox=True,
              framealpha=0.8)

    # 强制刷新布局
    plt.tight_layout()

    # 保存PNG和SVG格式
    output_png = os.path.join(script_dir, '3d_bar_W_v2_output.png')
    output_svg = os.path.join(script_dir, '3d_bar_W_v2_output.svg')

    plt.savefig(output_png, dpi=300, bbox_inches='tight')
    print(f"PNG saved to: {output_png}")

    plt.savefig(output_svg, format='svg', dpi=300, bbox_inches='tight')
    print(f"SVG saved to: {output_svg}")

    plt.show()
