import matplotlib.pyplot as plt
import matplotlib
import os

matplotlib.use('TkAgg')
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
plt.rcParams['mathtext.fontset'] = 'stix'

# 直接定义数据
categories = ['Media Rights', 'Gate Receipts', 'Sponsorships']
percentages = [55, 28, 17]

# 配色方案
color_schemes = {
    '1': ['#69b7a3', '#fde368', '#f69f98', '#99d2e7'],
    '2': ['#ff7f0e', '#1f77b4', '#2ca02c', '#9467bd'],
    '3': ['#fbb4ae', '#b3cde3', '#ccebc5', '#fed9a6'],
    '4': ['#8c564b', '#a9a9a9', '#d62728', '#bcbd22'],
    '5': ['#ccebc5', '#a8ddb5', '#7bccc4', '#43a2ca'],
    '6': ['#fee0d2', '#fc9272', '#ef3b2c', '#a50f15'],
    '7': ['#deebf7', '#9ecae1', '#4292c6', '#08519c'],
    '8': ['#e377c2', '#17becf', '#dbdb8d', '#7f7f7f'],
    '9': ['#efedf5', '#bcbddc', '#807dba', '#54278f'],
    '10': ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3']
}

# 选择绘图方案
selected_scheme_name = '10'
colors = color_schemes[selected_scheme_name][:len(categories)]

# 创建图表
fig, ax = plt.subplots(figsize=(10, 8))

# 设置分离效果（explode）- 让每个扇区都分离出来
explode = (0.1, 0.1, 0.1)  # 每个扇区分离的距离

# 绘制分离的饼图
wedges, texts, autotexts = ax.pie(
    percentages,
    labels=categories,
    colors=colors,
    autopct='%1.1f%%',
    startangle=90,
    explode=explode,  # 添加分离效果
    shadow=True,  # 添加阴影效果
    textprops={'fontsize': 12, 'fontweight': 'bold'}
)

# 设置百分比文字样式
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(11)
    autotext.set_fontweight('bold')

# 设置标签文字样式
for text in texts:
    text.set_fontsize(13)
    text.set_fontweight('bold')

# 设置标题
ax.set_title('Los Angeles Lakers Commercial Revenue Sources',
             fontsize=16, fontweight='bold', pad=20)

# 保存图表
plt.tight_layout()
plt.savefig('Components/lakers_revenue_donut.png', dpi=300, bbox_inches='tight')
plt.savefig('Components/lakers_revenue_donut.pdf', bbox_inches='tight')
plt.savefig('Components/lakers_revenue_donut.svg', bbox_inches='tight')
plt.show()

print("环形图已生成并保存！")
print(f"数据来源: {categories}")
print(f"百分比: {percentages}")
