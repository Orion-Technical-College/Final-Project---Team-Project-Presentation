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
    company_name = request.form["company_name"]
    contact_name = request.form["contact_name"]
    email = request.form["email"]
    region = request.form["region"]

    try:
        with get_conn() as conn:
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO CUSTOMER (CompanyName, ContactName, Email, Region)
                VALUES (%s, %s, %s, %s)
            """, (company_name, contact_name, email, region))

            conn.commit()

    except Exception as e:
        return f"Error inserting customer: {e}"

    return redirect(url_for("view_customers"))



# View all customers
@app.route("/customers")
def view_customers():
    with get_conn() as conn:
        cur = conn.cursor()

        cur.execute("""
            SELECT CustomerID, CompanyName, ContactName, Email, Region, created_at
            FROM CUSTOMER
            ORDER BY CustomerID
           """)

        customers = cur.fetchall()

        return render_template("customers.html", customers=customers)

# Edit customer details
@app.route("/edit/<int:customer_id>")
def edit_customer(customer_id):
    with get_conn() as conn:
        cur = conn.cursor()

        cur.execute("""
            SELECT CustomerID, CompanyName, ContactName, Email, Region
            FROM CUSTOMER
            WHERE CustomerID = %s
        """, (customer_id,))

        customer = cur.fetchone()

    return render_template("edit_customer.html", customer=customer)

# Update customer details
@app.route("/update/<int:customer_id>", methods=["POST"])
def update_customer(customer_id):
    company_name = request.form["company_name"]
    contact_name = request.form["contact_name"]
    email = request.form["email"]
    region = request.form["region"]

    try:
        with get_conn() as conn:
            cur = conn.cursor()

            cur.execute("""
                UPDATE CUSTOMER
                SET CompanyName = %s,
                    ContactName = %s,
                    Email = %s,
                    Region = %s
                WHERE CustomerID = %s
            """, (company_name, contact_name, email, region, customer_id))

            conn.commit()

    except Exception as e:
        return f"Error updating customer: {e}"

    return redirect(url_for("view_customers"))

# Delete customer
@app.route("/delete/<int:customer_id>")
def delete_customer(customer_id):
    
    try:
        with get_conn() as conn:
            cur = conn.cursor()

            cur.execute("""
                DELETE FROM CUSTOMER
                WHERE CustomerID = %s
            """, (customer_id,))

            conn.commit()

    except Exception as e:
        return f"Error deleting customer: {e}"

    return redirect(url_for("view_customers"))


if __name__ == "__main__":
    app.run(debug=True)
