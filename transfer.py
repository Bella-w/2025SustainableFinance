import pandas as pd

# 1. 匯入資料
file_path = 'GridExport_April_19_2025_15_31_28.csv'
df = pd.read_csv(file_path)

# 2. 清理資料
df_clean = df.dropna(subset=["Identifier"]).copy()
df_clean.columns = df_clean.columns.str.strip()

# 3. 定義欄位對應與年度
esg_cols = ['ESG Score\nIn the last 5 FY', 'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12']
esg3_cols = ['SDG 3 Good Health and Well-being\nIn the last 5 FY', 'Unnamed: 14', 'Unnamed: 15', 'Unnamed: 16', 'Unnamed: 17']
esg9_cols = ['SDG 9 Industry, Innovation and Infrastructure\nIn the last 5 FY', 'Unnamed: 19', 'Unnamed: 20', 'Unnamed: 21', 'Unnamed: 22']
years = ['FY0', 'FY-1', 'FY-2', 'FY-3', 'FY-4']

# 4. 展平資料（轉直）
long_df = []
for i, year in enumerate(years):
    temp = df_clean.copy()

    temp['ESG'] = pd.to_numeric(temp[esg_cols[i]], errors='coerce')
    temp['ESG3'] = temp[esg3_cols[i]].astype(str).str.upper().replace({'FALSE': None, 'NAN': None})
    temp['ESG9'] = temp[esg9_cols[i]].astype(str).str.upper().replace({'FALSE': None, 'NAN': None})
    temp = temp.dropna(subset=['ESG', 'ESG3', 'ESG9'])

    temp['YEAR'] = year
    long_df.append(temp)

# 5. 合併所有年度資料
final_df = pd.concat(long_df, ignore_index=True)

# 6. 排序：依 Identifier 與年度順序排序
year_order = {'FY0': 0, 'FY-1': 1, 'FY-2': 2, 'FY-3': 3, 'FY-4': 4}
final_df['YEAR_order'] = final_df['YEAR'].map(year_order)
final_df = final_df.sort_values(by=['Identifier', 'YEAR_order']).drop(columns='YEAR_order')

# 7. 調整欄位順序：公司資料 ➜ YEAR ➜ ESG ➜ ESG3 ➜ ESG9
columns_to_exclude = esg_cols + esg3_cols + esg9_cols
original_cols = [col for col in df_clean.columns if col not in columns_to_exclude]
column_order = original_cols + ['YEAR', 'ESG', 'ESG3', 'ESG9']
final_df = final_df[column_order]

# 8. 輸出結果
output_path = 'output.csv'
final_df.to_csv(output_path, index=False, encoding='utf-8-sig')

print("✅ 最終格式完成，檔案已儲存為：", output_path)
