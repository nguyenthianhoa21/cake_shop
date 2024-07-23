import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    admin_user = User(
        username='admin_pmec5',
        fullname='Admin User',
        email='trinhan06032003@gmail.com',
        phone='0586471106',
        password=generate_password_hash('admin_password_pmec'),
        bank_account='210405092004',
        bank_name='MB Bank',
        is_admin=True
    )
    db.session.add(admin_user)
    db.session.commit()
    print('Admin user created successfully!')
