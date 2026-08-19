-- scripts/02_transform.sql
-- Transformations: canonicalize and join sales + product info

CREATE OR REPLACE VIEW sales_canonical AS
SELECT
  s.order_id,
  s.customer_id,
  s.product_id,
  p.sku,
  p.product_name,
  p.category,
  COALESCE(s.quantity,0) AS quantity,
  COALESCE(s.price,0.0) AS price,
  (COALESCE(s.quantity,0) * COALESCE(s.price,0.0)) AS revenue,
  DATE_TRUNC('day', s.order_timestamp) AS order_date
FROM raw_sales s
LEFT JOIN raw_products p
  ON s.product_id = p.product_id;
