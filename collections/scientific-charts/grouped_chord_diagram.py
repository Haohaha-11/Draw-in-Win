"""
分组和弦图（Grouped Chord Diagram）
使用 pycirclize 库绘制，风格类似 R 语言的 circlize 包
基于中心性排序和Spearman相关性矩阵
"""

# 安装所需库（首次运行时取消注释）
# pip install pycirclize
# pip install pandas numpy matplotlib

import pandas as pd
import numpy as np
from pycirclize import Circos
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
COLLECTIONS_DIR = SCRIPT_DIR.parent

# 设置Times New Roman字体
font_path = fm.findfont('DejaVu Serif')
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = font_prop.get_name()
fm.fontManager.addfont(font_path)

# 1. 读取中心性数据并排序
centralities = {}
sdg_names = {}
with open(COLLECTIONS_DIR / 'sdg-systems' / 'network-and-prior' / 'model1' / 'centralities.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    # 使用正则表达式提取SDG编号和中心度值
    # 格式: 第 X名: SDG  Y - 名称 | 中心度: Z
    pattern = r'第\s*\d+名:\s*SDG\s+(\d+)\s*-\s*([^|]+)\s*\|\s*中心度:\s*([-\d.]+)'
    matches = re.findall(pattern, content)
    for match in matches:
        sdg_num = int(match[0])
        sdg_name = match[1].strip()
        centrality = float(match[2])
        centralities[sdg_num] = centrality
        sdg_names[sdg_num] = sdg_name

# 按中心度降序排序
sorted_elements = sorted(centralities.items(), key=lambda x: x[1], reverse=True)
print("中心性排序（从高到低）：")
for sdg_num, cent in sorted_elements:
    print(f"  SDG{sdg_num:2d} ({sdg_names[sdg_num]}): {cent:.6f}")

# 2. 根据排序结果分组（前5名一组，后面4个4个一组）
groups = {}
all_nodes = []
node_to_group = {}

# Group A: 前5名（中心性最高）
group_a_elements = [elem[0] for elem in sorted_elements[:5]]
groups['Group A'] = [f'SDG{i}' for i in group_a_elements]

# Group B: 第6-9名
group_b_elements = [elem[0] for elem in sorted_elements[5:9]]
groups['Group B'] = [f'SDG{i}' for i in group_b_elements]

# Group C: 第10-13名
group_c_elements = [elem[0] for elem in sorted_elements[9:13]]
groups['Group C'] = [f'SDG{i}' for i in group_c_elements]

# Group D: 第14-17名
group_d_elements = [elem[0] for elem in sorted_elements[13:17]]
groups['Group D'] = [f'SDG{i}' for i in group_d_elements]

print("\n分组结果：")
for group_name, nodes in groups.items():
    print(f"{group_name}: {nodes}")

# 创建所有节点列表和映射
for group_name, nodes in groups.items():
    all_nodes.extend(nodes)
    for node in nodes:
        node_to_group[node] = group_name

# 3. 读取Spearman相关性矩阵
df_spearman = pd.read_csv(
    COLLECTIONS_DIR / 'sdg-systems' / 'data' / 'Spearman_2.csv',
    index_col=0,
)

# 将对角线元素设为1
np.fill_diagonal(df_spearman.values, 1.0)

# 保留原始相关性值（不取绝对值，不过滤）
df_matrix = df_spearman.copy()

# 重新索引以匹配节点顺序
# Spearman矩阵索引0-16对应SDG1-SDG17（索引i对应SDG(i+1)）
# 所以SDG编号需要减1得到矩阵索引
node_indices = [int(node.replace('SDG', '')) - 1 for node in all_nodes]
df_matrix = df_matrix.iloc[node_indices, node_indices]
df_matrix.index = all_nodes
df_matrix.columns = all_nodes

print("\n相关性矩阵预览（保留原始值）：")
print(df_matrix.head())
print(f"\n矩阵形状: {df_matrix.shape}")
print(f"相关性范围: [{df_matrix.min().min():.4f}, {df_matrix.max().max():.4f}]")

# 4. 准备和弦图数据
# 将邻接矩阵转换为边列表格式（保留所有显著连接）
edges = []
for i, source in enumerate(all_nodes):
    for j, target in enumerate(all_nodes):
        if i < j:  # 只取上三角（避免重复）
            correlation = df_matrix.iloc[i, j]
            # 只显示相关性绝对值大于阈值的连接
            if abs(correlation) > 0.3 and correlation != 1.0:
                edges.append({
                    'source': source,
                    'target': target,
                    'value': abs(correlation),  # 用于确定连线宽度
                    'correlation': correlation  # 保留原始相关性值用于着色
                })

df_edges = pd.DataFrame(edges)
print(f"\n显著连接数量: {len(df_edges)}")
print(f"正相关数量: {len(df_edges[df_edges['correlation'] > 0])}")
print(f"负相关数量: {len(df_edges[df_edges['correlation'] < 0])}")

# 5. 计算每个节点的总权重（用于扇形大小）
node_values = {}
for node in all_nodes:
    # 计算该节点的所有连接权重之和（使用绝对值）
    outgoing = df_matrix.loc[node, :].abs().sum()
    incoming = df_matrix.loc[:, node].abs().sum()
    node_values[node] = max(0.1, (outgoing + incoming) / 2)  # 避免重复计数，最小值为0.1

# 标准化节点值到0-1范围
max_value = max(node_values.values())
node_values_normalized = {k: v / max_value for k, v in node_values.items()}

# 6. 准备 Circos 数据结构（按组组织，使用标准化的值）
# 为了让4个组明显分开，我们需要按组的顺序组织sectors
sectors = {}
for group_name in ['Group A', 'Group B', 'Group C', 'Group D']:
    nodes = groups[group_name]
    for node in nodes:
        sectors[node] = node_values_normalized[node]

# 7. 定义颜色方案（柔和配色）
group_colors = {
    'Group A': '#FFA07A',  # 浅橙色（Light Salmon）
    'Group B': '#FDAE61',  # 橙黄色
    'Group C': '#ABD9E9',  # 浅蓝色
    'Group D': '#87CEEB'   # 天蓝色（Sky Blue）
}

# 为每个节点分配颜色
node_colors = {}
for node in all_nodes:
    node_colors[node] = group_colors[node_to_group[node]]

# 8. 定义相关性到颜色的映射函数
import matplotlib.colors as mcolors
import matplotlib.cm as cm

def correlation_to_color(correlation):
    """
    将相关性系数映射到颜色（柔和色调）
    负相关: 浅蓝色系
    正相关: 浅橙色系
    """
    if correlation < 0:
        # 负相关：从很浅的蓝到中等蓝
        # -1.0 -> 中蓝, 0 -> 很浅蓝
        intensity = abs(correlation)
        # 使用浅蓝色渐变
        r = 0.7 - 0.3 * intensity  # 0.7 -> 0.4
        g = 0.85 - 0.25 * intensity  # 0.85 -> 0.6
        b = 1.0  # 保持蓝色通道满
        return mcolors.to_hex((r, g, b))
    else:
        # 正相关：从很浅的橙到浅橙
        # 0 -> 很浅橙, 1.0 -> 浅橙
        intensity = correlation
        # 使用浅橙色渐变
        r = 1.0
        g = 0.85 - 0.2 * intensity  # 0.85 -> 0.65
        b = 0.7 - 0.3 * intensity  # 0.7 -> 0.4
        return mcolors.to_hex((r, g, b))

# 9. 创建 Circos 图（增加组间间隔）
circos = Circos(sectors, space=3)

# 10. 为每个扇形添加轨道和标签
for sector in circos.sectors:
    # 获取当前扇形
    track = sector.add_track((95, 100))
    track.axis(fc=node_colors[sector.name], ec="black", lw=0.5)

    # 添加节点标签
    track.text(sector.name, size=10, color="black", fontweight='bold')

    # 添加刻度（标准化到0-1）
    track.xticks_by_interval(
        interval=0.2,  # 每0.2一个刻度
        label_size=7,
        label_orientation="vertical",
        label_formatter=lambda v: f"{v:.1f}"
    )

# 11. 为每个节点分配连接的起始位置（累积分配）
node_link_positions = {node: 0 for node in all_nodes}

# 11. 添加连接线（Ribbons）- 颜色根据相关性系数确定
for _, row in df_edges.iterrows():
    source = row['source']
    target = row['target']
    value = row['value']
    correlation = row['correlation']

    # 标准化value到对应的扇形范围
    normalized_value = value / max_value

    # 获取source和target的当前位置
    source_start = node_link_positions[source]
    target_start = node_link_positions[target]

    # 更新位置（累积）
    node_link_positions[source] += normalized_value
    node_link_positions[target] += normalized_value

    # 根据相关性系数确定颜色
    color = correlation_to_color(correlation)

    # 添加连接
    circos.link(
        (source, source_start, source_start + normalized_value),
        (target, target_start, target_start + normalized_value),
        color=color,
        alpha=0.7,
        lw=0.5
    )

# 12. 添加组标签（在外圈）
# 计算每个组的起始和结束位置
group_positions = {}
current_pos = 0
for group_name, nodes in groups.items():
    start_pos = current_pos
    group_size = sum([sectors[node] for node in nodes])
    end_pos = current_pos + group_size
    group_positions[group_name] = (start_pos, end_pos, (start_pos + end_pos) / 2)
    current_pos = end_pos

# 13. 绘制图形
fig = circos.plotfig(figsize=(14, 14))

# 添加标题
plt.title("Grouped Chord Diagram - Spearman Correlations",
          fontsize=18, fontweight='bold', pad=20, fontproperties=font_prop)

# 设置白色背景
fig.patch.set_facecolor('white')

# 保存主图为SVG格式
output_file_svg = SCRIPT_DIR / "grouped_chord_diagram.svg"
plt.savefig(output_file_svg, format='svg', bbox_inches='tight', facecolor='white')
print(f"\n主图（SVG）已保存至: {output_file_svg}")

# 同时保存PNG格式（高分辨率）
output_file_png = SCRIPT_DIR / "grouped_chord_diagram.png"
plt.savefig(output_file_png, dpi=300, bbox_inches='tight', facecolor='white')
print(f"主图（PNG）已保存至: {output_file_png}")

# 显示图形
plt.show()
plt.close()

# 14. 创建并保存单独的图例
fig_legend, ax_legend = plt.subplots(figsize=(6, 4))
ax_legend.axis('off')

# 添加颜色图例
from matplotlib.patches import Rectangle
legend_elements = [
    Rectangle((0, 0), 1, 1, fc='#27a5df', alpha=0.7, label='Strong Negative (-1.0)', edgecolor='black', linewidth=0.5),
    Rectangle((0, 0), 1, 1, fc='#7dc5e8', alpha=0.7, label='Weak Negative (-0.5)', edgecolor='black', linewidth=0.5),
    Rectangle((0, 0), 1, 1, fc='#f9b896', alpha=0.7, label='Weak Positive (0.5)', edgecolor='black', linewidth=0.5),
    Rectangle((0, 0), 1, 1, fc='#f46e44', alpha=0.7, label='Strong Positive (1.0)', edgecolor='black', linewidth=0.5)
]

legend = ax_legend.legend(handles=legend_elements, loc='center', fontsize=14,
                         title='Correlation Strength', title_fontsize=16,
                         frameon=True, fancybox=False, shadow=False,
                         prop=font_prop)
legend.get_title().set_fontproperties(font_prop)

# 保存图例为SVG
legend_file_svg = SCRIPT_DIR / "chord_diagram_legend.svg"
fig_legend.savefig(legend_file_svg, format='svg', bbox_inches='tight', facecolor='white')
print(f"图例（SVG）已保存至: {legend_file_svg}")

# 同时保存PNG格式
legend_file_png = SCRIPT_DIR / "chord_diagram_legend.png"
fig_legend.savefig(legend_file_png, dpi=300, bbox_inches='tight', facecolor='white')
print(f"图例（PNG）已保存至: {legend_file_png}")

plt.close()

# 15. 保存相关性矩阵到 CSV
df_matrix.to_csv(SCRIPT_DIR / "chord_adjacency_matrix.csv")
print("相关性矩阵已保存至: draw_pics/chord_adjacency_matrix.csv")

# 16. 打印统计信息
print("\n=== 统计信息 ===")
for group_name, nodes in groups.items():
    centrality_values = []
    for node in nodes:
        # 直接使用SDG编号
        sdg_id = int(node.replace('SDG', ''))
        centrality_values.append(centralities[sdg_id])
    avg_centrality = np.mean(centrality_values)
    print(f"{group_name}: {len(nodes)} 个节点 - {nodes}")
    print(f"  平均中心性: {avg_centrality:.6f}")

print(f"\n总节点数: {len(all_nodes)}")
print(f"总显著连接数: {len(df_edges)}")
if len(df_edges) > 0:
    print(f"正相关连接数: {len(df_edges[df_edges['correlation'] > 0])}")
    print(f"负相关连接数: {len(df_edges[df_edges['correlation'] < 0])}")
    print(f"平均相关性: {df_edges['correlation'].mean():.4f}")
    print(f"最强正相关: {df_edges['correlation'].max():.4f}")
    print(f"最强负相关: {df_edges['correlation'].min():.4f}")
