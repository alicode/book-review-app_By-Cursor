# 第 1 章：產品背景與目標
## 1.1 產品背景

本專案是一個以「**中文書籍**」為主的書本評論網站，目標使用者為一般讀者。
使用者可透過登入後的個人帳號，建立自己的書單、對書籍進行評分，並透過排行榜快速發現熱門書籍。
本產品為 **學習導向的 Portfolio 專案**，設計上以功能完整、架構清楚為優先，不追求過度商業化或複雜社群功能。

---

## 1.2 產品目標（Goals）

* 提供使用者一個簡單的平台，**整理個人書單與收藏**
* 讓使用者能對已閱讀的書籍進行評分
* 透過熱門排行榜，協助使用者發現值得閱讀的書籍
* 作為一個完整的全端練習專案（Flask + SQLite + Docker）

---

## 1.3 非目標（Out of Scope）

以下功能在 MVP 階段 **不納入**：

* 追蹤其他使用者 / 社交功能
* 即時聊天或通知系統
* 商業推薦、廣告或金流
* 行動 App（僅 Web）

---

## 1.4 技術限制（已確定）

* 前端：HTML / CSS / JavaScript
* 後端：Python Flask
* 資料庫：SQLite
* 部署方式：Docker（單容器或簡易 Compose）

---

# 第 2 章：使用者角色（User Persona）
## 2.1 訪客（Guest）

**身份說明**：
未登入使用者，可瀏覽網站公開資訊。

**可使用功能**：

* 瀏覽書籍列表
* 查看書籍評分（平均分）
* 查看熱門排行榜

**限制**：

* 無法收藏書籍
* 無法進行評分
* 無個人書單

---

## 2.2 註冊使用者（User）

**身份說明**：
完成註冊並登入的使用者，為本產品的核心使用族群。

**可使用功能**：

* 建立個人書單（收藏書籍）
* 書單狀態分類：

  * 想讀（Wishlist）
  * 已讀（Read）
* 對已收藏書籍進行評分
* 查看自己的書單列表

**設計重點**：

* 收藏與評分分離（可先收藏，之後再評分）
* 書單狀態可隨時修改

---

## 2.3 管理者（Admin）

**身份說明**：
負責維護系統資料的管理角色（單人或少量）。

**可使用功能**：

* 新增 / 編輯 / 刪除書籍資料
* 維護書籍基本資訊（書名、作者、封面、簡介）
* 管理不當內容（僅作預留，MVP 不實作細節）

---

# 第 3 章：核心功能定義（MVP）

## 3.1 MVP 功能清單（第一版必做）

#### 使用者系統

* 使用者註冊
* 使用者登入 / 登出
* 基本登入狀態驗證（Session）

---

#### 書籍瀏覽

* 書籍列表頁

  * 顯示書名、作者、平均評分
* 書籍詳細頁

  * 書籍封面
  * 書籍簡介
  * 平均評分
  * 使用者個人收藏 / 評分狀態

---

#### 書單與收藏

* 收藏書籍功能
* 書單狀態分類：

  * 想讀（Wishlist）
  * 已讀（Read）
* 使用者個人書單頁（我的書單）

---

#### 評分系統

* 登入後可對書籍進行 1–5 星評分
* 每位使用者對每本書僅能有一筆評分
* 修改評分會即時影響平均分數

---

#### 熱門排行榜

* 排行榜依據：

  * 平均評分
  * 收藏人數
* 排行榜僅顯示前 N 名（如 Top 10）

---

## 3.2 非 MVP（延後實作）

* 書籍搜尋
* 評論文字內容
* 社交功能（追蹤、留言）
* 推薦演算法

---

# 第 4 章：使用流程（User Flow）
---

## 4.1 訪客流程（未登入）

**入口：首頁 `/`**

1. 訪客進入首頁
2. 顯示內容：

   * 熱門排行榜（Top N）
   * 全部書籍列表
3. 訪客點擊書籍
4. 進入書籍詳細頁

   * 可查看書籍資訊與平均評分
   * 提示「登入後可收藏與評分」
5. 訪客可選擇：

   * 註冊帳號
   * 登入帳號

---

## 4.2 註冊 / 登入流程

1. 訪客點擊「註冊」
2. 填寫帳號資訊（Email / Username / Password）
3. 註冊成功後自動登入
4. 導向「登入後首頁」

---

## 4.3 登入使用者流程

**入口：登入後首頁 `/`**

1. 顯示內容：

   * 我的書單摘要

     * 想讀數量
     * 已讀數量
   * 熱門排行榜
   * 全部書籍列表
2. 使用者點擊書籍
3. 進入書籍詳細頁
4. 可進行操作：

   * 加入書單（想讀 / 已讀）
   * 給予或修改評分
5. 使用者可進入：

   * 我的書單頁 `/my-books`

---

## 4.4 管理者流程（Admin）

1. 管理者登入後
2. 進入後台管理頁
3. 新增 / 編輯 / 刪除書籍
4. 書籍資料即時更新於前台

---



# 第 5 章：資料庫設計（Database Design）
### 5.1 設計原則

* 採用正規化設計，避免資料重複
* 使用者、書籍、收藏、評分分離
* 支援未來功能擴充（評論、搜尋）

---

## 5.2 ERD（文字表示）

```
User
 ├─ id (PK)
 ├─ username
 ├─ email
 ├─ password_hash
 └─ created_at

Book
 ├─ id (PK)
 ├─ title
 ├─ author
 ├─ description
 ├─ cover_image_url
 └─ created_at

UserBook  (收藏 / 書單)
 ├─ id (PK)
 ├─ user_id (FK → User.id)
 ├─ book_id (FK → Book.id)
 ├─ status  (wishlist / read)
 └─ created_at

Rating
 ├─ id (PK)
 ├─ user_id (FK → User.id)
 ├─ book_id (FK → Book.id)
 ├─ score (1–5)
 └─ created_at
```

---

## 5.3 SQLite 資料表結構（建議）

### User

| 欄位            | 型別          | 說明     |
| ------------- | ----------- | ------ |
| id            | INTEGER PK  | 使用者 ID |
| username      | TEXT UNIQUE | 使用者名稱  |
| email         | TEXT UNIQUE | Email  |
| password_hash | TEXT        | 密碼雜湊   |
| created_at    | DATETIME    | 建立時間   |

---

### Book

| 欄位              | 型別         | 說明    |
| --------------- | ---------- | ----- |
| id              | INTEGER PK | 書籍 ID |
| title           | TEXT       | 書名    |
| author          | TEXT       | 作者    |
| description     | TEXT       | 簡介    |
| cover_image_url | TEXT       | 封面圖片  |
| created_at      | DATETIME   | 建立時間  |

---

### UserBook

| 欄位         | 型別         | 說明              |
| ---------- | ---------- | --------------- |
| id         | INTEGER PK | 收藏 ID           |
| user_id    | INTEGER FK | 使用者             |
| book_id    | INTEGER FK | 書籍              |
| status     | TEXT       | wishlist / read |
| created_at | DATETIME   | 收藏時間            |

> 🔒 建議加上 `(user_id, book_id)` UNIQUE constraint

---

### Rating

| 欄位         | 型別         | 說明    |
| ---------- | ---------- | ----- |
| id         | INTEGER PK | 評分 ID |
| user_id    | INTEGER FK | 使用者   |
| book_id    | INTEGER FK | 書籍    |
| score      | INTEGER    | 1–5   |
| created_at | DATETIME   | 評分時間  |

> 🔒 建議加上 `(user_id, book_id)` UNIQUE constraint

---

#  第 6 章：技術架構與部署
## 6.1 後端架構

* Flask **Application Factory Pattern**
* 使用 Blueprint 拆分模組
* ORM：Flask-SQLAlchemy
* Authentication：Session（Flask-Login 可後續加入）

---

## 6.2 專案目錄結構（建議）

```
book-review-app/
│
├── app/
│   ├── __init__.py          # create_app()
│   ├── config.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── book.py
│   │   ├── user_book.py
│   │   └── rating.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py          # login / register
│   │   ├── books.py         # list / detail
│   │   ├── user_books.py    # 收藏 / 書單
│   │   └── admin.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── book_detail.html
│   │   └── my_books.html
│   │
│   └── static/
│       ├── css/
│       └── js/
│
├── migrations/
├── instance/
│   └── app.db               # SQLite
│
├── Dockerfile
├── requirements.txt
├── run.py
└── README.md
```


---

## 6.3 Flask Application Factory（核心）

```python
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.books import books_bp
    from app.routes.user_books import user_books_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(user_books_bp)

    return app
```

```python
# run.py
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
```

---

## 6.4 SQLAlchemy Model 範例

### User

```python
# app/models/user.py
from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

---

### Book

```python
# app/models/book.py
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255))
    description = db.Column(db.Text)
    cover_image_url = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
```

---

### UserBook（收藏）

```python
# app/models/user_book.py
class UserBook(db.Model):
    __table_args__ = (
        db.UniqueConstraint('user_id', 'book_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    status = db.Column(db.String(20))  # wishlist / read
    created_at = db.Column(db.DateTime)
```

---

### Rating

```python
# app/models/rating.py
class Rating(db.Model):
    __table_args__ = (
        db.UniqueConstraint('user_id', 'book_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    score = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
```

---

## 6.5 排行榜 SQL 思路（重要）

### 平均評分排行榜

```sql
SELECT book_id, AVG(score) AS avg_score
FROM rating
GROUP BY book_id
ORDER BY avg_score DESC
LIMIT 10;
```

### 收藏數排行榜

```sql
SELECT book_id, COUNT(*) AS total
FROM user_book
GROUP BY book_id
ORDER BY total DESC
LIMIT 10;
```

---

## 6.6 Dockerfile（單容器）

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=run.py
ENV FLASK_ENV=development

CMD ["python", "run.py"]
```

---

## 6.7 requirements.txt（建議）

```
Flask
Flask-SQLAlchemy
Flask-Migrate
Werkzeug
```

---
