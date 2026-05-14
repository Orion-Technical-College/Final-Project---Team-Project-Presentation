import os

from flask import Flask, abort, render_template, request, redirect, url_for

from .db import get_conn

app = Flask(__name__)


@app.get("/health")
def health():
    return "", 200

# Homepage – form to add customer
@app.route("/")
def index():
    return render_template("form.html")



# Insert new customer
@app.route("/add_customer", methods=["POST"])
def add_customer():
    name = request.form["name"]
    email = request.form["email"]

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO customers (name, email) VALUES (%s, %s)",
            (name, email),
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        return f"Error: {e}"
    finally:
        cur.close()
        conn.close()

    return redirect(url_for("view_customers"))


# View all customers
@app.route("/customers")
def view_customers():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name, email, created_at FROM customers ORDER BY id")
    customers = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("customers.html", customers=customers)

if __name__ == "__main__":
    app.run(debug=True)
