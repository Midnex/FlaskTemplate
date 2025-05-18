import re

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash
from app import db
from datetime import datetime


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False, default=3)
    status = db.Column(db.String(64), default='not_verified', nullable=False)
    last_logged_in = db.Column(db.DateTime, default=None)

    role = db.relationship('Role', backref=db.backref('users', lazy=True))

    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            raise ValueError('Invalid email address')
        return email

    @validates('password')
    def validate_password(self, key, password):
        if len(password) < 8 or not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
            raise ValueError('Password must be at least 8 characters long and contain both letters and numbers')
        return generate_password_hash(password)
