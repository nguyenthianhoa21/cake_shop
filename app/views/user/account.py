from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import user
from app.models import User
from app import db

@user.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'change_password':
            old_password = request.form.get('old_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            if not check_password_hash(current_user.password, old_password):
                flash('Mật khẩu cũ không đúng.', 'error')
            elif new_password != confirm_password:
                flash('Mật khẩu mới không khớp.', 'error')
            else:
                current_user.password = generate_password_hash(new_password, method='sha256')
                db.session.commit()
                flash('Đổi mật khẩu thành công.', 'success')
        
        elif action == 'update_bank_info':
            bank_account = request.form.get('bank_account')
            bank_name = request.form.get('bank_name')
            
            current_user.bank_account = bank_account
            current_user.bank_name = bank_name
            db.session.commit()
            flash('Cập nhật thông tin tài khoản ngân hàng thành công.', 'success')
    
    return render_template('user/account.html', user=current_user)
