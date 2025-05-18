import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    from app import admin, auth, main
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(admin.bp)

    app.jinja_env.filters['time_ago'] = time_ago_filter

    return app

def time_ago_filter(date_str):
    if not date_str:
        return "Never"
    if isinstance(date_str, str):
        date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    else:
        date = date_str

    now = datetime.now(timezone.utc)
    if date.tzinfo is None:
        date = date.replace(tzinfo=timezone.utc)

    diff = now - date
    seconds = diff.total_seconds()

    if seconds < 3600:
        minutes = round(seconds / 60)
        return f"< {minutes} minute{'s' if minutes != 1 else ''}"
    elif seconds < 86400:
        hours = round(seconds / 3600)
        return f"< {hours} hour{'s' if hours != 1 else ''}"
    elif seconds < 2592000:
        days = round(seconds / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif seconds < 31536000:
        months = round(seconds / 2592000)
        return f"{months} month{'s' if months != 1 else ''} ago"
    else:
        years = round(seconds / 31536000)
        return f"{years} year{'s' if years != 1 else ''} ago"