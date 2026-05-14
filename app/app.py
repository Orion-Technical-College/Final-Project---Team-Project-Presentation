import os

from flask import Flask, abort, render_template, request, redirect, url_for

from .db import get_conn

app = Flask(__name__)


@app.get("/health")
def health():
    return "", 200

@app.route("/")
def index():
    return render_template("form.html")

# Add new customer
@app.route("/add_customer", methods=["POST"])
def add_customer():
    customer_id = request.form["customer_id"]
    company_name = request.form["company_name"]
    contact_name = request.form["contact_name"]
    email = request.form["email"]
    region = request.form["region"]

    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO CUSTOMER (CompanyName, ContactName, Email, Region)
            VALUES (%s, %s, %s, %s)
        """, (company_name, contact_name, email, region))

        conn.commit()

    except Exception as e:
        conn.rollback()
        return f"❌ Error inserting customer: {e}"

    finally:
        cur.close()
        conn.close()

    return redirect(url_for("view_customers"))


# View all customers
@app.route("/customers")
def view_customers():
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT CustomerID, CompanyName, ContactName, Email, Region, created_at
            FROM CUSTOMER
            ORDER BY CustomerID
        """)

        customers = cur.fetchall()

    except Exception as e:
        return f"❌ Error retrieving customers: {e}"

    finally:
        cur.close()
        conn.close()

    return render_template("customers.html", customers=customers)

if __name__ == "__main__":
    app.run(debug=True)
