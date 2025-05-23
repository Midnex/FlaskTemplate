import re

from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash

from app import db


class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(64), unique=True, nullable=False)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False, default=4)
    status = db.Column(db.String(64), default='not_verified', nullable=False)
    last_logged_in = db.Column(db.DateTime, default=None)

    role = db.relationship('Roles', backref=db.backref('users', lazy=True))

    @validates('email')
    def validate_email(self, key, email):
        if not email or not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            raise ValueError('Invalid email address')
        return email

    @validates('password')
    def validate_password(self, key, password):
        if len(password) < 8 or not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
            raise ValueError('Password must be at least 16 characters long and contain both letters and numbers')
        return generate_password_hash(password)
