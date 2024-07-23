from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Product
from app import db

# Khởi tạo blueprint cho admin product
admin_product = Blueprint('admin_product', __name__)

@admin_product.route('/products', methods=['GET', 'POST'])
@login_required
def manage_products():
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này.', 'error')
        return redirect(url_for('home.index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        estimated_time = int(request.form.get('estimated_time'))
        can_make = request.form.get('can_make') == 'yes'
        
        new_product = Product(
            name=name,
            description=description,
            price=price,
            estimated_time=estimated_time,
            can_make=can_make,
            image='default.png'  # Sử dụng ảnh mặc định, bạn có thể cập nhật phần tải lên ảnh sau
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Đã thêm sản phẩm mới.', 'success')
    
    products = Product.query.all()
    return render_template('admin/products.html', user=current_user, products=products)

@admin_product.route('/products/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này.', 'error')
        return redirect(url_for('home.index'))
    
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        flash('Đã xóa sản phẩm.', 'success')
    else:
        flash('Sản phẩm không tồn tại.', 'error')
    
    return redirect(url_for('admin_product.manage_products'))
