"""A fake store with the same methods as src/data/store.py, so tests need no database."""
import bcrypt
import pytest
from fastapi.testclient import TestClient

from src.main import create_app

PASSWORD = "splitmate-demo"
HASH = bcrypt.hashpw(PASSWORD.encode(), bcrypt.gensalt(4)).decode()  # cost 4: fast, tests only


class FakeStore:
    def __init__(self):
        self.users = {
            1: {"id": 1, "email": "ana@example.com", "name": "Ana", "password_hash": HASH},
            2: {"id": 2, "email": "google-only@example.com", "name": "Gina", "password_hash": None},
        }
        self.groups = {
            1: {"id": 1, "name": "Flat on Vitosha Blvd", "currency": "EUR"},
            2: {"id": 2, "name": "Weekend in Plovdiv", "currency": "EUR"},
            3: {"id": 3, "name": "Rila Monastery trip", "currency": "EUR"},
        }
        self.memberships = {(1, 1): "owner", (1, 2): "member"}
        self.sessions = {}

    def get_user_by_email(self, email):
        return next((dict(u) for u in self.users.values() if u["email"] == email), None)

    def create_session(self, token_hash, user_id, expires_at):
        self.sessions[token_hash] = (user_id, expires_at)

    def get_user_by_session(self, token_hash, now):
        found = self.sessions.get(token_hash)
        if found is None or found[1] <= now:
            return None
        u = self.users[found[0]]
        return {"id": u["id"], "email": u["email"], "name": u["name"]}

    def delete_session(self, token_hash):
        self.sessions.pop(token_hash, None)

    def list_groups_for_user(self, user_id):
        rows = [dict(self.groups[g], role=role) for (u, g), role in self.memberships.items() if u == user_id]
        return sorted(rows, key=lambda r: r["name"])


@pytest.fixture
def store():
    return FakeStore()


@pytest.fixture
def client(store):
    with TestClient(create_app(store=store), follow_redirects=False) as c:
        yield c


def sign_in(client, email="ana@example.com", password=PASSWORD):
    return client.post("/api/auth/login", json={"email": email, "password": password})
