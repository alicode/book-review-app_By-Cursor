"""
評分模型
"""
from app import db
from datetime import datetime
from typing import Optional


class Rating(db.Model):
    """評分資料表"""
    __tablename__ = 'rating'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'book_id', name='uq_user_book_rating'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False, index=True)
    score = db.Column(db.Integer, nullable=False)  # 1-5
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        return f'<Rating user_id={self.user_id} book_id={self.book_id} score={self.score}>'

