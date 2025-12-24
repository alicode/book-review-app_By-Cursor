"""
使用者模型
"""
from app import db
from datetime import datetime
from typing import Optional
import bcrypt


class User(db.Model):
    """使用者資料表"""
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # 關聯
    user_books = db.relationship('UserBook', backref='user', lazy=True, cascade='all, delete-orphan')
    ratings = db.relationship('Rating', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password: str) -> None:
        """
        設定密碼（使用 bcrypt 雜湊）
        
        Args:
            password: 明文密碼
        """
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password: str) -> bool:
        """
        檢查密碼是否正確
        
        Args:
            password: 明文密碼
        
        Returns:
            密碼是否正確
        """
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )
    
    def __repr__(self) -> str:
        return f'<User {self.username}>'

