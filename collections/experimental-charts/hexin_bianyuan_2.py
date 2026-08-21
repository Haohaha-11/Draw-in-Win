import math
import random
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.lines import Line2D
from sklearn.preprocessing import MinMaxScaler

# 1. 环境设置
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 2. 生成模拟数据 (Fix: 确保数据生成逻辑稳健)
def generate_mock_data():
    cities = [f"城市_{i}" for i in range(280)]
    # 模拟实际出现的城市名
    known = ["北京市", "上海市", "广州市", "深圳市", "南京市", "成都市", "重庆市", "长沙市", "武汉市", "郑州市"]
    for i, name in enumerate(known):
        cities[i] = name

    # 生成节点
    out_deg = [random.randint(5, 1200) for _ in range(280)]
    in_deg = [random.randint(5, 1200) for _ in range(280)]
    nodes_df = pd.DataFrame({
        'node': cities,
        'out_degree': out_deg,
        'in_degree': in_deg
    })
    nodes_df['total_degree'] = nodes_df['out_degree'] + nodes_df['in_degree']

    # 生成边
    edges_df = pd.DataFrame({
        'origin': [random.choice(cities) for _ in range(846)],
        'destination': [random.choice(cities) for _ in range(846)],
        'counts': [random.randint(15, 100) for _ in range(846)]
    })
    return nodes_df, edges_df

nodes, edges = generate_mock_data()

# 3. 数据处理与分级
# 节点分级 [cite: 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]
quantiles_nodes = nodes['total_degree'].quantile([0.65, 0.9, 0.99])
def classify_node(x):
    if x > quantiles_nodes[0.99]: return '核心层'
    elif x > quantiles_nodes[0.9]: return '次核心层'
    elif x > quantiles_nodes[0.65]: return '中间层'
    else: return '边缘层'
nodes['layer'] = nodes['total_degree'].apply(classify_node)

# 边权分级 [cite: 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67]
quantiles_edges = edges['counts'].quantile([0.4, 0.65, 0.9, 0.99])
def classify_edge(x):
    if x > quantiles_edges[0.99]: return 10
    elif x > quantiles_edges[0.9]: return 6
    elif x > quantiles_edges[0.65]: return 3
    elif x > quantiles_edges[0.4]: return 1.5
    else: return 0.5
edges['weight'] = edges['counts'].apply(classify_edge)

# 4. 网络图配置 [cite: 83, 89, 94, 99, 104]
layer_order = ["核心层", "次核心层", "中间层", "边缘层"]
layer_colors = {"核心层": "#d35052", "次核心层": "#b9bf5f", "中间层": "#57a66e", "边缘层": "#3c8bb3"}
layer_zorder = {"核心层": 3, "次核心层": 2, "中间层": 1, "边缘层": 0}
layer_radii = {"核心层": 0.2, "次核心层": 0.6, "中间层": 1.0, "边缘层": 1.4}

# 5. 构建 NetworkX 图对象 [cite: 109, 112, 121]
G = nx.Graph()
for _, row in nodes.iterrows():
    G.add_node(row["node"], layer=row["layer"], color=layer_colors[row["layer"]], total_degree=row['total_degree'])

for _, row in edges.iterrows():
    if row["origin"] in G.nodes and row["destination"] in G.nodes:
        G.add_edge(row["origin"], row["destination"], weight=row["weight"], origin=row["origin"])

# 6. 计算环形布局坐标 [cite: 129, 131, 134, 137, 139]
pos = {}
for layer in layer_order:
    nodes_in_layer = [n for n in G.nodes if G.nodes[n]["layer"] == layer]
    n_count = len(nodes_in_layer)
    if n_count == 0: continue
    radius = layer_radii[layer]
    for i, node in enumerate(nodes_in_layer):
        angle = 2 * math.pi * i / n_count
        pos[node] = (radius * math.cos(angle), radius * math.sin(angle))

# 7. 绘图 [cite: 241, 246, 256, 280, 288, 308]
plt.figure(figsize=(12, 12))
ax = plt.gca()
ax.set_title("核心-边缘网络", fontsize=20)

# 绘制弧形边 [cite: 260, 262, 263, 264]
for u, v, data in G.edges(data=True):
    p1, p2 = pos[u], pos[v]
    edge_color = G.nodes[data["origin"]]["color"]
    patch = FancyArrowPatch(p1, p2, connectionstyle="arc3,rad=0.3",
                            arrowstyle="-", lw=data["weight"],
                            color=edge_color, alpha=0.4,
                            zorder=layer_zorder[G.nodes[data["origin"]]["layer"]])
    ax.add_patch(patch)

# 绘制节点 [cite: 271, 274, 283, 286]
all_deg = [G.nodes[n]['total_degree'] for n in G.nodes()]
scaler = MinMaxScaler(feature_range=(10, 800))  # 调小节点大小范围
sizes = scaler.fit_transform([[d] for d in all_deg]).flatten()
colors = [G.nodes[n]["color"] for n in G.nodes()]

nodes_draw = nx.draw_networkx_nodes(G, pos, node_size=sizes, node_color=colors, alpha=1)
nodes_draw.set_zorder(100)

# 绘制标签 (展示逻辑：核心/次核心全显，其余随机) [cite: 290, 294, 296, 304]
show_labels = {}
for layer in layer_order:
    ly_nodes = [n for n in G.nodes if G.nodes[n]["layer"] == layer]
    selected = ly_nodes if layer in ["核心层", "次核心层"] else random.sample(ly_nodes, min(8, len(ly_nodes)))
    for n in selected: show_labels[n] = n

txts = nx.draw_networkx_labels(G, pos, labels=show_labels, font_size=9)
for t in txts.values(): t.set_zorder(200)

# 绘制图例 [cite: 320, 325, 327]
legend_el = [Line2D([0], [0], marker='o', color='w', label=k, markerfacecolor=v, markersize=12)
             for k, v in layer_colors.items()]
ax.legend(handles=legend_el, loc='lower center', ncol=4, bbox_to_anchor=(0.5, -0.05), frameon=False)

plt.axis("off")
plt.show()