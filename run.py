import os
import sys

from dotenv import load_dotenv

from app import create_app

<<<<<<< HEAD
if not os.path.exists(".env"):
    print("The .env file does not exist. Please run setup.py first.")
    sys.exit(1)
=======
    admin_username = input("Enter admin username (default: admin): ") or "admin"
    admin_password = getpass("Enter admin password (default: password): ") or "password"
    admin_email = input("Enter admin email: ") or "admin@site.com"
    database_name = input("Enter database name (default: database.db): ") or "database.db"
    site_name = input("Enter site name: ")
    debug_mode = input("Enter debug mode (default: True): ") or True
    ip_bind = input("Enter IP to bind to (default: 0.0.0.0): ") or "0.0.0.0"
    port = input("Enter port to bind to (default: 5000): ") or "5000"
>>>>>>> origin/master

load_dotenv()

app = create_app()

if __name__ == "__main__":
    host = os.getenv("FLASK_RUN_HOST")
    port = os.getenv("FLASK_RUN_PORT")
    debug = os.getenv("FLASK_DEBUG")
    app.run(host=host, port=port, debug=debug)
