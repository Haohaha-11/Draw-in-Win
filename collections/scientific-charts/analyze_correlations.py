"""
分析高优先级SDG与其他SDG的相关性关系
"""
import pandas as pd
import numpy as np
from pathlib import Path

# 读取数据
data_path = Path(__file__).resolve().parents[1] / 'sdg-systems' / 'data' / 'Spearman_2.csv'
df = pd.read_csv(data_path, index_col=0)

# 根据中心性分组
# Group A (高中心性): 元素7,9,5,17,4,6 -> SDG6,8,4,16,3,5
high_priority = [6, 8, 4, 16, 3]  # Group A
medium_high = [5, 0, 2, 7]  # Group B
medium_low = [10, 9, 1, 12]  # Group C
low_priority = [11, 14, 15, 13]  # Group D

print("=" * 80)
print("为什么高优先级SDG与低优先级SDG存在强负相关？")
print("=" * 80)

print("\n【关键发现】")
print("-" * 80)

# 1. 高优先级SDG之间的关系
print("\n1. 高优先级SDG（Group A）内部关系：")
print("   这些SDG彼此之间呈现强正相关，说明它们是协同发展的")
high_corrs = []
for i, h1 in enumerate(high_priority):
    for h2 in high_priority[i+1:]:
        corr = df.iloc[h1, h2]
        high_corrs.append(corr)
        print(f"   SDG{h1} <-> SDG{h2}: {corr:+.4f}")
print(f"   平均相关性: {np.mean(high_corrs):+.4f} (强正相关)")

# 2. 低优先级SDG之间的关系
print("\n2. 低优先级SDG（Group D）内部关系：")
print("   这些SDG彼此之间也呈现强正相关")
low_corrs = []
for i, l1 in enumerate(low_priority):
    for l2 in low_priority[i+1:]:
        corr = df.iloc[l1, l2]
        low_corrs.append(corr)
        print(f"   SDG{l1} <-> SDG{l2}: {corr:+.4f}")
print(f"   平均相关性: {np.mean(low_corrs):+.4f} (强正相关)")

# 3. 高优先级与低优先级之间的关系
print("\n3. 高优先级SDG（Group A）与低优先级SDG（Group D）之间：")
print("   两组之间呈现强负相关 - 这是关键现象！")
cross_corrs = []
for h in high_priority:
    for l in low_priority:
        corr = df.iloc[h, l]
        cross_corrs.append(corr)
        print(f"   SDG{h} <-> SDG{l}: {corr:+.4f}")
print(f"   平均相关性: {np.mean(cross_corrs):+.4f} (强负相关)")

print("\n" + "=" * 80)
print("【解释：为什么会出现这种现象？】")
print("=" * 80)

print("""
这种现象在可持续发展目标（SDGs）研究中是合理的，可能的原因包括：

1. 【资源竞争】
   - 高优先级SDG（如SDG3健康、SDG4教育、SDG8经济增长等）需要大量资源投入
   - 低优先级SDG（如SDG13气候行动、SDG14海洋、SDG15陆地生态）也需要资源
   - 在资源有限的情况下，两者存在竞争关系，形成负相关

2. 【发展阶段冲突】
   - 经济发展（高优先级）往往伴随着环境压力（低优先级）
   - 短期经济增长可能与长期环境保护存在权衡（trade-off）
   - 这是经典的"发展与环保"矛盾

3. 【政策优先级】
   - 中心性高的SDG获得更多政策关注和资源
   - 中心性低的SDG相对被边缘化
   - 这种优先级差异导致两者发展方向相反

4. 【系统性权衡】
   - SDGs系统中存在内在的权衡关系（trade-offs）
   - 某些目标的进步可能以其他目标的退步为代价
   - 这是复杂系统中的常见现象

5. 【数据反映的现实】
   - 负相关可能反映了当前全球发展的实际状况
   - 许多国家在追求经济发展时，环境指标确实在恶化
   - 这正是需要可持续发展理念的原因
""")

print("\n" + "=" * 80)
print("【中心性的含义】")
print("=" * 80)
print("""
中心性高 ≠ 一定好，中心性低 ≠ 一定差

- 高中心性：表示该SDG在网络中处于核心位置，与其他目标联系紧密
- 低中心性：可能表示该SDG相对独立，或者在当前发展模式下被边缘化

负相关的存在提醒我们：
→ 需要更加平衡的发展策略
→ 不能只关注高优先级目标而忽视低优先级目标
→ 需要寻找协同发展的路径，而不是简单的权衡
""")

# 4. 计算每个SDG的平均相关性
print("\n" + "=" * 80)
print("【每个SDG与其他所有SDG的平均相关性】")
print("=" * 80)
all_sdgs = list(range(17))
for sdg in all_sdgs:
    avg_corr = df.iloc[sdg, :].mean()
    print(f"SDG{sdg}: {avg_corr:+.4f}")
