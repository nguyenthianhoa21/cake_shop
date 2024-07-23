from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import user
from app.models import Order, Product
from app import db

@user.route('/orders', methods=['GET', 'POST'])
@login_required
def order_list():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        product = Product.query.get(product_id)

        if product:
            if product.can_make and product.current_orders + quantity <= 10:  # Giả sử giới hạn là 10 đơn
                total_price = product.price * quantity
                new_order = Order(
                    user_id=current_user.id,
                    product_id=product_id,
                    quantity=quantity,
                    total_price=total_price
                )
                product.current_orders += quantity
                db.session.add(new_order)
                db.session.commit()
                flash('Đặt hàng thành công!', 'success')
            else:
                flash('Không thể đặt hàng. Số lượng bánh đang làm quá nhiều hoặc không thể làm.', 'error')
        else:
            flash('Sản phẩm không tồn tại.', 'error')

    orders = Order.query.filter_by(user_id=current_user.id).all()
    products = Product.query.all()
    return render_template('user/order.html', user=current_user, orders=orders, products=products)
