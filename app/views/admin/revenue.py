from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Order, Revenue
from app import db
from datetime import datetime

# Khởi tạo blueprint cho admin revenue
admin_revenue = Blueprint('admin_revenue', __name__)

@admin_revenue.route('/revenue', methods=['GET', 'POST'])
@login_required
def manage_revenue():
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này.', 'error')
        return redirect(url_for('home.index'))
    
    if request.method == 'POST':
        date_str = request.form.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        total_revenue = float(request.form.get('total_revenue'))
        
        revenue_entry = Revenue.query.filter_by(date=date).first()
        if revenue_entry:
            revenue_entry.total_revenue = total_revenue
            flash('Đã cập nhật doanh thu.', 'success')
        else:
            new_revenue = Revenue(
                date=date,
                total_revenue=total_revenue
            )
            db.session.add(new_revenue)
            flash('Đã thêm doanh thu mới.', 'success')
        
        db.session.commit()
    
    revenues = Revenue.query.all()
    return render_template('admin/revenue.html', user=current_user, revenues=revenues)
