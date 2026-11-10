"""HTTP routes for sign-in. They read the request and shape the response; rules live in services."""
from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel

from src.config import SESSION_COOKIE, SESSION_DAYS, secure_cookies
from src.routes.deps import get_store, require_user, session_token
from src.services import auth

router = APIRouter(prefix="/api/auth")


class LoginBody(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(body: LoginBody, response: Response, store=Depends(get_store)):
    user, token = auth.login(store, body.email, body.password)
    response.set_cookie(
        SESSION_COOKIE, token, max_age=SESSION_DAYS * 86400,
        httponly=True, samesite="lax", secure=secure_cookies(),
    )
    return {"user": user}


@router.post("/logout")
def logout(request: Request, response: Response, store=Depends(get_store)):
    auth.logout(store, session_token(request))
    response.delete_cookie(SESSION_COOKIE)
    return {"ok": True}


@router.get("/me")
def me(user=Depends(require_user)):
    return {"user": user}
