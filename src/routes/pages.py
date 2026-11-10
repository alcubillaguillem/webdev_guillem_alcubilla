"""The HTML pages. A page that needs a session redirects to /login instead of answering 401."""
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, RedirectResponse

from src.routes.deps import get_store, session_token
from src.services import auth
from src.services.errors import NotAuthenticated

STATIC = Path(__file__).resolve().parents[2] / "static"
router = APIRouter()


def signed_in(request: Request):
    try:
        auth.current_user(get_store(request), session_token(request))
        return True
    except NotAuthenticated:
        return False


@router.get("/")
def home():
    return RedirectResponse("/groups", status_code=302)


@router.get("/login")
def login_page():
    return FileResponse(STATIC / "login.html")


@router.get("/groups")
def groups_page(request: Request):
    if not signed_in(request):
        return RedirectResponse("/login", status_code=302)
    return FileResponse(STATIC / "groups.html")
