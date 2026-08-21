"""
Monte Carlo云雨图绘制
从D/monte_carlo文件夹读取数据并绘制云雨图
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ==================== 1. 字体设置 ====================
script_dir = os.path.dirname(os.path.abspath(__file__))
font_path = fm.findfont('DejaVu Serif')
times_font = fm.FontProperties(fname=font_path)

plt.rcParams['font.family'] = times_font.get_name()
plt.rcParams['font.size'] = 12

# ==================== 2. 数据读取 ====================
monte_carlo_dir = os.path.join(script_dir, 'monte_carlo')

# 定义策略文件映射
strategy_files = {
    'Ours': 'monte_carlo_frequency_N1000_JJ_Ours.csv',
    'Laissez-faire': 'monte_carlo_zero_frequency.csv',
    'Aggressive': 'monte_carlo_frequency_N1000_Maxxl.csv',
    'Random': 'monte_carlo_frequency_N1000_Baseline-Random.csv',
    'Random2': 'monte_carlo_frequency_N1000_Baseline-Random2.csv',
    'Random3': 'monte_carlo_frequency_N1000_Baseline-Random3.csv'
}

# 读取所有策略的数据
data_dict = {}
for strategy_name, filename in strategy_files.items():
    file_path = os.path.join(monte_carlo_dir, filename)
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)

        # 根据策略名称过滤数据
        if strategy_name == 'Ours':
            df = df[df['policy'] == 'MPC']  # 只保留MPC的数据
        elif strategy_name == 'Aggressive':
            df = df[df['policy'] == 'MaxXL']  # 只保留MaxXL的数据
        elif strategy_name == 'Laissez-faire':
            df = df[df['policy'] == 'Zero']  # 只保留Zero的数据
        # 其他策略保持原样

        # 根据frequency重建数据分布
        v_values = []
        for _, row in df.iterrows():
            freq = int(row['frequency'])
            if freq > 0:  # 只保留出现过的值
                v_values.extend([row['V_value']] * freq)

        if len(v_values) > 0:
            data_dict[strategy_name] = np.array(v_values)
            print(f"Loaded {strategy_name}: {len(v_values)} data points")
            print(f"  Min: {min(v_values):.6f}, Max: {max(v_values):.6f}")
            print(f"  Mean: {np.mean(v_values):.6f}, Median: {np.median(v_values):.6f}")
            # 检查是否有负值
            negative_count = sum(1 for v in v_values if v < 0)
            if negative_count > 0:
                print(f"  WARNING: {negative_count} negative values found!")
            print()
        else:
            print(f"Warning: {strategy_name} has no data with frequency > 0")
    else:
        print(f"Warning: {filename} not found")

# 获取类别列表
categories = list(data_dict.keys())

# ==================== 3. 可视化设置 ====================
fig, ax = plt.subplots(figsize=(14, 8))

# 定义颜色方案（与之前的3D图保持一致）
colors = ['#16058b', '#6200aa', '#9e169d', '#cc4a74', '#eb7852', '#fcb431']

# 设置类别在x轴上的位置
positions = np.arange(len(categories))
box_width = 0.15
violin_width = 0.5

# ==================== 4. 绘制图形 ====================
for i, category in enumerate(categories):
    # 获取当前类别的数据值
    data_points = data_dict[category]

    # ------------------ 4.1 绘制箱形图 ------------------
    box_pos = positions[i] - box_width / 100

    box = ax.boxplot(
        data_points,
        positions=[box_pos],
        widths=box_width,
        patch_artist=True,
        showfliers=False,
        notch=True,
        medianprops={'color': 'black', 'linewidth': 3},
        boxprops={'facecolor': colors[i], 'edgecolor': colors[i]},
        whiskerprops={'color': colors[i], 'linewidth': 3},
        capprops={'color': colors[i], 'linewidth': 3}
    )

    # ------------------ 4.2 绘制半小提琴图 ------------------
    violin_pos = positions[i] + box_width / 50

    violin = ax.violinplot(
        data_points,
        positions=[violin_pos],
        widths=violin_width,
        showmeans=False,
        showmedians=False,
        showextrema=False
    )

    # 修改小提琴图只显示右侧一半
    for pc in violin['bodies']:
        pc.set_facecolor(colors[i])
        pc.set_edgecolor(colors[i])
        pc.set_alpha(0.35)

        vertices = pc.get_paths()[0].vertices
        vertices[:, 0] = np.where(
            vertices[:, 0] > violin_pos,
            vertices[:, 0],
            violin_pos
        )

    # ------------------ 4.3 添加散点 ------------------
    # 对数据进行采样以避免点过多
    sample_size = min(200, len(data_points))
    sampled_indices = np.random.choice(len(data_points), sample_size, replace=False)
    sampled_data = data_points[sampled_indices]

    ax.scatter(
        np.random.normal(positions[i] - box_width, 0.04, len(sampled_data)),
        sampled_data,
        color=colors[i],
        alpha=0.6,
        s=30,
        edgecolor='white',
        linewidth=0.5,
        zorder=3
    )

# ==================== 5. 图表美化 ====================
ax.set_xticks(positions)
ax.set_xticklabels(categories, fontsize=18, fontproperties=times_font)

ax.set_ylabel('V Value', fontsize=16, fontproperties=times_font)
ax.tick_params(axis='y', labelsize=12)

# 添加网格线
ax.grid(axis='y', linestyle='--', alpha=0.7)

# 显示边框
for spine in ['top', 'right', 'bottom', 'left']:
    ax.spines[spine].set_visible(True)
    ax.spines[spine].set_linewidth(2)
    ax.spines[spine].set_color('black')

# 删除标题
# plt.title('Monte Carlo Simulation Results - Raincloud Plot',
#           pad=20, fontsize=18, fontproperties=times_font)

plt.tight_layout()

# ==================== 6. 保存图形 ====================
output_png = os.path.join(script_dir, 'monte_carlo_raincloud.png')
output_svg = os.path.join(script_dir, 'monte_carlo_raincloud.svg')

plt.savefig(output_png, dpi=300, bbox_inches='tight')
print(f"\nPNG saved to: {output_png}")

plt.savefig(output_svg, format='svg', dpi=300, bbox_inches='tight')
print(f"SVG saved to: {output_svg}")

plt.show()
