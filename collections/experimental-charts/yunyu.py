# ----------云雨图-----------
# Python版本要求: 3.6
# 需要安装的库: numpy pandas matplotlib
# 镜像安装命令:
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple numpy pandas matplotlib
# 导入必要的库
import numpy as np  # 数值计算库
import pandas as pd  # 数据处理库
import matplotlib.pyplot as plt  # 绘图库

# ==================== 1. 数据准备 ====================
# 设置随机种子以保证结果可复现
np.random.seed(42)

# 数据集的特征变量 (列名)
categories = ['A', 'B', 'C', 'D', 'E']

# 生成随机数据
# 为每个类别生成不同分布的数据
data_dict = {
    'A': np.random.normal(50, 10, 100),   # 均值50, 标准差10, 100个数据点
    'B': np.random.normal(60, 15, 100),   # 均值60, 标准差15
    'C': np.random.normal(55, 8, 100),    # 均值55, 标准差8
    'D': np.random.normal(65, 12, 100),   # 均值65, 标准差12
    'E': np.random.normal(58, 10, 100)    # 均值58, 标准差10
}

# 创建DataFrame
df = pd.DataFrame(data_dict)

# ==================== 2. 可视化设置 ====================
# 创建绘图形和坐标轴, 设置图形大小为10x8英寸
fig, ax = plt.subplots(figsize=(10, 8))

# 定义颜色方案 (颜色个数与变量个数相同)
# # 小提琴图颜色 (半透明填充)  橙线图颜色 (实色填充)
box_colors = violin_colors = ["#d36a87", "#ea9979", "#83b6b5", "#bcdfa7", "#f5e8c8"]
# box_colors = violin_colors = ['#9bb55e', '#fcd744', '#dc8e4e', '#ba7ab1', '#8cadd4']

# 设置类别在x轴上的位置 (0,1,2,3,4)
positions = np.arange(len(categories))
box_width = 0.15  # 箱形图宽度
violin_width = 0.5  # 小提琴图宽度

# ==================== 3. 绘制图形 ====================
# 遍历每个类别进行绘图
for i, category in enumerate(categories):
    # 获取当前类别的数据值
    data_points = df[category].values

    # ------------------ 3.1 绘制箱形图 ------------------
    # 箱形图位置向左偏移 (避免与小提琴图完全重叠)
    box_pos = positions[i] - box_width / 100

    # 绘制箱形图 (boxplot)
    box = ax.boxplot(
        data_points,
        positions=[box_pos],  # 指定位置
        widths=box_width,  # 设置宽度
        patch_artist=True,  # 允许填充颜色
        showfliers=False,  # 不单独显示离群点 (因为后面会用散点图显示)
        notch=True,  # 显示中位数置信区间缺口
        # 中位数线属性设置
        medianprops={'color': 'black', 'linewidth': 3},
        # 箱体属性设置
        boxprops={'facecolor': box_colors[i], 'edgecolor': violin_colors[i]},
        # 须线属性设置
        whiskerprops={'color': violin_colors[i], 'linewidth': 3},
        # 端点线属性设置
        capprops={'color': violin_colors[i], 'linewidth': 3}
    )

    # ------------------ 3.2 绘制半小提琴图 ------------------
    # 小提琴图位置向右偏移 (与箱形图对称)
    violin_pos = positions[i] + box_width / 50

    # 绘制完整小提琴图 (violinplot)
    violin = ax.violinplot(
        data_points,
        positions=[violin_pos],  # 指定位置
        widths=violin_width,  # 设置宽度
        showmeans=False,  # 不显示均值
        showmedians=False,  # 不显示中位数 (箱线图已显示)
        showextrema=False  # 不显示极值
    )

    # 修改小提琴图只显示右侧一半
    for pc in violin['bodies']:
        # 设置小提琴图颜色和透明度
        pc.set_facecolor(violin_colors[i])
        pc.set_edgecolor(violin_colors[i])
        pc.set_alpha(0.35)  # 设置透明度

        # 获取路径顶点
        vertices = pc.get_paths()[0].vertices

        # 只保留x坐标大于中心位置的部分 (实现半小提琴图效果)
        vertices[:, 0] = np.where(
            vertices[:, 0] > violin_pos,
            vertices[:, 0],
            violin_pos
        )

    # ------------------ 3.3 添加散点 ------------------
    # 在箱形图位置添加抖动点 (jitter scatter plot)
    ax.scatter(
        # x坐标: 在箱形图位置附近添加随机抖动 (避免点重叠)
        np.random.normal(positions[i] - box_width, 0.04, len(data_points)),
        # y坐标: 实际数据值
        data_points,
        color=violin_colors[i],  # 颜色与小提琴图一致
        alpha=0.8,  # 透明度
        s=50,  # 点大小
        edgecolor='white',  # 边缘颜色
        linewidth=0.8,  # 边缘线宽
        zorder=3  # 图层顺序 (确保点在最上层)
    )

# ==================== 4. 图表美化 ====================
# 设置x轴刻度位置和标签
ax.set_xticks(positions)
ax.set_xticklabels(categories, fontsize=20)

# 设置y轴标签和刻度标签字体大小
ax.set_ylabel('Value', fontsize=20)
ax.set_yticklabels(ax.get_yticks(), fontsize=20)

# 添加轴网格线 (虚线, 半透明)
ax.grid(axis='y', linestyle='--', alpha=0.7)

# # 显示边框
for spine in ['top', 'right', 'bottom', 'left']:
    ax.spines[spine].set_visible(True)
    ax.spines[spine].set_linewidth(2)  # 设置边框线宽
    ax.spines[spine].set_color('black')  # 设置边框颜色

# 添加图表标题 (pad参数控制标题与图的间距)
plt.title('Raincloud plots', pad=20, fontsize=22)

# 调整子图布局 (避免元素被裁剪)
plt.tight_layout()

# 显示图形
plt.show()
