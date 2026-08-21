import numpy as np
import scipy.linalg as la
import pandas as pd
import sys
import os
from pathlib import Path
from map.sdg_mapping import sdg_mapping

# 使用脚本位置定位仓库内的CSV文件
csv_path = Path(__file__).resolve().parents[2] / 'data' / 'Spearman_1.csv'
data = pd.read_csv(csv_path, header=None)
print(data.shape)

# 将数据转换为加权邻接矩阵（omega）
omega = data.values

# 输出加权邻接矩阵
print(omega)

# 计算度中心性
def degree_centrality(omega):
    return np.sum(omega, axis=1)  # 计算每个节点的度（加权）

# 计算特征向量中心性
def eigenvector_centrality(omega):
    # 计算权重矩阵的最大特征值和特征向量
    eigvals, eigvecs = la.eig(omega)
    # 选择最大的特征值对应的特征向量
    max_eigvec = np.real(eigvecs[:, np.argmax(np.real(eigvals))])
    # 对特征向量进行归一化
    return max_eigvec / np.linalg.norm(max_eigvec)

# 计算加权中心性
def combined_centrality(omega, alpha=0.5, beta=0.5):
    # 计算度中心性
    degree_centralities = degree_centrality(omega)

    # 计算特征向量中心性
    eigenvector_centralities = eigenvector_centrality(omega)

    # 计算加权中心性
    combined_centralities = alpha * degree_centralities + beta * eigenvector_centralities
    return combined_centralities

# 输出计算结果
combined_centralities = combined_centrality(omega, alpha=0.028235, beta=0.971765)
print("------------------------------------------------------")
print("各SDG的加权中心度：")
for i in range(len(combined_centralities)):
    print(f"SDG {i+1} - {sdg_mapping[i+1]}: {combined_centralities[i]:.6f}")

print("\n" + "="*60)
print("按中心度排序（从高到低）：")
print("="*60)

# 创建SDG编号和中心度的配对列表
sdg_centrality_pairs = [(i+1, combined_centralities[i]) for i in range(len(combined_centralities))]

# 按中心度降序排序
sorted_sdgs = sorted(sdg_centrality_pairs, key=lambda x: x[1], reverse=True)

# 输出排序结果
for rank, (sdg_num, centrality) in enumerate(sorted_sdgs, 1):
    print(f"第{rank:2d}名: SDG {sdg_num:2d} - {sdg_mapping[sdg_num]:50s} | 中心度: {centrality:8.6f}")

print("\n" + "="*60)
