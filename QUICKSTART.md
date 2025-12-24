# 快速開始指南

## 前置需求

- Python 3.12+
- pip 或 uv

## 安裝步驟

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 初始化資料庫

**方法一：使用設定腳本（推薦，最簡單）**

```bash
python setup_db.py
```

這個腳本會自動建立所有必要的資料表，並驗證是否成功建立。

**方法二：使用 Flask-Migrate（適合需要版本控制的專案）**

```bash
# 設定環境變數
export FLASK_APP=run.py

# 初始化遷移
flask db init

# 建立初始遷移
flask db migrate -m "Initial migration"

# 執行遷移
flask db upgrade
```

**方法三：使用簡單初始化腳本**

```bash
python init_db.py
```

> **注意**：如果遇到 "no such table" 錯誤，請執行 `python setup_db.py` 重新建立資料表。

### 3. 啟動應用程式

```bash
python run.py
```

應用程式將在 `http://localhost:5000` 啟動。

## 首次使用

1. 訪問首頁 `http://localhost:5000`
2. 點擊「註冊」建立帳號
3. 登入後可以：
   - 在後台新增書籍（`/admin/books`）
   - 收藏書籍並加入書單
   - 為書籍評分

## 開發模式

設定環境變數以啟用開發模式：

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python run.py
```

## 常見問題

### 資料庫檔案位置

資料庫檔案預設位於 `instance/app.db`

### 重置資料庫

刪除 `instance/app.db` 檔案，然後重新執行遷移：

```bash
rm instance/app.db
flask db upgrade
```

