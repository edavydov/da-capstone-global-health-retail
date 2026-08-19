# da-capstone-global-health-retail (Exemplar)

Project title
- da-capstone-global-health-retail

Business problem
- Objective: Enable analysis of global health retail transactions to identify top-selling health products, detect data quality issues in transactions, and prepare cleaned data for reporting and modeling. Use-case examples include revenue analytics, inventory forecasting, and product safety signal detection.

Repository structure
- scripts/
  - 01_extract.sql — extract raw tables into raw views
  - 02_transform.sql — canonicalize and join sales and product data
  - 03_cleaning.sql — data quality fixes and QC flagging
- notebooks/
  - sample_analysis.ipynb — example notebook for exploratory analysis
- documentation/
  - governance.md — roles and responsibilities
  - lineage.md — data lineage and transformation summary

Governance framework
- Owner (Accountable)
  - Example: Alice Example (alice@example.org)
  - Responsibilities: Owning business outcomes, approving schema changes, sign-off on releases.
- Steward (Responsible)
  - Example: Bob Steward (bob@example.org)
  - Responsibilities: Day-to-day data quality, metadata, and access review.
- Custodian (Technical)
  - Example: Carla Custodian (carla@example.org)
  - Responsibilities: Pipeline operations, backups, runbook maintenance.

Data lineage summary
- Sources: source.orders (transactional) and source.products (catalog)
- Ingestion: scripts/01_extract.sql -> raw_sales, raw_products
- Transformation: scripts/02_transform.sql -> sales_canonical
- Cleaning: scripts/03_cleaning.sql -> sales_clean and sales_qc_flags
- Consumers: dashboards, ML pipelines, reporting extracts

Submission instructions
1. Fork this repository (if submitting a modification) or clone it.
2. Make your changes on a feature branch:
   - git checkout -b feature/your-change
3. Run tests / notebooks locally.
4. Commit with clear messages and push to your fork:
   - git add .
   - git commit -m "Short descriptive message"
   - git push origin feature/your-change
5. Open a Pull Request targeting the main branch of the original repository. Include:
   - Description of changes
   - Data schema changes (if any)
   - Impact assessment and owner approvals (if needed)

Contact & support
- For governance questions, contact the Owner or Steward listed in documentation/governance.md.
