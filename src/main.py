"""The FastAPI app: wires routes, static files and the error format together."""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from src.config import database_url
from src.data.db import make_engine, run_migrations
from src.data.store import Store
from src.routes import auth, groups, pages
from src.routes.pages import STATIC
from src.services.errors import DomainError


def create_app(store=None):
    """Build the app. Tests pass a fake store; the real one connects to DATABASE_URL."""

    @asynccontextmanager
    async def lifespan(app):
        if store is None:
            engine = make_engine(database_url())
            run_migrations(engine)
            app.state.store = Store(engine)
        else:
            app.state.store = store
        yield

    app = FastAPI(title="SplitMate", lifespan=lifespan)

    @app.exception_handler(DomainError)
    async def domain_error(request: Request, exc: DomainError):
        return JSONResponse({"error": exc.message}, status_code=exc.status)

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, exc: RequestValidationError):
        return JSONResponse({"error": "Some fields are missing or invalid"}, status_code=422)

    app.include_router(auth.router)
    app.include_router(groups.router)
    app.include_router(pages.router)
    app.mount("/static", StaticFiles(directory=STATIC), name="static")
    return app


app = create_app()
