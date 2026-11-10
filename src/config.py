"""Configuration from environment variables. No secret has a default here."""
import os

SESSION_COOKIE = "session"
SESSION_DAYS = 7


def database_url():
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set. See .env.example.")
    # Neon and most hosts give postgres://...; SQLAlchemy wants the driver named.
    for prefix in ("postgres://", "postgresql://"):
        if url.startswith(prefix):
            return "postgresql+psycopg://" + url[len(prefix):]
    return url


def secure_cookies():
    """Send the session cookie only over https once the app runs behind https."""
    return os.environ.get("PUBLIC_BASE_URL", "").startswith("https://")
