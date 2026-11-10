"""Data access: every SQL query of the app lives here, behind plain methods."""
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError


class Store:
    def __init__(self, engine):
        self.engine = engine

    def get_user_by_email(self, email):
        with self.engine.connect() as conn:
            row = conn.execute(
                text("SELECT id, email, name, password_hash FROM users WHERE email = :e"),
                {"e": email},
            ).mappings().first()
        return dict(row) if row else None

    def create_user(self, email, name, password_hash):
        """Insert a user; return None when the e-mail is already taken."""
        try:
            with self.engine.begin() as conn:
                row = conn.execute(
                    text(
                        "INSERT INTO users (email, name, password_hash) VALUES (:e, :n, :p)"
                        " RETURNING id, email, name"
                    ),
                    {"e": email, "n": name, "p": password_hash},
                ).mappings().first()
        except IntegrityError:
            return None
        return dict(row)

    def create_session(self, token_hash, user_id, expires_at):
        with self.engine.begin() as conn:
            conn.execute(
                text("INSERT INTO sessions (token_hash, user_id, expires_at) VALUES (:t, :u, :x)"),
                {"t": token_hash, "u": user_id, "x": expires_at},
            )

    def get_user_by_session(self, token_hash, now):
        with self.engine.connect() as conn:
            row = conn.execute(
                text(
                    "SELECT u.id, u.email, u.name FROM sessions s JOIN users u ON u.id = s.user_id"
                    " WHERE s.token_hash = :t AND s.expires_at > :now"
                ),
                {"t": token_hash, "now": now},
            ).mappings().first()
        return dict(row) if row else None

    def delete_session(self, token_hash):
        with self.engine.begin() as conn:
            conn.execute(text("DELETE FROM sessions WHERE token_hash = :t"), {"t": token_hash})

    def list_groups_for_user(self, user_id):
        with self.engine.connect() as conn:
            rows = conn.execute(
                text(
                    "SELECT g.id, g.name, g.currency, m.role FROM memberships m"
                    " JOIN groups g ON g.id = m.group_id WHERE m.user_id = :u ORDER BY g.name"
                ),
                {"u": user_id},
            ).mappings().all()
        return [dict(r) for r in rows]
