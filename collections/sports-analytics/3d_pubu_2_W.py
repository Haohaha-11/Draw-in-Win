# =============================================================================
# 1、导入所需库
# =============================================================================
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PolyCollection
import matplotlib.patches as mpatches
import pandas as pd
import matplotlib.font_manager as fm
import os

# Load Times New Roman font
script_dir = os.path.dirname(os.path.abspath(__file__))
font_path = fm.findfont('DejaVu Serif')
times_font = fm.FontProperties(fname=font_path)

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['axes.unicode_minus'] = False

# =============================================================================
# 2.定义颜色方案
# =============================================================================
custom_colors = ['#16058b', '#6200aa', '#9e169d', '#cc4a74', '#eb7852', '#fcb431']

# =============================================================================
# 3.数据加载函数
# =============================================================================
def load_data_from_csv(filepath):
    """从CSV文件加载WPC数据"""
    df = pd.read_csv(filepath)

    # Get unique policies and seasons
    policies = df['policy'].unique()
    seasons = sorted(df['season'].unique())

    # Create policy name mapping
    policy_mapping = {
        'Model(MPC)': 'Ours',
        'Baseline-Zero': 'Laissez-faire',
        'Baseline-MaxXL': 'Aggressive',
        'Baseline-Random': 'Random',
        'Baseline-Random2': 'Random2',
        'Baseline-Random3': 'Random3'
    }

    # Prepare data for W indicator
    all_y_data = []
    labels = []

    for policy in policies:
        policy_data = df[df['policy'] == policy].sort_values('season')
        all_y_data.append(policy_data['W'].values)
        labels.append(policy_mapping.get(policy, policy))

    print(f"成功从 {filepath} 加载数据。")
    return np.array(seasons), all_y_data, labels

# =============================================================================
# 4.瀑布图绘图函数
# =============================================================================
def plot_3d_waterfall(seasons, all_y_data, labels, colors):
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    num_datasets = len(all_y_data)

    # Plot each policy
    for i, y_data in enumerate(all_y_data):
        # Create closed polygon for filling
        padded_seasons = np.r_[seasons[0], seasons, seasons[-1]]
        padded_yd = np.r_[0, y_data, 0]
        verts = [list(zip(padded_seasons, padded_yd))]

        # Create polygon collection
        poly = PolyCollection(verts, facecolors=colors[i], alpha=0.4)
        ax.add_collection3d(poly, zs=i, zdir='x')

        # Plot line
        ax.plot(seasons, y_data, zs=i, zdir='x', color=colors[i], linewidth=2.5)

        # Add data labels
        for j, (season, w_value) in enumerate(zip(seasons, y_data)):
            ax.text(season, w_value + 0.03, i, f'{w_value:.2f}',
                   ha='center', va='bottom', fontsize=10,
                   fontproperties=times_font, color='black', fontweight='bold')

    # --- Axis settings ---
    ax.set_ylabel('Season', fontsize=14, labelpad=15, fontproperties=times_font)
    ax.set_zlabel('W Score', fontsize=14, labelpad=10, fontproperties=times_font)
    ax.set_xlabel('')

    # Set axis limits
    ax.set_ylim(seasons[-1] + 0.5, seasons[0] - 0.5)
    ax.set_xlim(-1, num_datasets)
    ax.set_zlim(0, max([max(y) for y in all_y_data]) * 1.15)

    # --- Tick settings ---
    ax.set_xticks(range(num_datasets))
    ax.set_xticklabels(labels, fontsize=11, rotation=0, ha='left', fontproperties=times_font)
    ax.tick_params(axis='x', pad=-5)
    ax.tick_params(axis='y', labelsize=11)
    ax.tick_params(axis='z', labelsize=11)

    # --- 3D view and background settings ---
    ax.view_init(elev=15, azim=-150)
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.xaxis.pane.set_edgecolor('k')
    ax.yaxis.pane.set_edgecolor((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.pane.set_edgecolor((1.0, 1.0, 1.0, 0.0))
    ax.set_box_aspect((35, 15, 12))
    ax.grid(False)

    # --- Manual tick lines and grid ---
    ax.tick_params(axis='x', length=0, color=(0, 0, 0, 0))
    ax.tick_params(axis='y', length=0, color=(0, 0, 0, 0))

    zmin, zmax = ax.get_zlim()
    xmin, xmax = ax.get_xlim()
    ymin_back, ymax_front = ax.get_ylim()

    xticks = ax.get_xticks()
    yticks = ax.get_yticks()
    tick_height = (zmax - zmin) * 0.025

    for x_pos in xticks:
        ax.plot([x_pos, x_pos], [ymin_back, ymin_back], [zmin, zmin + tick_height],
               color='k', linewidth=1)

    for y_pos in yticks:
        ax.plot([xmin, xmin], [y_pos, y_pos], [zmin, zmin + tick_height],
               color='k', linewidth=1)

    # Grid lines
    for x in xticks:
        if abs(x - xmin) < 1e-6:
            continue
        ax.plot([x, x], ax.get_ylim(), zmin, color='lightgray', linestyle='--', linewidth=0.5)

    for y in yticks:
        if abs(y - ymin_back) < 1e-6:
            continue
        ax.plot(ax.get_xlim(), [y, y], zmin, color='lightgray', linestyle='--', linewidth=0.5)

    # --- Legend ---
    legend_patches = [mpatches.Patch(color=colors[i], label=labels[i])
                     for i in range(len(labels))]
    ax.legend(handles=legend_patches, loc='upper right', bbox_to_anchor=(0.88, 0.75),
             fontsize=11, borderaxespad=0., prop=times_font)

# =============================================================================
# 6、主程序入口
# =============================================================================
if __name__ == '__main__':
    # Load data from CSV
    csv_file_path = os.path.join(script_dir, 'wpc.csv')
    seasons_data, y_datasets, data_labels = load_data_from_csv(csv_file_path)

    # Check if data loaded successfully
    if seasons_data is not None and y_datasets is not None:
        print(f"--- 使用自定义配色方案 ---")

        # Use custom colors
        plot_colors = custom_colors[:len(data_labels)]

        # Plot
        plot_3d_waterfall(seasons_data, y_datasets, data_labels, plot_colors)

        # Save outputs
        svg_path = os.path.join(script_dir, '3d_waterfall_2_W.svg')
        png_path = os.path.join(script_dir, '3d_waterfall_2_W.png')

        plt.savefig(svg_path, format='svg', dpi=300, bbox_inches='tight')
        print(f"W indicator 3D Waterfall Chart (Style 2) saved as '{svg_path}'")

        plt.savefig(png_path, format='png', dpi=300, bbox_inches='tight')
        print(f"Preview PNG also saved as '{png_path}'")

        plt.show()
