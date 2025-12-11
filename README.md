# 🍽️ 智慧廚房助手 - 食材Magic

一個結合 AI 技術的智慧食譜搜尋系統，為所有使用者根據現有食材找到合適的食譜，並提供中文翻譯、營養分析和家樂福商品比價功能。無需編程經驗，任何人都可以輕鬆使用。

## 📋 專案簡介

這個專案整合了多個 API 和 AI 技術，提供以下功能：
- 🔍 根據食材搜尋食譜（Spoonacular API）
- 🌐 自動翻譯食譜步驟和食材名稱（Google Gemini AI）
- 🛒 自動搜尋家樂福缺少食材並比價
- 🤖 智慧商品匹配（使用 Embedding 和相似度比對）
- 📊 營養成分分析
- 🚫 過敏原篩選

---

## 🎬 專案運作流程

### 1️⃣ 使用者輸入
- 在側邊欄輸入：
  - **Spoonacular API Key**（食譜搜尋）
  - **Gemini API Key**（翻譯和 AI 處理）
  - **食材清單**（英文，用逗號分隔）
  - **過敏原篩選**（可選）
  - **搜尋數量**（1-10個食譜）

### 2️⃣ 食譜搜尋
系統透過 `recipe_api.py` 呼叫 Spoonacular API：
```
GET https://api.spoonacular.com/recipes/complexSearch
```
- 根據輸入的食材搜尋相關食譜
- 取得食譜詳細資訊（步驟、營養、圖片等）
- 識別缺漏食材和已有食材

### 3️⃣ AI 翻譯處理
使用 `translation.py` 透過 Google Gemini AI：

**食材翻譯**
- 將英文食材名稱轉換為台灣超市常用的中文名稱
- 使用快取機制（`ingredients_dict.json`）避免重複翻譯
- 自動過濾形容詞和加工形式（如 diced, powdered 等）

**食譜步驟翻譯**
- 批次翻譯所有食譜的烹飪步驟
- 保持步驟順序和編號
- 使用繁體中文（台灣用語）

### 4️⃣ 家樂福商品搜尋
使用 `scraper.py` 爬取家樂福線上購物：
```
https://online.carrefour.com.tw/zh/search
```
- 搜尋缺漏食材的相關商品
- 擷取商品名稱、價格、連結
- 識別特價商品和折扣資訊

### 5️⃣ 智慧商品匹配
使用 Gemini Embedding API：
- 計算食材名稱和商品名稱的語義相似度
- 使用餘弦相似度（Cosine Similarity）找出最佳匹配
- 過濾相似度低於 0.45 的商品

### 6️⃣ 結果呈現
在 Streamlit 介面顯示：
- 📷 食譜圖片
- 📋 翻譯後的中文步驟
- 🛒 缺漏食材的家樂福商品推薦（含價格和連結）
- 💰 預估採購總價
- 📊 營養成分圖表

---

## 🛠️ 技術架構

```
project/
├── code/
│   ├── main.py              # Streamlit 主程式
│   ├── recipe_api.py        # Spoonacular API 介面
│   ├── translation.py       # Gemini AI 翻譯模組
│   └── scraper.py           # 家樂福爬蟲
├── ingredients_dict.json    # 食材翻譯快取
├── requirements.txt         # 依賴套件列表
└── README.md                # 專案說明文件
```

### 核心模組說明

#### `main.py`
- 使用 Streamlit 建立使用者介面
- 整合各模組功能
- 處理使用者輸入和結果顯示

#### `recipe_api.py`
- 封裝 Spoonacular API 呼叫
- 提取食譜資訊、營養成分、步驟
- 處理缺漏和已有食材

#### `translation.py`
- 使用 Gemini AI 進行翻譯
- 實作食材名稱轉換
- 實作食譜步驟翻譯
- 使用 Embedding 進行語義相似度計算

#### `scraper.py`
- 使用 BeautifulSoup 爬取家樂福網站
- 解析商品資訊和價格
- 識別特價和折扣

---

## 📦 需要安裝的套件

### 1️⃣ 系統需求
- **Python 3.8 或以上版本** - [下載 Python](https://www.python.org/downloads/)
- **網際網路連線** - 用於 API 呼叫和網路爬蟲

### 2️⃣ 安裝步驟

#### 步驟 1：複製專案
```powershell
# 複製此專案到你的電腦
git clone https://github.com/[your-username]/Let_food_cook.git
cd Let_food_cook
```

#### 步驟 2：安裝依賴套件
專案已準備好 `requirements.txt` 檔案，包含所有必要套件：

```powershell
pip install -r requirements.txt
```

完成後會自動安裝以下套件：
- **streamlit** - 使用者介面框架
- **pandas** - 資料處理
- **requests** - HTTP 請求
- **beautifulsoup4** - 網頁爬蟲
- **google-generativeai** - Gemini AI API
- **scikit-learn** - 機器學習（相似度計算）
- **numpy** - 數值計算
- **tabulate** - 表格格式化顯示

#### 步驟 3：驗證安裝
```powershell
pip list
```
確認所有套件都已安裝。

---

## 🔑 API 金鑰申請

### Spoonacular API
1. 前往 [Spoonacular API](https://spoonacular.com/food-api)
2. 註冊免費帳號
3. 取得 API Key（免費版每日 150 次請求）

### Google Gemini API
1. 前往 [Google AI Studio](https://aistudio.google.com/)
2. 登入 Google 帳號
3. 建立 API Key
4. 選擇 `gemini-2.5-flash-lite` 模型（免費版）

---

## 🚀 快速開始

### 1️⃣ 準備 API 金鑰（5 分鐘）

**Spoonacular API 金鑰：**
1. 前往 [Spoonacular API 官網](https://spoonacular.com/food-api)
2. 點擊「Get API Key」並註冊免費帳號
3. 確認電子郵件後，複製你的 API Key
4. 免費版每日可使用 150 次請求

**Google Gemini API 金鑰：**
1. 前往 [Google AI Studio](https://aistudio.google.com/)
2. 登入你的 Google 帳號（或建立新帳號）
3. 點擊「Create API Key」
4. 複製 API Key（免費版無日限制，但有配額限制）

### 2️⃣ 執行應用程式

#### Windows 使用者：
```powershell
# 進入專案資料夾
cd Let_food_cook

# 啟動應用程式
streamlit run code/main.py
```

#### Mac/Linux 使用者：
```bash
cd Let_food_cook
streamlit run code/main.py
```

應用程式會自動在瀏覽器開啟：`http://localhost:8501`

### 3️⃣ 使用應用程式

1. **在左側欄輸入 API 金鑰：**
   - 貼上 Spoonacular API Key
   - 貼上 Gemini API Key

2. **輸入食材：**
   - 英文食材名稱，用逗號分隔
   - 例：`Chicken, Tomato, Garlic, Pasta`

3. **（可選）設定過敏原篩選：**
   - 選擇需要避免的過敏原
   - 例：Dairy Free, Gluten Free

4. **選擇搜尋數量：**
   - 1 至 10 個食譜

5. **點擊「🔍 搜尋食譜」按鈕**

6. **查看結果：**
   - 食譜圖片和中文步驟
   - 缺漏食材的家樂福購物推薦
   - 預估採購總價
   - 營養成分分析

---

## 💡 使用範例

### 場景：尋找簡單的義大利麵食譜

**輸入內容：**
- 食材：`Chicken, Tomato, Pasta, Garlic, Olive Oil`
- 過敏原：`Dairy Free`（避免乳製品）
- 搜尋數量：`3`

**系統會為你：**
- 🔍 搜尋 3 個符合條件的食譜
- 📝 自動翻譯所有食譜步驟為繁體中文
- 🛒 在家樂福搜尋缺漏食材（例：鹽、黑胡椒）
- 💰 計算採購總價
- 📊 顯示每個食譜的營養成分

---

## ⚠️ 常見問題

### Q1: 執行時顯示「ModuleNotFoundError」
**A:** 表示套件未安裝。請執行：
```powershell
pip install -r requirements.txt
```

### Q2: 獲得免費 API 金鑰後無法使用
**A:** 
- Spoonacular 需要 24 小時才能啟用免費版
- Gemini API 金鑰需要確認已啟用

### Q3: 家樂福搜尋沒有結果
**A:** 
- 家樂福可能沒有該商品
- 網站結構可能已變動，請聯絡開發者報告

### Q4: Gemini 翻譯不準確
**A:** 
- 食材可編輯 `ingredients_dict.json` 手動調整
- 可試試不同的食材名稱英文版本

### Q5: 應用程式很慢
**A:** 
- 首次執行需要下載 AI 模型
- 網路搜尋耗時較久
- 請耐心等待進度條完成

---

## 🎯 未來改進方向

- [ ] 支援更多超市（全聯、大潤發等）
- [ ] 新增食譜收藏功能
- [ ] 實作購物車和價格追蹤
- [ ] 支援圖片辨識食材
- [ ] 優化翻譯品質和速度
- [ ] 新增使用者評分和回饋

---

## 📄 授權

本專案為教育用途，請遵守相關 API 的使用條款。

---

## 👥 貢獻者

- 專案開發者：[Zih-Ruei Huang]
- 最後更新：2025年12月11日

---

## 📞 獲得幫助

遇到問題嗎？
- 📧 電郵聯絡：[rey.gaming.0818@gmail.com]
- 🐛 提交 Bug 報告
- 💡 分享建議和改進想法
