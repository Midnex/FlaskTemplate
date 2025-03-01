import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    cursor = db.cursor()

    # Check if the roles table already exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='roles';")
    roles_table_exists = cursor.fetchone()

    # Check if the user table already exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user';")
    user_table_exists = cursor.fetchone()

    print(f"Roles table exists: {roles_table_exists}")
    print(f"User table exists: {user_table_exists}")

    if not roles_table_exists or not user_table_exists:
        print("Initializing database schema...")
        with current_app.open_instance_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf8'))

        # Create default admin user from current_app.config if the user table was created
        if not user_table_exists:
            print("Creating default admin user...")
            db.execute(
                'INSERT INTO user (username, email, password, role, status) VALUES (?, ?, ?, ?, ?)',
                (current_app.config['ADMIN_LOGIN'], current_app.config['ADMIN_EMAIL'], generate_password_hash(current_app.config['ADMIN_PASSWORD']), 1, 'Active')
            )
        db.commit()
        print("Database schema and default admin user created.")

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
