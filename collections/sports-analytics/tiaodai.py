# =========================================================================================
# ====================================== 1. 库的导入 =========================================
# =========================================================================================
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib
import os
from matplotlib import font_manager

# 设置字体路径
script_dir = os.path.dirname(os.path.abspath(__file__))
font_path = font_manager.findfont('DejaVu Serif')
font_prop = font_manager.FontProperties(fname=font_path)

plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['font.size'] = 10  # 与3d_pubu_P.py相同的全局字体大小
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

# =========================================================================================
# ====================================== 2.颜色库=========================================
# =========================================================================================
COLOR_SCHEMES = {
    1: ['#16058b', '#6200aa', '#9e169d', '#cc4a74', '#eb7852', '#fcb431'],
}

# =========================================================================================
# ======================================3.绘图函数=========================================
# =========================================================================================
def draw_3d_chart(data_dict, years_arr, county_list, color_list, font_prop):
    num_c = len(county_list)  # 计算数据类别的数量
    fig = plt.figure(figsize=(12, 10), dpi=150)  # 创建画布，与3d_pubu_P.py相同尺寸
    ax = fig.add_subplot(111, projection='3d')  # 添加一个3D子图

    # 定义条带宽度和其他参数
    half_width = 0.35  # 条带半宽度
    yticks = list(range(num_c))  # Y轴刻度位置

    # 计算Z轴基准线（用于垂线起点）
    all_z_values = []
    for county in county_list:
        all_z_values.extend(data_dict[county])
    z_baseline = min(all_z_values) - abs(min(all_z_values)) * 0.1  # 基准面设在最小值下方

    for i, county in enumerate(county_list):  # 遍历每一个区域
        zs = data_dict[county]  # 获取当前区域的数据

        # 绘制条带面（ribbons）
        for j in range(len(years_arr) - 1):  # 遍历年份区间
            X_segment = np.array([[years_arr[j], years_arr[j + 1]],
                                  [years_arr[j], years_arr[j + 1]]])
            Y_segment = np.array([[i - half_width, i - half_width],
                                  [i + half_width, i + half_width]])
            Z_segment = np.array([[zs[j], zs[j + 1]],
                                  [zs[j], zs[j + 1]]])

            # 绘制条带面 - 调低透明度，饱和色
            ax.plot_surface(X_segment,
                            Y_segment,
                            Z_segment,
                            color=color_list[i % len(color_list)],
                            alpha=0.75,  # 透明度设为0.75
                            edgecolor='black',  # 黑色边缘
                            linewidth=0.3,  # 细边缘
                            zorder=2,
                            shade=False)  # 不使用阴影效果

    # 设置坐标轴
    ax.set_xticks(years_arr)
    ax.set_xlim(years_arr[0] - 0.5, years_arr[-1] + 0.5)
    ax.set_yticks(yticks)
    ax.set_yticklabels(county_list,
                       fontsize=7,  # 与3d_pubu_P.py相同的字号
                       fontproperties=font_prop)

    # 不设置轴标签（取消标题和轴标签）
    # 注意：3d_pubu_P.py中没有设置tick_params，使用默认字号

    # 动态计算Z轴范围
    all_z_values = []
    for county in county_list:
        all_z_values.extend(data_dict[county])
    z_data_min = min(all_z_values)
    z_data_max = max(all_z_values)

    # 设置坐标轴范围，与3d_pubu_P.py相似的边距
    margin = 0.1
    x_min, x_max = min(years_arr), max(years_arr)
    y_min, y_max = 0, num_c - 1
    z_min = z_data_min - abs(z_data_min) * 0.15 if z_data_min < 0 else 0
    z_max = z_data_max * 1.15

    ax.set_xlim(x_min - margin, x_max + margin)
    ax.set_ylim(y_min - margin, y_max + margin)
    ax.set_zlim(z_min, z_max)

    # 动态计算Z轴范围
    all_z_values = []
    for county in county_list:
        all_z_values.extend(data_dict[county])
    z_data_min = min(all_z_values)
    z_data_max = max(all_z_values)

    # 设置坐标轴范围，与3d_pubu_P.py相似的边距
    margin = 0.1
    x_min, x_max = min(years_arr), max(years_arr)
    y_min, y_max = 0, num_c - 1
    z_min = z_data_min - abs(z_data_min) * 0.15 if z_data_min < 0 else 0
    z_max = z_data_max * 1.15

    ax.set_xlim(x_min - margin, x_max + margin)
    ax.set_ylim(y_min - margin, y_max + margin)
    ax.set_zlim(z_min, z_max)

    # 设置视角 - 与3d_pubu_P.py相同
    ax.view_init(elev=25, azim=-45)

    # 创建图例 - 与3d_pubu_P.py完全一致
    legend_patches = [plt.Rectangle((0, 0), 1, 1, color=color_list[i % len(color_list)], alpha=0.8) for i in range(num_c)]
    legend = plt.legend(
        legend_patches,
        county_list,
        loc='upper left',  # 与3d_pubu_P.py相同的位置
        fontsize=8,  # 与3d_pubu_P.py相同的字号
        frameon=True,
        shadow=False,
        fancybox=True,
        framealpha=0.8,
        prop=font_prop)

    # 调整布局 - 与3d_pubu_P.py相同
    plt.tight_layout()

# =========================================================================================
# ======================================4.执行部分=========================================
# =========================================================================================
if __name__ == "__main__":
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 从wpc.csv读取数据
    data_path = os.path.join(script_dir, 'wpc.csv')
    df = pd.read_csv(data_path)

    # 策略名称映射
    policy_name_mapping = {
        'Model(MPC)': 'Ours',
        'Baseline-Zero': 'Laissez-faire',
        'Baseline-MaxXL': 'Aggressive',
        'Baseline-Random': 'Random',
        'Baseline-Random2': 'Random2',
        'Baseline-Random3': 'Random3'
    }

    # 获取唯一的策略（policies）并按照指定顺序排列
    policy_order = ['Model(MPC)', 'Baseline-Zero', 'Baseline-MaxXL',
                    'Baseline-Random', 'Baseline-Random2', 'Baseline-Random3']
    policies = [p for p in policy_order if p in df['policy'].values]

    # 准备数据字典，使用C指标
    years = sorted(df['season'].unique())  # 获取年份（season）
    data = {}
    policy_display_names = []

    for policy in policies:
        policy_data = df[df['policy'] == policy].sort_values('season')
        display_name = policy_name_mapping.get(policy, policy)
        data[display_name] = policy_data['C'].values.tolist()
        policy_display_names.append(display_name)

    # 颜色方案
    scheme_index = 1  # 要使用的颜色方案
    current_colors = COLOR_SCHEMES.get(scheme_index, COLOR_SCHEMES[1])  # 颜色方案

    # 调用函数进行绘图
    draw_3d_chart(data, years, policy_display_names, current_colors, font_prop)

    # 保存图片（多种格式）
    output_png = os.path.join(script_dir, 'tiaodai_output.png')
    output_svg = os.path.join(script_dir, 'tiaodai_output.svg')
    output_pdf = os.path.join(script_dir, 'tiaodai_output.pdf')

    plt.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"PNG图片已保存至: {output_png}")

    plt.savefig(output_svg, format='svg', bbox_inches='tight', facecolor='white')
    print(f"SVG图片已保存至: {output_svg}")

    plt.savefig(output_pdf, format='pdf', bbox_inches='tight', facecolor='white')
    print(f"PDF图片已保存至: {output_pdf}")

    plt.show()
