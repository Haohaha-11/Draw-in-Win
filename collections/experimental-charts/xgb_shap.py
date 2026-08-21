import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import shap
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.colors as mcolors
from matplotlib import cm
import matplotlib
import joblib
import os

# =========================================================================================
# ====================================== 1. 配置参数 =======================================
# =========================================================================================
DATA_PATH = r'simulated_data.xlsx'  # 原始数据路径

# =========================================================================================
# ====================================== 2. 颜色库 =======================================
# =========================================================================================
COLOR_SCHEMES = {
    1: 'Spectral_r',
    2: 'RdYlBu_r',
    3: 'coolwarm',
}
SHAP_COLOR_INDEX = 1  # 蜂巢图的配色
POLAR_COLOR_INDEX = 1  # 极坐标玫瑰图的配色

# =========================================================================================
# ====================================== 3. 子图布局控制 =======================================
# =========================================================================================
# 蜂巢图的布局控制
SHAP_X = 0.05  # 蜂巢图左下角的 X 坐标
SHAP_Y = 0.15  # 蜂巢图左下角的 Y 坐标
SHAP_W = 0.55  # 蜂巢图的宽度
SHAP_H = 0.75  # 蜂巢图的高度

# 极坐标图的布局控制
POLAR_X = 0.50  # 极坐标图左下角的 X 坐标
POLAR_Y = 0.1  # 极坐标图左下角的 Y 坐标
POLAR_SIZE = 0.75  # 极坐标图的整体尺寸
POLAR_BOTTOM_VAL = 15  # 极坐标图内圈空心圆的半径
POLAR_GAP = 2.0  # 内圈实线与柱子之间的间隔大小

# =========================================================================================
# ====================================== 4. 数据生成函数 =======================================
# =========================================================================================
def generate_sample_data():
    """生成模拟数据并保存为Excel文件"""
    np.random.seed(42)

    # 定义特征名称（模拟地理环境指标）
    feature_names = [
        'SPI', 'Curv', 'Plan', 'Ele', 'Profile', 'Dist', 'Distan',
        'rain', 'POI', 'TWI', 'STI', 'NDVI', 'Lith', 'rivers', 'TRI', 'RDLS', 'Slope'
    ]

    n_samples = 1000
    n_features = len(feature_names)

    # 生成特征数据
    X = np.zeros((n_samples, n_features))
    for i in range(n_features):
        if i < 5:  # 高重要性特征
            X[:, i] = np.random.randn(n_samples) * 2 + np.random.uniform(-1, 1)
        elif i < 10:  # 中等重要性特征
            X[:, i] = np.random.randn(n_samples) * 1.5 + np.random.uniform(-0.5, 0.5)
        else:  # 低重要性特征
            X[:, i] = np.random.randn(n_samples) * 1 + np.random.uniform(-0.3, 0.3)

    # 生成目标变量（复杂非线性关系）
    y = (3.5 * X[:, 0] +
         2.8 * X[:, 1] ** 2 +
         2.2 * X[:, 2] * X[:, 3] +
         1.8 * np.sin(X[:, 4]) +
         1.5 * X[:, 5] +
         1.2 * X[:, 6] +
         1.0 * X[:, 7] +
         0.8 * X[:, 8] +
         0.6 * X[:, 9] +
         0.5 * X[:, 10] +
         0.4 * X[:, 11] +
         0.3 * X[:, 12] +
         0.25 * X[:, 13] +
         0.2 * X[:, 14] +
         0.15 * X[:, 15] +
         0.1 * X[:, 16] +
         np.random.randn(n_samples) * 0.8)

    # 创建DataFrame
    df = pd.DataFrame(X, columns=feature_names)
    df['Target'] = y

    # 保存为Excel
    df.to_excel(DATA_PATH, index=False)
    print(f"[OK] 模拟数据已生成并保存到: {DATA_PATH}")
    print(f"  数据形状: {df.shape}")
    print(f"  特征列表: {', '.join(feature_names)}")

    return df

# =========================================================================================
# ====================================== 5. 绘图函数 =======================================
# =========================================================================================
def draw_shap_analysis_plot(shap_values, X_val, df_polar):
    """绘制SHAP分析组合图"""
    fig = plt.figure(figsize=(20, 10))  # 创建画布

    # 获取配色
    shap_cmap_name = COLOR_SCHEMES.get(SHAP_COLOR_INDEX, 'coolwarm')  # 蜂巢图
    cmap_shap = matplotlib.colormaps[shap_cmap_name]
    polar_cmap_name = COLOR_SCHEMES.get(POLAR_COLOR_INDEX, 'Spectral_r')  # 极坐标图
    cmap_polar = matplotlib.colormaps[polar_cmap_name]

    # =======================
    # 左图：SHAP蜂巢图
    # =======================
    # 定义左图的位置参数
    ax1_pos = [SHAP_X,  # 左
               SHAP_Y,  # 下
               SHAP_W,  # 宽
               SHAP_H]  # 高

    # 在画布上添加左图坐标轴
    ax1 = fig.add_axes(ax1_pos)
    plt.sca(ax1)  # 将当前绘图区域切换到 ax1

    # 绘制蜂巢图
    shap.summary_plot(shap_values,  # SHAP 值
                      X_val,  # 特征数据
                      show=False,  # 不立即显示
                      plot_type="dot",  # 点图
                      max_display=len(df_polar),  # 最大显示的特征数量
                      sort=False,  # 关闭自动排序
                      cmap=cmap_shap)  # 颜色映射方案

    ax1.set_title("SHAP Factor Summary Plot", fontsize=16)  # 设置标题

    # 子图编号
    ax1.text(0.5,  # X 坐标
             -0.1,  # Y 坐标
             "(a)",  # 文本
             transform=ax1.transAxes,  # 坐标系
             ha='center',  # 水平对齐
             fontsize=16)  # 字体大小

    # =======================
    # 右图：极坐标图
    # =======================
    # 位置参数
    ax2_pos = [POLAR_X,  # 左
               POLAR_Y,  # 下
               POLAR_SIZE,  # 宽
               POLAR_SIZE]  # 高

    # 在画布上添加极坐标轴
    ax2 = fig.add_axes(ax2_pos, projection='polar')

    # 计算极坐标参数
    N = len(df_polar)
    theta = np.linspace(0, 2 * np.pi, N, endpoint=False)
    width = 2 * np.pi / N

    # 颜色映射
    norm = mcolors.Normalize(vmin=df_polar['Value'].min(), vmax=df_polar['Value'].max())
    colors = cmap_polar(norm(df_polar['Value']))

    # 绘制内圈圆
    circle_theta = np.linspace(0, 2 * np.pi, 100)
    circle_r = np.full_like(circle_theta, POLAR_BOTTOM_VAL)

    # 绘制极坐标柱状图
    bars = ax2.bar(theta,  # 每个柱子的角度中心位置
                   df_polar['Value'],  # 每个柱子的长度
                   width=width,  # 柱子的宽度
                   bottom=POLAR_BOTTOM_VAL + POLAR_GAP,  # 柱子底部的起始半径
                   color=colors,  # 填充颜色
                   edgecolor='black',  # 边框的颜色
                   linewidth=0.8)  # 边框线条的宽度

    ax2.plot(circle_theta,  # 角度坐标
             circle_r,  # 半径
             color='black',  # 线条的颜色
             linewidth=1,  # 线条的宽度
             linestyle='-')  # 样式

    ax2.set_theta_zero_location("N")  # 极坐标的零度方向为正北
    ax2.set_theta_direction(-1)  # 极坐标的角度增长方向为顺时针
    ax2.set_axis_off()  # 关闭默认的坐标轴

    # 遍历每个柱子，添加数值和标签
    for angle, value, feature, raw_val in zip(theta, df_polar['Value'], df_polar['Feature'], df_polar['Raw']):
        angle_deg = np.degrees(angle)  # 将弧度转换为角度

        # 计算半径 (基础 + 间隔 + 柱子长度)
        visual_top = POLAR_BOTTOM_VAL + POLAR_GAP + value
        pos_outer = visual_top + 2

        # 标签文本
        label_text = f"{feature}\n{value:.2f}%"

        # 如果在右半圆
        if 0 <= angle_deg < 180:
            rotation = 90 - angle_deg  # 文本旋转角度
            alignment_ha = 'left'  # 水平对齐
            alignment_va = 'center'  # 垂直对齐
        else:
            rotation = 270 - angle_deg
            alignment_ha = 'right'
            alignment_va = 'center'

        ax2.text(angle,  # 角度坐标
                 pos_outer,  # 半径坐标
                 label_text,  # 文本内容
                 ha=alignment_ha,  # 水平对齐
                 va=alignment_va,  # 垂直对齐
                 rotation=rotation,  # 文本旋转角度
                 rotation_mode='anchor',  # 旋转模式
                 fontsize=9,  # 字体大小
                 fontweight='bold',  # 字体粗细
                 color='black')  # 字体颜色

    # 在右图中插入一个子坐标轴用于颜色条
    cax = ax2.inset_axes([0.48, 0.35, 0.04, 0.3], transform=ax2.transAxes)
    sm = cm.ScalarMappable(cmap=cmap_polar, norm=norm)  # 创建 ScalarMappable 对象
    sm.set_array([])
    cbar = plt.colorbar(sm, cax=cax)
    cbar.set_label('SHAP Value %', fontsize=10)

    ax2.text(0.5,
             -0.05,
             "(b)",
             transform=ax2.transAxes,
             ha='center',
             fontsize=16)

    # 保存
    plt.savefig(fr'result_S{SHAP_COLOR_INDEX}_P{POLAR_COLOR_INDEX}.png', dpi=300, bbox_inches='tight')
    plt.savefig(fr'result_S{SHAP_COLOR_INDEX}_P{POLAR_COLOR_INDEX}.pdf', bbox_inches='tight')
    print(f"\n[OK] 图表已保存:")
    print(f"  - result_S{SHAP_COLOR_INDEX}_P{POLAR_COLOR_INDEX}.png")
    print(f"  - result_S{SHAP_COLOR_INDEX}_P{POLAR_COLOR_INDEX}.pdf")
    plt.show()

# =========================================================================================
# ====================================== 6. 主执行部分 =======================================
# =========================================================================================
if __name__ == '__main__':
    print("=" * 80)
    print("XGBoost + SHAP 分析程序")
    print("=" * 80)

    # 检查数据文件是否存在，不存在则生成
    if not os.path.exists(DATA_PATH):
        print(f"\n数据文件不存在，正在生成模拟数据...")
        df = generate_sample_data()
    else:
        print(f"\n正在加载数据: {DATA_PATH}")
        df = pd.read_excel(DATA_PATH)
        print(f"[OK] 数据加载成功，形状: {df.shape}")

    # 分离特征和目标变量
    X = df.iloc[:, :-1]  # 特征
    y = df.iloc[:, -1]  # 目标变量
    feature_names = X.columns.tolist()  # 获取特征名称

    print(f"\n特征数量: {len(feature_names)}")
    print(f"样本数量: {len(X)}")

    # 将数据集划分为训练集和验证集
    print("\n正在划分训练集和验证集...")
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"[OK] 训练集: {X_train.shape[0]} 样本")
    print(f"[OK] 验证集: {X_val.shape[0]} 样本")

    # 标准化处理
    print("\n正在进行标准化处理...")
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=feature_names)
    X_val_scaled = pd.DataFrame(scaler.transform(X_val), columns=feature_names)
    print("[OK] 标准化完成")

    # 定义超参数网格
    param_grid = {
        'n_estimators': [100, 200, 300]
        # 'learning_rate': [0.01, 0.05, 0.1],
        # 'max_depth': [3, 5, 7],
        # 'subsample': [0.8, 1.0]
    }

    print("\n" + "=" * 80)
    print("开始模型训练和超参数搜索...")
    print("=" * 80)

    # 初始化 XGBoost 回归模型
    xgb_model = xgb.XGBRegressor(random_state=42, n_jobs=-1)

    # 初始化网格搜索对象
    grid_search = GridSearchCV(
        estimator=xgb_model,  # 使用的模型
        param_grid=param_grid,  # 参数网格
        cv=5,  # 5折交叉验证
        scoring='neg_mean_squared_error',  # 评分标准
        verbose=1,  # 输出详细进度日志
        n_jobs=-1  # 使用所有CPU核心
    )

    # 在训练集上执行网格搜索
    grid_search.fit(X_train_scaled, y_train)

    # 获取最佳模型
    best_model = grid_search.best_estimator_
    print(f"\n[OK] 最佳参数组合: {grid_search.best_params_}")

    # 保存最佳模型到本地
    base_name = os.path.splitext(DATA_PATH)[0]
    model_save_path = f"{base_name}_best_model.pkl"
    joblib.dump(best_model, model_save_path)
    print(f"[OK] 最佳模型已保存到: {model_save_path}")

    print("\n" + "=" * 80)
    print("模型评估")
    print("=" * 80)

    # 对训练集进行预测
    y_train_pred = best_model.predict(X_train_scaled)  # 预测训练集

    # 对验证集进行预测
    y_val_pred = best_model.predict(X_val_scaled)  # 预测验证集

    # 训练集指标
    r2_train = r2_score(y_train, y_train_pred)  # R2
    rmse_train = np.sqrt(mean_squared_error(y_train, y_train_pred))  # RMSE
    mae_train = mean_absolute_error(y_train, y_train_pred)  # MAE

    # 验证集指标
    r2_val = r2_score(y_val, y_val_pred)  # R2
    rmse_val = np.sqrt(mean_squared_error(y_val, y_val_pred))  # RMSE
    mae_val = mean_absolute_error(y_val, y_val_pred)  # MAE

    # 打印评估指标
    print(f"\n训练集指标:")
    print(f"  R2: {r2_train:.4f}, RMSE: {rmse_train:.4f}, MAE: {mae_train:.4f}")
    print(f"\n验证集指标:")
    print(f"  R2: {r2_val:.4f}, RMSE: {rmse_val:.4f}, MAE: {mae_val:.4f}")
    print("=" * 80)

    # SHAP 分析
    print("\n" + "=" * 80)
    print("正在进行 SHAP 分析...")
    print("=" * 80)

    explainer = shap.TreeExplainer(best_model)  # 使用最佳模型创建 TreeExplainer 解释器
    shap_values_obj = explainer(X_val_scaled)  # 计算验证集的 SHAP 值对象
    shap_values = shap_values_obj.values  # 提取具体的 SHAP 数值矩阵

    # 计算每个特征的平均绝对SHAP值
    mean_abs_shap = np.abs(shap_values).mean(axis=0)

    # 计算百分比
    shap_percentages = (mean_abs_shap / mean_abs_shap.sum()) * 100

    # 创建DataFrame
    df_polar = pd.DataFrame({
        'Feature': feature_names,  # 特征名称列
        'Value': shap_percentages,  # 百分比数值列
        'Raw': mean_abs_shap  # 平均绝对 SHAP 值
    })

    # 按重要性排序
    df_polar = df_polar.sort_values('Value', ascending=False).reset_index(drop=True)

    print("\n[OK] SHAP 重要性排序:")
    print(df_polar.to_string(index=False))

    print("\n" + "=" * 80)
    print("正在生成可视化图表...")
    print("=" * 80)

    # 调用函数绘图
    draw_shap_analysis_plot(shap_values,
                             X_val_scaled,
                             df_polar)

    print("\n" + "=" * 80)
    print("分析完成!")
    print("=" * 80)
