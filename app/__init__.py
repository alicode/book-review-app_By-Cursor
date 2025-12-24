"""
Flask Application Factory
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class='app.config.Config'):
    """
    建立並配置 Flask 應用程式
    
    Args:
        config_class: 設定類別的路徑（字串）
    
    Returns:
        Flask 應用程式實例
    """
    app = Flask(__name__)
    
    # 載入設定
    app.config.from_object(config_class)
    
    # 如果設定類別有 init_app 方法，則呼叫它（用於啟用 WAL 模式等）
    import importlib
    module_path, class_name = config_class.rsplit('.', 1)
    module = importlib.import_module(module_path)
    config_obj = getattr(module, class_name)
    if hasattr(config_obj, 'init_app'):
        config_obj.init_app(app)
    
    # 確保資料庫目錄存在
    import os
    database_uri = app.config['SQLALCHEMY_DATABASE_URI']
    if database_uri.startswith('sqlite:///'):
        db_path = database_uri.replace('sqlite:///', '')
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
    
    # 初始化擴充套件
    db.init_app(app)
    migrate.init_app(app, db)
    
    # 註冊 Blueprint
    from app.routes.auth import auth_bp
    from app.routes.books import books_bp
    from app.routes.user_books import user_books_bp
    from app.routes.admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(user_books_bp)
    app.register_blueprint(admin_bp)
    
    return app

