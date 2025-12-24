# 書籍評論網站 (Book Review App)

一個以中文書籍為主的書本評論網站，使用 Flask 建置。

## 功能特色

- 使用者註冊、登入、登出
- 書籍瀏覽（列表、詳細頁）
- 個人書單管理（想讀、已讀）
- 書籍評分系統（1-5 星）
- 熱門排行榜（平均評分、收藏數）
- 管理者後台（新增、編輯、刪除書籍）

## 技術棧

- **後端框架**: Flask 3.1.2+
- **資料庫**: SQLite（啟用 WAL 模式）
- **ORM**: Flask-SQLAlchemy
- **資料庫遷移**: Flask-Migrate
- **密碼雜湊**: bcrypt
- **Python 版本**: 3.12+

## 安裝與設定

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

或使用 uv：
假若沒有uv 程式,需要[安裝uv](https://docs.astral.sh/uv/getting-started/installation/) ,如下
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**安裝 python 虛擬環境**
python 3.12 以上
```bash
uv venv -p 3.12 env
source env/bin/activate
```
假若沒有 python3.12 ,需要透過 uv 安裝python3.12
```bash
uv python list
```
```
cpython-3.14.0rc1-linux-x86_64-gnu                 <download available>
cpython-3.14.0rc1+freethreaded-linux-x86_64-gnu    <download available>
cpython-3.13.5-linux-x86_64-gnu                    <download available>
cpython-3.13.5+freethreaded-linux-x86_64-gnu       <download available>
cpython-3.12.11-linux-x86_64-gnu                   <download available>
```
```bash
uv python install cpython-3.12.11-linux-x86_64-gnu
```

```bash
uv pip install -r pyproject.toml
```

### 2. 初始化資料庫

**方法一：使用設定腳本（推薦，簡單快速）**

```bash
python setup_db.py
```

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

### 3. 執行應用程式

```bash
python run.py
```

應用程式將在 `http://0.0.0.0:5000` 啟動。

## Docker 部署

### 建立映像

```bash
docker build -t book-review-app .
```

### 執行容器

```bash
docker run -p 5000:5000 book-review-app
```

## 專案結構

```
book-review-app/
├── app/
│   ├── __init__.py          # Application Factory
│   ├── config.py            # 應用程式設定
│   ├── models/              # 資料模型
│   │   ├── user.py
│   │   ├── book.py
│   │   ├── user_book.py
│   │   └── rating.py
│   ├── routes/              # 路由 Blueprint
│   │   ├── auth.py
│   │   ├── books.py
│   │   ├── user_books.py
│   │   └── admin.py
│   ├── templates/           # HTML 模板
│   └── static/              # 靜態檔案
│       ├── css/
│       └── js/
├── migrations/              # 資料庫遷移檔案
├── instance/                # 資料庫檔案（.gitignore）
├── docs/                    # 文件
├── Dockerfile
├── requirements.txt
└── run.py
```

## 環境變數

- `SECRET_KEY`: Flask secret key（預設為開發用 key）
- `DATABASE_URL`: 資料庫連線 URL（預設為 SQLite）

## 開發說明

本專案遵循以下開發規範：

- Python 3.12+
- PEP 8 程式碼風格
- 型別註解
- Flask Application Factory Pattern
- SQLAlchemy ORM
- bcrypt 密碼雜湊（OWASP 指南）
- SQLite WAL 模式
- 參數化查詢（防止 SQL 注入）

## 授權

本專案為學習導向的 Portfolio 專案。

