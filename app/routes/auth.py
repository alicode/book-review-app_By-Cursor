"""
使用者認證路由（登入、註冊、登出）
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models.user import User
from typing import Tuple, Optional

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register() -> str:
    """
    使用者註冊
    
    Returns:
        註冊頁面或重定向到首頁
    """
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        # 驗證輸入
        errors = []
        if not username:
            errors.append('使用者名稱不能為空')
        if not email:
            errors.append('Email 不能為空')
        if not password:
            errors.append('密碼不能為空')
        if password != password_confirm:
            errors.append('兩次密碼輸入不一致')
        if len(password) < 6:
            errors.append('密碼長度至少需要 6 個字元')
        
        # 檢查使用者名稱或 Email 是否已存在
        if User.query.filter_by(username=username).first():
            errors.append('使用者名稱已被使用')
        if User.query.filter_by(email=email).first():
            errors.append('Email 已被使用')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html')
        
        # 建立新使用者
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        # 自動登入
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        flash('註冊成功！', 'success')
        
        return redirect(url_for('books.index'))
    
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login() -> str:
    """
    使用者登入
    
    Returns:
        登入頁面或重定向到首頁
    """
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('請輸入使用者名稱和密碼', 'error')
            return render_template('login.html')
        
        # 查詢使用者
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('登入成功！', 'success')
            
            # 重定向到來源頁面或首頁
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('books.index'))
        else:
            flash('使用者名稱或密碼錯誤', 'error')
            return render_template('login.html')
    
    return render_template('login.html')


@auth_bp.route('/logout')
def logout() -> str:
    """
    使用者登出
    
    Returns:
        重定向到首頁
    """
    session.clear()
    flash('已成功登出', 'success')
    return redirect(url_for('books.index'))


def get_current_user() -> Optional[User]:
    """
    取得目前登入的使用者
    
    Returns:
        使用者物件，未登入時返回 None
    """
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None


def login_required(f):
    """
    登入驗證裝飾器
    """
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('請先登入', 'error')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    管理者驗證裝飾器（預留，MVP 階段可選實作）
    """
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        # TODO: 實作管理者檢查邏輯
        # if not user or not user.is_admin:
        #     flash('需要管理者權限', 'error')
        #     return redirect(url_for('books.index'))
        return f(*args, **kwargs)
    return decorated_function



