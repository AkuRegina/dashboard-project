import click
from flask import Blueprint, abort, g, jsonify
from flask.cli import with_appcontext
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from . import db, limiter
from .models import User, utcnow
from .security import (
    ROLES, email_field, json_body, new_password, password_hasher,
    require_auth, revoke_sessions, text_field,
)

admin = Blueprint("admin", __name__, url_prefix="/admin")


def commit_user():
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(409, description="User could not be saved. The email may already be in use.")


@admin.post("/users")
@limiter.limit("20 per minute")
@require_auth("admin")
def create_user():
    body = json_body()
    role = body.get("role", "worker")
    if not isinstance(role, str) or role not in ROLES:
        abort(400, description="role must be admin, manager, or worker.")
    user = User(
        f_name=text_field(body, "f_name", 100),
        l_name=text_field(body, "l_name", 100),
        email=email_field(body),
        password_hash=password_hasher.hash(new_password(body)),
        role=role,
        password_changed_at=utcnow(),
    )
    db.session.add(user)
    commit_user()
    return jsonify(user=user.public()), 201


@admin.patch("/users/<int:user_id>")
@limiter.limit("20 per minute")
@require_auth("admin")
def update_user(user_id):
    body = json_body()
    allowed = {"f_name", "l_name", "email", "role", "is_active"}
    if not body or set(body) - allowed:
        abort(400, description="Provide f_name, l_name, email, role, or is_active.")
    user = db.session.get(User, user_id)
    if not user:
        abort(404, description="User not found.")
    for field in ("f_name", "l_name"):
        if field in body:
            setattr(user, field, text_field(body, field, 100))
    if "email" in body:
        user.email = email_field(body)
    if "role" in body:
        if not isinstance(body["role"], str) or body["role"] not in ROLES:
            abort(400, description="role must be admin, manager, or worker.")
        if user_id == g.user.user_id and body["role"] != "admin":
            abort(400, description="You cannot remove your own administrator role.")
        user.role = body["role"]
    if "is_active" in body:
        if not isinstance(body["is_active"], bool):
            abort(400, description="is_active must be a boolean.")
        if user_id == g.user.user_id and not body["is_active"]:
            abort(400, description="You cannot deactivate your own account.")
        user.is_active = body["is_active"]
    revoke_sessions(user_id)
    commit_user()
    return jsonify(user=user.public())


@click.command("create-admin")
@click.option("--email", prompt=True)
@click.option("--first-name", prompt=True)
@click.option("--last-name", prompt=True)
@click.password_option()
@with_appcontext
def create_admin(email, first_name, last_name, password):
    """Create the initial administrator; passwords are entered privately."""
    email = email.strip().lower()
    first_name, last_name = first_name.strip(), last_name.strip()
    if (not 1 <= len(email) <= 255 or len(email.split("@")) != 2
            or not all(email.split("@")) or any(c.isspace() for c in email)):
        raise click.ClickException("Enter a valid email address.")
    if not 1 <= len(first_name) <= 100 or not 1 <= len(last_name) <= 100:
        raise click.ClickException("Names must contain 1 to 100 characters.")
    if not 8 <= len(password) <= 128:
        raise click.ClickException("Password must contain 8 to 128 characters.")
    if db.session.scalar(select(User).where(func.lower(User.email) == email)):
        raise click.ClickException("An account with this email already exists.")
    db.session.add(User(
        email=email, f_name=first_name, l_name=last_name,
        password_hash=password_hasher.hash(password), role="admin",
        password_changed_at=utcnow(),
    ))
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise click.ClickException("An account with this email already exists.")
    click.echo("Administrator created.")
