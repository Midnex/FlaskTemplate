import re

from flask import Blueprint, jsonify, render_template, request
from werkzeug.security import generate_password_hash

from app.auth import admin_required, login_required
from app.models import db, Users, Roles

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/manage_users')
@login_required
@admin_required
def manage_users():
    users = Users.query.join(Roles, Users.role_id == Roles.id).add_columns(
        Users.id, Users.username, Users.email, Roles.role_name.label('role'), Users.status, Users.last_logged_in
    ).all()
    roles = Roles.query.all()
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

    users = Users.query.get(user_id)
    error = None

    if not email:
        error = 'Email is required.'
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        error = 'Invalid email address.'
    elif password and len(password) < 8:
        error = 'Password must be at least 8 characters long.'

    if error is None:
        users.email = email
        users.role_id = role_id
        users.status = status
        if password:
            users.password = generate_password_hash(password)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': error})

@bp.route('/ban_user', methods=['POST'])
@login_required
@admin_required
def ban_user():
    users_id = request.form['user_id']
    users = Users.query.get(users_id)
    users.status = 'Banned'
    db.session.commit()
    return jsonify({'status': 'success'})

@bp.route('/unban_user', methods=['POST'])
@login_required
@admin_required
def unban_user():
    users_id = request.form['user_id']
    users = Users.query.get(users_id)
    users.status = 'Active'
    db.session.commit()
    return jsonify({'status': 'success'})
