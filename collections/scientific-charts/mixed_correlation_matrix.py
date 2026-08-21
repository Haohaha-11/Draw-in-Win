"""
混合相关矩阵热图
- 下三角：热图方块 + 相关系数
- 上三角：六边形，大小与相关性强度成正比
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.font_manager as fm
import os
from pathlib import Path

# ============================================================================
# 设置字体
# ============================================================================
font_path = fm.findfont('DejaVu Serif')
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
fm.fontManager.addfont(font_path)

# ============================================================================
# 1. 读取数据
# ============================================================================
csv_path = Path(__file__).resolve().parents[1] / 'sdg-systems' / 'data' / 'Spearman_2.csv'
data_df = pd.read_csv(csv_path, index_col=0)

# 转换为numpy数组
corr_matrix = data_df.values
n_vars = corr_matrix.shape[0]

# 将对角线元素设置为1（自相关）
np.fill_diagonal(corr_matrix, 1.0)

print(f"数据维度: {n_vars} x {n_vars}")
print(f"相关系数范围: [{corr_matrix.min():.3f}, {corr_matrix.max():.3f}]")

# ============================================================================
# 2. 创建图形
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 12))

# 更浅的莫兰迪色系配色方案（两端颜色更浅）
colors_muted = [
    '#abd9e9',  # 浅蓝（原来是#74add1）
    '#d1e5f0',  # 极浅蓝
    '#f7f7f7',  # 浅灰白
    '#ffffff',  # 纯白中点
    '#fee090',  # 沙色
    '#fbb4ae',  # 粉红
    '#f46d43'   # 浅红（原来是#d73027深红）
]
cmap_muted = LinearSegmentedColormap.from_list('muted_coolwarm', colors_muted, N=256)

# ============================================================================
# 3. 绘制下三角（包括对角线）- 热图方块
# ============================================================================
for i in range(n_vars):
    for j in range(n_vars):
        if i >= j:  # 下三角和对角线
            # 绘制方块
            color = cmap_muted((corr_matrix[i, j] + 1) / 2)  # 映射到[0,1]
            rect = plt.Rectangle((j-0.5, i-0.5), 1, 1,
                                facecolor=color,
                                edgecolor='white',
                                linewidth=2)
            ax.add_patch(rect)

            # 添加相关系数文本
            corr_val = corr_matrix[i, j]

            # 文字颜色
            text_color = 'white' if abs(corr_val) > 0.5 else 'black'

            # 只显示相关系数，不显示星号
            ax.text(j, i, f'{corr_val:.2f}',
                   ha='center', va='center',
                   color=text_color, fontsize=9, weight='bold',
                   fontproperties=font_prop)

# ============================================================================
# 4. 绘制上三角 - 六边形（大小与相关性强度成正比）
# ============================================================================
hexagons = []
hex_colors = []

for i in range(n_vars):
    for j in range(n_vars):
        if i < j:  # 上三角
            corr_val = corr_matrix[i, j]
            abs_corr = abs(corr_val)

            # 六边形大小与相关性强度成正比
            hex_size = 0.35 * abs_corr + 0.1

            # 创建六边形
            hexagon = RegularPolygon((j, i),
                                    numVertices=6,
                                    radius=hex_size,
                                    orientation=0,
                                    edgecolor='white',
                                    linewidth=2)
            hexagons.append(hexagon)
            hex_colors.append(corr_val)

# 添加六边形集合
pc = PatchCollection(hexagons, cmap=cmap_muted, edgecolors='white', linewidths=2)
pc.set_array(np.array(hex_colors))
pc.set_clim(-1, 1)
ax.add_collection(pc)

# ============================================================================
# 5. 设置坐标轴和标签
# ============================================================================
# 使用SDG标签
var_labels = [f'SDG{i+1}' for i in range(n_vars)]

ax.set_xlim(-0.5, n_vars - 0.5)
ax.set_ylim(n_vars - 0.5, -0.5)  # 反转y轴

ax.set_xticks(range(n_vars))
ax.set_yticks(range(n_vars))
ax.set_xticklabels(var_labels, rotation=45, ha='right', fontsize=11,
                   weight='bold', fontproperties=font_prop)
ax.set_yticklabels(var_labels, fontsize=11, weight='bold',
                   fontproperties=font_prop)

# 移除刻度线
ax.tick_params(left=False, bottom=False)

# 设置纵横比
ax.set_aspect('equal')

# ============================================================================
# 6. 添加颜色条
# ============================================================================
sm = plt.cm.ScalarMappable(cmap=cmap_muted,
                           norm=plt.Normalize(vmin=-1, vmax=1))
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label('Correlation Coefficient', fontsize=12, weight='bold',
               fontproperties=font_prop)
cbar.ax.tick_params(labelsize=10)

# 移除边框
for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()

# ============================================================================
# 7. 保存图片（PNG和SVG格式）
# ============================================================================
# 保存PNG格式（高分辨率位图）
plt.savefig('mixed_correlation_matrix.png', dpi=300, bbox_inches='tight',
            facecolor='white')
print("[OK] PNG图片已保存: mixed_correlation_matrix.png")

# 保存SVG格式（矢量图，可无损缩放）
plt.savefig('mixed_correlation_matrix.svg', format='svg', bbox_inches='tight',
            facecolor='white')
print("[OK] SVG图片已保存: mixed_correlation_matrix.svg")

# ============================================================================
# 8. 输出统计信息
# ============================================================================
print("\n=== 相关性分析摘要 ===")
print(f"变量数量: {n_vars}")

# 只看上三角（不包括对角线）
upper_tri_indices = np.triu_indices(n_vars, k=1)
upper_tri_corr = corr_matrix[upper_tri_indices]

print(f"相关系数范围: [{upper_tri_corr.min():.3f}, {upper_tri_corr.max():.3f}]")
print(f"平均|相关系数|: {np.abs(upper_tri_corr).mean():.3f}")
print(f"强相关对数 (|r|>0.5): {(np.abs(upper_tri_corr) > 0.5).sum()}")
print(f"强相关对数 (|r|>0.7): {(np.abs(upper_tri_corr) > 0.7).sum()}")
print(f"强相关对数 (|r|>0.9): {(np.abs(upper_tri_corr) > 0.9).sum()}")

plt.show()
