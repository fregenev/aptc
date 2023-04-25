from app import app

from app import db
from app import bcrypt

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    street = db.Column(db.String(length=30), nullable=False)
    city = db.Column(db.String(length=20), nullable=False)
    lga = db.Column(db.String(length=20), nullable=True)
    state = db.Column(db.String(length=20), nullable=False)
    country = db.Column(db.String(length=20), nullable=False)
    qualification = db.Column(db.String(length=20), nullable=False)
    subject_area = db.Column(db.String(length=30), nullable=False)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    program_apply = db.Column(db.String(length=30), nullable=False)
    start_date = db.Column(db.DateTime(), nullable=False)
    stop_date = db.Column(db.DateTime(), nullable=True)
    admitted_status = db.Column(db.String(length=20), nullable=True)
    paid = db.Column(db.Integer(), nullable=False, default=0)
    balance = db.Column(db.Integer(), nullable=False, default=999999)
    user_status = db.Column(db.String(length=20), nullable=True)
    courses = db.relationship('Course', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

class Course(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    code = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    duration = db.Column(db.String(length=8), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Course {self.name}' 
