import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, ConnectionPatch
from matplotlib.colors import LinearSegmentedColormap, Normalize
from scipy.stats import pearsonr
from sklearn.preprocessing import StandardScaler

# =========================================================================================
# ====================================== 0. 文件与路径设置 ==================================
# =========================================================================================
SAVE_FOLDER = 'New_Draw_XYL'
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)
print(f"工作目录已设置为: {SAVE_FOLDER}")

# =========================================================================================
# ====================================== 1. 颜色与配置库 ====================================
# =========================================================================================
COLOR_SCHEMES = {
    1: {'cmap': ["#66C2A5", "white", "#FC8D62"],
        'p_colors': {'high': '#D73027', 'med': '#FC8D59', 'low': '#FEE090', 'none': '#E0E0E0'},
        'node': 'dimgray',
        'text': 'black'},
}
SCHEME_ID = 1
config = COLOR_SCHEMES.get(SCHEME_ID, COLOR_SCHEMES[1])

# 创建自定义颜色映射 (绿 -> 白 -> 红)
cmap = LinearSegmentedColormap.from_list("custom_cmap", config['cmap'])
norm = Normalize(vmin=-1, vmax=1)

# =========================================================================================
# ====================================== 2. 辅助工具函数 ====================================
# =========================================================================================
def get_mantel_color(p, p_colors):
    """根据 P 值返回线条颜色"""
    if p <= 0.001: return p_colors['high']
    if p <= 0.01:  return p_colors['med']
    if p <= 0.05:  return p_colors['low']
    return p_colors['none']

def get_dynamic_width(r, r_min, r_max):
    """根据 r 值计算线条宽度 (0.5 - 5.0)"""
    if r_max <= r_min: return 2.0
    val = abs(r)
    val = max(r_min, min(val, r_max))
    normalized = (val - r_min) / (r_max - r_min) if (r_max > r_min) else 0.5
    return 0.5 + normalized * 4.5

def get_sig_label(p):
    """根据 P 值返回显著性星号"""
    if p <= 0.001: return '***'
    if p <= 0.01:  return '**'
    if p <= 0.05:  return '*'
    return ''

# =========================================================================================
# ====================================== 3. 核心绘图函数 ====================================
# =========================================================================================
def plot_mantel_heatmap(variables, scales, corr_r, corr_p, mantel_df):
    text_color = config['text']
    p_colors = config['p_colors']

    n_vars = len(variables)
    n_scales = len(scales)

    # 初始化画布
    fig, ax = plt.subplots(figsize=(20, 14))
    ax.set_aspect('equal')
    ax.axis('off')

    # 布局参数
    # 网格坐标系: x从 0 到 n_vars, y从 0 到 n_vars
    # 这里的 grid_y 实际上我们要倒过来排，让(0,0)在左上角视觉上

    anchor_coords = {} # 存储对角线锚点，用于连接左侧线条

    print("正在绘制热图...")

    # --- 绘制右侧热图 (上三角) ---
    for i in range(n_vars):     # 行 (Variables)
        for j in range(n_vars): # 列 (Variables)
            if j >= i: # 只画对角线及右上方
                # 坐标转换：让 i=0 在最上面
                grid_x = j
                grid_y = (n_vars - 1) - i

                r_val = corr_r[i, j]
                p_val = corr_p[i, j]

                # 1. 绘制方格边框
                rect = Rectangle((grid_x - 0.5, grid_y - 0.5), 1, 1,
                                 fill=False, edgecolor='#E0E0E0', lw=1, zorder=1)
                ax.add_patch(rect)

                # 2. 绘制相关性圆圈
                # 圆的大小可以根据r值的绝对值微调，或者固定大小用颜色区分
                circle_size = 0.45 # 半径
                circle_color = cmap(norm(r_val))

                circle = plt.Circle((grid_x, grid_y), circle_size,
                                    color=circle_color, ec='none', zorder=2)
                ax.add_patch(circle)

                # 3. 绘制显著性标记 (*, **, ***)
                sig_text = get_sig_label(p_val)
                if sig_text:
                    # 如果背景色太深(红或绿)，字体用白色，否则黑色
                    font_c = 'white' if abs(r_val) > 0.4 else 'black'
                    # 稍微调整星号位置居中
                    ax.text(grid_x, grid_y - 0.1, sig_text,
                            ha='center', va='center',
                            color=font_c, fontsize=10, fontweight='bold', zorder=3)

                # 4. 如果是对角线，保存坐标用于连接，并绘制变量名
                if i == j:
                    # 记录连接点 (在方格左侧边缘稍微往左一点)
                    anchor_x = grid_x - 0.5
                    anchor_y = grid_y
                    anchor_coords[variables[i]] = (anchor_x, anchor_y)

                    # 在对角线右上方或者上方写变量名 (图片中是在对角线位置)
                    # 我们稍微往右上方偏移一点，或者直接替换为文本
                    # 这里模仿图片：变量名写在对角线圆圈的上方或右侧，图片显示的是对角线顶部有标签
                    # 为了简单，我们在对角线格子的“右上方”外部写标签
                    ax.text(grid_x, grid_y + 0.6, variables[i],
                            ha='center', va='bottom', rotation=45,
                            fontsize=10, fontweight='bold', color='black')

    # --- 绘制左侧 Scale 节点（45°对角线排列）---
    print("正在绘制网络连线...")
    scale_coords = {}

    # ========== 调整这些参数来控制Scale节点的位置 ==========
    diagonal_spacing = 5.0      # 【增大这个值】让节点之间距离更远，更分散
    start_x = -4.0              # 【调整这个值】控制整体左右位置（负数更靠左）
    start_y = n_vars -6        # 【调整这个值】控制整体上下位置（正数更靠上）
    # =====================================================

    for idx, scale_name in enumerate(scales):
        # 沿45°对角线分布：向右下方移动
        # x向右增加，y向下减少
        offset = idx * diagonal_spacing
        sx = start_x + offset * np.cos(np.radians(-45))  # x向右
        sy = start_y + offset * np.sin(np.radians(-45))  # y向下

        scale_coords[idx] = (sx, sy)

        # 绘制节点 (灰色圆点)
        ax.scatter(sx, sy, s=200, c='gray', ec='white', linewidths=2, zorder=10)

        # 绘制文字 (在节点左侧或左上方)
        ax.text(sx - 0.8, sy, scale_name,
                ha='right', va='center',
                fontsize=12, fontweight='bold', color='black')

    # --- 绘制 Mantel 连接线 ---
    # 准备线条宽度计算
    if not mantel_df.empty:
        r_abs_min = mantel_df['r'].abs().min()
        r_abs_max = mantel_df['r'].abs().max()
        if r_abs_min == r_abs_max: r_abs_min = 0

        # 遍历数据绘制线条
        # mantel_df 结构: ['scale_index', 'var_name', 'r', 'p']
        for _, row in mantel_df.iterrows():
            s_idx = int(row['scale_index'])
            v_name = row['var_name']
            m_r = row['r']
            m_p = row['p']

            if v_name not in anchor_coords: continue

            # 起点 (Scale) 和 终点 (Variable Diagonal)
            start_xy = scale_coords[s_idx]
            end_xy = anchor_coords[v_name] # 对角线方块的左边缘中心

            line_color = get_mantel_color(m_p, p_colors)
            line_width = get_dynamic_width(m_r, r_abs_min, r_abs_max)

            # 只有显著的或者有关系的才画线 (可选项，这里全部画)
            if m_p > 0.05:
                 line_color = p_colors['none']
                 # alpha = 0.2
            else:
                 pass
                 # alpha = 0.8

            # 创建曲线连接
            con = ConnectionPatch(xyA=start_xy, xyB=end_xy,
                                  coordsA="data", coordsB="data",
                                  axesA=ax, axesB=ax,
                                  arrowstyle="-",
                                  connectionstyle="arc3,rad=0.05", # 稍微有点弧度
                                  color=line_color, linewidth=line_width, alpha=0.7, zorder=5)
            ax.add_patch(con)

    # --- 绘制图例 (Legends) ---
    print("正在绘制图例...")

    # 1. Colorbar (Pearson's r)
    # 位置: 右侧 [left, bottom, width, height]
    cax = fig.add_axes([0.80, 0.65, 0.015, 0.2])
    cb = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax)
    cb.set_label("Pearson's r", labelpad=10, fontsize=12)

    # 2. Mantel's p (颜色图例)
    # 在 Colorbar 下方
    legend_x = 0.80
    legend_y_start = 0.55

    fig.text(legend_x, legend_y_start, "Mantel's p", fontsize=12, fontweight='bold')

    p_labels = [('< 0.001', p_colors['high']),
                ('< 0.01', p_colors['med']),
                ('< 0.05', p_colors['low']),
                ('>= 0.05', p_colors['none'])]

    for i, (label, color) in enumerate(p_labels):
        y_pos = legend_y_start - 0.03 - (i * 0.025)
        # 画点
        fig.patches.append(plt.Circle((legend_x + 0.005, y_pos), 0.006,
                                      transform=fig.transFigure, color=color))
        # 画文字
        fig.text(legend_x + 0.02, y_pos - 0.003, label, fontsize=10)

    # 3. Mantel's r (线宽图例)
    legend_y_r = legend_y_start - 0.16
    fig.text(legend_x, legend_y_r, "Mantel's r", fontsize=12, fontweight='bold')

    r_sizes = [0.1, 0.25, 0.5] # 示例刻度
    # 实际上我们应该取 r_max 和 r_min 的中间值
    if not mantel_df.empty:
        r_step = (r_abs_max - r_abs_min) / 3
        r_sizes = [r_abs_min, r_abs_min + r_step, r_abs_max]

    for i, r_s in enumerate(r_sizes):
        y_pos = legend_y_r - 0.03 - (i * 0.025)
        lw = get_dynamic_width(r_s, r_abs_min, r_abs_max)
        # 画线
        line_len = 0.02
        fig.lines.append(plt.Line2D([legend_x, legend_x + line_len], [y_pos, y_pos],
                                    transform=fig.transFigure, color='black', linewidth=lw))
        # 文字
        fig.text(legend_x + line_len + 0.01, y_pos - 0.003, f"{r_s:.2f}", fontsize=10)

    # 保存图片
    save_path = os.path.join(SAVE_FOLDER, 'mantel_heatmap.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"绘图完成！图片已保存至: {save_path}")

# =========================================================================================
# ====================================== 4. 主程序入口 ======================================
# =========================================================================================
if __name__ == "__main__":
    # ------------------ 数据准备 (模拟数据) ------------------
    # 由于没有 data.xlsx，这里生成与图片结构相似的随机数据
    # 假设有 18 个变量 (Variables) 和 4 个尺度 (Scales)

    np.random.seed(42) # 固定随机种子

    # 1. 变量名称
    variables = ['CO2', 'WF', 'EF', 'LF', 'LUC', 'N', 'P', 'PM2.5', 'O3', 'ED',
                 'EC', 'IN', 'EM', 'EN', 'SE', 'GE', 'LE', 'NU']
    scales = ['Landscape scale', 'National scale', 'Continental scale', 'Global scale']

    # 2. 生成相关性矩阵数据 (Heatmap数据)
    n_vars = len(variables)
    # 生成一个随机的相关系数矩阵
    # 先生成随机数据
    dummy_data = np.random.rand(100, n_vars)
    df_vars = pd.DataFrame(dummy_data, columns=variables)

    # 计算 Pearson R 和 P
    corr_matrix = df_vars.corr()
    p_matrix = np.zeros((n_vars, n_vars))

    # 计算 p-value 矩阵
    for i in range(n_vars):
        for j in range(n_vars):
            _, p = pearsonr(df_vars.iloc[:, i], df_vars.iloc[:, j])
            p_matrix[i, j] = p

    corr_r = corr_matrix.values
    corr_p = p_matrix

    # 3. 生成 Mantel Test 结果数据 (连线数据)
    # 这是一个列表，包含: 哪个Scale, 连哪个Variable, r值多少, p值多少
    mantel_results = []

    for s_idx, scale in enumerate(scales):
        for v_name in variables:
            # 随机生成 Mantel r 和 p (模拟)
            # 这里的 r 我们设小一点，通常 Mantel r 不会特别高
            m_r = np.random.uniform(0.01, 0.5)
            # 随机 p 值，让部分显著
            m_p = np.random.choice([0.001, 0.005, 0.04, 0.2, 0.6], p=[0.1, 0.1, 0.1, 0.3, 0.4])

            mantel_results.append({
                'scale_index': s_idx,
                'scale_name': scale,
                'var_name': v_name,
                'r': m_r,
                'p': m_p
            })

    mantel_df = pd.DataFrame(mantel_results)

    # ------------------ 执行绘图 ------------------
    plot_mantel_heatmap(variables, scales, corr_r, corr_p, mantel_df)