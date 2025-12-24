"""
完整的資料庫設定腳本
"""
from app import create_app, db
from app.models import User, Book, UserBook, Rating
import os

app = create_app()

with app.app_context():
    # 檢查資料庫 URI
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    print(f"資料庫 URI: {db_uri}")
    
    # 如果是 SQLite，檢查檔案路徑
    if db_uri.startswith('sqlite:///'):
        db_path = db_uri.replace('sqlite:///', '')
        print(f"資料庫檔案路徑: {db_path}")
        
        # 確保目錄存在
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
            print(f"資料庫目錄已確保存在: {db_dir}")
    
    # 刪除所有現有資料表（如果存在）
    print("\n檢查現有資料表...")
    try:
        db.drop_all()
        print("已刪除現有資料表（如果存在）")
    except Exception as e:
        print(f"刪除資料表時發生錯誤（可能沒有資料表）: {e}")
    
    # 建立所有資料表
    print("\n建立資料表...")
    db.create_all()
    
    # 驗證資料表是否建立成功
    print("\n驗證資料表...")
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    
    print("已建立的資料表：")
    for table in tables:
        print(f"  ✓ {table}")
    
    # 檢查模型對應的資料表
    expected_tables = ['user', 'book', 'user_book', 'rating']
    missing_tables = [t for t in expected_tables if t not in tables]
    
    if missing_tables:
        print(f"\n警告：缺少以下資料表: {missing_tables}")
    else:
        print("\n✓ 所有資料表已成功建立！")



