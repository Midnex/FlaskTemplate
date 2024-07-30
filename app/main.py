from flask import Blueprint, render_template, g, request, flash, redirect, url_for, send_from_directory, current_app
from werkzeug.security import generate_password_hash
from app.auth import login_required
from app.db import get_db
import re

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/profile', methods=('GET', 'POST'))
@login_required
def profile():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        db = get_db()
        error = None

        if not email:
            error = 'Email is required.'
        elif not validate_email(email):
            error = 'Invalid email address.'
        elif db.execute(
            'SELECT id FROM user WHERE email = ? AND id != ?', (email, g.user['id'])
        ).fetchone() is not None:
            error = f'Email {email} is already registered.'

        if not error and password:
            if password != confirm_password:
                error = 'Passwords do not match.'
            elif not validate_password(password):
                error = 'Password does not meet the requirements.'
            else:
                db.execute(
                    'UPDATE user SET password = ? WHERE id = ?',
                    (generate_password_hash(password), g.user['id'])
                )

        if not error:
            db.execute(
                'UPDATE user SET email = ? WHERE id = ?',
                (email, g.user['id'])
            )
            db.commit()
            flash('Profile updated successfully.')
        else:
            flash(error)

    return render_template('profile.html', email=g.user['email'])

@bp.route('/main')
@login_required
def main_page():
    return render_template('main.html', username=g.user['username'])

def validate_password(password):
    if (len(password) < 16 or
        not re.search(r"\d", password) or
        not re.search(r"[A-Z]", password) or
        not re.search(r"[!@#$%^&*(),.?\":{}|<>-]", password)):
        return False
    return True

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

@bp.route('/static/<path:filename>')
def custom_static(filename):
    return send_from_directory(current_app.config['STATIC_FOLDER'], filename)
