"""
資料模型模組
"""
from app.models.user import User
from app.models.book import Book
from app.models.user_book import UserBook
from app.models.rating import Rating

__all__ = ['User', 'Book', 'UserBook', 'Rating']



