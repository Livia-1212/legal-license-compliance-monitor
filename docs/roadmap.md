# Project Roadmap

## Attorney License Compliance Monitor

This project is evolving from a CSV-backed compliance dashboard into a PostgreSQL-backed legal compliance operations platform with future BigQuery analytics, document automation, and agentic AI workflow capabilities.

---

## Completed / Current Foundation

### Phase 1-7: Dashboard and Analytics Foundation

Completed foundation includes:

- Synthetic attorney, license, CLE, matter, and matter assignment datasets
- SQL compliance checks
- Python analytics layer
- Streamlit dashboard
- Executive Summary
- Attorney Directory
- Matters Directory
- CLE Compliance views
- Custom legal-finance UI styling
- Sign In / Register workflow foundation
- Role-based permission foundation
- CI/testing foundation

Current system still uses CSV files as the primary data source. CSV files will remain as seed/import data only after the persistence layer is implemented.

---

## Updated Roadmap

### Phase 8: PostgreSQL Persistence Layer

Goal: Replace CSV-backed runtime data with PostgreSQL-backed runtime data.

Planned work:

- Design normalized PostgreSQL schema
- Create PostgreSQL table scripts
- Add primary keys and foreign keys
- Seed PostgreSQL tables from existing CSV files
- Create Python database connection module
- Create repository functions for reading attorney, license, CLE, matter, and assignment data
- Begin replacing CSV reads with PostgreSQL reads

Target files:

- `sql/08_postgres_schema.sql`
- `scripts/seed_postgres_from_csv.py`
- `src/db/connection.py`
- `src/db/repositories.py`

---

### Phase 9: PostgreSQL-Backed Authentication and Role-Based Access

Goal: Move authentication and permissions into PostgreSQL.

Planned work:

- Create `users` table
- Store hashed passwords
- Support roles: anonymous, user, admin
- Complete Sign In / Register / Logout workflow
- Gate pages by role
- Protect admin-only functions

Target files:

- `src/auth.py`
- `src/db/auth_repository.py`
- `streamlit_app.py`

---

### Phase 10: Data Entry, Edit Workflows, and Audit Logging

Goal: Turn the dashboard into an operational legal compliance platform.

Planned work:

- Add attorney creation and edit forms
- Add license record creation and edit forms
- Add CLE record creation and edit forms
- Add matter creation and edit forms
- Add matter assignment workflows
- Add admin-only delete controls
- Add CSV upload/import
- Add CSV export
- Add audit logging for data changes

Target files:

- `src/data_entry.py`
- `src/db/audit_repository.py`
- `src/db/repositories.py`
- `streamlit_app.py`

---

### Phase 11: BigQuery Analytics Warehouse Extension

Goal: Add cloud analytics capability for resume-relevant data engineering and reporting.

Planned work:

- Create BigQuery dataset
- Create BigQuery table definitions
- Export PostgreSQL or CSV data into BigQuery
- Build BigQuery SQL views for compliance metrics
- Build analytics tables for attorney compliance, CLE deficiency, matter assignment review, revenue exposure, and agent run history

Target files:

- `sql/bigquery/01_create_tables.sql`
- `sql/bigquery/02_compliance_views.sql`
- `scripts/export_to_bigquery.py`
- `src/db/bigquery_client.py`

---

### Phase 12: Document Intake, PDF Parsing, and OCR

Goal: Add legal document automation capability.

Planned work:

- Upload PDF/image documents
- Extract text from PDFs
- Add OCR for scanned documents
- Classify document type
- Extract structured fields from CLE certificates, attorney registration records, matter intake forms, and supporting documents
- Add human review before saving extracted data
- Store document metadata and extracted text

Target files:

- `src/document_processing/pdf_parser.py`
- `src/document_processing/ocr.py`
- `src/document_processing/classifier.py`
- `src/document_processing/extractor.py`
- `src/document_processing/review.py`

---

## Optional BI Extension

Tableau and Power BI are not required core phases.

They may be added later only if useful for a target role requiring business intelligence or executive dashboarding.

Possible future BI flow:

- PostgreSQL or BigQuery as source
- Tableau / Power BI as optional executive dashboard layer
- Streamlit remains the operational application interface

---

## Future Agentic AI Direction

After Phase 12, the project can evolve into an agentic legal compliance workflow system.

Future phases may include:

- ChromaDB legal document retrieval layer
- Agent tool layer
- Compliance agent orchestrator
- Human review queue
- Evidence-backed compliance findings
- Automated compliance reports
- Agent run audit logs

The project should not simply add a chatbot. The goal is to build an AI workflow system that can retrieve data, use tools, plan compliance checks, generate findings, cite supporting evidence, and request human approval before sensitive updates.
