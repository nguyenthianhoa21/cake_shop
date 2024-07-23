from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Khởi tạo đối tượng SQLAlchemy
db = SQLAlchemy()

# Khởi tạo đối tượng LoginManager
login_manager = LoginManager()

def create_app():
    # Khởi tạo ứng dụng Flask
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Khởi tạo các tiện ích mở rộng với ứng dụng Flask
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Đăng ký các blueprint cho ứng dụng
    from .views.home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .views.user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')

    from .views.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .views.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from .views.admin.product import admin_product as admin_product_blueprint
    app.register_blueprint(admin_product_blueprint, url_prefix='/admin')
    
    from .views.admin.ingredient import admin_ingredient as admin_ingredient_blueprint
    app.register_blueprint(admin_ingredient_blueprint, url_prefix='/admin')
    
    from .views.admin.revenue import admin_revenue as admin_revenue_blueprint
    app.register_blueprint(admin_revenue_blueprint, url_prefix='/admin')
    
    return app

from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
