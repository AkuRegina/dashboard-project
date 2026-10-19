"""Local authentication playground with its own SQLite database."""
from pathlib import Path

from flask import Blueprint, jsonify, render_template

from . import create_app, db, limiter
from .admin import commit_user
from .models import User, utcnow
from .security import email_field, json_body, new_password, password_hasher, text_field

demo = Blueprint("demo", __name__)


@demo.get("/")
def index():
    return render_template("auth_demo.html")


@demo.post("/demo/register")
@limiter.limit("10 per minute; 50 per hour")
def register():
    body = json_body()
    user = User(
        f_name=text_field(body, "f_name", 100),
        l_name=text_field(body, "l_name", 100),
        email=email_field(body),
        password_hash=password_hasher.hash(new_password(body)),
        role="worker",
        password_changed_at=utcnow(),
    )
    db.session.add(user)
    commit_user()
    return jsonify(user=user.public()), 201


def create_demo_app(config=None):
    database_path = Path(__file__).resolve().parent.parent / "instance" / "auth-demo.sqlite"
    settings = {"SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path.as_posix()}"}
    settings.update(config or {})
    if not settings["SQLALCHEMY_DATABASE_URI"].startswith("sqlite:"):
        raise RuntimeError("The demo must use a separate SQLite database.")
    database_path.parent.mkdir(parents=True, exist_ok=True)
    app = create_app(settings)
    app.register_blueprint(demo)
    with app.app_context():
        db.create_all()
    return app
