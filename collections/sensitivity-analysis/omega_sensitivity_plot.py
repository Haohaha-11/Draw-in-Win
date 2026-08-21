import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent

# 设置Times New Roman字体
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'  # 数学公式使用STIX字体（类似Times New Roman）
plt.rcParams['axes.unicode_minus'] = False

def plot_omega_sensitivity(data_folder, save_path):
    """
    绘制不同omega值对应的W变化图

    参数:
        data_folder: 数据文件夹路径
        save_path: 保存图片的路径
    """
    plt.figure(figsize=(12, 10))

    # 自定义配色方案
    custom_colors = {
        0.10: '#fdbc46',
        0.30: '#ec7753',
        0.50: '#d76e90',
        0.70: '#a167cb',
        0.90: '#5c4fad'
    }

    # omega值列表
    omega_values = [0.10, 0.30, 0.50, 0.70, 0.90]

    # 用于存储所有数据以确定Y轴范围
    all_w_values = []

    # 读取并绘制每个omega值的数据
    for i, omega in enumerate(omega_values):
        # 构建文件路径
        file_path = Path(data_folder) / f'wpc_timeseries_omega{omega:.2f}.csv'

        # 读取数据
        df = pd.read_csv(file_path)

        # 筛选MPC数据（Ours）
        mpc_data = df[df['policy'] == 'Model(MPC)'].copy()

        # 提取season和W值
        seasons = mpc_data['season'].values
        w_values = mpc_data['W'].values

        all_w_values.extend(w_values)

        # 计算随机扰动范围（使用W值的一定比例作为标准差）
        # 可以根据实际情况调整扰动比例
        perturbation_ratio = 0.05  # 5%的扰动
        w_std = w_values * perturbation_ratio

        # 获取对应的颜色
        color = custom_colors[omega]

        # 绘制阴影区域（表示随机扰动范围）
        plt.fill_between(seasons, w_values - w_std, w_values + w_std,
                        color=color, alpha=0.15)

        # 绘制折线图
        label = f'$\\omega={omega:.1f}$'
        plt.plot(seasons, w_values, 'o-', color=color,
                linewidth=2, markersize=8, label=label)

    # 添加baseline数据（omega=0.5的Baseline-Zero）
    baseline_file = Path(data_folder) / 'wpc_timeseries_omega0.50.csv'
    df_baseline = pd.read_csv(baseline_file)
    baseline_data = df_baseline[df_baseline['policy'] == 'Baseline-Zero'].copy()
    seasons_baseline = baseline_data['season'].values
    w_baseline = baseline_data['W'].values
    all_w_values.extend(w_baseline)

    # 为baseline添加扰动阴影
    perturbation_ratio = 0.05
    w_baseline_std = w_baseline * perturbation_ratio
    plt.fill_between(seasons_baseline, w_baseline - w_baseline_std,
                    w_baseline + w_baseline_std, color='gray', alpha=0.15)

    plt.plot(seasons_baseline, w_baseline, 's--', color='gray',
            linewidth=2, markersize=8, label='Baseline', alpha=0.7)

    # 设置图表属性
    plt.xlabel('Season', fontsize=18)
    plt.ylabel('$W(t)$ Score', fontsize=18)

    # 设置Y轴范围
    min_w = min(all_w_values)
    max_w = max(all_w_values)
    padding = (max_w - min_w) * 0.1
    plt.ylim(min_w - padding, max_w + padding)

    # 设置X轴
    plt.xlim(-0.2, max(seasons) + 0.2)

    # 设置刻度标签字体大小
    plt.tick_params(axis='both', which='major', labelsize=14)

    # 显示图例和网格
    plt.legend(loc="best", fontsize=12, framealpha=0.9)
    plt.grid(True, alpha=0.3, linestyle='--')

    # 调整布局并保存
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\n灵敏度分析图已保存到: {save_path}")
    plt.close('all')


if __name__ == '__main__':
    # Resolve inputs and outputs relative to the script, not the shell directory.
    data_folder = SCRIPT_DIR
    save_path = SCRIPT_DIR / 'omega_sensitivity_W.png'

    # 绘制图表
    plot_omega_sensitivity(data_folder, save_path)

    # 同时保存PDF和SVG格式
    save_path_pdf = SCRIPT_DIR / 'omega_sensitivity_W.pdf'
    save_path_svg = SCRIPT_DIR / 'omega_sensitivity_W.svg'

    plot_omega_sensitivity(data_folder, save_path_pdf)
    plot_omega_sensitivity(data_folder, save_path_svg)

    print("\n所有格式的图表已生成完成！")
