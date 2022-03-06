"""Script that creates that Flask app"""
import os
from flask import Flask
from flask_hashing import Hashing
from flask_cors import CORS
from flask_redis import FlaskRedis


def create_app() -> Flask:
    """Creates the Flask app"""
    app = Flask(__name__)
    app.secret_key = os.environ["FLASK_SECRET"]
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        VERSION="0.0.2",
        UPLOAD_FOLDER=os.getenv("UPLOAD_FOLDER", "/tmp"),  # nosec
    )
    CORS(app, methods=["GET", "POST", "OPTIONS"], supports_credential=True)
    if os.getenv("REDIS_URL"):
        app.config.update(REDIS_URL=os.environ["REDIS_URL"])
        app.redis_client = FlaskRedis(app)
    app.hashing = Hashing(app)
    return app
