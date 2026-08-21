import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from matplotlib import font_manager

# 设置字体为 Times New Roman
font_path = font_manager.findfont('DejaVu Serif')
try:
    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
except:
    plt.rcParams['font.family'] = 'serif'

# 10个维度的标签（顺时针排列）
categories = ['SSO', 'CMO', 'CO', 'MCNO', 'CB', 'OV', 'DB', 'RD', 'DD', 'BI']
N = len(categories)

# 模拟数据（根据原图视觉估算，单位：百分比）
# 确保所有值都为正数，且 Total > Train > Test
# Total (最外层，深蓝色) - 最大值
total_data = np.array([69.5, 14.5, 24.1, 33.1, 23.8, 23.0, 14.9, 15.2, 30.1, 52.0])

# Train (中间层，珊瑚粉) - 中等值
train_data = np.array([69.4, 16.0, 16.0, 23.8, 12.8, 20.1, 15.4, 11.1, 48.5, 52.0])

# Test (最内层，金黄色) - 最小值
test_data = np.array([69.7, 8.7, 8.7, 20.4, 11.7, 13.7, 9.0, 9.8, 5.2, 5.2])

# 计算角度（不包含闭合点）
angles = np.linspace(0, 2 * np.pi, N, endpoint=False)

# 样条插值函数 - 创建平滑闭合曲线
def smooth_polar_curve(angles, values, num_points=500):
    """使用样条插值在极坐标下创建平滑闭合曲线"""
    # 关键修正：强制闭合 - 在插值前将首个点追加到末尾
    angles_closed = np.append(angles, angles[0])
    values_closed = np.append(values, values[0])

    # 为了更好的周期性，再添加一个点
    angles_closed = np.append(angles_closed, angles[1])
    values_closed = np.append(values_closed, values[1])

    # 创建参数 t
    t = np.arange(len(angles_closed))
    t_smooth = np.linspace(0, len(angles_closed) - 1, num_points)

    # 使用三次样条插值，k=3 提供平滑效果，但不会过度震荡
    # bc_type='periodic' 确保周期性边界条件
    try:
        spl_values = make_interp_spline(t, values_closed, k=3, bc_type='periodic')
    except:
        # 如果不支持 periodic，使用 natural
        spl_values = make_interp_spline(t, values_closed, k=3, bc_type='natural')

    values_smooth = spl_values(t_smooth)

    # 生成对应的平滑角度
    angles_smooth = np.linspace(angles[0], angles[0] + 2 * np.pi, num_points)

    # 确保值为非负，并限制过度震荡
    values_smooth = np.maximum(values_smooth, 0)

    # 截取完整的一圈（去掉重复部分）
    angles_smooth = angles_smooth[:-2]
    values_smooth = values_smooth[:-2]

    return angles_smooth, values_smooth

# 创建图形
fig = plt.figure(figsize=(10, 10), facecolor='white')
ax = fig.add_subplot(111, projection='polar')

# 设置起始角度为顶部（90度）
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)  # 顺时针

# 生成平滑闭合曲线
angles_smooth_total, total_smooth = smooth_polar_curve(angles, total_data, num_points=600)
angles_smooth_train, train_smooth = smooth_polar_curve(angles, train_data, num_points=600)
angles_smooth_test, test_smooth = smooth_polar_curve(angles, test_data, num_points=600)

# 绘制三层（严格按照 Z-order：深蓝色最底层 -> 粉色中层 -> 黄色最顶层）
# 最外层 - Total (深蓝色) - zorder=1 最底层
ax.fill(angles_smooth_total, total_smooth, color='#003f5c', alpha=0.95, label='Total', zorder=1)
ax.plot(angles_smooth_total, total_smooth, color='#002840', linewidth=1.5, zorder=1)

# 中间层 - Train (珊瑚粉) - zorder=2 中层
ax.fill(angles_smooth_train, train_smooth, color='#ff6361', alpha=0.95, label='Train', zorder=2)
ax.plot(angles_smooth_train, train_smooth, color='#d94442', linewidth=1.5, zorder=2)

# 最内层 - Test (金黄色) - zorder=3 最顶层
ax.fill(angles_smooth_test, test_smooth, color='#ffa600', alpha=0.95, label='Test', zorder=3)
ax.plot(angles_smooth_test, test_smooth, color='#cc8500', linewidth=1.5, zorder=3)

# 设置径向网格线（虚线）
ax.set_ylim(0, max(total_data) * 1.2)
ax.yaxis.grid(True, linestyle='--', color='gray', alpha=0.5, linewidth=0.8)
ax.xaxis.grid(True, linestyle='--', color='gray', alpha=0.5, linewidth=0.8)

# 设置类别标签
ax.set_xticks(angles)
ax.set_xticklabels(categories, fontsize=14, fontweight='bold')

# 移除径向刻度标签（数字圆圈）
ax.set_yticklabels([])

# 添加数值标注（优化位置，避免被色块遮挡）
for i, (angle, total_val, train_val, test_val) in enumerate(zip(angles, total_data, train_data, test_data)):
    # 计算文字旋转角度
    angle_deg = np.degrees(angle)
    rotation = angle_deg - 90 if angle < np.pi else angle_deg + 90

    # Total 数值 - 在最外层外侧
    ax.text(angle, total_val + 3.5, f'{total_val}%',
            ha='center', va='center', fontsize=7.5, color='#003f5c', fontweight='bold',
            rotation=rotation, zorder=10)

    # Train 数值 - 在中间层
    if train_val > test_val + 3:  # 只在有足够空间时显示
        ax.text(angle, (train_val + test_val) / 2, f'{train_val}%',
                ha='center', va='center', fontsize=7.5, color='#ff6361', fontweight='bold',
                rotation=rotation, zorder=10)

    # Test 数值 - 在最内层内侧
    if test_val > 8:  # 只在值足够大时显示
        ax.text(angle, test_val * 0.7, f'{test_val}%',
                ha='center', va='center', fontsize=7.5, color='#ffa600', fontweight='bold',
                rotation=rotation, zorder=10)

# 添加图例
legend = ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0),
                   frameon=True, fontsize=12, facecolor='white', edgecolor='gray')

# 移除外边框
ax.spines['polar'].set_visible(False)

# 保存为 SVG 矢量格式
plt.tight_layout()
plt.savefig('smooth_radial_chart.svg',
            format='svg', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('smooth_radial_chart.png',
            format='png', dpi=300, bbox_inches='tight', facecolor='white')

print("平滑曲线雷达图已生成：smooth_radial_chart.svg 和 smooth_radial_chart.png")
plt.show()
