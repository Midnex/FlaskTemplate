import click

from flask import current_app
from flask.cli import with_appcontext

from .models import db, Users, Roles

def init_db():
    db.create_all()

    required_roles = {'admin', 'moderator', 'donator', 'user'}
    existing_roles = {r.role_name for r in Roles.query.all()}
    missing_roles = required_roles - existing_roles

    if missing_roles:
        db.session.add_all([Roles(role_name=r) for r in missing_roles])
        db.session.commit()
        print(f"Inserted roles: {', '.join(missing_roles)}")

    admin_login = current_app.config.get('ADMIN_LOGIN')
    admin_email = current_app.config.get('ADMIN_EMAIL')
    admin_pass = current_app.config.get('ADMIN_PASSWORD')

    if not all([admin_login, admin_email, admin_pass]):
        raise RuntimeError("Missing ADMIN_LOGIN, ADMIN_EMAIL, or ADMIN_PASSWORD in environment")

    if not Users.query.filter_by(username=admin_login).first():
        admin_role = Roles.query.filter_by(role_name='admin').first()
        admin_user = Users(
            username=admin_login,
            email=admin_email,
            password=admin_pass,
            role_id=admin_role.id,
            status='Active'
        )
        db.session.add(admin_user)
        db.session.commit()
        print(f"Created admin user: {admin_login}")

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()

def init_app(app):
    db.init_app(app)
    app.cli.add_command(init_db_command)
