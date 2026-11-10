"""Creating an account with e-mail and password."""
import pytest

from src.services import auth
from src.services.errors import InvalidInput


def register(client, email="new@example.com", name="Nora", password="long-enough"):
    return client.post("/api/auth/register", json={"email": email, "name": name, "password": password})


def test_ac17_new_account_is_created_hashed_and_signed_in(client, store):
    response = register(client)
    assert response.status_code == 201
    assert response.json()["user"]["email"] == "new@example.com"
    row = next(u for u in store.users.values() if u["email"] == "new@example.com")
    assert row["password_hash"].startswith("$2b$")
    assert "long-enough" not in row["password_hash"]
    assert client.get("/api/auth/me").json()["user"]["name"] == "Nora"
    assert client.get("/groups").status_code == 200


def test_ac18_existing_email_is_refused_with_409(client, store):
    before = len(store.users)
    response = register(client, email="ANA@example.com")
    assert response.status_code == 409
    assert response.json() == {"error": "An account with this e-mail already exists"}
    assert len(store.users) == before


def test_ac18_short_password_is_refused_with_422(client, store):
    before = len(store.users)
    response = register(client, password="short")
    assert response.status_code == 422
    assert response.json() == {"error": "The password needs at least 8 characters"}
    assert len(store.users) == before


@pytest.mark.parametrize("email,name,message", [
    ("not-an-email", "Nora", "Enter a valid e-mail address"),
    ("nora@nodot", "Nora", "Enter a valid e-mail address"),
    ("nora@example.com", "   ", "Enter your name"),
])
def test_invalid_email_or_name_is_refused(store, email, name, message):
    with pytest.raises(InvalidInput, match=message):
        auth.register(store, email, name, "long-enough")


def test_register_page_is_served(client):
    assert "Create an account" in client.get("/register").text
