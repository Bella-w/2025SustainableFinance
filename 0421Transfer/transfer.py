import pandas as pd # 匯入 pandas 套件，用於資料處理

"""
1. 匯入資料
"""
file_path = 'GridExport_April_19_2025_15_31_28.csv' # 引號中輸入需要的檔案，可以直接複製相對路徑
df = pd.read_csv(file_path)  # 使用 pandas 讀取 CSV 檔，讀入為 DataFrame

"""
2. 清理資料
"""
df_clean = df.dropna(subset=["Identifier"]).copy()  # 移除 Identifier 欄位為空值的資料列，並複製為新資料集
df_clean.columns = df_clean.columns.str.strip()  # 去除所有欄位名稱前後的空白字元

"""
3. 定義欄位對應與年度
"""
# 這是 ESG 分數在過去五個會計年度的欄位名稱列表
esg_cols = ['ESG Score\nIn the last 5 FY', 'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12']
# SDG3 (健康福祉) 對應的欄位名稱列表
esg3_cols = ['SDG 3 Good Health and Well-being\nIn the last 5 FY', 'Unnamed: 14', 'Unnamed: 15', 'Unnamed: 16', 'Unnamed: 17']
# SDG9 (產業創新基礎建設) 對應的欄位名稱列表
esg9_cols = ['SDG 9 Industry, Innovation and Infrastructure\nIn the last 5 FY', 'Unnamed: 19', 'Unnamed: 20', 'Unnamed: 21', 'Unnamed: 22']
# 五個會計年度的名稱，FY0 為最新年度
years = ['FY0', 'FY-1', 'FY-2', 'FY-3', 'FY-4']

"""
4. 展平資料（轉直）
"""
long_df = [] # 初始化一個空列表，用於儲存轉直後的每個年度資料
# 使用 enumerate 同時取得年份與其索引值
for i, year in enumerate(years):
    temp = df_clean.copy() # 複製一份清理過的原始資料

    # 將對應年度的 ESG 欄位轉換為數值型別，錯誤時設為 NaN
    temp['ESG'] = pd.to_numeric(temp[esg_cols[i]], errors='coerce')
    # 將 ESG3 值轉為大寫字串，並將 'FALSE' 與 'NAN' 替換為 None
    temp['ESG3'] = temp[esg3_cols[i]].astype(str).str.upper().replace({'FALSE': None, 'NAN': None})
    # 對 ESG9 欄位做相同處理
    temp['ESG9'] = temp[esg9_cols[i]].astype(str).str.upper().replace({'FALSE': None, 'NAN': None})
    # 去除任一關鍵欄位缺值的資料列
    temp = temp.dropna(subset=['ESG', 'ESG3', 'ESG9'])

    temp['YEAR'] = year  # 新增一個欄位表示對應的年度
    long_df.append(temp) # 將這年度處理過的資料加入總列表

"""
5. 合併所有年度資料
"""
final_df = pd.concat(long_df, ignore_index=True) # 合併所有年度資料為一個總表，並重設索引

"""
6. 排序：依 Identifier 與年度順序排序
"""
year_order = {'FY0': 0, 'FY-1': 1, 'FY-2': 2, 'FY-3': 3, 'FY-4': 4} # 定義年度的排序順序
final_df['YEAR_order'] = final_df['YEAR'].map(year_order) # 建立排序用欄位
final_df = final_df.sort_values(by=['Identifier', 'YEAR_order']).drop(columns='YEAR_order')  # 排序後移除排序輔助欄位

"""
7. 調整欄位順序：公司資料 ➜ YEAR ➜ ESG ➜ ESG3 ➜ ESG9
"""
columns_to_exclude = esg_cols + esg3_cols + esg9_cols # 需要排除的原始欄位（因為已轉成 ESG、ESG3、ESG9）
original_cols = [col for col in df_clean.columns if col not in columns_to_exclude]  # 除去那些欄位後剩下的欄位（公司基本資料）
column_order = original_cols + ['YEAR', 'ESG', 'ESG3', 'ESG9']  # 設定欄位的理想順序
final_df = final_df[column_order] # 依
照指定欄位順序重新排列資料

"""
8. 輸出結果
"""
output_path = 'output.csv' # 設定輸出檔案的名稱與路徑
final_df.to_csv(output_path, index=False, encoding='utf-8-sig') # 匯出為 CSV 檔，使用 utf-8-sig 編碼（適用於 Excel）

print("✅ 最終格式完成，檔案已儲存為：", output_path) # 顯示處理完成訊息
