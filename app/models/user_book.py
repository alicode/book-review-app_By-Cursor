"""
使用者書籍收藏模型
"""
from app import db
from datetime import datetime
from typing import Optional


class UserBook(db.Model):
    """使用者書籍收藏資料表（書單）"""
    __tablename__ = 'user_book'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'book_id', name='uq_user_book'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False)  # 'wishlist' 或 'read'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        return f'<UserBook user_id={self.user_id} book_id={self.book_id} status={self.status}>'

