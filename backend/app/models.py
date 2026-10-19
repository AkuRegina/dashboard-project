from datetime import datetime, timezone

from . import db


def utcnow():
    return datetime.now(timezone.utc)


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(100), nullable=False)
    l_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="worker")
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow)
    password_changed_at = db.Column(db.DateTime(timezone=True))

    def public(self):
        return {
            "user_id": self.user_id,
            "f_name": self.f_name,
            "l_name": self.l_name,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
        }


class Session(db.Model):
    __tablename__ = "auth_sessions"

    token_hash = db.Column(db.String(64), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow)
    expires_at = db.Column(db.DateTime(timezone=True), nullable=False)
    user = db.relationship(User)
