"""Shared route helpers: the store and the signed-in user, read from the request."""
from fastapi import Request

from src.config import SESSION_COOKIE
from src.services import auth


def get_store(request: Request):
    return request.app.state.store


def session_token(request: Request):
    return request.cookies.get(SESSION_COOKIE)


def require_user(request: Request):
    """Raise NotAuthenticated (401) when the request carries no valid session."""
    return auth.current_user(get_store(request), session_token(request))
