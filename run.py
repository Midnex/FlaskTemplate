import os
import sys

from dotenv import load_dotenv

from app import create_app

if not os.path.exists(".env"):
    print("The .env file does not exist. Please run setup.py first.")
    sys.exit(1)

load_dotenv()

app = create_app()

if __name__ == "__main__":
    host = os.getenv("FLASK_RUN_HOST")
    port = os.getenv("FLASK_RUN_PORT")
    debug = os.getenv("FLASK_DEBUG")
    app.run(host=host, port=port, debug=debug)
