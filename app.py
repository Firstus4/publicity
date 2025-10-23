import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from models import db, Admin
from public import public_bp
from dotenv import load_dotenv
from admin import admin_bp
from sqlalchemy import inspect

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback_secret') 
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # 4MB upload limit
app.config['SESSION_COOKIE_SECURE'] = os.getenv('FLASK_ENV') == 'production' 
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

csrf = CSRFProtect(app) 
login_manager = LoginManager(app)
login_manager.login_view = 'admin.login'
db.init_app(app)

migrate = Migrate(app, db)

@login_manager.user_loader
def load_user(admin_id):
    return Admin.query.get(int(admin_id))

with app.app_context():
    inspector = inspect(db.engine)
    if not inspector.has_table("student"):
        db.create_all()
    admin_email = os.getenv('ADMIN_EMAIL')
    admin_password = os.getenv('ADMIN_PASSWORD')

    if admin_email and admin_password:
        existing_admin = Admin.query.filter_by(email=admin_email).first()
        if not existing_admin:
            a = Admin(
                email=admin_email,
                password_hash=generate_password_hash(admin_password),
                role='super_admin'
            )
            db.session.add(a)
            db.session.commit()
            print(f"✅ Default super admin created: {admin_email}")
        else:
            print(f"ℹ️ Super admin already exists: {admin_email}")
    else:
        print("⚠️ No default admin created (ADMIN_EMAIL or ADMIN_PASSWORD missing).")


app.register_blueprint(public_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8000))
    print(f"Starting Flask app on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=True)
