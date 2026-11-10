"""Sign-in rules: password check, session creation and lookup."""
import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import bcrypt

from src.config import SESSION_DAYS
from src.services.errors import Conflict, InvalidCredentials, InvalidInput, NotAuthenticated

WRONG_CREDENTIALS = "Wrong e-mail or password"
MIN_PASSWORD = 8


def hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()


def _start_session(store, user, now):
    token = secrets.token_urlsafe(32)
    store.create_session(hash_token(token), user["id"], now + timedelta(days=SESSION_DAYS))
    return {"id": user["id"], "email": user["email"], "name": user["name"]}, token


def register(store, email, name, password, now=None):
    """Create a password account and sign it in. Return (user, token)."""
    email = (email or "").strip().lower()
    name = (name or "").strip()
    password = password or ""
    if "@" not in email or "." not in email.split("@")[-1]:
        raise InvalidInput("Enter a valid e-mail address")
    if not name:
        raise InvalidInput("Enter your name")
    if len(password) < MIN_PASSWORD:
        raise InvalidInput(f"The password needs at least {MIN_PASSWORD} characters")
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = store.create_user(email, name, password_hash)
    if user is None:
        raise Conflict("An account with this e-mail already exists")
    return _start_session(store, user, now or datetime.now(timezone.utc))


def login(store, email, password, now=None):
    """Return (user, token) for a correct e-mail and password; raise otherwise."""
    user = store.get_user_by_email((email or "").strip().lower())
    # Same message for an unknown e-mail and a wrong password: do not reveal which accounts exist.
    if user is None or not user["password_hash"]:
        raise InvalidCredentials(WRONG_CREDENTIALS)
    if not bcrypt.checkpw((password or "").encode(), user["password_hash"].encode()):
        raise InvalidCredentials(WRONG_CREDENTIALS)
    return _start_session(store, user, now or datetime.now(timezone.utc))


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
