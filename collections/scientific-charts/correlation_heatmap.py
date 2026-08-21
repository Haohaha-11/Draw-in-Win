import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 设置随机种子以便复现
np.random.seed(42)

# 生成随机数据矩阵 (假设有24个变量，每个变量100个观测值)
n_vars = 24
n_samples = 100

# 生成相关的随机数据
data = np.random.randn(n_samples, n_vars)

# 添加一些相关性
for i in range(n_vars):
    if i > 0:
        data[:, i] += 0.3 * data[:, i-1]  # 与前一个变量相关

# 计算相关系数矩阵和p值
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
          'G1', 'G2', 'G3', 'G4']

# 如果变量数不够，补齐标签
if len(labels) < n_vars:
    labels.extend([f'V{i}' for i in range(len(labels), n_vars)])

# 创建显著性标记
def get_significance_marker(p_value):
    """根据p值返回显著性标记"""
    if p_value < 0.001:
        return '***'
    elif p_value < 0.01:
        return '**'
    elif p_value < 0.05:
        return '*'
    else:
        return ''

# 创建图形
fig, ax = plt.subplots(figsize=(16, 14))

# 使用seaborn绘制热图
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)  # 只显示下三角
sns.heatmap(corr_matrix,
            mask=mask,
            cmap='RdBu_r',  # 红蓝配色
            center=0,
            vmin=-1,
            vmax=1,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": 0.8, "label": "Correlation"},
            xticklabels=labels[:n_vars],
            yticklabels=labels[:n_vars],
            ax=ax)

# 在每个单元格中添加相关系数和显著性标记
for i in range(n_vars):
    for j in range(n_vars):
        if i > j:  # 只处理下三角
            # 相关系数值
            corr_val = corr_matrix[i, j]
            # 显著性标记
            sig_marker = get_significance_marker(p_values[i, j])

            # 根据背景色选择文字颜色
            text_color = 'white' if abs(corr_val) > 0.5 else 'black'

            # 添加文本
            text = f'{corr_val:.2f}\n{sig_marker}'
            ax.text(j + 0.5, i + 0.5, text,
                   ha='center', va='center',
                   color=text_color,
                   fontsize=7,
                   weight='bold' if sig_marker else 'normal')

# 设置标题和标签
ax.set_title('Correlation Matrix with Significance Levels\n(* p<0.05, ** p<0.01, *** p<0.001)',
             fontsize=14, pad=20)

# 调整布局
plt.tight_layout()

# 保存图片
plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
print("图片已保存为 correlation_heatmap.png")

plt.show()
