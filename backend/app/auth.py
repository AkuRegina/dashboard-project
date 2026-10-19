import secrets

from flask import Blueprint, abort, current_app, g, jsonify
from sqlalchemy import func, select

from . import db, limiter
from .models import Session, User, utcnow
from .security import (
    email_field, json_body, new_password, password_hasher,
    require_auth, revoke_sessions, text_field, token_digest, verify_password,
)

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.post("/login")
@limiter.limit("5 per minute; 30 per hour")
def login():
    body = json_body()
    email = email_field(body)
    password = text_field(body, "password", 128, strip=False)
    user = db.session.scalar(select(User).where(func.lower(User.email) == email))
    valid = verify_password(user.password_hash if user else None, password)
    if not valid or not user or not user.is_active:
        abort(401, description="Invalid email or password.")
    if password_hasher.check_needs_rehash(user.password_hash):
        user.password_hash = password_hasher.hash(password)
    token = secrets.token_urlsafe(32)
    expires_at = utcnow() + current_app.config["SESSION_LIFETIME"]
    db.session.add(Session(token_hash=token_digest(token), user_id=user.user_id, expires_at=expires_at))
    db.session.commit()
    return jsonify(token=token, token_type="Bearer", expires_at=expires_at.isoformat(), user=user.public())


@auth.get("/me")
@require_auth()
def me():
    return jsonify(user=g.user.public())


@auth.post("/logout")
@require_auth()
def logout():
    db.session.delete(g.auth_session)
    db.session.commit()
    return "", 204


@auth.post("/change-password")
@limiter.limit("5 per minute")
@require_auth()
def change_password():
    body = json_body()
    current_password = text_field(body, "current_password", 128, strip=False)
    password = new_password(body, "new_password")
    if not verify_password(g.user.password_hash, current_password):
        abort(400, description="Current password is incorrect.")
    g.user.password_hash = password_hasher.hash(password)
    g.user.password_changed_at = utcnow()
    revoke_sessions(g.user.user_id)
    db.session.commit()
    return jsonify(message="Password changed. Log in again.")
