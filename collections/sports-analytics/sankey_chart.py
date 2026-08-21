import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib
import numpy as np

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['font.size'] = 10

# 读取数据
df = pd.read_csv('Components/qiuyuan.csv')

# 使用所有10名球员
all_players = df['Player'].tolist()

# 选择所有8个指标
metrics = ['Local (Votes)', 'Young (IG)', 'Female (Like)', 'Intl (Score)',
           'Hardcore (PER)', 'Gossip (Buzz)', 'Brand (Salary)', 'Comm (Good)']
metric_labels = ['Local Fans', 'Young Fans', 'Female Fans', 'International',
                 'Performance', 'Media Buzz', 'Brand Value', 'Community']

# 配色方案（参考图片）
# 指标配色（左侧）- 使用第一组配色
metric_colors = ['#377EB8', '#B23648', '#c2d4b9', '#DBEBCD', '#dfd7a2', '#DAD4B9',
                 '#b4b9ba', '#cadbe1']

# 球员配色（右侧）- 使用第二组配色
player_colors = ['#eb687a', '#f1837a', '#f5a8a2', '#f6dfd7', '#ad7d71', '#ac9c97',
                 '#d5d1d0', '#d5d3de', '#d0cce3', '#b7b3d6']

# ========== 可调整参数区域 ==========

# 【色块间距调整】修改这个值来调整色块之间的间距
BLOCK_SPACING = 0.35  # 色块之间的间距，默认0.05

# 【左右两列距离调整】修改这个值来调整指标和球员之间的距离
LAYER_DISTANCE = 5.0  # 左侧指标和右侧球员之间的距离，增大=距离更远

# 【权重带出发位置调整】修改这些值来调整权重带的起点和终点位置
FLOW_START_OFFSET = 1.2   # 权重带从色块右边缘的偏移量（左侧指标）
FLOW_END_OFFSET = 0       # 权重带到色块左边缘的偏移量（右侧球员）

# 【权重带透明度调整】
FLOW_ALPHA = 0.5           # 权重带透明度，默认0.5

# ====================================
FLOW_ALPHA = 0.4           # 权重带透明度，默认0.4

# ====================================

# 创建图表
fig, ax = plt.subplots(figsize=(16, 12))
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis('off')

# 第一层（左侧）：8个指标
layer1_x = 0.5
layer1_height = 10
layer1_y_start = 1

# 计算每个指标的高度（均匀分布，和球员一样大）
metric_height = layer1_height / len(metrics)
metric_y_positions = []
current_y = layer1_y_start

for idx, metric_label in enumerate(metric_labels):
    metric_y_positions.append(current_y)

    # 绘制指标矩形（去掉边框）
    rect = FancyBboxPatch(
        (layer1_x, current_y), 1.2, metric_height - BLOCK_SPACING,  # 使用间距参数
        boxstyle="round,pad=0.03",
        facecolor=metric_colors[idx],
        edgecolor='none',  # 去掉边框
        linewidth=0,
        alpha=0.8
    )
    ax.add_patch(rect)

    # 添加指标名称
    ax.text(layer1_x + 0.6, current_y + metric_height/2 - BLOCK_SPACING/2, metric_label,
            ha='center', va='center', fontsize=14, fontweight='bold',
            color='black')

    current_y += metric_height

# 第二层（右侧）：10名球员
# 根据LAYER_DISTANCE参数计算layer2_x的位置
layer2_x = layer1_x + 1.2 + LAYER_DISTANCE  # 1.2是色块宽度
layer2_height = 10
layer2_y_start = 1

# 计算每个球员的高度（均匀分布，和指标一样大）
player_height = layer2_height / len(all_players)
player_y_positions = []
current_y = layer2_y_start

for idx, row in df.iterrows():
    player_y_positions.append(current_y)

    # 绘制球员矩形（去掉边框）
    rect = FancyBboxPatch(
        (layer2_x, current_y), 1.2, player_height - BLOCK_SPACING,  # 使用间距参数
        boxstyle="round,pad=0.03",
        facecolor=player_colors[idx % len(player_colors)],
        edgecolor='none',  # 去掉边框
        linewidth=0,
        alpha=0.8
    )
    ax.add_patch(rect)

    # 添加球员名称
    player_name = row['Player']
    # 缩短名字以适应空间
    if len(player_name) > 20:
        player_name = player_name[:19] + '...'
    ax.text(layer2_x + 0.6, current_y + player_height/2 - BLOCK_SPACING/2, player_name,
            ha='center', va='center', fontsize=14, fontweight='bold',
            color='black')

    current_y += player_height

# 绘制流向（从指标到球员）- 真正的桑基图
# 权重带在两端都按比例分布在色块范围内

# 首先为每个球员计算累积高度字典
player_cumulative_heights = {p_idx: 0 for p_idx in range(len(df))}

for m_idx, metric in enumerate(metrics):
    # 计算该指标所有连接的总值，用于分配色块高度
    metric_total = df[metric].sum()

    # 当前指标色块的起始y位置
    metric_block_start_y = metric_y_positions[m_idx]
    metric_block_height = metric_height - BLOCK_SPACING

    # 累积高度，用于在指标色块内分配权重带的起点
    metric_cumulative_height = 0

    for p_idx, (_, player_row) in enumerate(df.iterrows()):
        value = player_row[metric]

        if value > 0.1:  # 显示所有有值的连接
            # 计算该连接在指标色块中占据的高度比例
            if metric_total > 0:
                height_ratio_metric = value / metric_total
            else:
                height_ratio_metric = 0

            # 该连接在指标色块中的高度
            flow_height_metric = height_ratio_metric * metric_block_height

            # 该连接在指标色块中的起始和结束y位置
            metric_flow_start_y = metric_block_start_y + metric_cumulative_height
            metric_flow_end_y = metric_flow_start_y + flow_height_metric

            # 更新指标侧累积高度
            metric_cumulative_height += flow_height_metric

            # 计算该连接在球员色块中占据的高度
            # 需要计算该球员所有指标的总值
            player_total = df.iloc[p_idx][metrics].sum()

            if player_total > 0:
                height_ratio_player = value / player_total
            else:
                height_ratio_player = 0

            # 球员色块的起始y位置和高度
            player_block_start_y = player_y_positions[p_idx]
            player_block_height = player_height - BLOCK_SPACING

            # 该连接在球员色块中的高度
            flow_height_player = height_ratio_player * player_block_height

            # 该连接在球员色块中的起始和结束y位置
            player_flow_start_y = player_block_start_y + player_cumulative_heights[p_idx]
            player_flow_end_y = player_flow_start_y + flow_height_player

            # 更新球员侧累积高度
            player_cumulative_heights[p_idx] += flow_height_player

            # 绘制填充的流向区域（使用多边形）
            from matplotlib.path import Path
            import matplotlib.patches as patches

            # 创建流向的四个顶点（形成一个扭曲的四边形）
            x_start = layer1_x + FLOW_START_OFFSET
            x_end = layer2_x + FLOW_END_OFFSET
            x_mid1 = layer1_x + 3.5
            x_mid2 = layer2_x - 2.5

            # 使用贝塞尔曲线创建上下两条边界
            # 上边界
            verts_top = [
                (x_start, metric_flow_start_y),
                (x_mid1, metric_flow_start_y),
                (x_mid2, player_flow_start_y),
                (x_end, player_flow_start_y),
            ]

            # 下边界（反向）
            verts_bottom = [
                (x_end, player_flow_end_y),
                (x_mid2, player_flow_end_y),
                (x_mid1, metric_flow_end_y),
                (x_start, metric_flow_end_y),
            ]

            # 合并顶点形成闭合路径
            verts = verts_top + verts_bottom + [verts_top[0]]

            codes = [Path.MOVETO] + [Path.CURVE4] * 3 + \
                    [Path.LINETO] + [Path.CURVE4] * 3 + \
                    [Path.CLOSEPOLY]

            path = Path(verts, codes)

            alpha = FLOW_ALPHA

            patch = patches.PathPatch(
                path,
                facecolor=metric_colors[m_idx],
                edgecolor='none',
                alpha=alpha
            )
            ax.add_patch(patch)

# 添加标题
ax.text(5, 11.5, 'Lakers Players Impact Flow',
        ha='center', va='center', fontsize=18, fontweight='bold')

# 添加层标签
ax.text(1.1, 0.3, 'Impact Categories (8)', ha='center', fontsize=12, fontweight='bold')
ax.text(8.9, 0.3, 'Players (10)', ha='center', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('Components/lakers_sankey.png', dpi=300, bbox_inches='tight')
plt.savefig('Components/lakers_sankey.pdf', bbox_inches='tight')
plt.savefig('Components/lakers_sankey.svg', bbox_inches='tight')
plt.show()

print("桑基图已生成并保存！")
print(f"球员数量: {len(all_players)}")
print(f"指标数量: {len(metric_labels)}")
print(f"球员: {all_players}")
print(f"指标: {metric_labels}")
