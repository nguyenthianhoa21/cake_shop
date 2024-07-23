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
    from .views import register_blueprints
    register_blueprints(app)
    
    return app

from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
