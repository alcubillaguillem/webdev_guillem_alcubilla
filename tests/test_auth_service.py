"""Edge cases of the sign-in rules in src/services/auth.py."""
from datetime import datetime, timedelta, timezone

import pytest

from src.services import auth
from src.services.errors import InvalidCredentials, NotAuthenticated
from tests.conftest import PASSWORD, sign_in


def test_unknown_email_gets_the_same_message_as_a_wrong_password(store):
    with pytest.raises(InvalidCredentials, match="Wrong e-mail or password"):
        auth.login(store, "nobody@example.com", PASSWORD)


def test_google_only_account_cannot_sign_in_with_a_password(store):
    with pytest.raises(InvalidCredentials):
        auth.login(store, "google-only@example.com", "")


def test_email_is_matched_case_insensitively(store):
    user, token = auth.login(store, "  ANA@example.com ", PASSWORD)
    assert user["email"] == "ana@example.com"
    assert auth.current_user(store, token)["id"] == 1


def test_only_the_token_hash_is_stored(store):
    _, token = auth.login(store, "ana@example.com", PASSWORD)
    assert token not in store.sessions
    assert auth.hash_token(token) in store.sessions


def test_expired_session_is_not_accepted(store):
    past = datetime.now(timezone.utc) - timedelta(days=30)
    _, token = auth.login(store, "ana@example.com", PASSWORD, now=past)
    with pytest.raises(NotAuthenticated):
        auth.current_user(store, token)


def test_missing_or_unknown_token_is_not_authenticated(store):
    with pytest.raises(NotAuthenticated):
        auth.current_user(store, None)
    with pytest.raises(NotAuthenticated):
        auth.current_user(store, "not-a-real-token")


def test_logout_ends_the_session(client, store):
    sign_in(client)
    assert client.get("/api/auth/me").json()["user"]["email"] == "ana@example.com"
    client.post("/api/auth/logout")
    assert store.sessions == {}
    assert client.get("/api/auth/me").status_code == 401


def test_logout_without_session_is_harmless(store):
    auth.logout(store, None)


def test_missing_fields_get_a_readable_422(client):
    response = client.post("/api/auth/login", json={"email": "ana@example.com"})
    assert response.status_code == 422
    assert response.json() == {"error": "Some fields are missing or invalid"}


def test_home_redirects_to_groups_and_login_page_is_served(client):
    assert client.get("/").headers["location"] == "/groups"
    assert "Sign in" in client.get("/login").text
