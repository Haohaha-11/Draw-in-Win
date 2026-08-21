# =========================================================================================
# ====================================== 1. 环境设置 =======================================
# =========================================================================================
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
from scipy import stats
import pandas as pd
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import os
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.size'] = 12

# =========================================================================================
# ======================================2.颜色库=======================================
# =========================================================================================
COLOR_SCHEMES = {
    1: ['#4d4d4d', '#ff9f4b', '#1f77b4'],
}
scheme_index = 40  # 选择配色方案

# =========================================================================================
# ======================================3.绘图函数=========================================
# =========================================================================================
def plot_simulation_results(data):
    # 解包数据
    grp_a_x, grp_a_y, resid_a = data['grp_a']
    grp_b_x, grp_b_y, resid_b = data['grp_b']
    grp_c_x, grp_c_y, resid_c = data['grp_c']
    slope_fit, intercept_fit = data['reg']
    all_resid = data['all_resid']

    colors = COLOR_SCHEMES[1]
    c_a, c_b, c_c = colors[0], colors[1], colors[2]  # 分配颜色
    fig = plt.figure(figsize=(10, 10))  # 创建画布

    # 定义网格布局
    gs = GridSpec(2,  # 行
                  2,  # 列
                  figure=fig,  # 绑定到当前figure
                  hspace=0.05,  # 子图垂直间距
                  wspace=0.05,  # 子图水平间距
                  height_ratios=[1, 5],  # 设置行高比例,顶部边际图占1份,主图占5份
                  width_ratios=[5, 1])  # 设置列宽比例,主图占5份,右侧边际图占1份

    ax_main = fig.add_subplot(gs[1, 0])  # 添加主散点图坐标轴
    ax_top = fig.add_subplot(gs[0, 0], sharex=ax_main)  # 添加顶部KDE图坐标轴,与主图共享X轴
    ax_right = fig.add_subplot(gs[1, 1], sharey=ax_main)  # 添加右侧KDE图坐标轴,与主图共享Y轴

    # 绘制A组散点图
    ax_main.scatter(grp_a_x,  # X坐标
                    grp_a_y,  # Y坐标
                    c=c_a,  # 颜色
                    alpha=0.3,  # 透明度
                    s=20,  # 点的大小
                    label=f'Group A',  # 图例标签
                    edgecolors='none')  # 无边框

    # 绘制B组散点图
    ax_main.scatter(grp_b_x,  # X坐标
                    grp_b_y,  # Y坐标
                    c=c_b,  # 颜色
                    alpha=0.3,  # 透明度
                    s=20,  # 点的大小
                    label=f'Group B',  # 图例标签
                    edgecolors='none')  # 无边框

    # 绘制C组散点图
    ax_main.scatter(grp_c_x,  # X坐标
                    grp_c_y,  # Y坐标
                    c=c_c,  # 颜色
                    alpha=0.6,  # 透明度
                    s=30,  # 点的大小
                    label=f'Group C',  # 图例标签
                    edgecolors='none')  # 无边框

    ax_main.set_xlim(-70, 70)  # 主图X轴范围
    ax_main.set_ylim(-70, 70)  # 主图Y轴范围

    bandwidth = 0.05  # KDE的带宽调节参数

    # 顶部A组X轴数据的密度曲线
    sns.kdeplot(grp_a_x,  # 数据
                ax=ax_top,  # 指定坐标轴
                color=c_a,  # 颜色
                fill=True,  # 填充曲线下方
                alpha=0.3,  # 透明度
                linewidth=1,  # 线宽
                bw_adjust=bandwidth)  # 带宽

    # 顶部图B组X轴数据的密度曲线
    sns.kdeplot(grp_b_x,  # 数据
                ax=ax_top,  # 指定坐标轴
                color=c_b,  # 指定颜色
                fill=True,  # 填充曲线下方
                alpha=0.3,  # 透明度
                linewidth=1,  # 线宽
                bw_adjust=bandwidth)  # 带宽

    # 顶部C组X轴数据的密度曲线
    sns.kdeplot(grp_c_x,  # 数据
                ax=ax_top,  # 坐标轴
                color=c_c,  # 颜色
                fill=True,  # 填充曲线下方
                alpha=0.3,  # 透明度
                linewidth=1,  # 线宽
                bw_adjust=bandwidth)  # 带宽参数

    # 右侧A组Y轴数据的密度曲线
    sns.kdeplot(y=grp_a_y,  # 数据
                ax=ax_right,  # 坐标轴
                color=c_a,  # 颜色
                fill=True,  # 填充
                alpha=0.3,  # 透明度
                linewidth=1,  # 线宽
                bw_adjust=bandwidth)  # 带宽

    # 右侧B组Y轴数据的密度曲线
    sns.kdeplot(y=grp_b_y,  # 数据
                ax=ax_right,  # 坐标轴
                color=c_b,  # 颜色
                fill=True,  # 填充
                alpha=0.3,  # 透明度
                linewidth=1,  # 线宽
                bw_adjust=bandwidth)  # 带宽

    # 右侧C组Y轴数据的密度曲线
    sns.kdeplot(y=grp_c_y,  # 数据
                ax=ax_right,  # 坐标轴
                color=c_c,  # 颜色
                fill=True,  # 填充
                alpha=0.3,  # 透明度
                linewidth=1,  # 线宽
                bw_adjust=bandwidth)  # 带宽

    # 绘制回归线
    x_line = np.linspace(-70, 70, 100)
    y_line = slope_fit * x_line + intercept_fit
    ax_main.plot(x_line, y_line, 'r--', linewidth=2, label='Regression Line')

    # 设置主图标签和图例
    ax_main.set_xlabel('X', fontsize=14, fontweight='bold')
    ax_main.set_ylabel('Y', fontsize=14, fontweight='bold')
    ax_main.legend(loc='upper left', fontsize=10)
    ax_main.grid(True, alpha=0.3)

    # 隐藏顶部和右侧图的刻度标签
    ax_top.set_yticks([])
    ax_right.set_xticks([])
    plt.setp(ax_top.get_xticklabels(), visible=False)
    plt.setp(ax_right.get_yticklabels(), visible=False)

    # 在主图中创建嵌入式坐标轴
    ax_inset = ax_main.inset_axes([0.5,  # 左
                                   0.05,  # 下
                                   0.45,  # 宽
                                   0.25])  # 高

    # 绘制水平箱线图
    bp = ax_inset.boxplot([resid_c, resid_b, resid_a],
                           labels=['C', 'B', 'A'],
                           patch_artist=True,
                           vert=False,  # 设置为水平方向
                           flierprops=dict(marker='d',  # 异常值点设为菱形
                                         markersize=4,  # 异常点大小
                                         markerfacecolor='black',  # 异常点颜色
                                         alpha=0.5),  # 异常点透明度
                           boxprops=dict(linewidth=1.5),  # 箱体边框线宽
                           medianprops=dict(linewidth=1.5,  # 中位数线宽
                                          color='black'),  # 中位数线颜色
                           whiskerprops=dict(linewidth=1.5),  # 线线宽
                           capprops=dict(linewidth=1.5))  # 须线末端横杠线宽

    # 设置箱体颜色
    bp['boxes'][0].set_facecolor(c_c)
    bp['boxes'][1].set_facecolor(c_b)
    bp['boxes'][2].set_facecolor(c_a)

    ax_inset.set_title("Residuals",  # 嵌入图标题
                       fontsize=12,  # 字体大小
                       fontweight='bold')  # 加粗
    ax_inset.set_xticks([])  # 隐藏嵌入图X轴刻度
    ax_inset.set_ylabel("")  # 清空嵌入图Y轴标签

    # 显著性标记函数
    def get_stars(p):
        if p < 0.0001:
            return "****"
        elif p < 0.001:
            return "***"
        elif p < 0.01:
            return "**"
        elif p < 0.05:
            return "*"
        else:
            return "ns"

    # 添加显著性标记函数（水平方向）
    def add_sig(ax, data1, data2, y1, y2, line_num):
        if len(data1) == 0 or len(data2) == 0:
            return
        _, p = stats.ttest_ind(data1, data2)
        star = get_stars(p)
        x_max = max(ax.get_xlim()[1], np.max(np.concatenate([data1, data2])))
        x1_pos = x_max * (1 + 0.05 * line_num)
        x2_pos = x1_pos
        y_line = max(y1, y2)
        ax.plot([x1_pos, x1_pos + x_max * 0.02, x1_pos + x_max * 0.02, x2_pos],
                [y1, y1, y2, y2],
                'k-', linewidth=1.5)
        ax.text(x1_pos + x_max * 0.03,  # X坐标
                (y1 + y2) / 2,  # Y坐标
                star,  # 星号
                ha='left',  # 水平对齐
                va='center',  # 垂直对齐
                rotation=0,  # 不旋转
                fontsize=10,  # 字体大小
                fontweight='bold')  # 字体加粗

    # 添加C和B的显著性标记
    add_sig(ax_inset, resid_c, resid_b, 1, 2, 1)
    # 添加B和A的显著性标记
    add_sig(ax_inset, resid_b, resid_a, 2, 3, 2)
    # 添加C和A的显著性标记
    add_sig(ax_inset, resid_c, resid_a, 1, 3, 3)

    curr_xlim = ax_inset.get_xlim()  # 获取当前嵌入图X轴范围
    # 设置范围，为显著性标记留出空间
    ax_inset.set_xlim(curr_xlim[0], curr_xlim[1] * 1.5)

    # 收集所有坐标轴对象
    all_axes = [ax_main, ax_top, ax_right, ax_inset]

    for ax in all_axes:
        ax.minorticks_on()  # 开启次刻度

    # 保存
    output_dir = os.path.dirname(__file__) if os.path.dirname(__file__) else '.'
    png_path = os.path.join(output_dir, f"{scheme_index}.png")
    pdf_path = os.path.join(output_dir, f"{scheme_index}.pdf")
    plt.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.savefig(pdf_path, bbox_inches='tight')
    print(f"图表已保存到 {png_path} 和 {pdf_path}")
    plt.show()

# =========================================================================================
# ======================================4.执行部分=========================================
# =========================================================================================
if __name__ == "__main__":
    # 生成模拟数据
    np.random.seed(42)  # 设置随机种子以保证可重复性

    # 设置真实的回归参数
    true_slope = 0.8
    true_intercept = 5.0

    # 生成A组数据 (100个点，较小噪声)
    n_a = 100
    x_a = np.random.uniform(-60, 60, n_a)
    y_a = true_slope * x_a + true_intercept + np.random.normal(0, 5, n_a)
    group_a = ['A'] * n_a

    # 生成B组数据 (100个点，中等噪声)
    n_b = 100
    x_b = np.random.uniform(-60, 60, n_b)
    y_b = true_slope * x_b + true_intercept + np.random.normal(0, 8, n_b)
    group_b = ['B'] * n_b

    # 生成C组数据 (80个点，较大噪声)
    n_c = 80
    x_c = np.random.uniform(-60, 60, n_c)
    y_c = true_slope * x_c + true_intercept + np.random.normal(0, 12, n_c)
    group_c = ['C'] * n_c

    # 合并所有数据
    all_x = np.concatenate([x_a, x_b, x_c])
    all_y = np.concatenate([y_a, y_b, y_c])
    all_groups = group_a + group_b + group_c

    # 创建DataFrame
    df = pd.DataFrame({
        'X': all_x,
        'Y': all_y,
        'Group': all_groups
    })

    # 保存数据到Excel文件（可选）
    output_path = os.path.join(os.path.dirname(__file__), "data.xlsx")
    df.to_excel(output_path, index=False)
    print(f"模拟数据已生成并保存到 {output_path}")

    # 线性回归拟合
    slope_fit, intercept_fit, r_value, p_value, std_err = stats.linregress(all_x, all_y)
    print(f"回归模型拟合完成: y = {slope_fit:.4f}x + {intercept_fit:.4f}")
    print(f"R² = {r_value**2:.4f}, p-value = {p_value:.4e}")

    # 数据处理函数
    def process_group(group_name):
        sub_df = df[df['Group'] == group_name]  # 筛选出指定组名的数据子集
        if sub_df.empty:  # 如果为空
            return np.array([]), np.array([]), np.array([])  # 返回空的数组
        x = sub_df['X'].values  # X
        y = sub_df['Y'].values  # Y
        pred = slope_fit * x + intercept_fit  # 根据模型计算预测值
        resid = y - pred  # 计算残差
        return x, y, resid  # 返回X数据,Y数据和残差

    grp_a_x, grp_a_y, resid_a = process_group('A')  # 处理A组数据
    grp_b_x, grp_b_y, resid_b = process_group('B')  # 处理B组数据
    grp_c_x, grp_c_y, resid_c = process_group('C')  # 处理C组数据

    # 将处理后的数据打包成字典
    data_pack = {
        'grp_a': (grp_a_x, grp_a_y, resid_a),  # A组数据包
        'grp_b': (grp_b_x, grp_b_y, resid_b),  # B组数据包
        'grp_c': (grp_c_x, grp_c_y, resid_c),  # C组数据包
        'reg': (slope_fit, intercept_fit),  # 回归参数包
        'all_resid': np.concatenate([resid_a, resid_b, resid_c])  # 合并所有残差用于后续计算范围
    }

    # 调用绘图函数
    plot_simulation_results(data_pack)
