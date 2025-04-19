📘【ESG 評分資料轉換教學說明】

這份程式是為了將一份 ESG 資料表中「橫向」的年度資料（例如第一年ESG、第二年ESG...）轉成「直式」的資料格式，讓每一列代表一家公司在某一個年度的 ESG 評分與 SDG 對應情況。這樣的格式比較方便後續分析，例如畫圖、統計、篩選等等。

### 1. 載入資料（pandas 套件）
```python
import pandas as pd
df = pd.read_csv('原始檔案.csv')
``` 

這行是把 CSV 檔案讀進來，變成一個表格形式（DataFrame），我們就能用程式處理它。


### 2. 清理資料
```python
df_clean = df.dropna(subset=["Identifier"]).copy()
df_clean.columns = df_clean.columns.str.strip()
```
這兩行：

移除公司代碼為空的列（空的通常是空行）

去掉欄位名稱中可能有的空白符號（避免之後找不到欄位）

### 3. 設定橫向資料欄位對應

原先的資料篩選條件有：

a. ESG Score>=65

b. TRBC Industry Name != "Tobacoo" & "Aerospace&Defense" & "Oil&Gas"

c. SDG 3 & SDG 9 == true

d. Market Capitalization > 50 billions

e. Country of Headquarters in Asia

共有38間公司，並顯示出這些公司的 :

5 年的 ESG 分數、SDG 3、SDG 9 欄位


這些欄位是以欄的方式存在，要轉成「每一列是一個年度」的格式，所以要先指定欄位名稱給程式知道。

### 4. 逐年轉直（for 迴圈）
```python
for i, year in enumerate(years):
    temp = df_clean.copy()
    temp["ESG"] = ...
    temp["ESG3"] = ...
    temp["ESG9"] = ...
    temp["YEAR"] = year
    long_df.append(temp)
```
這段會重複跑 5 次，對應 FY0 ~ FY-4，每次把一間公司該年度的 ESG / ESG3 / ESG9 取出來，變成一列，然後全部合併起來。

### 5. 清除不需要的欄位

把那些橫向的原始 ESG 欄位刪掉，只保留公司原始資料（像是 Identifier, 公司名稱...）加上 ESG / YEAR / ESG3 / ESG9

### 6. 排序
```python
final_df.sort_values(by=['Identifier', 'YEAR_order'])
```
確保每家公司的資料是按照 FY0 → FY-4 的順序排列。

### 7. 最後輸出
```python
final_df.to_csv("轉換後_FINAL.csv")
```
輸出轉換好的 CSV 檔案，就可以用 Excel 打開或再做進一步處理嘍！

---

### 延伸補充

這個程式用到的基本知識有：

pandas 套件的 DataFrame 操作

for 迴圈（處理每一年）

資料清理（去除空值、false 值）

資料轉置（pivot-like 的概念）

檔案輸入輸出 (read_csv, to_csv)

可以根據這些要點去做額外的搜尋及學習

/n

**🌟 可接著做的對象或運用：**

解析 ESG 資料在不同年度的變化趨勢

針對不同產業判斷 ESG 貼簽結果

進一步用 seaborn/matplotlib 畫成時間變化圖

製作好看的資料表或報表出來

🎉 希望這份說明有助於了解 ESG 資料轉換的過程 ~

