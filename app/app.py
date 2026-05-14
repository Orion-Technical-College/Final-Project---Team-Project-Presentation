import os

from flask import Flask, abort, render_template, request

from .db import get_conn

app = Flask(__name__)


@app.get("/health")
def health():
    return "", 200


@app.get("/customers")
def customers():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, email FROM customers ORDER BY id")
            rows = cur.fetchall()
    return render_template("list.html", rows=rows)


@app.get("/orders/new")
def create_form():
    return render_template("create.html")


@app.post("/orders")
def create_order():
    payload = request.get_json(silent=True) or {}
    try:
        customer_id = int(payload.get("customer_id"))
        status = str(payload.get("status", "NEW"))
    except (TypeError, ValueError):
        abort(400)
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO orders (customer_id, status) VALUES (%s, %s) RETURNING id",
                (customer_id, status),
            )
            new_id = cur.fetchone()[0]
        conn.commit()
    return {"id": new_id}, 201
