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

# 读取baseline数据以建立选手到颜色的映射
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
df_baseline = pd.read_csv(os.path.join(script_dir, 'baseline_candidate_rank.csv'))
df_baseline_sorted = df_baseline.sort_values('Total_Score', ascending=False).reset_index(drop=True)

# 读取Case B数据
df = pd.read_csv(os.path.join(script_dir, 'candidate_rank_change_Case_B(受众重叠型).csv'))

# 按Total_Score排序（从大到小）
df_sorted = df.sort_values('Total_Score', ascending=False).reset_index(drop=True)

# 配色方案（从深到浅，扩展到10个颜色）
color_palette = ['#16048a', '#6201a9', '#914dc3', '#a82da8', '#cd4a74',
                 '#763c2a', '#ec7753', '#fdc35a', '#b8e6b8', '#87ceeb']

# 建立选手到颜色的映射（基于baseline排名）
player_color_map = {}
for i, player in enumerate(df_baseline_sorted['player_id']):
    if i < len(color_palette):
        player_color_map[player] = color_palette[i]

# 打印颜色映射以验证
print("选手颜色映射（基于baseline排名）：")
for player, color in player_color_map.items():
    print(f"  {player}: {color}")

def plot_bar_chart(save_path=None):
    """
    绘制候选球员排名条形图的函数, 并根据提供的路径保存图片。
    参数:
    - save_path (str, optional): 图片保存的完整路径。如果为 None, 则不保存。
    """
    # 提取数据（乘以10000以便显示）
    players = df_sorted['player_id'].tolist()
    total_scores = (df_sorted['Total_Score'] * 10000).tolist()

    # 根据选手获取对应的颜色
    colors = [player_color_map.get(player, '#cccccc') for player in players]

    # 打印Case B中的实际绘图顺序和颜色
    print("\nCase B实际绘图顺序和颜色：")
    for i, (player, color, score) in enumerate(zip(players, colors, total_scores)):
        print(f"  排名{i+1} - {player}: {color} (分数: {score:.2f})")

    # 创建图表
    fig, ax = plt.subplots(figsize=(10, 7))

    # 绘制水平条形图（反转顺序，使最大值在顶部）
    bars = ax.barh(players[::-1], total_scores[::-1], color=colors[::-1], alpha=0.5)

    # 自定义坐标轴和标签
    ax.set_xlabel('Value Increment ΔV (×10⁴)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Candidate Players', fontsize=14, fontweight='bold', rotation=90, labelpad=10)

    # 设置x轴范围和刻度
    max_val = max(total_scores)
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
    for bar, value in zip(bars, total_scores[::-1]):
        width = bar.get_width()
        ax.text(width + max_val * 0.01, bar.get_y() + bar.get_height() / 2,
                f'{value:.2f}',
                va='center', ha='left', fontsize=11, fontweight='bold')

    # 添加标题
    ax.set_title('Case B Candidate Players Ranking (Audience Overlap)', fontsize=16, fontweight='bold', pad=15)

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
output_dir = os.path.dirname(os.path.abspath(__file__))
fig, ax = plot_bar_chart(os.path.join(output_dir, 'case_b_candidate_rank_bar.png'))
plt.savefig(os.path.join(output_dir, 'case_b_candidate_rank_bar.pdf'), bbox_inches='tight')
plt.savefig(os.path.join(output_dir, 'case_b_candidate_rank_bar.svg'), bbox_inches='tight')
plt.show()

print("所有格式的Case B候选球员排名条形图已生成并保存！")
print(f"排名前三的球员：")
for i in range(min(3, len(df_sorted))):
    print(f"{i+1}. {df_sorted.iloc[i]['player_id']}: {df_sorted.iloc[i]['Total_Score']*10000:.2f}")
