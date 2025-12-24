"""
書籍相關路由（列表、詳細頁、排行榜）
"""
from flask import Blueprint, render_template, request
from app import db
from app.models.book import Book
from app.models.rating import Rating
from app.models.user_book import UserBook
from app.routes.auth import get_current_user, login_required
from sqlalchemy import func, desc
from typing import Optional

books_bp = Blueprint('books', __name__)


@books_bp.route('/')
def index() -> str:
    """
    首頁：顯示熱門排行榜和書籍列表
    
    Returns:
        首頁模板
    """
    user = get_current_user()
    
    # 取得熱門排行榜（平均評分 Top 10）
    top_rated = db.session.query(
        Book.id,
        Book.title,
        Book.author,
        Book.cover_image_url,
        func.avg(Rating.score).label('avg_score'),
        func.count(Rating.id).label('rating_count')
    ).join(Rating, Book.id == Rating.book_id)\
     .group_by(Book.id)\
     .order_by(desc('avg_score'))\
     .limit(10)\
     .all()
    
    # 取得收藏數排行榜（Top 10）
    top_collected = db.session.query(
        Book.id,
        Book.title,
        Book.author,
        Book.cover_image_url,
        func.count(UserBook.id).label('collection_count')
    ).join(UserBook, Book.id == UserBook.book_id)\
     .group_by(Book.id)\
     .order_by(desc('collection_count'))\
     .limit(10)\
     .all()
    
    # 取得所有書籍列表
    books = Book.query.order_by(Book.created_at.desc()).all()
    
    # 計算每本書的平均評分
    book_ratings = {}
    if books:
        rating_data = db.session.query(
            Rating.book_id,
            func.avg(Rating.score).label('avg_score'),
            func.count(Rating.id).label('count')
        ).group_by(Rating.book_id).all()
        
        for book_id, avg_score, count in rating_data:
            book_ratings[book_id] = {
                'avg_score': round(float(avg_score), 2),
                'count': count
            }
    
    # 如果使用者已登入，取得使用者的書單摘要
    user_stats = None
    if user:
        wishlist_count = UserBook.query.filter_by(
            user_id=user.id,
            status='wishlist'
        ).count()
        read_count = UserBook.query.filter_by(
            user_id=user.id,
            status='read'
        ).count()
        user_stats = {
            'wishlist_count': wishlist_count,
            'read_count': read_count
        }
    
    return render_template(
        'index.html',
        user=user,
        top_rated=top_rated,
        top_collected=top_collected,
        books=books,
        book_ratings=book_ratings,
        user_stats=user_stats
    )


@books_bp.route('/book/<int:book_id>')
def book_detail(book_id: int) -> str:
    """
    書籍詳細頁
    
    Args:
        book_id: 書籍 ID
    
    Returns:
        書籍詳細頁模板
    """
    book = Book.query.get_or_404(book_id)
    user = get_current_user()
    
    # 取得平均評分
    avg_rating = book.get_average_rating()
    rating_count = book.get_rating_count()
    collection_count = book.get_collection_count()
    
    # 如果使用者已登入，取得使用者的收藏狀態和評分
    user_book = None
    user_rating = None
    if user:
        user_book = UserBook.query.filter_by(
            user_id=user.id,
            book_id=book_id
        ).first()
        
        user_rating = Rating.query.filter_by(
            user_id=user.id,
            book_id=book_id
        ).first()
    
    return render_template(
        'book_detail.html',
        book=book,
        user=user,
        avg_rating=avg_rating,
        rating_count=rating_count,
        collection_count=collection_count,
        user_book=user_book,
        user_rating=user_rating
    )



