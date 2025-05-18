import re
import os

from app.decorators import login_required
from app.models import db, User
from flask import Blueprint, g, redirect, render_template, request, url_for, current_app
from werkzeug.security import generate_password_hash

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    template_path = current_app.template_folder

    if os.path.exists(template_path):
        print("Templates directory contents:", os.listdir(template_path))
    else:
        print("Template folder not found:", template_path)
    return render_template('index.html')

@bp.route('/profile', methods=('GET', 'POST'))
@login_required
def profile():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        error = None

        if not email:
            error = 'Email is required.'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            error = 'Invalid email address.'
        elif password and password != confirm_password:
            error = 'Passwords do not match.'
        elif password and len(password) < 8:
            error = 'Password must be at least 8 characters long.'

        if error is None:
            user = g.user
            user.email = email
            if password:
                user.password = generate_password_hash(password)
            db.session.commit()
            return redirect(url_for('main.profile'))
        else:
            return render_template('profile.html', email=email, error=error)

    return render_template('profile.html', email=g.user.email)

@bp.route('/main')
@login_required
def main_page():
    return render_template('main.html', username=g.user.username)

@bp.route('/static/<path:filename>')
def custom_static(filename):
    return send_from_directory(current_app.config['STATIC_FOLDER'], filename)
