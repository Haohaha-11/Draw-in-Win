import pandas as pd
from pathlib import Path

# Excel文件路径
xlsx_file = Path(__file__).with_name("Score_Spearman_nums.xlsx")

# 检查文件是否存在
if not xlsx_file.exists():
    print(f"错误：找不到文件 {xlsx_file}")
    exit(1)

# 读取Excel文件
excel_data = pd.ExcelFile(xlsx_file)

# 显示所有sheet名称
print(f"Excel文件包含的sheet: {excel_data.sheet_names}")
print("-" * 60)

# 遍历每个sheet并转换为CSV
for sheet_name in excel_data.sheet_names:
    # 读取sheet数据
    df = pd.read_excel(excel_data, sheet_name=sheet_name)

    # 生成CSV文件名
    csv_filename = Path(__file__).with_name(f"{sheet_name}.csv")

    # 保存为CSV
    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')

    print(f"[OK] 已转换: {sheet_name} -> {csv_filename}")

print("-" * 60)
print(f"转换完成！共生成 {len(excel_data.sheet_names)} 个CSV文件")
