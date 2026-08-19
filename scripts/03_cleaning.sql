-- scripts/03_cleaning.sql
-- Cleaning and data quality fixes — resolves known flags (nulls, negative values)

-- 1) Remove or correct negative quantities/prices
CREATE OR REPLACE VIEW sales_clean AS
SELECT
  order_id,
  customer_id,
  product_id,
  sku,
  product_name,
  category,
  CASE WHEN quantity < 0 THEN 0 ELSE quantity END AS quantity,
  CASE WHEN price < 0 THEN NULL ELSE price END AS price,
  CASE
    WHEN price IS NULL THEN 0.0
    ELSE price
  END AS price_filled,
  CASE WHEN (CASE WHEN quantity < 0 THEN 0 ELSE quantity END) IS NULL THEN 0
       ELSE (CASE WHEN quantity < 0 THEN 0 ELSE quantity END)
  END AS quantity_filled,
  (COALESCE(quantity,0) * COALESCE(price,0.0)) AS revenue,
  order_date
FROM sales_canonical
WHERE order_date IS NOT NULL;

-- 2) Flag suspicious rows for downstream review
CREATE OR REPLACE VIEW sales_qc_flags AS
SELECT
  order_id,
  CASE WHEN price IS NULL THEN 'missing_price' ELSE NULL END AS price_flag,
  CASE WHEN quantity < 0 THEN 'negative_quantity' ELSE NULL END AS quantity_flag,
  CASE WHEN product_name IS NULL THEN 'missing_product' ELSE NULL END AS product_flag
FROM sales_canonical
WHERE price IS NULL OR quantity < 0 OR product_name IS NULL;
