import pytest
import app.app as app_module


@pytest.fixture
def client():
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as c:
        yield c


def test_health(client):
    assert client.get("/health").status_code == 200


def test_customers_lists_seed_marker(client):
    rv = client.get("/customers")
    assert rv.status_code == 200
    body = rv.data.decode("utf-8")
    assert "Avery" in body or "avery.lopez@example.com" in body


def test_create_order_inserts_row(client):
    payload = {"customer_id": 1, "status": "NEW"}
    rv = client.post("/orders", json=payload)
    assert rv.status_code in (200, 201)
    from app.db import get_conn

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id FROM orders WHERE customer_id = %s AND status = %s ORDER BY id DESC LIMIT 1",
                (1, "NEW"),
            )
            row = cur.fetchone()
    assert row is not None
