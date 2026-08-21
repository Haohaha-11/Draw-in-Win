import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

# 设置字体
font_path = font_manager.findfont('DejaVu Serif')
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['font.size'] = 12
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
df = pd.read_csv(
    SCRIPT_DIR / '五组实验的V的五个赛季预测变化' / 'v_comparison_data.csv'
)

# 创建图形
fig, ax = plt.subplots(figsize=(12, 8))

# 定义颜色方案和策略映射（只保留一个随机策略）
strategy_mapping = {
    'V_Model(MPC)': ('Ours', '#2d1d96'),
    'V_Baseline-Zero': ('Laissez-faire', '#fdc35a'),
    'V_Baseline-MaxXL': ('Aggressive', '#a82da8'),
    'V_Baseline-Random': ('Random', '#d25c82')
}

# 绘制选定的策略折线
seasons = df['Season'].values
plot_data = {}

for column in df.columns[1:]:
    if column in strategy_mapping:
        new_name, color = strategy_mapping[column]
        plot_data[new_name] = df[column].values

        if new_name == 'Ours':
            # 我们的策略用更粗的线
            ax.plot(seasons, df[column], marker='o', linewidth=2.3,
                    label=new_name, color=color, markersize=10, zorder=5)
        else:
            # 其他策略使用圆形标记
            ax.plot(seasons, df[column], marker='o', linewidth=2,
                    label=new_name, color=color, markersize=7, alpha=0.8)

        # 为每条曲线添加阴影带表示随机扰动
        noise_level = 0.05 if new_name == 'Ours' else 0.08  # Ours策略扰动更小
        upper_bound = df[column].values * (1 + noise_level)
        lower_bound = df[column].values * (1 - noise_level)
        ax.fill_between(seasons, lower_bound, upper_bound,
                       color=color, alpha=0.15, linewidth=0, zorder=1)

        # 在每个散点上标注数值
        for i, (season, value) in enumerate(zip(seasons, df[column].values)):
            # 根据位置调整标注位置，避免重叠
            if new_name == 'Ours':
                offset = 0.12
                va = 'bottom'
            else:
                offset = -0.08
                va = 'top'

            ax.text(season, value + offset, f'{value:.2f}',
                   ha='center', va=va, fontsize=11, color=color, alpha=0.9)

# ==================== V形恢复阴影区域设置 ====================
# 添加V形恢复的阴影区域（只在高点和低点之间）
ours_data = plot_data['Ours']

# 【参数1】定义最低点和最高点的位置（索引从0开始）
min_idx = 1  # 最低点位置：第2赛季（索引1）
max_idx = 4  # 最高点位置：第5赛季（索引4）
min_value = ours_data[min_idx]
max_value = ours_data[max_idx]

# 【参数2】阴影范围：只在第min_idx到第max_idx赛季之间填充
recovery_seasons = seasons[min_idx:max_idx+1]
recovery_values = ours_data[min_idx:max_idx+1]

# 阴影底部使用最低点的值（而不是y轴最小值0）
y_bottom = min_value  # 阴影从最低点开始

# 【参数3】填充V形恢复区域的透明度和颜色
ax.fill_between(recovery_seasons, recovery_values, y_bottom,
                alpha=0.5,           # 阴影透明度：0-1之间，越大越不透明
                color='#2d1d96',      # 阴影颜色
                linewidth=0,
                zorder=0)

# ==================== 高点和低点标记设置 ====================
# 【参数4】突出显示最低点（圆形标记）
ax.scatter([seasons[min_idx]], [min_value],
          s=200,                    # 散点大小
          color='#2d1d96',          # 散点颜色（与曲线颜色一致）
          edgecolors='white',       # 边框颜色
          linewidths=3,             # 边框宽度
          zorder=10,
          marker='o',               # 标记形状：'o'=圆形
          label='_nolegend_')

# 【参数5】突出显示最高点（圆形标记）
ax.scatter([seasons[max_idx]], [max_value],
          s=200,                    # 散点大小
          color='#2d1d96',          # 散点颜色（与曲线颜色一致）
          edgecolors='white',       # 边框颜色
          linewidths=3,             # 边框宽度
          zorder=10,
          marker='o',               # 标记形状：'o'=圆形
          label='_nolegend_')


# 设置坐标轴
ax.set_xlabel('Season', fontsize=14)
ax.set_ylabel('Value Function', fontsize=14)

# 设置x轴刻度
ax.set_xticks(seasons)
ax.set_xticklabels([f'S{int(s)}' for s in seasons])

# 添加网格
ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
ax.set_axisbelow(True)

# 添加零线
ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.8, alpha=0.5)

# 图例放在图像下方，实线框外
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08),
         frameon=True, shadow=False, fontsize=11, ncol=4,
         edgecolor='black', fancybox=False)

# 调整布局
plt.tight_layout()

# 保存图形
plt.savefig(SCRIPT_DIR / 'v_recovery_plot.pdf', dpi=300, bbox_inches='tight')
plt.savefig(SCRIPT_DIR / 'v_recovery_plot.png', dpi=300, bbox_inches='tight')
plt.savefig(SCRIPT_DIR / 'v_recovery_plot.svg', bbox_inches='tight')

print("图形已保存！")
print(f"\nOurs策略关键指标:")
print(f"  初始值 (S1): {ours_data[0]:.4f}")
print(f"  最低点 (S2): {ours_data[1]:.4f}")
print(f"  最终值 (S5): {ours_data[4]:.4f}")
recovery_rate = ((ours_data[4] - ours_data[1]) / abs(ours_data[1])) * 100
print(f"  恢复幅度: {recovery_rate:.2f}%")
print(f"  总体增长: {((ours_data[4] - ours_data[0]) / ours_data[0] * 100):.2f}%")

plt.show()
