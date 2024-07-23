from flask import Blueprint, render_template

# Khởi tạo blueprint cho home
home = Blueprint('home', __name__)

@home.route('/')
def index():
    return render_template('home.html')
