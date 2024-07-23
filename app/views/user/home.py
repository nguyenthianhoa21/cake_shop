from flask import render_template
from flask_login import login_required, current_user
from . import user

@user.route('/home')
@login_required
def home():
    return render_template('user/home.html', user=current_user)
