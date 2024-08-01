import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
    DATABASE = os.path.join(os.getcwd(), 'instance', os.getenv('DATABASE_NAME', 'database.db'))
    ADMIN_LOGIN = os.getenv('ADMIN_LOGIN')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
    SITE_NAME = os.getenv('SITE_NAME')
    FLASK_RUN_PORT = int(os.getenv('FLASK_RUN_PORT', 5000))
    FLASK_RUN_HOST = os.getenv('FLASK_RUN_HOST', '0.0.0.0')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1']
