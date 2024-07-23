from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Ingredient
from app import db

# Khởi tạo blueprint cho admin ingredient
admin_ingredient = Blueprint('admin_ingredient', __name__)

@admin_ingredient.route('/ingredients', methods=['GET', 'POST'])
@login_required
def manage_ingredients():
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này.', 'error')
        return redirect(url_for('home.index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        quantity = float(request.form.get('quantity'))
        unit = request.form.get('unit')
        
        new_ingredient = Ingredient(
            name=name,
            quantity=quantity,
            unit=unit
        )
        db.session.add(new_ingredient)
        db.session.commit()
        flash('Đã thêm nguyên liệu mới.', 'success')
    
    ingredients = Ingredient.query.all()
    return render_template('admin/ingredients.html', user=current_user, ingredients=ingredients)

@admin_ingredient.route('/ingredients/delete/<int:ingredient_id>', methods=['POST'])
@login_required
def delete_ingredient(ingredient_id):
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này.', 'error')
        return redirect(url_for('home.index'))
    
    ingredient = Ingredient.query.get(ingredient_id)
    if ingredient:
        db.session.delete(ingredient)
        db.session.commit()
        flash('Đã xóa nguyên liệu.', 'success')
    else:
        flash('Nguyên liệu không tồn tại.', 'error')
    
    return redirect(url_for('admin_ingredient.manage_ingredients'))
