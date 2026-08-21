# =========================================================================================
# ====================================== 1. 库的导入 =========================================
# =========================================================================================
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from matplotlib.patches import Circle
import pandas as pd
from scipy.interpolate import make_interp_spline
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

mpl.rcParams['font.family'] = 'DejaVu Serif'
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

# =========================================================================================
# ======================================2.颜色库设置=========================================
# =========================================================================================
COLOR_THEMES = {
    1: {
        'series1': '#a29bd0',  # Average - 浅紫色
        'series2': '#7e127e',  # Brandon Ingram - 深蓝紫色
        'series3': '#5c4fad',  # Kyrie Irving - 中紫色
        'center_bg': '#f0ebe2',
        'labels': [
            '#d95f02', '#2ca02c', '#d62728', '#17becf', '#17becf', '#17becf', '#17becf',
            '#17becf', '#17becf', '#1f77b4', '#ff7f0e', '#ff7f0e', '#ff7f0e', '#ff7f0e',
            '#9467bd', '#d62728', '#1f77b4', '#1f77b4', '#1f77b4', '#1f77b4', '#1f77b4'
        ]
    },
}

# =========================================================================================
# ======================================3.绘图函数=========================================
# =========================================================================================
def create_and_save_radar_chart(categories, data_avg, data_ingram, data_irving, palette):
    series1_color = palette['series1']
    series2_color = palette['series2']
    series3_color = palette['series3']
    center_bg_color = palette['center_bg']
    label_colors = palette['labels']

    # 调试输出：打印颜色值
    print(f"Average颜色: {series1_color}")
    print(f"Brandon Ingram颜色: {series2_color}")
    print(f"Kyrie Irving颜色: {series3_color}")

    num_vars = len(categories)
    data_avg_closed = data_avg + data_avg[:1]
    data_ingram_closed = data_ingram + data_ingram[:1]
    data_irving_closed = data_irving + data_irving[:1]

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    # 创建平滑的角度和数据点
    angles_smooth = np.linspace(0, 2 * np.pi, 500)

    # 对每组数据进行样条插值以实现平滑效果
    def smooth_data(data_list, angles_original):
        # 移除闭合点，使用原始数据
        angles_arr = np.array(angles_original[:-1])
        data_arr = np.array(data_list[:-1])

        # 为了实现周期性，在两端添加额外的点
        angles_extended = np.concatenate([
            angles_arr[-2:] - 2*np.pi,
            angles_arr,
            angles_arr[:2] + 2*np.pi
        ])
        data_extended = np.concatenate([
            data_arr[-2:],
            data_arr,
            data_arr[:2]
        ])

        # 创建插值函数
        spl = make_interp_spline(angles_extended, data_extended, k=3)
        return spl(angles_smooth)

    data_avg_smooth = smooth_data(data_avg_closed, angles)
    data_ingram_smooth = smooth_data(data_ingram_closed, angles)
    data_irving_smooth = smooth_data(data_irving_closed, angles)

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

    ax.set_theta_offset(np.pi / 2)  # 角度的起始位置
    ax.set_theta_direction(-1)  # 角度的增长方向，顺时针
    ax.grid(True, color='#d0d0d0', linewidth=0.8)  # 【参数】显示网格线，设置颜色和粗细

    # 设置径向网格线（从中心射向周围的线）的颜色
    ax.xaxis.grid(True, color='#d0d0d0', linewidth=0.8)  # 【参数】径向线颜色和粗细

    yticks = [0.1, 0.2, 0.3, 0.4, 0.45]  # 定义要在哪些半径位置显示刻度
    ax.set_yticks(yticks)  # 设置半径刻度位置
    ax.set_yticklabels([])  # 隐藏半径刻度的数字标签

    gridlines = ax.yaxis.get_gridlines()  # 获取所有的环形网格线对象
    for i, line in enumerate(gridlines):  # 遍历每一条环形网格线
        tick_value = yticks[i]  # 获取当前网格线对应的刻度值
        if tick_value in [0.2, 0.3, 0.4]:
            line.set_visible(False)  # 隐藏这条线
        elif tick_value == 0.1:
            line.set_linestyle('--')  # 线型
            line.set_color('black')  # 颜色
            line.set_linewidth(2)  # 【参数】内圈虚线的粗细
        elif tick_value == 0.45:
            line.set_linestyle('-')  # 线型
            line.set_color('#808080')  # 颜色 - 灰色
            line.set_linewidth(2.5)  # 【参数】最外圈实线的粗细（调整这里改变外圈粗细）

    # 绘制平滑的填充阴影 - 现役球员平均值
    ax.fill(angles_smooth, data_avg_smooth, color=series1_color, alpha=0.15, zorder=10)

    # 绘制平滑的填充阴影 - Brandon Ingram
    ax.fill(angles_smooth, data_ingram_smooth, color=series2_color, alpha=0.25, zorder=15)

    # 绘制平滑的填充阴影 - Kyrie Irving
    ax.fill(angles_smooth, data_irving_smooth, color=series3_color, alpha=0.25, zorder=20)

    # 绘制平滑的雷达图线条 - 现役球员平均值
    ax.plot(angles_smooth,
            data_avg_smooth,
            color=series1_color,
            linewidth=2,  # 【参数】连线的粗细
            label='Active Players Average',
            zorder=30)

    # Brandon Ingram数据
    ax.plot(angles_smooth, data_ingram_smooth, color=series2_color, linewidth=2,  # 【参数】连线的粗细
            label='Brandon Ingram', zorder=35)

    # Kyrie Irving数据
    ax.plot(angles_smooth, data_irving_smooth, color=series3_color, linewidth=2,  # 【参数】连线的粗细
            label='Kyrie Irving', zorder=40)

    # 在原始数据点上添加标记点
    ax.plot(angles, data_avg_closed, 'o', color=series1_color, markersize=8, zorder=31)  # 【参数】数据点圆圈大小
    ax.plot(angles, data_ingram_closed, 'o', color=series2_color, markersize=8, zorder=36)  # 【参数】数据点圆圈大小
    ax.plot(angles, data_irving_closed, 'o', color=series3_color, markersize=8, zorder=41)  # 【参数】数据点圆圈大小

    inner_radius = 0.03  # 【参数】中心圆圈的大小（调整这里改变中心圆圈大小）
    center_circle = Circle((0, 0),
                           inner_radius,
                           transform=ax.transData._b,
                           color=center_bg_color,
                           zorder=2,
                           clip_on=False)
    ax.add_patch(center_circle)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([])

    for i, category in enumerate(categories):
        angle_rad = angles[i]
        visual_angle_deg = np.rad2deg(np.pi / 2 - angle_rad) % 360
        if 90 < visual_angle_deg < 270:
            rotation = visual_angle_deg - 90
            horizontal_alignment = 'center'
        else:
            rotation = visual_angle_deg - 90
            horizontal_alignment = 'center'

        # 在外圈添加标签
        ax.text(angle_rad, 0.50, category,  # 【参数】0.58控制字体距离圆圈的距离（数值越大距离越远）
                fontsize=20,  # 【参数】外圈标签的字体大小
                ha=horizontal_alignment,
                va='center',
                rotation=rotation,
                color='black',
                weight='bold')

    ax.set_ylim(0, 0.47)  # 【参数】雷达图的半径范围（稍大于最大刻度以显示外圈线）


    ax.spines['polar'].set_visible(False)  # 隐藏polar边框线（使用gridline作为外圈）

    ax.legend(loc='lower center',
              bbox_to_anchor=(0.5, -0.15),
              ncol=3,
              frameon=False,
              fontsize=16,  # 【参数】图例的字体大小
              handlelength=2.5)

    plt.tight_layout(pad=2)

    # 保存图片
    plt.savefig(SCRIPT_DIR / 'player_radar_chart.png', dpi=300, bbox_inches='tight')
    plt.savefig(SCRIPT_DIR / 'player_radar_chart.pdf', bbox_inches='tight')
    plt.savefig(SCRIPT_DIR / 'player_radar_chart.svg', bbox_inches='tight')
    print("雷达图已保存！")
    # plt.show()  # 暂时注释以查看调试输出

# =========================================================================================
# ======================================4.执行部分========================================
# =========================================================================================
if __name__ == '__main__':
    print("=" * 60)
    print("开始执行雷达图绘制程序")
    print("=" * 60)

    # 读取数据
    csv_data_path = SCRIPT_DIR / 'now_and_plan_players.csv'
    df = pd.read_csv(csv_data_path, encoding='utf-8')

    # 打印列名以便调试
    print("列名:", df.columns.tolist())

    # 定义8个维度（使用实际的列名）
    categories_main = ['Local (死忠)', 'Young (流量)', 'Female (女性)', 'Intl (国际)',
                       'Hardcore (硬核)', 'Gossip (八卦)', 'Brand (商业)', 'Comm (公益)']

    # 定义显示用的英文标签
    categories_display = ['Local', 'Young', 'Female', 'Intl', 'Hardcore', 'Gossip', 'Brand', 'Comm']

    # 计算现役球员的平均值
    active_players = df[df['身份'] == '现役']
    data_avg_main = []
    for cat in categories_main:
        avg_value = active_players[cat].mean()
        data_avg_main.append(avg_value)

    # 获取Brandon Ingram的数据
    ingram_data = df[df['球员 (Player)'] == 'Brandon Ingram']
    data_ingram_main = []
    for cat in categories_main:
        data_ingram_main.append(ingram_data[cat].values[0])

    # 获取Kyrie Irving的数据
    irving_data = df[df['球员 (Player)'] == 'Kyrie Irving']
    data_irving_main = []
    for cat in categories_main:
        data_irving_main.append(irving_data[cat].values[0])

    # 提取配色方案
    select_color = COLOR_THEMES.get(1, 1)

    # 调用绘图函数
    create_and_save_radar_chart(
        categories=categories_display,  # 使用英文标签
        data_avg=data_avg_main,
        data_ingram=data_ingram_main,
        data_irving=data_irving_main,
        palette=select_color,
    )
