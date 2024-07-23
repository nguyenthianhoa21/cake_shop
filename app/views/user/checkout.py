from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import user
from app.models import Order
from app import db
import os

# Cấu hình đường dẫn lưu trữ ảnh hóa đơn
UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout_page():
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        file = request.files['receipt_image']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            order = Order.query.get(order_id)
            if order:
                order.receipt_image = filename
                order.status = 'Pending Admin Approval'
                db.session.commit()
                flash('Đã tải lên hóa đơn. Đang chờ admin xử lý.', 'success')
            else:
                flash('Đơn hàng không tồn tại.', 'error')
        else:
            flash('Tệp không hợp lệ. Vui lòng tải lên ảnh có định dạng png, jpg, jpeg hoặc gif.', 'error')
    
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('user/checkout.html', user=current_user, orders=orders)
