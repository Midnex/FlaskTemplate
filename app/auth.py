import functools
import re
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif password != confirm_password:
            error = 'Passwords do not match.'
        elif not validate_password(password):
            error = 'Password does not meet the requirements.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f'User {username} is already registered.'
        elif db.execute(
            'SELECT id FROM user WHERE email = ?', (email,)
        ).fetchone() is not None:
            error = f'Email {email} is already registered.'

        if error is None:
            db.execute(
                'INSERT INTO user (username, email, password) VALUES (?, ?, ?)',
                (username, email, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        elif user['status'] == 'Banned':
            error = 'This account has been banned.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('main.main_page'))

        flash(error)

    return render_template('auth/login.html')

@bp.route('/account_settings', methods=('GET', 'POST'))
def account_settings():
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        db = get_db()
        error = None

        if password and password != confirm_password:
            error = 'Passwords do not match.'
        elif password and not validate_password(password):
            error = 'Password does not meet the requirements.'

        if error is None:
            if password:
                db.execute(
                    'UPDATE user SET password = ? WHERE id = ?',
                    (generate_password_hash(password), g.user['id'])
                )
            db.commit()
            return redirect(url_for('main.index'))

        flash(error)

    return render_template('auth/account_settings.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def validate_password(password):
    if (len(password) < 16 or
        not re.search(r"\d", password) or
        not re.search(r"[A-Z]", password) or
        not re.search(r"[!@#$%^&*(),.?\":{}|<>-]", password)):
        return False
    return True

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or g.user['role'] != 1:  # Assuming role ID 1 is admin
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
