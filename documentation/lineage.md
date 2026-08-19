# Data Lineage Summary

Sources:
- source.orders (transaction system)
- source.products (catalog system)

Ingestion:
- scripts/01_extract.sql creates raw_views (raw_sales, raw_products) that mirror source state.

Transformations:
- scripts/02_transform.sql creates sales_canonical, joining products with sales and normalizing amounts.
- scripts/03_cleaning.sql applies QC rules, fills/masks nulls, and creates sales_clean and sales_qc_flags.

Consumers:
- BI dashboards: daily revenue rollups (consuming sales_clean)
- ML models: pricing elasticity features (consuming sales_canonical)
- Quality reports: scheduled qc job reads sales_qc_flags and opens tickets for problematic orders

Notes:
- Timestamps: order_timestamp -> order_date (truncated to day) in sales_canonical; track upstream timestamp fields to allow backtrace.
- Ownership: Owner / Steward / Custodian defined in governance.md for accountability in the lineage.
