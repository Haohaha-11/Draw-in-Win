# =========================================================================================
# ====================================== 1. 环境设置 =======================================
# =========================================================================================
import matplotlib.pyplot as plt
from pycirclize import Circos
import pandas as pd
import numpy as np
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['axes.unicode_minus'] = False

# =========================================================================================
# ======================================2.颜色库=======================================
# =========================================================================================
COLOR_SCHEMES = {
    1: ["#4DBBD5", "#E64B35", "#00A087", "#3C5488", "#F39B7F", "#8491B0", "#91D1C2", "#DC0000", "#7E6148", "#B09C85",
        "#374E55", "#DF8F44", "#00A1D5", "#B98C46", "#6D9731", "#2878B5", "#9AC9DB", "#C82423", "#FF8884", "#54B345",
        "#05B9E2", "#8983BF", "#C76DA2", "#587848", "#E89132", "#08519C", "#41AB5D", "#A50F15", "#6A51A3", "#238B45",
        "#2171B5", "#6BAED6", "#4292C6", "#238B45", "#74C476"],
}

scheme_index = 20  # 选择配色方案

# =========================================================================================
# ======================================3.绘图函数=======================================
# =========================================================================================
def draw_chord_diagram(df, labels, scheme_id=1):
    N = len(labels)  # 特征总数量

    # 每个扇区的大小 = 行和 + 列和（出度 + 入度）
    row_sums = df.sum(axis=1).values  # 行和（出度）
    col_sums = df.sum(axis=0).values  # 列和（入度）
    sector_sizes = row_sums + col_sums
    sectors_dict = dict(zip(labels, sector_sizes))
    circos = Circos(sectors=sectors_dict, space=0)  # 初始化Circos对象，传入扇区数据

    # 获取颜色方案
    full_color_list = COLOR_SCHEMES.get(scheme_id, COLOR_SCHEMES[1])

    # 创建颜色字典
    color_dict = dict(zip(labels, full_color_list[:N]))

    # 绘制扇区和特征标签
    for sector in circos.sectors:  # 遍历每一个扇区
        # 获取颜色
        fill_color = color_dict.get(sector.name, "#CCCCCC")

        # 绘制半径93到100的主颜色环，带黑色细边框
        sector.rect(r_lim=(93, 100),
                    facecolor=fill_color,
                    edgecolor="black",
                    linewidth=0.5)

        # 绘制外圈阴影圆环
        sector.rect(r_lim=(101, 108),
                    facecolor="#F0F0F0",
                    edgecolor="#D0D0D0",
                    linewidth=0)

        label_text = sector.name  # 获取当前扇区的名称作为特征标签文本

        # 绘制特征标签文本
        sector.text(label_text,
                    r=104,
                    orientation="vertical",
                    size=14,
                    color="black")

    # 绘制连线
    # 为每个节点维护累计偏移量
    # 源节点从0开始，目标节点从行和之后开始
    src_offsets = [0] * N  # 源节点偏移量（出度部分）
    tgt_offsets = row_sums.copy()  # 目标节点偏移量（入度部分，从行和之后开始）

    for i in range(N):  # 遍历行
        for j in range(N):  # 遍历列
            value = df.iloc[i, j]

            # 只有当数值大于0时才绘制连线
            if value > 0:
                source_label = labels[i]  # 获取源节点标签
                target_label = labels[j]  # 获取目标节点标签

                # 计算源节点的起始和结束位置（出度部分）
                src_start = src_offsets[i]
                src_end = src_start + value

                # 计算目标节点的起始和结束位置（入度部分）
                tgt_start = tgt_offsets[j]
                tgt_end = tgt_start + value

                color = color_dict.get(source_label, "#888888")

                # 绘制连线
                circos.link(
                    (source_label, src_start, src_end),  # 源点坐标元组（标签，起点，终点）
                    (target_label, tgt_start, tgt_end),  # 终点坐标元组
                    color=color,  # 连线颜色
                    alpha=0.6,  # 连线透明度
                    direction=0  # 连线方向参数
                )

                # 更新偏移量
                src_offsets[i] = src_end
                tgt_offsets[j] = tgt_end

    fig = circos.plotfig()  # 生成并绘制最终的图形对象

    # 设置标题
    plt.title("Circos Graph",
              fontsize=18,
              pad=80)

    # 保存
    plt.savefig(fr"chord_diagram_{scheme_index}.png", dpi=300, bbox_inches="tight")
    plt.savefig(fr"chord_diagram_{scheme_index}.pdf", bbox_inches="tight")

# =========================================================================================
# ======================================4.执行部分=======================================
# =========================================================================================
def generate_sample_data(n=8):
    """生成示例数据矩阵"""
    # 设置随机种子以保证可重复性
    np.random.seed(42)

    # 创建标签
    labels = [f"Feature_{i+1}" for i in range(n)]

    # 生成随机矩阵（非负值）
    data = np.random.rand(n, n) * 10

    # 将对角线设为0（自己到自己没有连接）
    np.fill_diagonal(data, 0)

    # 可选：使矩阵对称（如果需要无向图）
    # data = (data + data.T) / 2

    # 创建DataFrame
    df = pd.DataFrame(data, index=labels, columns=labels)

    return df, labels


if __name__ == '__main__':
    # 生成示例数据
    df, labels = generate_sample_data(n=8)

    print("生成的数据矩阵：")
    print(df)
    print("\n开始绘制 Circos 图...")

    # 调用绘图函数
    draw_chord_diagram(df, labels, scheme_id=scheme_index)

    print(f"\n图表已保存为 chord_diagram_{scheme_index}.png 和 chord_diagram_{scheme_index}.pdf")
