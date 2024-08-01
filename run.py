import os
from dotenv import load_dotenv
from getpass import getpass

def create_env_file():
    print("Creating .env file for the first-time setup.")

    admin_username = input("Enter admin username (default: admin): ") or "admin"
    admin_password = getpass("Enter admin password (default: password): ") or "password"
    admin_email = input("Enter admin email: ") or "admin@site.com"
    database_name = input("Enter database name (default: database.db): ") or "database.db"
    site_name = input("Enter site name: ")
    debug_mode = input("Enter debug mode (default: True): ") or True
    ip_bind = input("Enter IP to bind to (default: 0.0.0.0): ") or "0.0.0.0"
    port = input("Enter port to bind to (default: 5000): ") or "5000"

    with open(".env", "w") as f:
        f.write(f"ADMIN_LOGIN={admin_username}\n")
        f.write(f"ADMIN_PASSWORD={admin_password}\n")
        f.write(f"ADMIN_EMAIL={admin_email}\n")
        f.write(f"DATABASE_NAME={database_name}\n")
        f.write(f"SITE_NAME={site_name}\n")
        f.write(f"FLASK_DEBUG={debug_mode}\n")
        f.write(f"FLASK_RUN_HOST={ip_bind}\n")
        f.write(f"FLASK_RUN_PORT={port}\n")

def check_database():
    load_dotenv()
    from config import Config
    database_path = Config.DATABASE
    print(f"Loaded database path from config: {database_path}")

    if not os.path.exists(database_path):
        print(f"Database file not found at {database_path}. Initializing database.")
        initialize_database()
    else:
        from app import create_app
        app = create_app()
        with app.app_context():
            from app.db import get_db
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='roles';")
            roles_table_exists = cursor.fetchone()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user';")
            user_table_exists = cursor.fetchone()
            print(f"Roles table exists: {roles_table_exists}")
            print(f"User table exists: {user_table_exists}")
            if not roles_table_exists or not user_table_exists:
                print("Necessary tables not found. Initializing database.")
                initialize_database()
            else:
                print("Database and necessary tables exist. Proceeding with application start.")

def initialize_database():
    from app import create_app
    app = create_app()
    with app.app_context():
        from app.db import init_db
        init_db()
    print("Database initialized. Please restart the application.")
    exit(0)

if __name__ == "__main__":
    if not os.path.exists(".env"):
        create_env_file()

    check_database()

    from app import create_app
    app = create_app()
    app.run(host=app.config['FLASK_RUN_HOST'], port=app.config['FLASK_RUN_PORT'], debug=app.config['FLASK_DEBUG'])
