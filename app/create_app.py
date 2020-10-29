from flask import Flask
from flask_hashing import Hashing
from flask_cors import CORS
from flask_redis import FlaskRedis
import os


def create_app():
    app = Flask(__name__)
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        REDIS_URL=os.environ["REDIS_URL"],
        VERSION="0.0.1-dev",
        UPLOAD_FOLDER=os.getenv("UPLOAD_FOLDER", "./uploads")
    )
    CORS(app,
         methods=["GET", "POST", "OPTIONS"],
         supports_credential=True)
    app.redis_client = FlaskRedis(app)
    app.hashing = Hashing(app)
    app.secret_key = os.environ["FLASK_SECRET"]
    return app
