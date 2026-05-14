import os
import time

import psycopg
import pytest


def _dsn() -> str:
    return (
        f"host={os.environ.get('PGHOST', 'localhost')} "
        f"port={os.environ.get('PGPORT', '5432')} "
        f"dbname={os.environ.get('PGDATABASE', 'ia510')} "
        f"user={os.environ.get('PGUSER', 'ia510_user')} "
        f"password={os.environ.get('PGPASSWORD', 'ia510_pass')}"
    )


def wait_for_db(timeout: int = 120) -> None:
    start = time.time()
    while time.time() - start < timeout:
        try:
            with psycopg.connect(_dsn(), connect_timeout=5) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
            return
        except Exception:
            time.sleep(1)
    raise RuntimeError("Postgres did not become ready in time")


def pytest_sessionstart(session) -> None:
    wait_for_db()


@pytest.fixture
def db_conn():
    with psycopg.connect(_dsn()) as conn:
        conn.autocommit = True
        yield conn
