import os
from contextlib import contextmanager

import psycopg


def _dsn() -> str:
    return (
        f"host={os.environ['PGHOST']} port={os.environ['PGPORT']} "
        f"dbname={os.environ['PGDATABASE']} user={os.environ['PGUSER']} "
        f"password={os.environ['PGPASSWORD']}"
    )


@contextmanager
def get_conn():
    conn = psycopg.connect(_dsn())
    try:
        yield conn
    finally:
        conn.close()
