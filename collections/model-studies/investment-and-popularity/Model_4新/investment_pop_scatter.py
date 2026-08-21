import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.interpolate import make_interp_spline

# 设置Times New Roman字体
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.unicode_minus'] = False

def plot_investment_pop_scatter(data_folder, save_path):
    """
    绘制投资-人口散点图，点的大小表示投资强度

    参数:
        data_folder: 数据文件夹路径
        save_path: 保存图片的路径
    """
    plt.figure(figsize=(14, 10))

    # 文件列表和对应的标签
    files = {
        'Laissez_faire.csv': 'Laissez-faire',
        'Aggressive.csv': 'Aggressive',
        'Bankrupt.csv': 'Bankrupt',
        'Ours.csv': 'Ours'
    }

    # 自定义配色方案
    colors = {
        'Laissez-faire': '#fdbc46',
        'Aggressive': '#ec7753',
        'Bankrupt': '#a167cb',
        'Ours': '#5c4fad'
    }

    # 标记样式 - 全部使用圆形
    markers = {
        'Laissez-faire': 'o',
        'Aggressive': 'o',
        'Bankrupt': 'o',
        'Ours': 'o'
    }

    # 采样间隔（每隔几个点取一个）
    sample_interval = 5

    # 先读取所有数据，找到全局I值范围
    all_i_values = []
    for filename in files.keys():
        file_path = Path(data_folder) / filename
        df_temp = pd.read_csv(file_path)
        all_i_values.extend(df_temp['I'].values)

    global_i_min = min(all_i_values)
    global_i_max = max(all_i_values)
    print(f"全局I值范围: {global_i_min:.4f} - {global_i_max:.4f}")

    # 读取并绘制每个文件的数据
    for filename, label in files.items():
        file_path = Path(data_folder) / filename

        # 读取数据
        df = pd.read_csv(file_path)

        # 采样数据
        df_sampled = df.iloc[::sample_interval, :]

        # 提取数据
        t_values = df_sampled['t'].values
        pop_values = df_sampled['Pop'].values
        i_values = df_sampled['I'].values

        # 将I值映射到点的大小（使用全局范围归一化）
        # 对Laissez_faire特别处理，增大其点的大小
        i_normalized = np.sqrt((i_values - global_i_min) / (global_i_max - global_i_min))

        if label == 'Laissez-faire':
            # Laissez_faire的点增大3倍
            sizes = i_normalized * 300 + 40
        else:
            sizes = i_normalized * 100 + 15

        # 绘制散点图（去掉边框）
        plt.scatter(t_values, pop_values, s=sizes, c=colors[label],
                   marker=markers[label], alpha=0.8, edgecolors='none',
                   linewidth=0, label=label, zorder=3)

        # 添加平滑曲线拟合
        # 使用样条插值创建平滑曲线
        if len(t_values) > 3:  # 需要至少4个点才能做三次样条插值
            # 创建更密集的点用于绘制平滑曲线
            t_smooth = np.linspace(t_values.min(), t_values.max(), 300)

            # 使用三次样条插值
            spl = make_interp_spline(t_values, pop_values, k=3)
            pop_smooth = spl(t_smooth)

            # 绘制平滑曲线
            plt.plot(t_smooth, pop_smooth, color=colors[label],
                    linewidth=2, alpha=0.6, zorder=2)

    # 设置图表属性
    plt.xlabel('Time ($t$)', fontsize=22)
    plt.ylabel('Population ($Pop$)', fontsize=22)

    # 设置刻度标签字体大小
    plt.tick_params(axis='both', which='major', labelsize=16)

    # 显示图例
    plt.legend(loc="best", fontsize=19, framealpha=0.9, markerscale=1.5)
    plt.grid(True, alpha=0.3, linestyle='--')

    # 调整布局并保存
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\n投资-人口散点图已保存到: {save_path}")
    plt.close('all')


if __name__ == '__main__':
    # 设置路径
    data_folder = '.'
    save_path = 'investment_pop_scatter.png'

    # 绘制图表
    plot_investment_pop_scatter(data_folder, save_path)

    # 同时保存PDF和SVG格式
    save_path_pdf = 'investment_pop_scatter.pdf'
    save_path_svg = 'investment_pop_scatter.svg'

    plot_investment_pop_scatter(data_folder, save_path_pdf)
    plot_investment_pop_scatter(data_folder, save_path_svg)

    print("\n所有格式的图表已生成完成！")
