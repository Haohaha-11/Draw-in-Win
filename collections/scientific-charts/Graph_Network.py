import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# 1. 生成或加载模拟数据 (以17个SDG指标为例)
np.random.seed(42)
cols = [f'Goal{i}' for i in range(1, 18)]
data = pd.DataFrame(np.random.rand(100, 17), columns=cols)

# 2. 计算相关性矩阵 (通常使用 Spearman 或 Pearson)
corr_matrix = data.corr(method='spearman')

# 3. 构建图对象
G = nx.Graph()

# 添加节点
G.add_nodes_from(cols)

# 设定阈值，只展示显著的相关性连线
threshold = 0.3

for i in range(len(corr_matrix.columns)):
    for j in range(i + 1, len(corr_matrix.columns)):
        val = corr_matrix.iloc[i, j]
        if abs(val) > threshold:
            # 添加边，并存储相关性作为权重
            G.add_edge(corr_matrix.columns[i], corr_matrix.columns[j], weight=val)

# 4. 绘图设置
plt.figure(figsize=(10, 8), dpi=300)
# 使用 Spring Layout 布局，使节点分布更均匀美观
pos = nx.spring_layout(G, k=0.5, seed=42)

# 分别提取正相关和负相关的边
edges_pos = [(u, v) for u, v, d in G.edges(data=True) if d['weight'] > 0]
edges_neg = [(u, v) for u, v, d in G.edges(data=True) if d['weight'] < 0]

# 5. 绘制组件
# 绘制节点
nx.draw_networkx_nodes(G, pos, node_size=600, node_color='white', edgecolors='gray', alpha=0.8)

# 绘制正相关边（红色，宽度随权重变化）
weights_pos = [G[u][v]['weight'] * 3 for u, v in edges_pos]
nx.draw_networkx_edges(G, pos, edgelist=edges_pos, width=weights_pos, edge_color='salmon', alpha=0.6)

# 绘制负相关边（蓝色，虚线）
weights_neg = [abs(G[u][v]['weight']) * 3 for u, v in edges_neg]
nx.draw_networkx_edges(G, pos, edgelist=edges_neg, width=weights_neg, edge_color='skyblue', alpha=0.6, style='dashed')

# 绘制标签
nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')

plt.title("Correlation Network of SDGs", fontsize=15)
plt.axis('off') # 隐藏轴线
plt.show()