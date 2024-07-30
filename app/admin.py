from flask import Blueprint, render_template, request, jsonify, g, redirect, url_for
from app.auth import login_required, admin_required
from app.db import get_db
from werkzeug.security import generate_password_hash
import re

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/manage_users')
@login_required
@admin_required
def manage_users():
    db = get_db()
    users = db.execute('''
        SELECT user.id, user.username, user.email, roles.role_name as role, user.status, user.last_logged_in
        FROM user
        JOIN roles ON user.role = roles.id
    ''').fetchall()
    roles = db.execute('SELECT id, role_name FROM roles').fetchall()
    return render_template('admin/manage_users.html', users=users, roles=roles)

@bp.route('/manage_site')
@login_required
@admin_required
def manage_site():
    return render_template('admin/manage_site.html')

@bp.route('/manage_database')
@login_required
@admin_required
def manage_database():
    return render_template('admin/manage_database.html')

@bp.route('/update_user', methods=['POST'])
@login_required
@admin_required
def update_user():
    user_id = request.form['user_id']
    email = request.form['email']
    role_id = request.form['role_id']
    status = request.form['status']
    password = request.form.get('password')

    db = get_db()
    error = None

    if not email:
        error = 'Email is required.'
    elif not validate_email(email):
        error = 'Invalid email address.'
    elif password and not validate_password(password):
        error = 'Password does not meet the requirements.'

    if error is None:
        db.execute(
            'UPDATE user SET email = ?, role = ?, status = ? WHERE id = ?',
            (email, role_id, status, user_id)
        )
        if password:
            db.execute(
                'UPDATE user SET password = ? WHERE id = ?',
                (generate_password_hash(password), user_id)
            )
        db.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': error})

@bp.route('/ban_user', methods=['POST'])
@login_required
@admin_required
def ban_user():
    user_id = request.form['user_id']
    db = get_db()
    db.execute(
        'UPDATE user SET status = ? WHERE id = ?',
        ('Banned', user_id)
    )
    db.commit()
    return jsonify({'status': 'success'})

@bp.route('/unban_user', methods=['POST'])
@login_required
@admin_required
def unban_user():
    user_id = request.form['user_id']
    db = get_db()
    db.execute(
        'UPDATE user SET status = ? WHERE id = ?',
        ('Active', user_id)
    )
    db.commit()
    return jsonify({'status': 'success'})

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def validate_password(password):
    if (len(password) < 16 or
        not re.search(r"\d", password) or
        not re.search(r"[A-Z]", password) or
        not re.search(r"[!@#$%^&*(),.?\":{}|<>-]", password)):
        return False
    return True
