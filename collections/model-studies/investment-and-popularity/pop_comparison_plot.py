import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib import font_manager

# 设置字体
try:
    font_path = font_manager.findfont('DejaVu Serif')
    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
except:
    plt.rcParams['font.family'] = 'serif'

# 读取四种策略的数据
data_files = {
    'Conservative': '投资过程中的各项指标变化/保守/static_case1_low_pop_path.csv',
    'Aggressive': '投资过程中的各项指标变化/激进/static_case2_profit_redline_path.csv',
    'Irrational': '投资过程中的各项指标变化/失去理智/static_case3_cashflow_bankrupt_path.csv',
    'Our Model': '投资过程中的各项指标变化/我们的模型/ours_case_path.csv'
}

# 创建图形
fig, ax = plt.subplots(figsize=(12, 6))

# 颜色和线型设置（参考图片风格）
colors = ['#4472C4', '#ED7D31', '#70AD47', '#C00000']  # 蓝、橙、绿、红
linestyles = ['-', '-', '-', '--']  # 实线和虚线
markers = ['', '', 'x', 'o']  # 不同的标记
linewidths = [2, 2, 2, 2.5]

# 步长设置
step = 50

# 绘制每种策略的Pop变化
for i, (strategy, file_path) in enumerate(data_files.items()):
    df = pd.read_csv(file_path)

    # 每隔step个数据点取一个
    df_sampled = df.iloc[::step, :]

    # 绘制折线
    ax.plot(df_sampled['t'], df_sampled['Pop'],
           color=colors[i], linestyle=linestyles[i],
           marker=markers[i], markersize=6 if markers[i] else 0,
           linewidth=linewidths[i], label=strategy, alpha=0.8)

# 设置坐标轴
ax.set_xlabel('Time (t)', fontsize=13, fontweight='bold')
ax.set_ylabel('Popularity (Pop)', fontsize=13, fontweight='bold')

# 设置网格
ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.8)
ax.set_axisbelow(True)

# 添加图例
ax.legend(loc='best', fontsize=11, framealpha=0.9,
         edgecolor='black', fancybox=True)

# 设置y轴范围
ax.set_ylim(0, 1.2)

# 调整布局
plt.tight_layout()

# 保存图片
plt.savefig('pop_comparison.png', dpi=300, bbox_inches='tight')
plt.savefig('pop_comparison.pdf', bbox_inches='tight')
plt.savefig('pop_comparison.svg', bbox_inches='tight')

print("图表已保存:")
print("- pop_comparison.png")
print("- pop_comparison.pdf")
print("- pop_comparison.svg")

plt.show()
