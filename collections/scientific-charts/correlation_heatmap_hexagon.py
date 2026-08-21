import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from matplotlib.collections import PatchCollection
from scipy import stats

# 设置随机种子
np.random.seed(42)

# 生成随机数据
n_vars = 24
n_samples = 100
data = np.random.randn(n_samples, n_vars)

# 添加相关性
for i in range(n_vars):
    if i > 0:
        data[:, i] += 0.4 * data[:, i-1]

# 计算相关系数和p值
corr_matrix = np.corrcoef(data.T)
p_values = np.zeros((n_vars, n_vars))

for i in range(n_vars):
    for j in range(n_vars):
        if i != j:
            _, p_values[i, j] = stats.pearsonr(data[:, i], data[:, j])

# 创建标签
labels = ['A1', 'A2', 'A3', 'A4', 'A5',
          'B1', 'B2', 'B3',
          'C1', 'C2', 'C3', 'C4', 'C5',
          'D1', 'D2',
          'E1', 'E2',
          'F1', 'F2',
          'G1', 'G2', 'G3', 'G4'][:n_vars]

# 显著性标记函数
def get_significance_marker(p_value):
    if p_value < 0.001:
        return '***'
    elif p_value < 0.01:
        return '**'
    elif p_value < 0.05:
        return '*'
    else:
        return ''

# 创建图形
fig, ax = plt.subplots(figsize=(18, 16))
ax.set_aspect('equal')

# 颜色映射
from matplotlib.colors import LinearSegmentedColormap
colors = ['#d73027', '#f46d43', '#fdae61', '#fee090', '#ffffff',
          '#e0f3f8', '#abd9e9', '#74add1', '#4575b4']
n_bins = 100
cmap = LinearSegmentedColormap.from_list('custom_RdBu', colors, N=n_bins)

# 六边形参数
hex_size = 0.45
x_offset = 0.87  # 六边形水平间距
y_offset = 1.0   # 六边形垂直间距

# 绘制六边形
patches = []
colors_list = []

for i in range(n_vars):
    for j in range(n_vars):
        # 计算六边形中心位置
        x = j * x_offset
        y = (n_vars - 1 - i) * y_offset

        # 创建六边形
        hexagon = RegularPolygon((x, y), numVertices=6, radius=hex_size,
                                orientation=0,
                                edgecolor='white', linewidth=1.5)
        patches.append(hexagon)

        # 根据相关系数设置颜色
        corr_val = corr_matrix[i, j]
        colors_list.append(corr_val)

# 添加六边形集合
pc = PatchCollection(patches, cmap=cmap, edgecolors='white', linewidths=1.5)
pc.set_array(np.array(colors_list))
pc.set_clim(-1, 1)
ax.add_collection(pc)

# 添加文本（相关系数和显著性）
for i in range(n_vars):
    for j in range(n_vars):
        x = j * x_offset
        y = (n_vars - 1 - i) * y_offset

        corr_val = corr_matrix[i, j]
        sig_marker = get_significance_marker(p_values[i, j])

        # 对角线显示1.00
        if i == j:
            text = '1.00'
        else:
            text = f'{corr_val:.2f}'

        # 文字颜色
        text_color = 'white' if abs(corr_val) > 0.5 else 'black'

        # 添加相关系数
        ax.text(x, y + 0.08, text, ha='center', va='center',
               color=text_color, fontsize=7, weight='bold')

        # 添加显著性标记
        if sig_marker and i != j:
            ax.text(x, y - 0.15, sig_marker, ha='center', va='center',
                   color=text_color, fontsize=6, weight='bold')

# 添加行列标签
for i, label in enumerate(labels):
    # 左侧标签
    y = (n_vars - 1 - i) * y_offset
    ax.text(-1.2, y, label, ha='right', va='center', fontsize=10, weight='bold')

    # 底部标签
    x = i * x_offset
    ax.text(x, -1.2, label, ha='center', va='top', fontsize=10, weight='bold', rotation=45)

# 设置坐标轴范围
ax.set_xlim(-2, n_vars * x_offset)
ax.set_ylim(-2, n_vars * y_offset)
ax.axis('off')

# 添加颜色条
cbar = plt.colorbar(pc, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label('Correlation Coefficient', fontsize=12)

# 添加标题
plt.title('Correlation Matrix with Significance Levels\n(* p<0.05, ** p<0.01, *** p<0.001)',
         fontsize=14, pad=20, weight='bold')

# 保存
plt.tight_layout()
plt.savefig('correlation_heatmap_hexagon.png', dpi=300, bbox_inches='tight', facecolor='white')
print("六边形热图已保存为 correlation_heatmap_hexagon.png")

plt.show()
