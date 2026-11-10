"""Sign-in rules: password check, session creation and lookup."""
import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import bcrypt

from src.config import SESSION_DAYS
from src.services.errors import InvalidCredentials, NotAuthenticated

WRONG_CREDENTIALS = "Wrong e-mail or password"


def hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()


def login(store, email, password, now=None):
    """Return (user, token) for a correct e-mail and password; raise otherwise."""
    user = store.get_user_by_email((email or "").strip().lower())
    # Same message for an unknown e-mail and a wrong password: do not reveal which accounts exist.
    if user is None or not user["password_hash"]:
        raise InvalidCredentials(WRONG_CREDENTIALS)
    if not bcrypt.checkpw((password or "").encode(), user["password_hash"].encode()):
        raise InvalidCredentials(WRONG_CREDENTIALS)
    now = now or datetime.now(timezone.utc)
    token = secrets.token_urlsafe(32)
    store.create_session(hash_token(token), user["id"], now + timedelta(days=SESSION_DAYS))
    return {"id": user["id"], "email": user["email"], "name": user["name"]}, token


def current_user(store, token, now=None):
    """The user behind a session token; raise NotAuthenticated if there is none."""
    if not token:
        raise NotAuthenticated("Sign in first")
    user = store.get_user_by_session(hash_token(token), now or datetime.now(timezone.utc))
    if user is None:
        raise NotAuthenticated("Sign in first")
    return user


def logout(store, token):
    if token:
        store.delete_session(hash_token(token))
