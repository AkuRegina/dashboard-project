# Authentication backend

Flask API for the Flutter Windows dashboard, using the existing PostgreSQL users.
No Flutter application exists in this repository yet.

## Local test page

With backend dependencies installed, run from `backend/`:

```powershell
.\.venv\Scripts\python.exe -m flask --app app.demo:create_demo_app run --host 127.0.0.1 --port 5050 --no-reload
```

Open http://127.0.0.1:5050 to create an account, log in, check your session,
change your password, and log out. Passwords need at least 8 characters.
Accounts persist in `backend/instance/auth-demo.sqlite`, a separate local database.
No PostgreSQL setup or `.env` is needed for this preview. Stop it with Ctrl+C.
The browser keeps its session token in memory; refreshing the page requires login
again (the server session remains until logout or expiry).

Self-registration at `/demo/register` is enabled only in this demo application;
the regular backend continues to require administrator-created accounts.

## Local setup (PowerShell)

Install Python 3.11 or newer with the Windows `py` launcher, plus PostgreSQL.
If Python is installed without the launcher, substitute `python` for `py` below.
Alternatively, with `uv` installed, use `uv venv .venv --python 3.14` and
`uv pip install --python .venv\Scripts\python.exe -r requirements.txt` from `backend/`.

Create `deviation_dashboard` and run `database/schema.sql` only for a new database.
For both new and existing databases, run `database/migrations/001_authentication.sql`
once, using pgAdmin or psql. The migration preserves existing records. It stops if
two existing emails differ only by case; resolve those duplicates before retrying.
Do not rerun schema.sql on a populated database: it drops the tables.

From the repository root:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` with your database credentials (URL-encode special characters in the
database password), then create a new administrator and start the local server:

```powershell
.\.venv\Scripts\python.exe -m flask --app app:create_app create-admin
.\.venv\Scripts\python.exe -m flask --app app:create_app run --host 127.0.0.1 --port 5000
```

The administrator command prompts privately for a password. Passwords must contain
8 to 128 characters. Existing seed password placeholders are not valid credentials;
create new accounts through the administrator API. There is no public registration.

## API

Requests with bodies use `Content-Type: application/json`.
Protected requests use `Authorization: Bearer <token>`.

| Method | Path | Body / purpose |
|---|---|---|
| POST | `/auth/login` | `email`, `password`; returns token, expiration, user |
| GET | `/auth/me` | Return current user |
| POST | `/auth/logout` | Revoke current session; returns 204 |
| POST | `/auth/change-password` | `current_password`, `new_password`; revokes all sessions |
| POST | `/admin/users` | `f_name`, `l_name`, `email`, `password`, optional `role` |
| PATCH | `/admin/users/<id>` | Any of `f_name`, `l_name`, `email`, `role`, `is_active` |

Roles are `admin`, `manager`, and `worker`; new users default to worker.
Only administrators can manage accounts. Account updates revoke that user's sessions.
Administrators cannot deactivate or demote themselves. Passwords and token hashes
are never included in user responses. Errors return a JSON `error` field.

Example login from PowerShell:

```powershell
$credentials = Get-Credential -Message 'Dashboard login'
$loginBody = @{
    email = $credentials.UserName
    password = $credentials.GetNetworkCredential().Password
} | ConvertTo-Json
$login = Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/auth/login -ContentType application/json -Body $loginBody
$authHeaders = @{ Authorization = "Bearer $($login.token)" }
Invoke-RestMethod -Uri http://127.0.0.1:5000/auth/me -Headers $authHeaders
```

## Connecting Flutter and deviation routes

After login, keep the token in memory and send it on every protected request.
On 401, discard it and show login. Logout discards it locally after calling the API.
If persistent login is added, use Windows credential storage rather than a plain file.

Future Flask routes should use `@require_auth()` from `app.security`, or
`@require_auth("admin", "manager")` for manager actions. The authenticated user is
`flask.g.user`. Set `submitted_by` and comment `user_id` from this user.
For worker access, constrain deviation queries to `assigned_to == g.user.user_id`;
apply this to details, status changes, comments, images, and analytics as well.
These domain endpoints are not implemented yet.

## Deployment

Serve through a production WSGI server behind HTTPS. Flask's development server is
for local use. Session lifetime defaults to eight hours with no automatic renewal;
logout and password changes revoke sessions in PostgreSQL immediately.

Use a shared Redis `RATELIMIT_STORAGE_URI` for multiple server processes; the local
memory setting is per process and resets on restart. Login limits are keyed to the
request's remote address. Behind a proxy, configure trusted proxy forwarding for
your actual topology before relying on client IP limits. Do not enable Flask debug
mode in production or log passwords, request bodies, or Authorization headers.

Periodically remove expired sessions:

```sql
DELETE FROM auth_sessions WHERE expires_at <= CURRENT_TIMESTAMP;
```

Email invitations, password recovery, MFA, and company SSO are future additions.

## Authentication tests

From `backend/`, after installing dependencies:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The tests use isolated in-memory SQLite databases and do not touch your PostgreSQL
data. They cover credentials, session storage and expiry, logout, password changes,
administrator permissions, account deactivation, validation, and login rate limits.
They do not validate the PostgreSQL migration or PostgreSQL-specific constraints.
The demo tests also cover frontpage assets, registration, duplicate emails,
registration-to-login-to-logout, and separation from the regular backend.

## PostgreSQL integration tests

Start Docker Desktop and run from `backend/`:

```powershell
.\.venv\Scripts\python.exe test_postgres.py
```

The runner downloads `postgres:17-alpine` if needed and starts a temporary container
with a random password, a random localhost port, and a dedicated test database.
It applies the actual `database/schema.sql` and authentication migration in isolated
schemas, runs authentication and test-page registration checks, then removes the
container and its data. It does not read your application's DATABASE_URL or change
your existing databases or the running SQLite preview.

Migration checks cover preservation of users, deviations, comments, and views;
case-insensitive email uniqueness; valid roles; session foreign keys; and rollback
when existing emails conflict. The suite also includes the shared rate-limit check,
which does not require database access. A normal unittest run skips PostgreSQL
integration tests unless POSTGRES_TEST_URL is supplied; use this runner for isolation.
