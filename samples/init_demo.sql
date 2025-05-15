-- --------------------------
-- Örnek şema + dummy veri
-- --------------------------

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
  customer_id SERIAL PRIMARY KEY,
  first_name  TEXT,
  last_name   TEXT
);

CREATE TABLE orders (
  order_id     SERIAL PRIMARY KEY,
  customer_id  INT REFERENCES customers(customer_id),
  total_amount NUMERIC
);

-- 50 müşteri
INSERT INTO customers(first_name, last_name)
SELECT 'Name' || g, 'Surname' || g FROM generate_series(1, 50) AS g;

-- Her müşteri için 1-200 sipariş, tutar 10-210 ₺
INSERT INTO orders(customer_id, total_amount)
SELECT (random()*49 + 1)::INT, (random()*200 + 10)::NUMERIC
FROM generate_series(1, 5000);
