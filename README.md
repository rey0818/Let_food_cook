# 🍽️ 智慧廚房助手 - 食材Magic

一個結合 AI 技術的智慧食譜搜尋系統，幫助用戶根據現有食材找到合適的食譜，並提供中文翻譯、營養分析和家樂福商品比價功能。

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
final_project_ICP/
├── core/
│   ├── main.py              # Streamlit 主程式
│   ├── recipe_api.py        # Spoonacular API 介面
│   ├── translation.py       # Gemini AI 翻譯模組
│   └── scraper.py           # 家樂福爬蟲
├── ingredients_dict.json    # 食材翻譯快取
└── Document/                # 文件資料夾
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

### 1️⃣ Python 環境
- Python 3.8 或以上版本

### 2️⃣ 必要套件

建立 `requirements.txt` 檔案：
```txt
streamlit>=1.28.0
pandas>=2.0.0
requests>=2.31.0
beautifulsoup4>=4.12.0
google-generativeai>=0.3.0
scikit-learn>=1.3.0
numpy>=1.24.0
```

### 安裝指令
```powershell
pip install -r requirements.txt
```

或手動安裝：
```powershell
pip install streamlit pandas requests beautifulsoup4 google-generativeai scikit-learn numpy
```

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

## 🚀 如何執行

### 1️⃣ 安裝套件
```powershell
pip install -r requirements.txt
```

### 2️⃣ 執行程式
```powershell
cd c:\Users\user\Desktop\final_project_ICP\core
streamlit run main.py
```

### 3️⃣ 使用系統
1. 在瀏覽器開啟 `http://localhost:8501`
2. 在側邊欄輸入 API Keys
3. 輸入食材（英文，用逗號分隔）
4. 選擇過敏原篩選（可選）
5. 點擊「🔍 搜尋食譜」
6. 查看結果和採購建議

---

## 💡 使用範例

### 輸入
```
食材: Chicken, Tomato, Pasta
過敏原: Dairy Free
搜尋數量: 2
```

### 輸出
- 2 個符合條件的食譜
- 每個食譜包含：
  - 食譜圖片
  - 翻譯後的中文步驟
  - 缺漏食材的家樂福商品推薦
  - 營養成分圖表

---

## ⚠️ 注意事項

### API 使用限制
- **Spoonacular**: 免費版每日 150 次請求
- **Gemini**: 免費版有每日配額限制

### 網路爬蟲
- 家樂福網站結構可能變動
- 建議定期檢查 `scraper.py` 的解析邏輯

### 資料快取
- `ingredients_dict.json` 儲存已翻譯的食材
- 可手動編輯調整翻譯結果

### 相似度閾值
- 目前設定為 0.45
- 可在 `translation.py` 的 `choose_best()` 函式中調整

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

- 專案開發：[zih-ruei huang]
- 最後更新：2025年12月11日

---

## 📞 聯絡方式

如有問題或建議，請聯絡：[rey.gaming.0818@gmail.com]
