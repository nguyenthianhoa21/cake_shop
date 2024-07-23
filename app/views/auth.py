from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app.models import User
from app import db

# Khởi tạo blueprint cho auth
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin.admin_home'))
            else:
                return redirect(url_for('user.home'))
        else:
            flash('Đăng nhập thất bại. Vui lòng kiểm tra lại tên đăng nhập và mật khẩu.', 'error')
    return render_template('auth/login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        bank_account = request.form.get('bank_account')
        bank_name = request.form.get('bank_name')

        if password != confirm_password:
            flash('Mật khẩu không khớp. Vui lòng thử lại.', 'error')
            return redirect(url_for('auth.signup'))

        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            fullname=fullname,
            email=email,
            phone=phone,
            password=hashed_password,
            bank_account=bank_account,
            bank_name=bank_name
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('user.home'))
    return render_template('auth/signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))
