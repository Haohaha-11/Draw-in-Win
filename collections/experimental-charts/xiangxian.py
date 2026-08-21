import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# 设置随机种子以保证可重复性
np.random.seed(42)

# 1. 数据模拟与生成
# Apple组：深紫色，数据集中在10-15之间
apple_data = np.random.normal(loc=12.5, scale=1.5, size=100)

# Banana组：蓝绿色，数据集中在13-20之间，分布范围较广
banana_data = np.random.normal(loc=16.5, scale=2.0, size=100)

# Carrot组：翠绿色，数据集中在3-10之间
carrot_data = np.random.normal(loc=6.5, scale=1.8, size=100)

# Date组：明黄色，数据集中在3-8之间
date_data = np.random.normal(loc=5.5, scale=1.2, size=100)

# 创建DataFrame
data = pd.DataFrame({
    'value': np.concatenate([apple_data, banana_data, carrot_data, date_data]),
    'category': ['Apple']*100 + ['Banana']*100 + ['Carrot']*100 + ['Date']*100
})

# 定义类别顺序
category_order = ['Apple', 'Banana', 'Carrot', 'Date']
data['category'] = pd.Categorical(data['category'], categories=category_order, ordered=True)

# 2. 配色方案
colors = {
    'Apple': '#6A4C93',    # 深紫色
    'Banana': '#1E88A8',   # 蓝绿色/孔雀蓝
    'Carrot': '#2ECC71',   # 翠绿色
    'Date': '#F4D03F'      # 明黄色
}

# 3. 创建图表
fig, ax = plt.subplots(figsize=(8, 10))

# 设置位置参数
positions = np.arange(len(category_order))
width = 0.3

# 为每个类别绘制云雨图（纵向）
for i, category in enumerate(category_order):
    cat_data = data[data['category'] == category]['value'].values
    color = colors[category]

    # 下方：抖动散点图
    x_jitter = np.random.normal(i - width, 0.05, size=len(cat_data))
    ax.scatter(x_jitter, cat_data, alpha=0.4, s=20, color=color, edgecolors='none')

    # 中间：箱线图（纵向）
    bp = ax.boxplot([cat_data], positions=[i], widths=0.15, vert=True,
                     patch_artist=True, showfliers=False,
                     boxprops=dict(facecolor='white', edgecolor='black', linewidth=1.5),
                     whiskerprops=dict(color='black', linewidth=1.5),
                     capprops=dict(color='black', linewidth=1.5),
                     medianprops=dict(color='black', linewidth=2))

    # 右侧：半小提琴图（KDE密度图）
    from scipy.stats import gaussian_kde
    kde = gaussian_kde(cat_data)
    y_range = np.linspace(cat_data.min() - 1, cat_data.max() + 1, 200)
    density = kde(y_range)

    # 归一化密度以适应图表
    density_normalized = density / density.max() * 0.4

    # 绘制半小提琴（只显示右半部分）
    ax.fill_betweenx(y_range, i, i + density_normalized,
                      color=color, alpha=0.6, edgecolor='black', linewidth=1)

# 4. 统计显著性标注（纵向版本 - 横线在上方）
def add_significance_bar(ax, x1, x2, y_height, p_value):
    """添加显著性横线和P值标注（横向标注在图表上方）"""
    # 绘制竖线和横线
    ax.plot([x1, x1], [ax.get_ylim()[1] * 0.85, y_height], 'k-', linewidth=1.5)
    ax.plot([x1, x2], [y_height, y_height], 'k-', linewidth=1.5)
    ax.plot([x2, x2], [ax.get_ylim()[1] * 0.85, y_height], 'k-', linewidth=1.5)

    # 添加P值文本（横向）
    ax.text((x1 + x2) / 2, y_height + 0.3, f'p = {p_value}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

# 添加三组显著性标注
add_significance_bar(ax, 0, 1, 25, '3.5e-18')  # Apple vs Banana
add_significance_bar(ax, 1, 2, 23, '1.5e-66')  # Banana vs Carrot
add_significance_bar(ax, 2, 3, 21, '0.073')    # Carrot vs Date

# 5. 美学设置
ax.set_xticks(positions)
ax.set_xticklabels(category_order, fontweight='bold', fontstyle='italic', fontsize=12)
ax.set_ylabel('xiaoxu shixiong', fontweight='bold', fontsize=14)
ax.set_xlabel('')

# 设置背景和边框
ax.set_facecolor('white')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.5)
ax.spines['bottom'].set_linewidth(1.5)

# 设置Y轴范围
ax.set_ylim(0, 25)
ax.set_xlim(-0.5, 4)

# 添加图例
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=colors[cat], label=cat) for cat in category_order]
ax.legend(handles=legend_elements, loc='upper right',
          frameon=True, fontsize=11, title_fontsize=12,
          prop={'weight': 'bold', 'style': 'italic'})

# 调整布局
plt.tight_layout()

# 6. 保存为矢量图
import os
# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, 'recreated_chart.svg')
plt.savefig(output_path, format='svg', dpi=300, bbox_inches='tight')
print(f"图表已成功保存为 '{output_path}'")
plt.show()
