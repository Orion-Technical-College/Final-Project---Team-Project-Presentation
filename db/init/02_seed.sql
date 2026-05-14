-- Canonical seed (must stay aligned with MP7 autograde marker: Avery / avery.lopez@example.com).

INSERT INTO customers (name, email)
VALUES
    ('Avery Lopez', 'avery.lopez@example.com'),
    ('Morgan Chen', 'morgan.chen@example.com');

INSERT INTO products (sku, name, unit_price)
VALUES
    ('SKU-001', 'Widget A', 19.99),
    ('SKU-002', 'Widget B', 29.50);

INSERT INTO orders (customer_id, status)
VALUES (1, 'CONFIRMED');

INSERT INTO order_lines (order_id, product_id, qty, line_total)
VALUES (1, 1, 2, 39.98);
