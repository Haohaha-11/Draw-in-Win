import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

# 设置字体
font_path = font_manager.findfont('DejaVu Serif')
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['font.size'] = 12
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
df = pd.read_csv(SCRIPT_DIR / 'model_1_res_v2.csv')

# 筛选我们的策略（Model(MPC)）的第2和第3赛季数据
ours_data = df[df['policy'] == 'Model(MPC)']
season2 = ours_data[ours_data['season'] == 2].iloc[0]
season3 = ours_data[ours_data['season'] == 3].iloc[0]

# 提取x和L的值
data = {
    'Season 2': [season2['decision_x'], season2['decision_L']],
    'Season 3': [season3['decision_x'], season3['decision_L']]
}

# 创建图形
fig, ax = plt.subplots(figsize=(10, 7))

# 设置柱状图参数
categories = ['x', 'L']
x_pos = np.arange(len(categories))
width = 0.35

# 配色
colors = ['#4536a1', '#fdbc46']

# 绘制柱状图
bars1 = ax.bar(x_pos - width/2, data['Season 2'], width,
               label='Season 2', color=colors[0], alpha=0.9, edgecolor='white', linewidth=1.5)
bars2 = ax.bar(x_pos + width/2, data['Season 3'], width,
               label='Season 3', color=colors[1], alpha=0.9, edgecolor='white', linewidth=1.5)

# 在柱子上添加数值标签
def add_value_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.03,
                f'{height:.2f}',
                ha='center', va='bottom', fontsize=12, weight='bold')

add_value_labels(bars1)
add_value_labels(bars2)

# 设置坐标轴
ax.set_xlabel('Decision Variables', fontsize=14, weight='bold')
ax.set_ylabel('Value', fontsize=14, weight='bold')
ax.set_title('Comparison of Decision Variables (x, L) between Season 2 and Season 3',
             fontsize=15, weight='bold', pad=20)
ax.set_xticks(x_pos)
ax.set_xticklabels(categories, fontsize=13)

# 添加网格
ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5, axis='y')
ax.set_axisbelow(True)

# 图例
ax.legend(loc='upper right', frameon=True, shadow=False, fontsize=12,
         edgecolor='black', fancybox=False)

# 设置y轴范围
ax.set_ylim(0, max(max(data['Season 2']), max(data['Season 3'])) * 1.2)

# 调整布局
plt.tight_layout()

# 保存图形
plt.savefig(SCRIPT_DIR / 'season_comparison_bar.pdf', dpi=300, bbox_inches='tight')
plt.savefig(SCRIPT_DIR / 'season_comparison_bar.png', dpi=300, bbox_inches='tight')
plt.savefig(SCRIPT_DIR / 'season_comparison_bar.svg', bbox_inches='tight')

print("图形已保存！")
print(f"\n数据对比:")
print(f"Season 2: x={season2['decision_x']:.3f}, L={season2['decision_L']:.3f}")
print(f"Season 3: x={season3['decision_x']:.3f}, L={season3['decision_L']:.3f}")
print(f"\n变化:")
print(f"Δx = {season3['decision_x'] - season2['decision_x']:.3f}")
print(f"ΔL = {season3['decision_L'] - season2['decision_L']:.3f}")

plt.show()
