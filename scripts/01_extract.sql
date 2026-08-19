-- scripts/01_extract.sql
-- Extract source tables for global health retail example

-- Example: pull raw sales and product data from source systems
-- (replace table names/columns with your real source tables)
CREATE OR REPLACE VIEW raw_sales AS
SELECT
  order_id,
  customer_id,
  product_id,
  quantity,
  price,
  order_timestamp
FROM source.orders
WHERE order_timestamp >= CURRENT_DATE - INTERVAL '365 days';

CREATE OR REPLACE VIEW raw_products AS
SELECT
  product_id,
  sku,
  product_name,
  category,
  manufacturer,
  created_at
FROM source.products;
