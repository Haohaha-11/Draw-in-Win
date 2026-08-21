# =============================================================================
# 1、导入所需库
# =============================================================================
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PolyCollection
import matplotlib.patches as mpatches
import pandas as pd

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['axes.unicode_minus'] = False

# =============================================================================
# 2.定义颜色库
# =============================================================================
color_schemes = {
    1: ['#440154', '#3b528b', '#21908d', '#5dc863'],
    2: ['#0d0887', '#7201a8', '#bd3786', '#f0744e'],
    20: ['#d62728', '#2ca02c', '#1f77b4', '#9467bd'],
    21: ['#581845', '#008080', '#90EE90', '#FFD700']
}

# =============================================================================
# 3.数据加载函数
# =============================================================================
def load_data_from_excel(filepath):
    # 使用 pandas 读取 Excel 文件
    df = pd.read_excel(filepath)
    # 提取第一列数据作为x 轴数据
    wavelength = df.iloc[:, 0].values
    # 循环提取从第二列开始的所有数据列，作为 y 轴数据集
    all_y_data = [df.iloc[:, i].values for i in range(1, len(df.columns))]
    # 提取从第二列开始的列名，作为每条曲线的标签
    labels = df.columns[1:].tolist()
    print(f"成功从 {filepath} 加载数据。")
    # 返回加载和解析好的数据
    return wavelength, all_y_data, labels

# =============================================================================
# 3.5 生成随机高斯峰数据函数
# =============================================================================
def generate_gaussian_data(num_curves=7):
    """生成模拟的高斯峰数据"""
    # 定义高斯函数
    def gaussian(x, amplitude, center, width):
        return amplitude * np.exp(-((x - center) ** 2) / (2 * width ** 2))

    # 生成波长数据：800到1700 nm
    wavelength = np.linspace(800, 1700, 600)

    # 为每条曲线定义不同的峰位置、高度和宽度
    # 7条曲线的参数配置
    curve_params = [
        (1200, 1000, 75),   # Curve 1: 峰在1200nm
        (1350, 1400, 80),   # Curve 2: 峰在1350nm
        (1220, 1100, 70),   # Curve 3: 峰在1220nm
        (1400, 1600, 85),   # Curve 4: 峰在1400nm
        (1550, 2200, 90),   # Curve 5: 峰在1550nm
        (1520, 2000, 88),   # Curve 6: 峰在1520nm
        (1600, 2500, 95),   # Curve 7: 峰在1600nm
    ]

    all_y_data = []
    labels = []

    for i in range(num_curves):
        center, amplitude, width = curve_params[i]
        # 生成高斯峰数据
        y_data = gaussian(wavelength, amplitude, center, width)
        # 确保非负
        y_data = np.maximum(y_data, 0)
        all_y_data.append(y_data)
        labels.append(f'Amplitude_{i+1}')

    print(f"成功生成 {num_curves} 条模拟曲线数据。")
    return wavelength, all_y_data, labels

# =============================================================================
# 4.瀑布图绘图函数
# =============================================================================
def plot_3d_waterfall(wavelength, all_y_data, labels, colors, group_colors_for_legend):
    fig = plt.figure(figsize=(14, 10))
    # 在图形窗口中添加一个子图，并指定其为 3D 投影
    ax = fig.add_subplot(111, projection='3d')
    # 获取曲线的总数
    num_datasets = len(all_y_data)
    # 遍历所有的数据集，i 是索引，y_data 是对应的光谱数据
    for i, y_data in enumerate(all_y_data):
        # 为了创建封闭的填充区域，在波长数据的首尾各添加一个点
        padded_wl = np.r_[wavelength[0], wavelength, wavelength[-1]]
        # 对应地，在 y 轴数据的首尾各添加一个 0，使填充区域的底部落在基线上
        padded_yd = np.r_[0, y_data, 0]
        # 将 x (padded_wl) 和 y (padded_yd) 坐标配对，形成多边形的顶点
        verts = [list(zip(padded_wl, padded_yd))]
        # 创建一个多边形集合（即填充区域），设置其顶点、填充颜色和透明度
        poly = PolyCollection(verts, facecolors=colors[i], alpha=0.4)
        # 将创建的多边形添加到3D坐标系中。zs=i 指定其在x轴方向的深度位置，zdir='x' 表示深度方向是x轴
        ax.add_collection3d(poly, zs=i, zdir='x')
        # 在同样的位置绘制曲线的轮廓线，使其颜色与填充区域一致，并设置线宽
        ax.plot(wavelength, y_data, zs=i, zdir='x', color=colors[i], linewidth=2.0)

    # --- 坐标轴范围和标签设置 ---
    ax.set_ylabel('Wavelength (nm)', fontsize=14, labelpad=15)
    ax.set_zlabel('Amplitude (mV)', fontsize=14, labelpad=10)
    ax.set_xlabel('')
    ax.set_ylim(1700, 800)
    ax.set_xlim(-1, num_datasets)
    ax.set_zlim(0, 2600)

    # --- 坐标轴刻度和刻度标签设置 ---
    ax.set_xticks(range(num_datasets))
    ax.set_xticklabels(labels, fontsize=12, rotation=0, ha='left')
    ax.tick_params(axis='x', pad=-5)
    ax.tick_params(axis='y', labelsize=12)
    ax.tick_params(axis='z', labelsize=12)

    # --- 3D视图、背景和边框设置 ---
    ax.view_init(elev=10, azim=-160)
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.xaxis.pane.set_edgecolor('k')
    ax.yaxis.pane.set_edgecolor((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.pane.set_edgecolor((1.0, 1.0, 1.0, 0.0))
    ax.set_box_aspect((35, 15, 12))
    ax.grid(False)

    # --- 手动绘制刻度线和网格线 ---
    ax.tick_params(axis='x', length=0, color=(0, 0, 0, 0))
    ax.tick_params(axis='y', length=0, color=(0, 0, 0, 0))
    zmin, zmax = ax.get_zlim()
    xmin, xmax = ax.get_xlim()
    ymin_back, ymax_front = ax.get_ylim()
    xticks = ax.get_xticks()
    yticks = ax.get_yticks()
    tick_height = (zmax - zmin) * 0.025
    for x_pos in xticks:
        ax.plot([x_pos, x_pos], [ymin_back, ymin_back], [zmin, zmin + tick_height], color='k', linewidth=1)
    for y_pos in yticks:
        ax.plot([xmin, xmin], [y_pos, y_pos], [zmin, zmin + tick_height], color='k', linewidth=1)
    y_lim_bottom, y_lim_top = ax.get_ylim()
    x_lim_left, x_lim_right = ax.get_xlim()
    for x in xticks:
        if abs(x - x_lim_left) < 1e-6:
            continue
        ax.plot([x, x], ax.get_ylim(), zmin, color='lightgray', linestyle='--', linewidth=0.5)
    for y in yticks:
        if abs(y - y_lim_bottom) < 1e-6:
            continue
        ax.plot(ax.get_xlim(), [y, y], zmin, color='lightgray', linestyle='--', linewidth=0.5)

    # --- 图例设置 ---
    legend_patches = [mpatches.Patch(color=color, label=group) for group, color in group_colors_for_legend.items()]
    ax.legend(handles=legend_patches, loc='upper right', bbox_to_anchor=(0.83, 0.72), fontsize=12, borderaxespad=0.)

# =============================================================================
# 6、主程序入口
# =============================================================================
if __name__ == '__main__':
    # 选择数据来源：True=从Excel加载，False=生成随机数据
    use_excel = False

    if use_excel:
        # 数据的路径
        excel_file_path = r"lated_gaussian_data.xlsx"
        # 调用函数从指定的 Excel 文件加载数据
        wavelength_data, y_datasets, data_labels = load_data_from_excel(excel_file_path)
    else:
        # 生成随机高斯峰数据
        wavelength_data, y_datasets, data_labels = generate_gaussian_data(num_curves=7)

    # 选择要使用的配色
    color_scheme_choice = 21
    # 定义四个分组的名称
    group_names = ['groupA', 'groupB', 'groupC', 'groupD']
    # 定义一个映射关系，指定7条曲线中的每一条分别属于哪个分组
    series_to_group_map = [
        'groupD', 'groupC', 'groupD', 'groupC', 'groupA', 'groupB', 'groupA'
    ]

    # 检查数据是否成功加载
    if wavelength_data is not None and y_datasets is not None:
        # 从颜色库中获取选定的配色方案
        selected_palette = color_schemes.get(color_scheme_choice, color_schemes[21])
        print(f"--- 已选择配色方案: {color_scheme_choice} ---")
        # 检查所选配色方案的颜色数量是否足够分配给所有分组
        if len(selected_palette) < len(group_names):
            raise ValueError(f"配色方案 {color_scheme_choice} 的颜色数量不足4种。")
        # 创建一个字典，将分组名称与所选方案的颜色一一对应
        group_colors = dict(zip(group_names, selected_palette))
        # 根据映射关系，为7条曲线生成一个对应的颜色列表
        plot_colors = [group_colors[group] for group in series_to_group_map]
        # 使用加载的数据和生成的颜色列表来调用主绘图函数
        plot_3d_waterfall(wavelength_data, y_datasets, data_labels, plot_colors, group_colors)
        # 显示图形
        plt.show()
