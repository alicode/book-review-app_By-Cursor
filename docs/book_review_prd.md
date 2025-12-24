# Book Review Website PRD

# 📚 Book Review Website
**A Full-Stack Flask Portfolio Project**

## 第 1 章：產品背景與目標
### 1.1 產品背景
本專案是一個以「**中文書籍**」為主的書本評論網站，目標使用者為一般讀者。使用者可透過登入後的個人帳號，建立自己的書單、對書籍進行評分，並透過排行榜快速發現熱門書籍。本產品為 **學習導向的 Portfolio 專案**，設計上以功能完整、架構清楚為優先。

### 1.2 產品目標（Goals）
- 提供使用者整理個人書單與收藏的功能
- 讓使用者能對已閱讀書籍進行評分
- 透過熱門排行榜，協助使用者發現值得閱讀的書籍
- 作為完整的全端練習專案（Flask + SQLite + Docker）

### 1.3 非目標（Out of Scope）
- 追蹤其他使用者 / 社交功能
- 即時聊天或通知系統
- 商業推薦、廣告或金流
- 行動 App（僅 Web）

### 1.4 技術限制
- 前端：HTML / CSS / JavaScript
- 後端：Python Flask
- 資料庫：SQLite
- 部署方式：Docker（單容器）

## 第 2 章：使用者角色（User Persona）
### 2.1 訪客（Guest）
**可使用功能**：瀏覽書籍列表、查看書籍評分、查看熱門排行榜
**限制**：無法收藏書籍、無法評分、無個人書單

### 2.2 註冊使用者（User）
**可使用功能**：建立個人書單（收藏書籍）、書單狀態分類（想讀 / 已讀）、評分書籍、查看個人書單
**設計重點**：收藏與評分分離，可隨時修改書單狀態

### 2.3 管理者（Admin）
**可使用功能**：新增 / 編輯 / 刪除書籍資料、維護書籍基本資訊、管理不當內容

## 第 3 章：核心功能定義（MVP）
### 3.1 核心功能清單
- 使用者系統：註冊 / 登入 / 登出
- 書籍瀏覽：書籍列表頁、書籍詳細頁
- 書單與收藏：收藏書籍功能、書單狀態分類、個人書單頁
- 評分系統：1–5 星評分、每人每書一筆、修改即時更新平均分
- 熱門排行榜：平均評分、收藏人數，Top N

### 3.2 非 MVP（延後實作）
- 書籍搜尋、評論文字內容、社交功能、REST API

## 第 4 章：使用流程（User Flow）
### 4.1 訪客流程
首頁 `/` → 顯示熱門排行榜 + 全部書籍列表 → 點擊書籍查看詳細 → 提示登入後可收藏/評分 → 註冊/登入

### 4.2 註冊 / 登入流程
註冊 → 填寫帳號資訊 → 註冊成功自動登入 → 導向登入後首頁

### 4.3 登入使用者流程
登入後首頁 `/` → 顯示「我的書單摘要」、熱門排行榜、全部書籍列表 → 點擊書籍 → 加入書單 / 評分 → 查看我的書單頁 `/my-books`

### 4.4 管理者流程
登入後台 → 新增 / 編輯 / 刪除書籍 → 書籍資料即時更新於前台

## 第 5 章：資料庫設計（Database Design）
### ERD
```
User ───< UserBook >─── Book
  │                      │
  └────────< Rating >────┘
```
### User
id, username, email, password_hash, created_at
### Book
id,title, author, description, cover_image_url, created_at
### UserBook
id, user_id, book_id, status, created_at (unique user_id+book_id)
### Rating
id, user_id, book_id, score, created_at (unique user_id+book_id)

## 第 6 章：技術架構與部署
### 架構
- Flask Application Factory + Blueprints
- SQLite + SQLAlchemy ORM
- Docker 化單容器部署

### 專案結構
```
book-review-app/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── templates/
│   └── static/
├── instance/app.db
├── Dockerfile
├── requirements.txt
└── run.py
```

### Dockerfile 範例
```
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_APP=run.py
ENV FLASK_ENV=development
CMD ["python", "run.py"]
```

### SQLAlchemy Model 範例
見 User, Book, UserBook, Rating（前述 Chapter 6 範例）

### 排行榜 SQL
- 平均評分：GROUP BY book_id ORDER BY AVG(score) DESC
- 收藏數：GROUP BY book_id ORDER BY COUNT(*) DESC

## README.md 教學版摘要
- 專案簡介、核心功能、使用者角色
- 技術棧、專案架構、資料庫設計
- Docker 啟動方式、學習重點、未來可擴充方向
- 面試亮點：SQLite 選擇、Application Factory、排行榜 SQL 優化

