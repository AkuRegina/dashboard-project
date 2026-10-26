-- Run once against the existing deviation_dashboard database.
-- Existing users become workers. Placeholder passwords cannot authenticate.
BEGIN;

ALTER TABLE users
    ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT 'worker'
        CHECK (role IN ('admin', 'manager', 'worker')),
    ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT TRUE,
    ADD COLUMN created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ADD COLUMN password_changed_at TIMESTAMPTZ;

-- Fails safely if existing emails differ only by case; resolve those first.
CREATE UNIQUE INDEX users_email_lower_unique ON users (LOWER(email));

CREATE TABLE auth_sessions (
    token_hash VARCHAR(64) PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMPTZ NOT NULL
);
CREATE INDEX auth_sessions_user_id_idx ON auth_sessions (user_id);
CREATE INDEX auth_sessions_expires_at_idx ON auth_sessions (expires_at);

COMMIT;
