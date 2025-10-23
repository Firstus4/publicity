from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    middle_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150), nullable=False)
    sex = db.Column(db.String(20))
    state = db.Column(db.String(120))
    lga = db.Column(db.String(120))
    dob = db.Column(db.String(20))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    ppa = db.Column(db.String(200))
    school = db.Column(db.String(300))
    unit = db.Column(db.String(200))
    room_allocated = db.Column(db.String(100))
    photo_filename = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default = datetime.utcnow)

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)
    role = db.Column(db.String(20), default='admin') 
    created_at = db.Column(db.DateTime, default = datetime.utcnow)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def is_super_admin(self):
        return self.role == 'super_admin'