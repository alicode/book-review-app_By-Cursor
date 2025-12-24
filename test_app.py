"""
簡單的應用程式測試腳本
"""
import sys

def test_imports():
    """測試所有模組是否能正常導入"""
    print("測試模組導入...")
    try:
        from app import create_app, db
        from app.models import User, Book, UserBook, Rating
        from app.routes.auth import auth_bp
        from app.routes.books import books_bp
        from app.routes.user_books import user_books_bp
        from app.routes.admin import admin_bp
        print("✓ 所有模組導入成功")
        return True
    except Exception as e:
        print(f"✗ 模組導入失敗: {e}")
        return False

def test_app_creation():
    """測試應用程式是否能正常建立"""
    print("\n測試應用程式建立...")
    try:
        from app import create_app
        app = create_app()
        print(f"✓ 應用程式建立成功")
        print(f"  - 應用程式名稱: {app.name}")
        print(f"  - Blueprint 數量: {len(app.blueprints)}")
        return True
    except Exception as e:
        print(f"✗ 應用程式建立失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_models():
    """測試資料模型"""
    print("\n測試資料模型...")
    try:
        from app.models import User, Book, UserBook, Rating
        
        # 測試 User 模型
        assert hasattr(User, 'username')
        assert hasattr(User, 'set_password')
        assert hasattr(User, 'check_password')
        
        # 測試 Book 模型
        assert hasattr(Book, 'title')
        assert hasattr(Book, 'get_average_rating')
        
        # 測試 UserBook 模型
        assert hasattr(UserBook, 'status')
        
        # 測試 Rating 模型
        assert hasattr(Rating, 'score')
        
        print("✓ 所有資料模型正常")
        return True
    except Exception as e:
        print(f"✗ 資料模型測試失敗: {e}")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("應用程式測試")
    print("=" * 50)
    
    success = True
    success &= test_imports()
    success &= test_app_creation()
    success &= test_models()
    
    print("\n" + "=" * 50)
    if success:
        print("✓ 所有測試通過！")
        sys.exit(0)
    else:
        print("✗ 部分測試失敗")
        sys.exit(1)



