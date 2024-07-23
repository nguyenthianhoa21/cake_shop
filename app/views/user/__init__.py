from flask import Blueprint

# Khởi tạo blueprint cho user
user = Blueprint('user', __name__)

# Import các view để đăng ký với blueprint
from . import home, account, product, order, checkout
