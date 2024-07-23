# Khởi tạo các blueprint
from .user import user
from .admin import admin
from .auth import auth
from .admin.product import admin_product
from .admin.ingredient import admin_ingredient
from .admin.revenue import admin_revenue

# Đăng ký các blueprint với ứng dụng
def register_blueprints(app):
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(auth)
    app.register_blueprint(admin_product, url_prefix='/admin')
    app.register_blueprint(admin_ingredient, url_prefix='/admin')
    app.register_blueprint(admin_revenue, url_prefix='/admin')
