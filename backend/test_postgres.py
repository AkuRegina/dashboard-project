"""Run authentication integration tests in a disposable PostgreSQL Docker container."""
import os
from pathlib import Path
import secrets
import subprocess
import sys
import time
import unittest
import uuid

import psycopg


def docker(*args, **kwargs):
    return subprocess.run(["docker", *args], check=True, capture_output=True, text=True, **kwargs).stdout.strip()


def main():
    name = "dashboard-auth-test-" + uuid.uuid4().hex[:12]
    password = secrets.token_hex(24)
    environment = dict(os.environ, POSTGRES_PASSWORD=password)
    started = False
    try:
        print("Starting isolated PostgreSQL 17 container...", flush=True)
        docker("run", "--detach", "--rm", "--name", name,
               "--publish", "127.0.0.1::5432", "--env", "POSTGRES_PASSWORD",
               "--env", "POSTGRES_DB=dashboard_auth_test", "postgres:17-alpine", env=environment)
        started = True
        port = int(docker("port", name, "5432/tcp").rsplit(":", 1)[1])
        ready = False
        for _ in range(60):
            try:
                with psycopg.connect(host="127.0.0.1", port=port, user="postgres",
                                     password=password, dbname="dashboard_auth_test", connect_timeout=2):
                    ready = True
                    break
            except psycopg.OperationalError:
                time.sleep(1)
        if not ready:
            raise RuntimeError("The PostgreSQL test container did not become ready.")
        os.environ["POSTGRES_TEST_URL"] = f"postgresql+psycopg://postgres:{password}@127.0.0.1:{port}/dashboard_auth_test"
        with psycopg.connect(host="127.0.0.1", port=port, user="postgres",
                             password=password, dbname="dashboard_auth_test") as connection:
            print("Connected to " + connection.execute("SELECT version()").fetchone()[0].split(" on ")[0], flush=True)
        tests = Path(__file__).resolve().parent / "tests"
        suite = unittest.defaultTestLoader.discover(str(tests), pattern="test_postgres_auth.py")
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        return 0 if result.wasSuccessful() else 1
    finally:
        os.environ.pop("POSTGRES_TEST_URL", None)
        if started:
            docker("rm", "--force", name)
            print("Removed the temporary PostgreSQL container and its test data.", flush=True)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (subprocess.CalledProcessError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        if isinstance(error, subprocess.CalledProcessError) and error.stderr:
            print(error.stderr, file=sys.stderr)
        sys.exit(1)
