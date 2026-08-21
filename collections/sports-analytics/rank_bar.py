import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib
import numpy as np
import pandas as pd

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['font.size'] = 12

# 读取数据
df = pd.read_csv('Rank/lakers_current_deltaV_ranking.csv')

# 按DeltaV排序（从大到小）
df_sorted = df.sort_values('DeltaV', ascending=False).reset_index(drop=True)

# 配色方案（与玫瑰图一致，从深到浅）
color_palette = ['#3E236D', '#573388', '#2D5191', '#3B89C0', '#3AA09D',
                 '#4FB38E', '#8BC34A', '#B2D963', '#CDEB80', '#F0F4C3']

def plot_bar_chart(save_path=None):
    """
    绘制DeltaV条形图的函数, 并根据提供的路径保存图片。
    参数:
    - save_path (str, optional): 图片保存的完整路径。如果为 None, 则不保存。
    """
    # 提取数据
    players = df_sorted['Player_ID'].tolist()
    delta_values = df_sorted['DeltaV'].tolist()

    # 创建图表
    fig, ax = plt.subplots(figsize=(10, 7))

    # 绘制水平条形图（反转顺序，使最大值在顶部）
    bars = ax.barh(players[::-1], delta_values[::-1], color=color_palette[::-1], alpha=0.75)

    # 自定义坐标轴和标签
    ax.set_xlabel('ΔV (Value Impact)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Players', fontsize=14, fontweight='bold', rotation=90, labelpad=10)

    # 设置x轴范围和刻度
    max_val = max(delta_values)
    ax.set_xlim(0, max_val * 1.15)

    # 美化图表样式
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)

    ax.tick_params(axis='x', which='major', direction='out', length=5, width=1.5)
    ax.tick_params(axis='y', which='major', direction='out', length=5, width=1.5)
    ax.tick_params(axis='both', labelsize=12)

    # 添加网格线
    ax.xaxis.grid(True, linestyle='--', color='gray', linewidth=0.5, alpha=0.7)
    ax.set_axisbelow(True)

    # 在每个条形图右侧添加数值标签
    for bar, value in zip(bars, delta_values[::-1]):
        width = bar.get_width()
        ax.text(width + max_val * 0.01, bar.get_y() + bar.get_height() / 2,
                f'{value:.2f}',
                va='center', ha='left', fontsize=11, fontweight='bold')

    # 保存和显示图表
    plt.tight_layout()

    if save_path:
        try:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"条形图已保存到: {save_path}")
        except Exception as e:
            print(f"保存条形图时出错: {e}")

    return fig, ax


# 调用函数并保存图片
fig, ax = plot_bar_chart('Rank/lakers_deltaV_bar_chart.png')
plt.savefig('Rank/lakers_deltaV_bar_chart.pdf', bbox_inches='tight')
plt.savefig('Rank/lakers_deltaV_bar_chart.svg', bbox_inches='tight')
plt.show()

print("所有格式的条形图已生成并保存！")
