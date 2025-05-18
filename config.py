import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'instance', os.getenv('DATABASE_NAME', 'database.db'))}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_LOGIN = os.getenv("ADMIN_LOGIN")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
    SITE_NAME = os.getenv("SITE_NAME")
    FLASK_RUN_PORT = os.getenv("FLASK_RUN_PORT")
    FLASK_RUN_HOST = os.getenv("FLASK_RUN_HOST")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG")