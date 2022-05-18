"""Script that creates that Flask app"""
import os
from urllib.parse import urlparse

from flask import Flask
from flask_hashing import Hashing
from flask_cors import CORS
from flask_redis import FlaskRedis
import redis


def create_app() -> Flask:
    """Creates the Flask app"""
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET", "INSECURE-SECRET")
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        VERSION="0.0.2",
        UPLOAD_FOLDER=os.getenv("UPLOAD_FOLDER", "/tmp"),  # nosec
    )
    CORS(app, methods=["GET", "POST", "OPTIONS"], supports_credential=True)
    if os.environ.get("REDIS_TLS_URL"):
        url = urlparse(os.environ["REDIS_TLS_URL"])
        redis_cls = redis.Redis(
            host=url.hostname,
            port=url.port,
            username=url.username,
            password=url.password,
            ssl=True,
            ssl_cert_reqs=None,
        )
    elif os.environ.get("REDIS_URL"):
        url = urlparse(os.environ["REDIS_URL"])
        redis_cls = redis.Redis(
            host=url.hostname,
            port=url.port,
            username=url.username,
            password=url.password,
        )
    if redis_cls:
        print("using redis")
        app.redis_client = FlaskRedis.from_custom_provider(provider=redis_cls, app=app)
        app.using_redis = True
    else:
        app.using_redis = False
    app.hashing = Hashing(app)
    return app
