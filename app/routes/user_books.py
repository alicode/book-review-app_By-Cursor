"""
使用者書單相關路由（收藏、評分、我的書單）
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models.book import Book
from app.models.user_book import UserBook
from app.models.rating import Rating
from app.routes.auth import get_current_user, login_required
from typing import Tuple

user_books_bp = Blueprint('user_books', __name__, url_prefix='/my-books')


@user_books_bp.route('/')
@login_required
def my_books() -> str:
    """
    我的書單頁面
    
    Returns:
        我的書單模板
    """
    user = get_current_user()
    
    # 取得使用者的所有收藏
    user_books = UserBook.query.filter_by(user_id=user.id).all()
    
    # 分類書單
    wishlist = []
    read_list = []
    
    for user_book in user_books:
        book = user_book.book
        rating = Rating.query.filter_by(
            user_id=user.id,
            book_id=book.id
        ).first()
        
        book_data = {
            'book': book,
            'user_book': user_book,
            'rating': rating,
            'avg_rating': book.get_average_rating()
        }
        
        if user_book.status == 'wishlist':
            wishlist.append(book_data)
        else:
            read_list.append(book_data)
    
    return render_template(
        'my_books.html',
        user=user,
        wishlist=wishlist,
        read_list=read_list
    )


@user_books_bp.route('/add', methods=['POST'])
@login_required
def add_book() -> str:
    """
    加入書單（收藏書籍）
    
    Returns:
        JSON 回應或重定向
    """
    user = get_current_user()
    book_id = request.form.get('book_id', type=int)
    status = request.form.get('status', 'wishlist')  # 'wishlist' 或 'read'
    
    if not book_id:
        flash('無效的書籍 ID', 'error')
        return redirect(url_for('books.index'))
    
    if status not in ['wishlist', 'read']:
        status = 'wishlist'
    
    book = Book.query.get_or_404(book_id)
    
    # 檢查是否已經收藏
    existing = UserBook.query.filter_by(
        user_id=user.id,
        book_id=book_id
    ).first()
    
    if existing:
        # 更新狀態
        existing.status = status
        flash('書單狀態已更新', 'success')
    else:
        # 新增收藏
        user_book = UserBook(
            user_id=user.id,
            book_id=book_id,
            status=status
        )
        db.session.add(user_book)
        flash('已加入書單', 'success')
    
    db.session.commit()
    
    return redirect(url_for('books.book_detail', book_id=book_id))


@user_books_bp.route('/remove', methods=['POST'])
@login_required
def remove_book() -> str:
    """
    移除書單（取消收藏）
    
    Returns:
        重定向
    """
    user = get_current_user()
    book_id = request.form.get('book_id', type=int)
    
    if not book_id:
        flash('無效的書籍 ID', 'error')
        return redirect(url_for('books.index'))
    
    user_book = UserBook.query.filter_by(
        user_id=user.id,
        book_id=book_id
    ).first()
    
    if user_book:
        db.session.delete(user_book)
        db.session.commit()
        flash('已從書單移除', 'success')
    
    return redirect(url_for('books.book_detail', book_id=book_id))


@user_books_bp.route('/update-status', methods=['POST'])
@login_required
def update_status() -> str:
    """
    更新書單狀態（想讀 / 已讀）
    
    Returns:
        重定向
    """
    user = get_current_user()
    book_id = request.form.get('book_id', type=int)
    status = request.form.get('status', 'wishlist')
    
    if not book_id:
        flash('無效的書籍 ID', 'error')
        return redirect(url_for('books.index'))
    
    if status not in ['wishlist', 'read']:
        flash('無效的狀態', 'error')
        return redirect(url_for('books.book_detail', book_id=book_id))
    
    user_book = UserBook.query.filter_by(
        user_id=user.id,
        book_id=book_id
    ).first()
    
    if user_book:
        user_book.status = status
        db.session.commit()
        flash('書單狀態已更新', 'success')
    else:
        flash('找不到該書籍的收藏記錄', 'error')
    
    return redirect(url_for('books.book_detail', book_id=book_id))


@user_books_bp.route('/rate', methods=['POST'])
@login_required
def rate_book() -> str:
    """
    評分書籍（1-5 星）
    
    Returns:
        重定向
    """
    user = get_current_user()
    book_id = request.form.get('book_id', type=int)
    score = request.form.get('score', type=int)
    
    if not book_id or not score:
        flash('無效的輸入', 'error')
        return redirect(url_for('books.book_detail', book_id=book_id))
    
    if score < 1 or score > 5:
        flash('評分必須在 1 到 5 之間', 'error')
        return redirect(url_for('books.book_detail', book_id=book_id))
    
    book = Book.query.get_or_404(book_id)
    
    # 檢查是否已經評分
    existing_rating = Rating.query.filter_by(
        user_id=user.id,
        book_id=book_id
    ).first()
    
    if existing_rating:
        # 更新評分
        existing_rating.score = score
        flash('評分已更新', 'success')
    else:
        # 新增評分
        rating = Rating(
            user_id=user.id,
            book_id=book_id,
            score=score
        )
        db.session.add(rating)
        flash('評分已提交', 'success')
    
    db.session.commit()
    
    return redirect(url_for('books.book_detail', book_id=book_id))


