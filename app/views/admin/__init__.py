from flask import Blueprint

# Khởi tạo blueprint cho admin
admin = Blueprint('admin', __name__)

# Import các view để đăng ký với blueprint
from . import home, product, ingredient, revenue
