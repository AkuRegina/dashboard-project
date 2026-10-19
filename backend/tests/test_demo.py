import unittest

from app import create_app, db
from app.demo import create_demo_app


class DemoTests(unittest.TestCase):
    def setUp(self):
        self.app = create_demo_app({
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "TESTING": True,
            "RATELIMIT_ENABLED": False,
        })
        self.client = self.app.test_client()
        self.body = {"f_name": "Demo", "l_name": "User", "email": "demo@example.test",
                     "password": "demo1234"}

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def test_frontpage_and_assets(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Create account", response.data)
        for path in ("/static/auth_demo.css", "/static/auth_demo.js"):
            with self.client.get(path) as asset:
                self.assertEqual(asset.status_code, 200)

    def test_registration_login_and_logout(self):
        response = self.client.post("/demo/register", json={**self.body, "role": "admin"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["user"]["role"], "worker")
        response = self.client.post("/auth/login", json={
            "email": self.body["email"], "password": self.body["password"]})
        self.assertEqual(response.status_code, 200)
        headers = {"Authorization": "Bearer " + response.json["token"]}
        self.assertEqual(self.client.get("/auth/me", headers=headers).status_code, 200)
        self.assertEqual(self.client.post("/auth/logout", headers=headers).status_code, 204)
        self.assertEqual(self.client.get("/auth/me", headers=headers).status_code, 401)

    def test_duplicate_and_invalid_registration(self):
        self.assertEqual(self.client.post("/demo/register", json=self.body).status_code, 201)
        duplicate = {**self.body, "email": "DEMO@example.test"}
        self.assertEqual(self.client.post("/demo/register", json=duplicate).status_code, 409)
        self.assertEqual(self.client.post("/demo/register", json={**self.body, "password": "1234567"}).status_code, 400)

    def test_registration_available_only_in_demo(self):
        app = create_app({"SQLALCHEMY_DATABASE_URI": "sqlite://", "TESTING": True,
                          "RATELIMIT_ENABLED": False})
        self.assertEqual(app.test_client().post("/demo/register", json=self.body).status_code, 404)


if __name__ == "__main__":
    unittest.main()
