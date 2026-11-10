"""The database engine and the migration runner. Only src/data/ talks SQL."""
from pathlib import Path

from sqlalchemy import create_engine, text

MIGRATIONS = Path(__file__).resolve().parents[2] / "migrations"


def make_engine(url):
    return create_engine(url, pool_pre_ping=True)


def run_migrations(engine):
    """Apply every numbered file in migrations/ that has not run yet, in order."""
    with engine.begin() as conn:
        conn.execute(text(
            "CREATE TABLE IF NOT EXISTS schema_migrations ("
            " name TEXT PRIMARY KEY, applied_at TIMESTAMPTZ NOT NULL DEFAULT now())"
        ))
        done = {row[0] for row in conn.execute(text("SELECT name FROM schema_migrations"))}
    for path in sorted(MIGRATIONS.glob("[0-9][0-9][0-9]_*.sql")):
        if path.name in done:
            continue
        # One transaction per file: a migration either runs completely or not at all.
        with engine.begin() as conn:
            conn.exec_driver_sql(path.read_text(encoding="utf-8"))
            conn.execute(text("INSERT INTO schema_migrations (name) VALUES (:n)"), {"n": path.name})
