import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException

db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)


def create_app(config=None):
    load_dotenv()
    app = Flask(__name__)
    database_url = (config or {}).get("SQLALCHEMY_DATABASE_URI") or os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("Set DATABASE_URL before starting the backend.")
    hours = int(os.environ.get("SESSION_HOURS", "8"))
    if hours < 1:
        raise RuntimeError("SESSION_HOURS must be at least 1.")
    app.config.update(
        SQLALCHEMY_DATABASE_URI=database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_LIFETIME=timedelta(hours=hours),
        RATELIMIT_STORAGE_URI=os.environ.get("RATELIMIT_STORAGE_URI", "memory://"),
        MAX_CONTENT_LENGTH=16 * 1024,
    )
    if config:
        app.config.update(config)
    db.init_app(app)
    limiter.init_app(app)

    from .auth import auth
    from .admin import admin, create_admin

    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.cli.add_command(create_admin)

    @app.errorhandler(HTTPException)
    def http_error(error):
        return jsonify(error=error.description), error.code

    @app.errorhandler(SQLAlchemyError)
    def database_error(error):
        db.session.rollback()
        app.logger.error("Database operation failed (%s)", type(error).__name__)
        return jsonify(error="Database operation failed."), 503

    @app.after_request
    def security_headers(response):
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

    return app
