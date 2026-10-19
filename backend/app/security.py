import hashlib
from functools import wraps

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError
from flask import abort, g, request
from sqlalchemy import delete, select

from . import db
from .models import Session, utcnow

password_hasher = PasswordHasher()
_dummy_hash = password_hasher.hash("dummy-password-for-login-timing")
ROLES = {"admin", "manager", "worker"}


def token_digest(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def verify_password(encoded, password):
    try:
        return password_hasher.verify(encoded or _dummy_hash, password)
    except (VerificationError, InvalidHashError):
        return False


def json_body():
    body = request.get_json()
    if not isinstance(body, dict):
        abort(400, description="Expected a JSON object.")
    return body


def text_field(body, field, maximum, minimum=1, strip=True):
    value = body.get(field)
    if not isinstance(value, str):
        abort(400, description=f"{field} must be a string.")
    if strip:
        value = value.strip()
    if not minimum <= len(value) <= maximum:
        abort(400, description=f"{field} must contain {minimum} to {maximum} characters.")
    return value


def email_field(body):
    email = text_field(body, "email", 255).lower()
    if len(email.split("@")) != 2 or not all(email.split("@")) or any(c.isspace() for c in email):
        abort(400, description="Enter a valid email address.")
    return email


def new_password(body, field="password"):
    return text_field(body, field, 128, minimum=8, strip=False)


def revoke_sessions(user_id):
    db.session.execute(delete(Session).where(Session.user_id == user_id))


def require_auth(*roles):
    def decorate(function):
        @wraps(function)
        def protected(*args, **kwargs):
            parts = request.headers.get("Authorization", "").split()
            if len(parts) != 2 or parts[0].lower() != "bearer" or len(parts[1]) > 256:
                abort(401, description="Authentication required.")
            session = db.session.scalar(select(Session).where(
                Session.token_hash == token_digest(parts[1]),
                Session.expires_at > utcnow(),
            ))
            if not session or not session.user.is_active:
                abort(401, description="Session is invalid or expired.")
            if roles and session.user.role not in roles:
                abort(403, description="You do not have permission for this action.")
            g.user = session.user
            g.auth_session = session
            return function(*args, **kwargs)
        return protected
    return decorate
