from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import admin
from app.models import Order, Product
from app import db

@admin.route('/home', methods=['GET', 'POST'])
@login_required
def admin_home():
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này.', 'error')
        return redirect(url_for('home.index'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        order_id = request.form.get('order_id')
        order = Order.query.get(order_id)
        
        if action == 'approve_payment' and order:
            order.status = 'Paid'
            db.session.commit()
            flash('Đã xác nhận thanh toán.', 'success')
        elif action == 'complete_order' and order:
            order.status = 'Completed'
            product = Product.query.get(order.product_id)
            if product:
                product.current_orders -= order.quantity
                db.session.commit()
            flash('Đã hoàn thành đơn hàng.', 'success')
        else:
            flash('Đơn hàng không tồn tại.', 'error')

    orders = Order.query.all()
    return render_template('admin/home.html', user=current_user, orders=orders)
