"""
應用程式設定檔
"""
import os
from pathlib import Path

# 取得專案根目錄
BASE_DIR = Path(__file__).parent.parent

class Config:
    """基礎設定類別"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{BASE_DIR / "instance" / "app.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'check_same_thread': False,
            'timeout': 20,
        },
        'pool_pre_ping': True,
    }
    
    @staticmethod
    def init_app(app):
        """初始化應用程式設定"""
        # 為 SQLite 啟用 WAL 模式
        database_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        if database_uri.startswith('sqlite:///'):
            # 使用事件監聽器在連線建立時設定 WAL
            from sqlalchemy import event
            from sqlalchemy.engine import Engine
            
            @event.listens_for(Engine, "connect")
            def set_sqlite_pragma(dbapi_conn, connection_record):
                """設定 SQLite WAL 模式"""
                cursor = dbapi_conn.cursor()
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.close()

