import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. 模型参数配置 (基于文档 1.2 & 1.3)
# ==========================================
class Config:
    # 受众细分段 K=8
    SEGMENTS = [
        "Local/Core", "Young/Trendy", "Female Fans", "International",
        "Hardcore", "Gossip/Variety", "Brand/Sponsor", "Community/Charity"
    ]
    K = len(SEGMENTS)

    # 含金量权重 (示例值，和为1)
    WEIGHTS = np.array([0.20, 0.15, 0.15, 0.10, 0.10, 0.15, 0.10, 0.05])

    # 变现函数参数 (Softplus)
    A = 1000  # 市场规模系数
    BETA = 1.2  # 需求弹性
    ETA = 0.5   # 胜率弹性
    B = 50      # 门槛

    # 约束参数
    W_MIN = 0.45 # 胜率底线
    EPSILON = 1e-6 # 防止除零

# ==========================================
# 2. 核心模型类
# ==========================================
class EntertainmentModel:
    def __init__(self, all_players_df, current_roster_ids):
        """
        all_players_df: 包含所有球员(现有+候选)原始数据 x_ik 的DataFrame
        current_roster_ids: 当前阵容的球员ID列表
        """
        self.raw_df = all_players_df.set_index('player_id')
        self.current_roster_ids = current_roster_ids

        # 1. 数据归一化 (Min-Max)
        # r_ik = (x - min) / (max - min + eps)
        self.norm_df = self._normalize_data()

    def _normalize_data(self):
        df = self.raw_df[Config.SEGMENTS].copy()
        # 对每一列(每个受众段)进行归一化
        min_vals = df.min()
        max_vals = df.max()
        norm_data = (df - min_vals) / (max_vals - min_vals + Config.EPSILON)
        return norm_data

    def get_roster_reach(self, roster_ids):
        """
        计算指定阵容 S 的受众覆盖度 Reach_k(S)
        Formula: 1 - prod(1 - r_ik)
        """
        if not roster_ids:
            return np.zeros(Config.K)

        roster_data = self.norm_df.loc[roster_ids].values # Shape: (N, K)
        # 概率聚合: 1 - (所有人都覆盖不到的概率)
        reach = 1.0 - np.prod(1.0 - roster_data, axis=0)
        return reach

    def get_demand_index(self, reach_vec):
        """
        计算可变现需求指数 D(S)
        Formula: sum(w_k * log(1 + Reach_k))
        """
        # u(x) = log(1 + x)
        utility = np.log(1 + reach_vec)
        demand = np.sum(Config.WEIGHTS * utility)
        return demand

    def get_marginal_utility(self, reach_vec):
        """
        计算 u'(x) = 1 / (1+x)
        用于计算优先级
        """
        return 1.0 / (1.0 + reach_vec)

    def calculate_owner_value(self, roster_ids, win_rate):
        """
        计算老板价值 V(S)
        M(D,W) = softplus(A * D^beta * (1+W)^eta - B)
        """
        reach = self.get_roster_reach(roster_ids)
        D = self.get_demand_index(reach)

        # 核心变现公式
        z = Config.A * (D ** Config.BETA) * ((1 + win_rate) ** Config.ETA) - Config.B
        value = np.log(1 + np.exp(z)) # Softplus
        return value

    # ==========================================
    # 3. 诊断与策略生成 (Task 2 核心逻辑)
    # ==========================================
    def diagnose_current_roster(self, target_reach=0.8):
        """
        诊断当前阵容短板
        """
        current_reach = self.get_roster_reach(self.current_roster_ids)
        marginal_u = self.get_marginal_utility(current_reach)

        # 计算缺口 Gap_k
        # 假设目标覆盖 target_reach 对所有段一致(也可设为向量)
        gap = np.maximum(0, target_reach - current_reach)

        # 计算优先级 Priority_k
        # P = w_k * u'(Reach) * Gap
        priority = Config.WEIGHTS * marginal_u * gap

        diagnosis_df = pd.DataFrame({
            'Segment': Config.SEGMENTS,
            'Weight': Config.WEIGHTS,
            'Current_Reach': current_reach,
            'Gap': gap,
            'Marginal_Gain': marginal_u,
            'Priority_Score': priority
        }).sort_values('Priority_Score', ascending=False)

        return diagnosis_df, priority

    def evaluate_candidates(self, candidates_ids, priority_vec):
        """
        计算候选球员评分 Score_i
        Score = sum(Priority_k * Delta_Reach_ik)
        """
        current_reach = self.get_roster_reach(self.current_roster_ids)
        scores = []

        for pid in candidates_ids:
            # 模拟加入该球员后的新 Reach
            new_roster = self.current_roster_ids + [pid]
            new_reach = self.get_roster_reach(new_roster)

            # 边际覆盖增量 Delta Reach
            delta_reach = new_reach - current_reach

            # 评分公式
            score = np.sum(priority_vec * delta_reach)

            scores.append({
                'player_id': pid,
                'Total_Score': score,
                'Delta_Reach_Avg': np.mean(delta_reach)
            })

        return pd.DataFrame(scores).sort_values('Total_Score', ascending=False)

    def check_synergy(self, p1_id, p2_id):
        """
        计算两名球员的协同效应 Syn(i,j)
        Syn = D(S+i+j) - D(S+i) - D(S+j) + D(S)
        """
        base_ids = self.current_roster_ids
        D_base = self.get_demand_index(self.get_roster_reach(base_ids))

        D_i = self.get_demand_index(self.get_roster_reach(base_ids + [p1_id]))
        D_j = self.get_demand_index(self.get_roster_reach(base_ids + [p2_id]))
        D_ij = self.get_demand_index(self.get_roster_reach(base_ids + [p1_id, p2_id]))

        synergy = D_ij - D_i - D_j + D_base
        return synergy

# ==========================================
# 4. 模拟运行
# ==========================================

# --- A. 生成模拟数据 ---
np.random.seed(42)
# 假设有20个球员：ID 1-10是现有阵容，11-20是自由市场候选人
player_ids = [f'P{i}' for i in range(1, 21)]
data = np.random.randint(10, 100, size=(20, 8)) # 原始渠道数据 x_ik
# 增加一些特征：P11是年轻潮流巨星(idx 1)，P12是国际巨星(idx 3)
data[10, 1] = 500 # P11 young trend
data[11, 3] = 450 # P12 international

df_players = pd.DataFrame(data, columns=Config.SEGMENTS)
df_players['player_id'] = player_ids

current_roster = [f'P{i}' for i in range(1, 11)]
candidates = [f'P{i}' for i in range(11, 21)]

# --- B. 实例化模型 ---
model = EntertainmentModel(df_players, current_roster)

# --- C. 第一步：商业短板诊断 ---
print(">>> Step 1: Diagnosing Commercial Shortfalls")
diag_df, priority_vector = model.diagnose_current_roster(target_reach=0.9)
print(diag_df[['Segment', 'Current_Reach', 'Priority_Score']].round(4))

# 可视化：商业优先级
plt.figure(figsize=(10, 6))
sns.barplot(data=diag_df, x='Priority_Score', y='Segment', palette='viridis')
plt.title('Commercial Priority by Segment (Where to Recruit?)')
plt.xlabel('Priority Score (Weight * Marginal * Gap)')
plt.tight_layout()
plt.show() #
# --- D. 第二步：候选球员评分与排序 ---
print("\n>>> Step 2: Scoring Candidates based on Priority")
ranked_candidates = model.evaluate_candidates(candidates, priority_vector)
print(ranked_candidates.head())

top_pick = ranked_candidates.iloc[0]['player_id']
second_pick = ranked_candidates.iloc[1]['player_id']
print(f"\nTop Recommendation: {top_pick}")

# --- E. 第三步：协同效应检查 ---
# 检查前两名候选人是一起买更好(互补)，还是有冲突(重叠)
syn_val = model.check_synergy(top_pick, second_pick)
print(f"\n>>> Step 3: Synergy Check between {top_pick} and {second_pick}")
print(f"Synergy Value: {syn_val:.5f}")
if syn_val > 0:
    print("Result: POSITIVE synergy (Complementary segments). Buy both!")
else:
    print("Result: NEGATIVE synergy (Overlapping segments). Diminishing returns.")

# --- F. 第四步：最终老板价值预测 ---
# 假设当前胜率0.5，引入Top Pick后胜率变为0.52 (需外部胜率模型)
initial_value = model.calculate_owner_value(current_roster, win_rate=0.5)
new_roster = current_roster + [top_pick]
new_value = model.calculate_owner_value(new_roster, win_rate=0.52)

print(f"\n>>> Step 4: Owner Value Projection")
print(f"Current Value: ${initial_value:.2f}M")
print(f"Projected Value (with {top_pick}): ${new_value:.2f}M")
print(f"Value Increase: ${new_value - initial_value:.2f}M")