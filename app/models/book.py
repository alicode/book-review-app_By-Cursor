"""
書籍模型
"""
from app import db
from datetime import datetime
from typing import Optional


class Book(db.Model):
    """書籍資料表"""
    __tablename__ = 'book'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    author = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    cover_image_url = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # 關聯
    user_books = db.relationship('UserBook', backref='book', lazy=True, cascade='all, delete-orphan')
    ratings = db.relationship('Rating', backref='book', lazy=True, cascade='all, delete-orphan')
    
    def get_average_rating(self) -> Optional[float]:
        """
        取得平均評分
        
        Returns:
            平均評分（無評分時返回 None）
        """
        if not self.ratings:
            return None
        total = sum(rating.score for rating in self.ratings)
        return round(total / len(self.ratings), 2)
    
    def get_rating_count(self) -> int:
        """
        取得評分數量
        
        Returns:
            評分數量
        """
        return len(self.ratings)
    
    def get_collection_count(self) -> int:
        """
        取得收藏數量
        
        Returns:
            收藏數量
        """
        return len(self.user_books)
    
    def __repr__(self) -> str:
        return f'<Book {self.title}>'

