import os
import secrets

from dotenv import load_dotenv

from app import create_app
from app.db import init_db

def create_env_file():
    print("Creating .env file for the first-time setup.")
    secret_key = secrets.token_hex(64)
    site_name = input("Enter site name: ") or "Test Site"
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

if __name__ == "__main__":
    if not os.path.exists(".env"):
        create_env_file()

    load_dotenv(override=True)

    from config import Config
    
    app = create_app()
    app.config.from_object(Config)

    print(f"Default admin: {app.config['ADMIN_LOGIN']} / {app.config['ADMIN_PASSWORD']}")


    with app.app_context():
        init_db()
