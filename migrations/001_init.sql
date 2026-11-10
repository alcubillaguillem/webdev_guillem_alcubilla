-- Users, sessions, groups and memberships (users <-> groups, many-to-many).
CREATE TABLE users (
    id            SERIAL PRIMARY KEY,
    email         TEXT NOT NULL UNIQUE,
    name          TEXT NOT NULL,
    password_hash TEXT,            -- NULL for an account created through Google only
    google_sub    TEXT UNIQUE,     -- Google's account id, set when the account is linked
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Only the SHA-256 of the session token is stored: a leaked table cannot be replayed.
CREATE TABLE sessions (
    token_hash TEXT PRIMARY KEY,
    user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expires_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE groups (
    id         SERIAL PRIMARY KEY,
    name       TEXT NOT NULL,
    currency   TEXT NOT NULL DEFAULT 'EUR',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE memberships (
    user_id  INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    group_id INTEGER NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
    role     TEXT NOT NULL CHECK (role IN ('owner', 'member')),
    PRIMARY KEY (user_id, group_id)
);
