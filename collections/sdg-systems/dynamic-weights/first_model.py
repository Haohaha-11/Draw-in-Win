import numpy as np
import pandas as pd
from scipy.optimize import minimize
from pathlib import Path

# 载入Excel文件，读取Score和Spearman的sheet
file_path = Path(__file__).with_name('Score_Spearman_nums.xlsx')
excel_data = pd.ExcelFile(file_path)

# 读取数据
score_data = pd.read_excel(excel_data, sheet_name='Score')
spearman_data = pd.read_excel(excel_data, sheet_name='Spearman')

# 提取SDG得分（2015-2019）和Spearman相关系数（ωij）。
# 第一列是行标签；按位置移除可避免依赖工作簿中的本地化列名。
sdg_scores_values = score_data.iloc[:, 1:].values.T
spearman_corr = spearman_data.iloc[:, 1:].values

# 初步优先级设定（这里我给的固定值，来源于昨天刘心语给的第一个优先级排序结果，就是和我没加权情况一样的那个结果）
priorities_raw = [
    1.1380245844711485, 1.13596127915552407, 1.1183749309303155, 1.1067941509024443, 1.1067941509024428,
    1.1067941509024428, 1.068467591894999, 1.068467591894999, 0.2201967971280886, -0.447277273745765,
    -0.479444887056648524, -1.1273467657225242, -1.2301050368542402, -1.7106265208360396,
    -1.9321728545508422, -1.9321728545508422, -2.154733166961954
]

# 每个优先级值对应的SDG编号（根据图片中的“第几个元素”）
priority_indices = [
    6, 9, 5, 17, 4, 6, 1, 1, 8, 11, 10, 2, 13, 12, 15, 16, 14
]

# 根据优先级对应SDG的顺序重新排列优先级
initial_priorities = np.zeros(17)
for i, idx in enumerate(priority_indices):
    initial_priorities[idx-1] = priorities_raw[i]  # 对应SDG编号为 idx-1（从0开始）

# 输出优先级数组，以便检查
print("SDG 优先级对应：", initial_priorities)

# 定义动态增长因子 α(t)
def alpha_t(alpha_0, r, t):
    return alpha_0 * np.exp(-r * t)

# 定义更新公式（引入Sigmoid函数和动态增长因子）
def logistic_growth_model(S, alpha_0, r, beta, gamma, spearman_matrix, priorities, C, t):
    alpha = alpha_t(alpha_0, r, t)  # 计算当前时间的α(t)
    S_new = np.copy(S)

    for i in range(len(S)):
        # 计算该SDG的得分更新
        interaction_term = sum(spearman_matrix[i, j] * S[j] for j in range(len(S)))
        # 更新公式
        S_new[i] = 100 / (1 + np.exp(-1 * (S[i] + alpha) * (1 - S[i] / 100) + beta * interaction_term + gamma * priorities[i] - C))

    return S_new

# 定义损失函数，用于拟合模型
def loss_function(params):
    alpha_0, r, beta, gamma, C = params
    predicted_scores = np.copy(sdg_scores_values[:, 0])  # 初始值为2015年的得分
    actual_scores = sdg_scores_values[:, 1:]  # 2016-2019年的实际得分

    # 计算每一年SDG的预测得分，并与实际得分进行比较
    total_loss = 0
    for year in range(1, len(sdg_scores_values[0])):  # 从2016年到2019年
        predicted_scores = logistic_growth_model(predicted_scores, alpha_0, r, beta, gamma, spearman_corr, initial_priorities, C, year)
        # 计算损失：实际得分与预测得分之间的差异（平方误差）
        total_loss += np.sum((predicted_scores - actual_scores[:, year - 1]) ** 2)

    return total_loss

# 使用最小化方法来估计模型参数α_0, r, β, γ, C
result = minimize(loss_function, [0.1, 0.01, 0.01, 0.01, 0.1], bounds=[(0, 10), (0, 1), (0, 1), (0, 1), (0, 1)])

# 提取拟合的参数
alpha_0_fit, r_fit, beta_fit, gamma_fit, C_fit = result.x
print(f"拟合参数：\nα_0 = {alpha_0_fit}\nr = {r_fit}\nβ = {beta_fit}\nγ = {gamma_fit}\nC = {C_fit}")

# 使用拟合的参数来预测2030年每个SDG的得分
predicted_scores_2030 = np.copy(sdg_scores_values[:, -1])  # 初始值为2019年的得分

# 模拟从2020年到2030年
years_to_predict = 2030 - 2019
for year in range(1, years_to_predict + 1):
    predicted_scores_2030 = logistic_growth_model(predicted_scores_2030, alpha_0_fit, r_fit, beta_fit, gamma_fit, spearman_corr, initial_priorities, C_fit, year)

# 输出2030年每个SDG的预测得分
print("2030年各SDG的预测得分：")
print(predicted_scores_2030)
