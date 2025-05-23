import functools

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import db, Users, Roles

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        error = None

        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif password != confirm_password:
            error = 'Passwords do not match.'
        elif len(password) < 8:
            error = 'Password must be at least 8 characters long.'
        elif Users.query.filter_by(username=username).first():
            error = f'User {username} is already registered.'
        elif Users.query.filter_by(email=email).first():
            error = f'Email {email} is already registered.'

        if error is None:
            user_role = Roles.query.filter_by(role_name='user').first()
            if not user_role:
                error = "Default user role not found. Please contact an administrator."
                flash(error)
            else:
                user = Users(username=username, email=email, password=password, role_id=user_role.id)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None
        user = Users.query.filter_by(username=username).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'
        elif user.status == 'Banned':
            error = 'This account has been banned.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.main_page'))

        flash(error)

    return render_template('auth/login.html')

@bp.route('/account_settings', methods=('GET', 'POST'))
def account_settings():
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        error = None

        if password and password != confirm_password:
            error = 'Passwords do not match.'
        elif password and len(password) < 16:
            error = 'Password must be at least 16 characters long.'

        if error is None:
            user = g.user
            if password:
                user.password = generate_password_hash(password)
            db.session.commit()
            return redirect(url_for('main.index'))

        flash(error)

    return render_template('auth/account_settings.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = Users.query.get(user_id)

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

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or g.user.role_id != 1:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
