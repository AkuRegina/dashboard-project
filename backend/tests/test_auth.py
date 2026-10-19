import os
import unittest
from datetime import timedelta
from unittest.mock import patch

from sqlalchemy import select

from app import create_app, db
from app.models import Session, User, utcnow
from app.security import password_hasher, token_digest

PASSWORD = "test-only-long-password"
PASSWORD_HASH = password_hasher.hash(PASSWORD)


class AuthenticationTests(unittest.TestCase):
    def make_app(self):
        # Never load credentials or touch the project's real database.
        with patch.dict(os.environ, {"DATABASE_URL": "sqlite://"}):
            return create_app({"TESTING": True, "RATELIMIT_ENABLED": False})

    def initialize_database(self):
        db.create_all()

    def cleanup_database(self):
        db.drop_all()

    def setUp(self):
        self.app = self.make_app()
        self.context = self.app.app_context()
        self.context.push()
        self.initialize_database()
        db.session.add_all([
            User(f_name="Test", l_name="Admin", email="admin@example.test",
                 password_hash=PASSWORD_HASH, role="admin"),
            User(f_name="Test", l_name="Worker", email="worker@example.test",
                 password_hash=PASSWORD_HASH, role="worker"),
        ])
        db.session.commit()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        self.cleanup_database()
        db.engine.dispose()
        self.context.pop()

    def login(self, email="worker@example.test"):
        response = self.client.post("/auth/login", json={"email": email, "password": PASSWORD})
        self.assertEqual(response.status_code, 200)
        token = response.json["token"]
        return {"Authorization": f"Bearer {token}"}, token

    def test_login_case_insensitive_and_token_is_hashed(self):
        headers, token = self.login("  WORKER@example.test  ")
        session = db.session.scalar(select(Session))
        self.assertEqual(session.token_hash, token_digest(token))
        self.assertNotEqual(session.token_hash, token)
        response = self.client.get("/auth/me", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["user"]["role"], "worker")
        self.assertNotIn("password_hash", response.json["user"])
        self.assertEqual(response.headers["Cache-Control"], "no-store")

    def test_invalid_credentials_have_generic_error(self):
        for email in ("worker@example.test", "missing@example.test"):
            response = self.client.post("/auth/login", json={"email": email, "password": "wrong"})
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json["error"], "Invalid email or password.")

    def test_placeholder_password_cannot_login(self):
        user = db.session.scalar(select(User).where(User.role == "worker"))
        user.password_hash = "placeholder_hash"
        db.session.commit()
        response = self.client.post("/auth/login", json={"email": user.email, "password": PASSWORD})
        self.assertEqual(response.status_code, 401)

    def test_protected_routes_reject_missing_and_invalid_tokens(self):
        for headers in ({}, {"Authorization": "Bearer unknown"}, {"Authorization": "Basic abc"}):
            self.assertEqual(self.client.get("/auth/me", headers=headers).status_code, 401)

    def test_expired_session_is_rejected(self):
        headers, token = self.login()
        session = db.session.get(Session, token_digest(token))
        session.expires_at = utcnow() - timedelta(seconds=1)
        db.session.commit()
        self.assertEqual(self.client.get("/auth/me", headers=headers).status_code, 401)

    def test_logout_revokes_session(self):
        headers, token = self.login()
        self.assertEqual(self.client.post("/auth/logout", headers=headers).status_code, 204)
        self.assertEqual(self.client.get("/auth/me", headers=headers).status_code, 401)
        self.assertIsNone(db.session.get(Session, token_digest(token)))

    def test_password_change_revokes_all_sessions(self):
        headers, _ = self.login()
        other_headers, _ = self.login()
        response = self.client.post("/auth/change-password", headers=headers,
            json={"current_password": PASSWORD, "new_password": "newpass8"})
        self.assertEqual(response.status_code, 200)
        for old_headers in (headers, other_headers):
            self.assertEqual(self.client.get("/auth/me", headers=old_headers).status_code, 401)
        for password, expected in ((PASSWORD, 401), ("newpass8", 200)):
            response = self.client.post("/auth/login", json={"email": "worker@example.test", "password": password})
            self.assertEqual(response.status_code, expected)

    def test_wrong_current_password_preserves_session(self):
        headers, _ = self.login()
        response = self.client.post("/auth/change-password", headers=headers,
            json={"current_password": "wrong", "new_password": "replacement-long-password"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.client.get("/auth/me", headers=headers).status_code, 200)

    def test_worker_cannot_manage_accounts(self):
        headers, _ = self.login()
        self.assertEqual(self.client.post("/admin/users", headers=headers, json={}).status_code, 403)
        self.assertEqual(self.client.patch("/admin/users/1", headers=headers, json={"role": "admin"}).status_code, 403)

    def test_admin_creates_user_and_duplicate_is_rejected(self):
        headers, _ = self.login("admin@example.test")
        body = {"f_name": "New", "l_name": "User", "email": "NEW@example.test", "password": "newpass8"}
        response = self.client.post("/admin/users", headers=headers, json=body)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["user"]["role"], "worker")
        user = db.session.get(User, response.json["user"]["user_id"])
        self.assertTrue(password_hasher.verify(user.password_hash, "newpass8"))
        self.assertEqual(self.client.post("/admin/users", headers=headers, json=body).status_code, 409)

    def test_deactivation_revokes_session_and_blocks_login(self):
        worker_headers, _ = self.login()
        admin_headers, _ = self.login("admin@example.test")
        worker = db.session.scalar(select(User).where(User.role == "worker"))
        response = self.client.patch(f"/admin/users/{worker.user_id}", headers=admin_headers,
                                    json={"is_active": False})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get("/auth/me", headers=worker_headers).status_code, 401)
        response = self.client.post("/auth/login", json={"email": worker.email, "password": PASSWORD})
        self.assertEqual(response.status_code, 401)

    def test_admin_cannot_deactivate_or_demote_self(self):
        headers, _ = self.login("admin@example.test")
        admin = db.session.scalar(select(User).where(User.role == "admin"))
        for body in ({"is_active": False}, {"role": "worker"}):
            response = self.client.patch(f"/admin/users/{admin.user_id}", headers=headers, json=body)
            self.assertEqual(response.status_code, 400)

    def test_input_validation(self):
        headers, _ = self.login("admin@example.test")
        for body in ([], {"email": "invalid", "password": PASSWORD}):
            self.assertEqual(self.client.post("/auth/login", json=body).status_code, 400)
        body = {"f_name": "New", "l_name": "User", "email": "new@example.test", "password": "1234567"}
        self.assertEqual(self.client.post("/admin/users", headers=headers, json=body).status_code, 400)

    def test_administrator_cli_password_length(self):
        runner = self.app.test_cli_runner()
        args = ["create-admin", "--email", "cli@example.test", "--first-name", "CLI",
                "--last-name", "Admin", "--password"]
        for password in ("1234567", "x" * 129):
            result = runner.invoke(args=args + [password])
            self.assertNotEqual(result.exit_code, 0)
            self.assertIn("8 to 128", result.output)
        result = runner.invoke(args=args + ["newpass8"])
        self.assertEqual(result.exit_code, 0, result.output)
        response = self.client.post("/auth/login", json={
            "email": "cli@example.test", "password": "newpass8"})
        self.assertEqual(response.status_code, 200)

    def test_login_rate_limit(self):
        with patch.dict(os.environ, {"DATABASE_URL": "sqlite://"}):
            app = create_app({"TESTING": True, "RATELIMIT_ENABLED": True})
        client = app.test_client()
        for _ in range(5):
            response = client.post("/auth/login", json={"email": "bad-email", "password": "wrong"})
            self.assertEqual(response.status_code, 400)
        self.assertEqual(client.post("/auth/login", json={}).status_code, 429)


if __name__ == "__main__":
    unittest.main()
