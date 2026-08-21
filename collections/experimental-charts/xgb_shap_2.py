# =========================================================================================
# ====================================== 1. 环境设置 =======================================
# =========================================================================================
import pandas as pd
import numpy as np
import xgboost
import shap
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as ticker
from matplotlib.cm import ScalarMappable
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from shap.plots import beeswarm
from sklearn.model_selection import GridSearchCV

# =========================================================================================
# ======================================2.颜色库=======================================
# =========================================================================================
COLOR_SCHEMES = {
    1: ["blue", "#4B0082", "red"],
}

# 设置当前使用的颜色方案
CURRENT_SCHEME_ID = 15

# =========================================================================================
# ======================================3.特征重要性条形图和径向图/玫瑰图绘制函数=======================================
# =========================================================================================
def draw_bar_and_radial(sorted_features, sorted_shap_values, bar_colors, cmap, color_norm):
    fig = plt.figure(figsize=(16, 15))  # 创建画布

    # 画布边距
    left_margin, right_margin, bottom_margin, top_margin = 0.08, 0.08, 0.12, 0.12

    # 颜色条宽度
    colorbar_width = 0.02

    # 计算绘图区域的底部位置和高度
    plot_bottom = bottom_margin
    plot_height = 1.0 - bottom_margin - top_margin

    # 颜色条的左侧位置
    cbar_left = left_margin

    # 条形图的左侧位置
    main_ax_left = cbar_left + colorbar_width + 0.04

    # 条形图的宽度
    main_ax_width = 1.0 - main_ax_left - right_margin

    # 添加颜色条的坐标轴
    ax_cbar = fig.add_axes([cbar_left, plot_bottom, colorbar_width, plot_height])

    # 创建ScalarMappable对象
    sm = ScalarMappable(cmap=cmap, norm=color_norm)

    # 绘制颜色条
    cbar = fig.colorbar(sm, cax=ax_cbar, orientation='vertical')
    cbar.set_label('', size=18, labelpad=5)
    cbar.set_ticks([])

    # 颜色条下方文本
    ax_cbar.text(0.5,
                 -0.01,
                 'Low',
                 transform=ax_cbar.transAxes,
                 ha='center',
                 va='top',
                 fontsize=24)

    # 去掉颜色条边框
    cbar.outline.set_visible(False)

    # 颜色条标题
    ax_cbar.text(-1.4,
                 0.5,
                 'Contribution for CEs ($10^4$ t)',
                 transform=ax_cbar.transAxes,
                 fontsize=24,
                 rotation=90,
                 va='center')

    # 添加条形图坐标轴
    ax_bar = fig.add_axes([main_ax_left, plot_bottom, main_ax_width, plot_height])

    ax_bar.xaxis.tick_bottom()  # 条形图x轴刻度位置
    ax_bar.xaxis.set_label_position("bottom")  # 设置x轴标签位置

    # 反转x轴方向
    ax_bar.invert_xaxis()

    # 绘制水平条形图
    ax_bar.barh(y=range(len(sorted_features)),  # Y坐标
                width=sorted_shap_values,  # 水平条形宽度
                color=bar_colors,  # 条形颜色
                height=0.6)  # 条形高度

    # 反转y轴方向，使最重要的特征排在顶部
    ax_bar.invert_yaxis()

    # 设置x轴标签
    ax_bar.set_xlabel('Contribution for CEs ($10^4$ t)', size=24, labelpad=20)

    # 移除y轴刻度
    ax_bar.set_yticks([])

    # 去掉左侧和顶部边框
    ax_bar.spines[['left', 'top']].set_visible(False)

    # 设置右侧边框位置
    ax_bar.spines['right'].set_position(('data', 0))

    # 显示边框
    ax_bar.spines['right'].set_visible(True)
    ax_bar.spines['bottom'].set_visible(True)

    # 设置x轴主刻度样式
    ax_bar.tick_params(axis='x',  # X轴
                       which='major',  # 应用于主刻度
                       direction='in',  # 朝内
                       labelsize=24,  # 刻度标签字体大小
                       length=6,  # 刻度线长度
                       pad=8)  # 标签与刻度线之间的距离

    # 子图标签
    ax_bar.text(0.02,
                0.98,
                '(a)',
                transform=ax_bar.transAxes,
                fontsize=30,
                weight='bold',
                ha='left',
                va='top')

    # 径向图/玫瑰图设置
    num_vars = len(sorted_features)

    inset_left = main_ax_left - 0.15  # 径向图/玫瑰图的左侧位置
    inset_bottom = plot_bottom - 0.05  # 径向图/玫瑰图的底部位置
    inset_size = min(main_ax_width, plot_height) * 0.85  # 径向图/玫瑰图的大小

    # 定义径向图/玫瑰图的矩形区域
    inset_ax_rect = [inset_left, inset_bottom, inset_size, inset_size]

    # 添加坐标轴作为径向图/玫瑰图
    ax_radial_inset = fig.add_axes(inset_ax_rect, projection='polar')

    # 背景透明
    ax_radial_inset.patch.set_alpha(0)

    # 计算每个特征占比百分比
    percentages = (sorted_shap_values / sorted_shap_values.sum()) * 100

    # 根据占比计算每个扇形的宽度
    widths = (sorted_shap_values / sorted_shap_values.sum()) * 2 * np.pi

    # 设置基础长度、增量和彩色环宽度
    base_length, fixed_increment, colored_ring_width = 3.0, 0.5, 2.0

    # 每个扇形的总长度
    total_lengths = [base_length + i * fixed_increment for i in range(num_vars)]

    # 内部灰色部分的高度
    inner_heights = [max(0, tl - colored_ring_width) for tl in total_lengths]

    # 定义内部颜色列表
    inner_colors = ['#EAEAEA', '#FFFFFF'] * (num_vars // 2 + 1)
    inner_colors = inner_colors[:num_vars]

    # 偏移量，使图形从12点钟方向开始
    one_oclock_offset = np.pi / 2

    # 每个扇形的起始角度
    thetas = np.cumsum([0] + widths[:-1].tolist()) - one_oclock_offset

    # 绘制内部灰色扇形
    ax_radial_inset.bar(x=thetas,  # 条形的起始角度位置
                        height=inner_heights,  # 内部灰色部分的长度
                        width=widths,  # 指定每个条形的角宽度
                        color=inner_colors,  # 条形的填充颜色
                        align='edge',  # 对齐方式为边缘对齐
                        edgecolor='white',  # 条形边框的颜色为白色
                        linewidth=1.5)  # 条形边框线的宽度

    # 绘制外部彩色环形
    ax_radial_inset.bar(x=thetas,
                        height=[colored_ring_width] * num_vars,
                        width=widths,
                        bottom=inner_heights,
                        color=bar_colors,
                        align='edge',
                        edgecolor='white',
                        linewidth=1.5)

    ax_radial_inset.set_yticklabels([])  # 移除径向图的y轴标签
    ax_radial_inset.set_xticklabels([])  # 移除径向图的x轴标签

    # 隐藏极坐标轴的脊柱
    ax_radial_inset.spines['polar'].set_visible(False)

    # 关闭网格
    ax_radial_inset.grid(False)

    ax_radial_inset.set_theta_zero_location('N')  # 正北方向
    ax_radial_inset.set_theta_direction(-1)  # 顺时针
    ax_radial_inset.set_ylim(0, max(total_lengths) + 2)  # 半径范围

# =========================================================================================
# ======================================4.SHAP蜂巢图函数=======================================
# =========================================================================================
def draw_native_beeswarm(shap_values, X, cmap):
    plt.figure(figsize=(16, 15))  # 创建画布

    # 绘制蜂巢图
    shap.summary_plot(shap_values,  # SHAP值数据
                      X,  # 对应的特征矩阵数据
                      plot_type="dot",  # 蜂巢图
                      show=False,  # 不立即显示
                      cmap=cmap)  # 颜色映射

    # 如果存在多个坐标轴
    if len(plt.gcf().axes) > 1:
        cbar_ax = plt.gcf().axes[-1]  # 获取颜色条坐标轴
        cbar_ax.set_ylabel('Feature Value', size=16, rotation=-90, labelpad=20)  # 设置颜色条标签
        cbar_ax.tick_params(labelsize=14)  # 设置颜色条刻度标签大小

    # 调整布局
    plt.tight_layout()

# =========================================================================================
# ======================================5.无Y轴标签的SHAP蜂巢图的函数=======================================
# =========================================================================================
def draw_beeswarm_no_labels(shap_values, X, cmap):
    # 创建画布
    plt.figure(figsize=(16, 15))

    # 绘制蜂巢图
    shap.summary_plot(shap_values,
                      X,
                      plot_type="dot",
                      show=False,
                      cmap=cmap)

    # 获取当前坐标轴
    ax_third_plot = plt.gca()

    # 移除y轴刻度标签（特征名）
    ax_third_plot.set_yticklabels([])
    ax_third_plot.set_ylabel('')

    # x轴标题
    ax_third_plot.set_xlabel("SHAP Value (impact on model output)", fontsize=18)

    # x轴刻度标签
    ax_third_plot.tick_params(axis='x', labelsize=14)

    # 处理颜色条（如果存在）
    if len(plt.gcf().axes) > 1:
        cbar_ax_third = plt.gcf().axes[-1]  # 获取当前图形对象列表中的最后一个坐标轴
        cbar_ax_third.set_ylabel('Feature Value',  # Y轴名
                                 size=16,  # 字体大小
                                 rotation=-90,  # 旋转
                                 labelpad=20)  # 文本与坐标轴之间的距离
        cbar_ax_third.tick_params(labelsize=14)  # 字体大小

    # 调整布局
    plt.tight_layout()

# =========================================================================================
# ======================================6.特征重要性条形图+蜂巢图+玫瑰图组合图绘制函数=======================================
# =========================================================================================
def draw_combined_plot(sorted_features, sorted_shap_values, shap_values, bar_colors, cmap, color_norm):
    # 创建画布 - 调整为适合窗口的大小
    fig_combined = plt.figure(figsize=(16, 10))

    # 定义边距和间距参数
    left_margin, right_margin, bottom_margin, top_margin = 0.05, 0.05, 0.02, 0.1

    space_between = 0.01  # 左右子图之间的间距
    plot_bottom = bottom_margin  # 绘图区域的底部
    plot_height = 1 - bottom_margin - top_margin  # 绘图区域的高度
    total_plot_width = 1 - left_margin - right_margin - space_between  # 宽度

    # 左右子图宽度分配
    left_plot_width = total_plot_width * 0.45
    right_plot_width = total_plot_width * 0.55

    # 颜色条参数
    colorbar_width = 0.015
    cbar_left = left_margin

    # 颜色条坐标轴
    ax_cbar_new = fig_combined.add_axes([cbar_left, plot_bottom, colorbar_width, plot_height])

    # 创建ScalarMappable对象，用于颜色映射
    sm = ScalarMappable(cmap=cmap, norm=color_norm)

    # 绘制颜色条
    cbar = fig_combined.colorbar(sm,
                                 cax=ax_cbar_new,
                                 orientation='vertical')

    # 设置标签
    cbar.set_label('', size=18, labelpad=5)

    # 移除刻度
    cbar.set_ticks([])

    # 设置刻度位置
    cbar.ax.text(0.5, -0.01, 'Low', transform=cbar.ax.transAxes, ha='center', va='top', fontsize=14)
    cbar.ax.text(0.5, 1.01, 'High', transform=cbar.ax.transAxes, ha='center', va='bottom', fontsize=14)

    # 去掉边框
    cbar.outline.set_visible(False)

    # 颜色条标题
    ax_cbar_new.text(-1.4,  # x坐标
                     0.5,  # y坐标
                     'Contribution for CEs ($10^4$ t)',  # 文本内容
                     transform=ax_cbar_new.transAxes,  # 使用相对坐标
                     fontsize=16,  # 字体大小
                     rotation=90,  # 旋转90度
                     va='center')

    # 左侧条形图的位置
    main_ax_left = cbar_left + colorbar_width + 0.05

    # 添加条形图坐标轴
    ax_bar_new = fig_combined.add_axes([main_ax_left,  # 左
                                        plot_bottom,  # 下
                                        left_plot_width,  # 宽度
                                        plot_height])  # 高度

    # x轴刻度在底部
    ax_bar_new.xaxis.tick_bottom()

    # 设置x轴标签
    ax_bar_new.xaxis.set_label_position("bottom")

    # 反转x轴
    ax_bar_new.invert_xaxis()

    # 绘制水平条形
    ax_bar_new.barh(y=range(len(sorted_features)),  # 数据
                    width=sorted_shap_values,  # 条形宽度
                    color=bar_colors,  # 颜色
                    height=0.6)  # 条形高度

    # 反转y轴
    ax_bar_new.invert_yaxis()

    # 设置x轴标题
    ax_bar_new.set_xlabel('Contribution for CEs ($10^4$ t)', size=16, labelpad=20)

    # 移除y轴刻度
    ax_bar_new.set_yticks([])

    # 去掉左侧和顶部边框
    ax_bar_new.spines[['left', 'top']].set_visible(False)

    # 设置右侧边框
    ax_bar_new.spines['right'].set_position(('data', 0))
    ax_bar_new.spines['right'].set_visible(True)
    ax_bar_new.spines['bottom'].set_visible(True)

    # 主刻度样式
    ax_bar_new.tick_params(axis='x',  # 轴
                           which='major',  # 主刻度
                           direction='in',  # 朝内
                           labelsize=14,  # 标签大小
                           length=6,  # 刻度长度
                           pad=8)  # 间距

    # 图标签
    ax_bar_new.text(0.02,  # x坐标
                    0.98,  # y坐标
                    '(a)',  # 文本内容
                    transform=ax_bar_new.transAxes,  # 使用相对坐标
                    fontsize=18,  # 字体大小
                    weight='bold',  # 字体加粗
                    ha='left',  # 水平左对齐
                    va='top')  # 垂直顶部对齐

    # 径向图设置
    num_vars = len(sorted_features)  # 特征数量

    # 百分比
    percentages = (sorted_shap_values / sorted_shap_values.sum()) * 100

    # 每个扇形的宽度
    widths = (sorted_shap_values / sorted_shap_values.sum()) * 2 * np.pi

    # 设置基础长度、增量和彩色环宽度
    base_length, fixed_increment, colored_ring_width = 3.0, 0.5, 2.0

    # 每个扇形的总长度
    total_lengths = [base_length + i * fixed_increment for i in range(num_vars)]

    # 内部灰色部分的高度
    inner_heights = [max(0, tl - colored_ring_width) for tl in total_lengths]

    # 定义内部颜色列表
    inner_colors = ['#EAEAEA', '#FFFFFF'] * (num_vars // 2 + 1)
    inner_colors = inner_colors[:num_vars]

    # 偏移量
    one_oclock_offset = np.pi / 2

    # 每个扇形的起始角度
    thetas = np.cumsum([0] + widths[:-1].tolist()) - one_oclock_offset

    # 径向图位置
    inset_left = main_ax_left - 0.08
    inset_bottom = plot_bottom - 0.03
    inset_size = min(left_plot_width, plot_height) * 0.75

    # 定义插图矩形区域
    inset_ax_rect = [inset_left, inset_bottom, inset_size, inset_size]

    # 添加径向极坐标轴
    ax_radial_inset_new = fig_combined.add_axes(inset_ax_rect, projection='polar')

    # 背景透明
    ax_radial_inset_new.patch.set_alpha(0)

    # 绘制内部背景条
    ax_radial_inset_new.bar(x=thetas,  # 角度
                            height=inner_heights,  # 高度
                            width=widths,  # 宽度
                            color=inner_colors,  # 颜色
                            align='edge',  # 对齐方式
                            edgecolor='white',  # 边缘颜色
                            linewidth=1.5)  # 线宽

    # 绘制外部彩色条
    ax_radial_inset_new.bar(x=thetas,  # 角度
                            height=[colored_ring_width] * num_vars,  # 高度
                            width=widths,  # 宽度
                            bottom=inner_heights,  # 底部起始位置
                            color=bar_colors,  # 颜色
                            align='edge',  # 对齐方式
                            edgecolor='white',  # 边缘颜色
                            linewidth=1.5)  # 线宽

    # 移除标签
    ax_radial_inset_new.set_yticklabels([])
    ax_radial_inset_new.set_xticklabels([])

    # 隐藏脊柱
    ax_radial_inset_new.spines['polar'].set_visible(False)

    # 隐藏网格
    ax_radial_inset_new.grid(False)

    ax_radial_inset_new.set_theta_zero_location('N')  # 正北
    ax_radial_inset_new.set_theta_direction(-1)  # 顺时针
    ax_radial_inset_new.set_ylim(0, max(total_lengths) + 2)  # 半径范围

    # 右侧蜂巢图位置
    right_plot_left = main_ax_left + left_plot_width + space_between

    # 添加蜂巢图坐标轴
    ax_beeswarm = fig_combined.add_axes([right_plot_left, plot_bottom, right_plot_width, plot_height])

    # 绘制蜂巢图
    beeswarm(shap_values,  # 数据
             max_display=len(sorted_features),  # 最大显示特征数
             ax=ax_beeswarm,  # 指定坐标轴
             show=False,  # 不立即显示
             color=cmap,  # 颜色映射
             plot_size=None)  # 不自动调整大小

    ax_beeswarm.set_yticklabels([])  # 移除y轴标签
    ax_beeswarm.set_ylabel('')  # 移除y轴标题

    # 设置x轴标题
    ax_beeswarm.set_xlabel('SHAP Value (impact on model output)', fontsize=16, labelpad=20)

    # x轴刻度标签大小
    ax_beeswarm.tick_params(axis='x', labelsize=14)

    # 子图标签
    ax_beeswarm.text(0.02, 0.98, '(b)', transform=ax_beeswarm.transAxes,
                     fontsize=18, weight='bold', ha='left', va='top')

    # 处理颜色条
    if len(fig_combined.axes) > 4:
        cbar_ax_right = fig_combined.axes[-1]
        cbar_ax_right.set_ylabel('Feature Value', size=16, rotation=-90, labelpad=30)

        # 刻度标签大小
        cbar_ax_right.tick_params(labelsize=14)

# =========================================================================================
# ======================================4.执行部分=======================================
# =========================================================================================
if __name__ == '__main__':
    # 生成模拟数据
    np.random.seed(42)
    n_samples = 500
    n_features = 10

    # 生成特征数据
    X = np.random.randn(n_samples, n_features)

    # 生成目标变量（带有一些非线性关系）
    y = (2 * X[:, 0] + 3 * X[:, 1]**2 - 1.5 * X[:, 2] +
         0.5 * X[:, 3] * X[:, 4] + np.random.randn(n_samples) * 0.5)

    # 创建特征名称
    feature_names = [f'Feature_{i+1}' for i in range(n_features)]

    # 转换为DataFrame
    X = pd.DataFrame(X, columns=feature_names)
    y = pd.Series(y, name='Target_y')

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 转换为DataFrame
    X_train_df = pd.DataFrame(X_train, columns=feature_names)
    X_test_df = pd.DataFrame(X_test, columns=feature_names)

    # 初始化回归模型
    xgb_reg = xgboost.XGBRegressor(objective='reg:squarederror', random_state=42)

    # 定义参数网格
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1, 0.2],
        'subsample': [0.8, 1.0],
        'colsample_bytree': [0.8, 1.0]
    }

    # 网格搜索
    grid_search = GridSearchCV(estimator=xgb_reg, param_grid=param_grid, cv=5,
                               scoring='neg_mean_squared_error', n_jobs=-1, verbose=2)
    grid_search.fit(X_train_df, y_train)

    # 获取搜索到的最佳模型
    best_model = grid_search.best_estimator_
    print(f"找到的最佳参数: {grid_search.best_params_}")

    # 最佳模型
    model = best_model

    # 创建SHAP树解释器对象，用于解释模型
    explainer = shap.TreeExplainer(model)

    # 计算测试集数据的SHAP值
    shap_values = explainer(X_test_df)

    # 计算所有样本SHAP绝对值的平均值，衡量特征整体重要性
    mean_abs_shap = np.abs(shap_values.values).mean(axis=0)

    # 创建包含特征重要性数值的Series，索引为特征名
    shap_series = pd.Series(mean_abs_shap, index=feature_names)

    # 对特征重要性进行降序排序
    shap_series.sort_values(ascending=False, inplace=True)

    # 获取排序后的特征名和SHAP值
    sorted_features = shap_series.index.tolist()
    sorted_shap_values = shap_series.values

    # 设置颜色映射
    cmap = plt.cm.get_cmap('RdYlBu_r')
    color_norm = mcolors.Normalize(vmin=sorted_shap_values.min(), vmax=sorted_shap_values.max())

    # 生成每个条形对应的具体颜色值
    bar_colors = cmap(color_norm(sorted_shap_values))

    print(pd.DataFrame(shap_values.values[:5, :3], columns=feature_names[:3]).round(4))
    print("\n测试集特征平均重要性 (Mean |SHAP|):")
    print(np.round(sorted_shap_values, 4))

    # 只绘制组合图
    draw_combined_plot(sorted_features, sorted_shap_values, shap_values, bar_colors, cmap, color_norm)

    plt.show()
