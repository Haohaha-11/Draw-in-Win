import matplotlib.pyplot as plt
import pandas as pd
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

# 获取每种策略最后的Pop值
final_pops = {}
for strategy, file_path in data_files.items():
    df = pd.read_csv(file_path)
    final_pop = df['Pop'].iloc[-1]  # 获取最后一行的Pop值
    final_pops[strategy] = final_pop
    print(f"{strategy}: {final_pop:.4f}")

# 准备饼图数据
labels = list(final_pops.keys())
sizes = list(final_pops.values())
colors = ['#4472C4', '#ED7D31', '#70AD47', '#C00000']  # 蓝、橙、绿、红
explode = (0, 0, 0, 0.1)  # 突出显示Our Model

# 创建图形
fig, ax = plt.subplots(figsize=(10, 8))

# 绘制饼图
wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                                    autopct='%1.1f%%', startangle=90,
                                    textprops={'fontsize': 12, 'fontweight': 'bold'})

# 设置百分比文字样式
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(11)
    autotext.set_fontweight('bold')

# 设置标签文字样式
for text in texts:
    text.set_fontsize(13)
    text.set_fontweight('bold')

# 添加标题
ax.set_title('Final Popularity Distribution by Strategy',
            fontsize=15, fontweight='bold', pad=20)

# 确保饼图是圆形
ax.axis('equal')

# 添加图例（显示具体数值）
legend_labels = [f'{label}: {size:.4f}' for label, size in zip(labels, sizes)]
ax.legend(legend_labels, loc='upper left', bbox_to_anchor=(1, 1),
         fontsize=11, framealpha=0.9)

# 调整布局
plt.tight_layout()

# 保存图片
plt.savefig('pop_pie_chart.png', dpi=300, bbox_inches='tight')
plt.savefig('pop_pie_chart.pdf', bbox_inches='tight')
plt.savefig('pop_pie_chart.svg', bbox_inches='tight')

print("\n图表已保存:")
print("- pop_pie_chart.png")
print("- pop_pie_chart.pdf")
print("- pop_pie_chart.svg")

plt.show()
