import os

import click
from flask import current_app
from flask.cli import with_appcontext

from .models import Role, User, db

def init_db():
    if not os.path.exists(current_app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')):
        print("Initializing database schema...")
        db.create_all()

        admin_role = Role(name='Admin')
        user_role = Role(name='User')
        db.session.add(admin_role)
        db.session.add(user_role)
        db.session.commit()

        admin_user = User(
            username=current_app.config['ADMIN_LOGIN'],
            email=current_app.config['ADMIN_EMAIL'],
            password=current_app.config['ADMIN_PASSWORD'],
            role_id=admin_role.id,
            status='Active'
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Database schema and default admin user created.")

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    db.init_app(app)
    app.cli.add_command(init_db_command)
