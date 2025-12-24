"""
管理者路由（書籍管理）
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.book import Book
from app.routes.auth import get_current_user, login_required, admin_required
from typing import Optional

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/books')
@login_required
# @admin_required  # MVP 階段可選
def book_list() -> str:
    """
    管理者書籍列表頁面
    
    Returns:
        書籍管理頁面模板
    """
    books = Book.query.order_by(Book.created_at.desc()).all()
    return render_template('admin/books.html', books=books)


@admin_bp.route('/books/new', methods=['GET', 'POST'])
@login_required
# @admin_required  # MVP 階段可選
def book_new() -> str:
    """
    新增書籍
    
    Returns:
        新增書籍表單或重定向
    """
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        description = request.form.get('description', '').strip()
        cover_image_url = request.form.get('cover_image_url', '').strip()
        
        if not title:
            flash('書名不能為空', 'error')
            return render_template('admin/book_form.html')
        
        book = Book(
            title=title,
            author=author if author else None,
            description=description if description else None,
            cover_image_url=cover_image_url if cover_image_url else None
        )
        
        db.session.add(book)
        db.session.commit()
        
        flash('書籍已新增', 'success')
        return redirect(url_for('admin.book_list'))
    
    return render_template('admin/book_form.html', book=None)


@admin_bp.route('/books/<int:book_id>/edit', methods=['GET', 'POST'])
@login_required
# @admin_required  # MVP 階段可選
def book_edit(book_id: int) -> str:
    """
    編輯書籍
    
    Args:
        book_id: 書籍 ID
    
    Returns:
        編輯書籍表單或重定向
    """
    book = Book.query.get_or_404(book_id)
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        description = request.form.get('description', '').strip()
        cover_image_url = request.form.get('cover_image_url', '').strip()
        
        if not title:
            flash('書名不能為空', 'error')
            return render_template('admin/book_form.html', book=book)
        
        book.title = title
        book.author = author if author else None
        book.description = description if description else None
        book.cover_image_url = cover_image_url if cover_image_url else None
        
        db.session.commit()
        
        flash('書籍已更新', 'success')
        return redirect(url_for('admin.book_list'))
    
    return render_template('admin/book_form.html', book=book)


@admin_bp.route('/books/<int:book_id>/delete', methods=['POST'])
@login_required
# @admin_required  # MVP 階段可選
def book_delete(book_id: int) -> str:
    """
    刪除書籍
    
    Args:
        book_id: 書籍 ID
    
    Returns:
        重定向到書籍列表
    """
    book = Book.query.get_or_404(book_id)
    
    db.session.delete(book)
    db.session.commit()
    
    flash('書籍已刪除', 'success')
    return redirect(url_for('admin.book_list'))


