import unittest
from datetime import timedelta

from sqlalchemy import text

from app import create_app, db
from app.models import Session, User, utcnow
from app.security import token_digest


class AnalyticsTests(unittest.TestCase):
    def setUp(self):
        app = create_app({"SQLALCHEMY_DATABASE_URI": "sqlite://", "TESTING": True,
                          "RATELIMIT_ENABLED": False})
        with app.app_context():
            db.create_all()
            for user_id, role in enumerate(("worker", "manager", "admin"), start=1):
                user = User(user_id=user_id, role=role, f_name="Test", l_name=role,
                            email=f"{role}@example.test", password_hash="unused")
                db.session.add(Session(user=user, token_hash=token_digest(role),
                                       expires_at=utcnow() + timedelta(hours=1)))
            db.session.execute(text("""
                CREATE VIEW deviation_details AS
                SELECT 'Safety' AS concern_type, 'High' AS severity, 'Open' AS status,
                       '2026-10-15 08:00' AS created_at, 1 AS assigned_to, CURRENT_DATE AS deadline
                UNION ALL SELECT 'Safety', 'Low', 'Closed', '2026-10-15 20:00', 1, date('now', '-1 day')
                UNION ALL SELECT 'Quality Issue', 'Medium', 'In Progress', '2026-10-12', NULL, date('now', '-1 day')
                UNION ALL SELECT 'Quality', 'High', 'Open', NULL, 2, NULL
            """))
            db.session.commit()
        self.client = app.test_client()

    def test_summary(self):
        url = "/analytics/summary"
        self.assertEqual(self.client.get(url).status_code, 401)
        all_records = dict(total_deviations=4, open=2, in_progress=1, closed=1, overdue=1)
        worker = dict(total_deviations=2, open=1, in_progress=0, closed=1, overdue=0)
        for role, expected in [("worker", worker), ("manager", all_records), ("admin", all_records)]:
            with self.subTest(role=role):
                response = self.client.get(url, headers={"Authorization": f"Bearer {role}"})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json, expected)

    def test_breakdowns_and_visibility(self):
        for route, field, worker, all_records in [
            ("by-type", "type",
             [("Safety", 2)], [("Quality", 2), ("Safety", 2)]),
            ("by-severity", "severity", [("High", 1), ("Low", 1)],
             [("High", 2), ("Low", 1), ("Medium", 1)]),
            ("by-status", "status", [("Open", 1), ("In Progress", 0), ("Closed", 1)],
             [("Open", 2), ("In Progress", 1), ("Closed", 1)]),
            ("over-time", "date", [("2026-10-15", 2)], [("2026-10-12", 1), ("2026-10-15", 2)]),
        ]:
            url = f"/analytics/{route}"
            self.assertEqual(self.client.get(url).status_code, 401)
            for role, expected in [("worker", worker), ("manager", all_records), ("admin", all_records)]:
                with self.subTest(route=route, role=role):
                    response = self.client.get(url, headers={"Authorization": f"Bearer {role}"})
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.json, [{field: key, "count": n} for key, n in expected])
