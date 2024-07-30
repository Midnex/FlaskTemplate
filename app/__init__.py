import os
from flask import Flask
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def create_app():
    template_dir = os.path.abspath('templates')
    static_dir = os.path.abspath('static')
    app = Flask(__name__, instance_relative_config=True, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object('config.Config')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth, main, admin
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(admin.bp)

    @app.template_filter('time_ago')
    def time_ago_filter(date_str):
        date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        now = datetime.utcnow()
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

    return app
