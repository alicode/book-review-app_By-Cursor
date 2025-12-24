### 專案識別
專案名稱:book-review-app 完整規格查看 docs/PRD.md

### 核心守則 (不可違反)
1. 程式碼必用 Python 3.12，符合 PEP 8 與型別註解慣例。
2. 架構：Flask Blueprint 與 SQLAlchemy ORM；資料表遷移交給 Flask-Migrate。
3. 密碼必須 bcrypt 雜湊並加鹽（依 OWASP 指南）。
4. 資料庫採 SQLite，啟用 WAL，避免拼接 SQL，全部使用參數化查詢。
5. 回覆一律使用繁體中文；遵守 KISS 與 DRY 原則，避免過度工程。
6. 在撰寫程式碼時，嚴格遵守 docs/PRD.md 的規則。
