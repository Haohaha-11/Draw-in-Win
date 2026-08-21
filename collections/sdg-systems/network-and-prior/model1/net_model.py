import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# 读取 CSV 文件
data_path = Path(__file__).resolve().parents[2] / 'data' / 'Spearman_1.csv'
data = pd.read_csv(data_path, header=None)

# 显示数据的前几行，检查数据是否正确加载
print(data.head())


# 1. 创建图并添加 17 个 SDG 节点
G = nx.Graph()
nodes = range(1, 18)
G.add_nodes_from(nodes)

# 2. 手动添加边和权重 (权重 rho 取值范围 [-1, 1])
# 格式: (节点i, 节点j, 权重)
# edges_with_weights = [
#     (1, 2, 0.85),   # 示例：SDG1 和 SDG2 强正相关
#     (1, 13, -0.4),  # 示例：SDG1 和 SDG13 负相关
#     (5, 7, 0.6),    # 你可以在这里继续添加边...
#     (3, 7, 0.9),
#     (3, 8, 0.1)
# ]

# 查看数据的形状，确认是否为 17x17 的矩阵
print(data.shape)

# 构建加权边列表
edges_with_weights = []

# 获取目标数目（应该是17）
num_sdgs = len(data)

# 遍历矩阵的每一对目标，生成加权边
for i in range(num_sdgs):
    for j in range(i+1, num_sdgs):  # 避免重复计算
        weight = data.iloc[i, j]  # 获取相关系数作为边的权重
        edges_with_weights.append((i+1, j+1, weight))  # SDG编号从1到17，所以索引要加1

# 输出加权边
for edge in edges_with_weights:
    print(f"({edge[0]}, {edge[1]}, {edge[2]})")  # 格式：节点1, 节点2, 权重

for u, v, w in edges_with_weights:
    G.add_edge(u, v, weight=w)

# 3. 可视化
plt.figure(figsize=(8, 8))

# 使用圆形布局，适合展示 17 个目标的结构
pos = nx.circular_layout(G)

# 分别提取正负相关的边，用于涂色
edges = G.edges(data=True)
pos_edges = [(u, v) for u, v, d in edges if d['weight'] > 0]
neg_edges = [(u, v) for u, v, d in edges if d['weight'] < 0]

# 画节点
nx.draw_networkx_nodes(G, pos, node_size=600, node_color='skyblue')
nx.draw_networkx_labels(G, pos, font_size=10)

# 画边：正相关用蓝色，负相关用红色
# --- 核心逻辑：根据权重绝对值设置粗细 ---
edges = G.edges(data=True)
if edges:
    # 获取权重绝对值并放大，作为线条宽度
    widths = [abs(d['weight']) * 10 for u, v, d in edges]

    # 获取颜色：正相关蓝色，负相关红色
    colors = ['blue' if d['weight'] > 0 else 'red' for u, v, d in edges]

    nx.draw_networkx_edges(G, pos, width=widths, edge_color=colors, alpha=0.5)
plt.title("SDG Network (Spearman Correlation Weights)")
plt.axis('off')
plt.show()
