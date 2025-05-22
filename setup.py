import os
import secrets
import sys

from sqlalchemy import inspect
from dotenv import load_dotenv

from app import create_app
from app.models import Role, User, db
from config import Config

def create_env_file():
    print("Creating .env file for the first-time setup.")
    secret_key = secrets.token_hex(64)
    site_name = input("Enter site name: ")
    debug_mode = input("Enter debug mode (default: True): ") or "True"
    ip_bind = input("Enter IP to bind to (default: 0.0.0.0): ") or "0.0.0.0"
    port = input("Enter port to bind to (default: 5000): ") or "5000"

    with open(".env", "w", encoding="utf-8") as f:
        f.write(f"SECRET_KEY={secret_key}\n")
        f.write("ADMIN_LOGIN=admin\n")
        f.write("ADMIN_PASSWORD=admin1234\n")
        f.write("ADMIN_EMAIL=admin@example.com\n")
        f.write("DATABASE_NAME=database.db\n")
        f.write(f"SITE_NAME={site_name}\n")
        f.write(f"FLASK_DEBUG={debug_mode}\n")
        f.write(f"FLASK_RUN_HOST={ip_bind}\n")
        f.write(f"FLASK_RUN_PORT={port}\n")

    load_dotenv(override=True)

def check_database(app):
    load_dotenv(override=True)
    with app.app_context():
        database_path = Config.SQLALCHEMY_DATABASE_URI.replace("sqlite:///", "")
        print(f"Loaded database path from config: {database_path}")

        if not os.path.exists(database_path):
            print("Database file not found. Initializing database.")
            initialize_database(app)
            return

        inspector = inspect(db.engine)
        if not inspector.has_table("role") or not inspector.has_table("user"):
            print("Necessary tables missing. Initializing database.")
            initialize_database(app)
            return

        existing_admin = User.query.filter_by(username=os.getenv("ADMIN_LOGIN")).first()
        if existing_admin is None:
            print("Admin user not found. Initializing database.")
            initialize_database(app)
        else:
            print("Database and necessary tables exist. Proceeding with application start.")

def initialize_database(app):
    with app.app_context():
        os.makedirs(app.instance_path, exist_ok=True)
        db.create_all()

        admin_role = Role.query.filter_by(name="Admin").first()
        if not admin_role:
            admin_role = Role(name="Admin")
            db.session.add(admin_role)

        if not Role.query.filter_by(name="User").first():
            db.session.add(Role(name="User"))

        db.session.commit()

        if not User.query.filter_by(username=os.getenv("ADMIN_LOGIN")).first():
            print("Creating default admin account...")
            default_admin = User(
                username=os.getenv("ADMIN_LOGIN"),
                email=os.getenv("ADMIN_EMAIL"),
                password=app.config["ADMIN_PASSWORD"],
                role_id=admin_role.id,
                status="Active"
            )
            db.session.add(default_admin)
            db.session.commit()
            print(f"Default admin created: {os.getenv('ADMIN_LOGIN')} / admin1234")

        print("Database initialized.")
        sys.exit(0)

if __name__ == "__main__":
    if not os.path.exists(".env"):
        create_env_file()
        
    load_dotenv(override=True)

    app = create_app()
    app.config.from_prefixed_env()
    check_database(app)
    