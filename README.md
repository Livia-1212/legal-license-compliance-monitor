# Legal License Compliance Monitor

A legal compliance analytics platform for monitoring attorney license status, CLE completion, matter assignment eligibility, and revenue exposure across multiple jurisdictions.

This project combines legal-domain knowledge with SQL, Python analytics, Streamlit, testing, and a planned PostgreSQL persistence layer.

---

## Overview

Law firms and legal departments need reliable ways to track whether attorneys remain properly licensed, satisfy CLE requirements, and are eligible to work on client matters in specific jurisdictions.

This project simulates that workflow using synthetic legal operations data. It identifies compliance deficiencies, generates management-level metrics, and provides a foundation for a future PostgreSQL-backed compliance operations platform.

---

## Current Features

- Attorney, license, CLE, matter, and matter assignment datasets
- SQL-based compliance checks
- Python analytics layer using pandas
- Streamlit dashboard
- Executive Summary view
- Attorney Directory
- Matters Directory
- CLE Compliance view
- Compliance assistant prototype
- Sign In / Register workflow foundation
- Role-based permission foundation
- Automated tests with pytest
- GitHub Actions CI workflow

---

## Dashboard Views

| View | Purpose |
|---|---|
| Executive Summary | Displays key management metrics |
| Attorney Directory | Reviews attorney profile and compliance-related data |
| Matters Directory | Reviews matter assignments and jurisdiction eligibility |
| CLE Compliance | Tracks required and completed CLE hours |
| Sign In / Register | Provides authentication workflow foundation |

---

## Data Model

Core datasets:

| Dataset | Description |
|---|---|
| `attorneys.csv` | Attorney demographic and employment information |
| `licenses.csv` | Attorney licensing and registration records |
| `cle_records.csv` | CLE completion and compliance data |
| `jurisdiction_rules.csv` | Jurisdiction-specific compliance requirements |
| `matters.csv` | Matter-level business information |
| `matter_assignments.csv` | Attorney assignments to matters |

Additional documentation:

- `docs/product_plan.md`
- `docs/roadmap.md`
- `docs/architecture.md`
- `docs/data_dictionary.md`
- `docs/ERD.md`

---

## Compliance Checks

The current analytics layer reviews:

- Expired licenses
- Suspended licenses
- CLE deficient records
- Attorneys assigned to matters without an active license in the matter jurisdiction
- Revenue exposure connected to compliance review items
- Data quality issues across source datasets

---

## SQL Modules

| File | Purpose |
|---|---|
| `sql/01_create_tables.sql` | Creates base SQL tables |
| `sql/02_license_monitoring.sql` | License compliance monitoring |
| `sql/03_cle_compliance_checks.sql` | CLE validation checks |
| `sql/04_attorney_compliance_summary.sql` | Attorney-level compliance summary |
| `sql/05_data_quality_checks.sql` | Data quality and integrity validation |
| `sql/06_management_dashboard.sql` | Executive dashboard metrics |
| `sql/07_risk_metrics.sql` | Scoring and exposure analysis |
| `sql/08_postgres_schema.sql` | Planned PostgreSQL schema |

---

## Python Modules

| Module | Purpose |
|---|---|
| `src/analysis/load_data.py` | Loads source datasets |
| `src/analysis/matter_license_check.py` | Reviews matter assignment licensing alignment |
| `src/analysis/risk_scoring.py` | Calculates attorney-level compliance scoring |
| `src/dashboard/dashboard_summary.py` | Generates executive dashboard metrics |
| `src/assistant/compliance_assistant.py` | Provides command-line compliance assistant prototype |

---

## Run the Project Locally

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Legal License Compliance Monitor

A legal compliance analytics platform for monitoring attorney license status, CLE completion, matter assignment eligibility, and revenue exposure across multiple jurisdictions.

This project combines legal-domain knowledge with SQL, Python analytics, Streamlit, testing, and a planned PostgreSQL persistence layer.

---

## Overview

Law firms and legal departments need reliable ways to track whether attorneys remain properly licensed, satisfy CLE requirements, and are eligible to work on client matters in specific jurisdictions.

This project simulates that workflow using synthetic legal operations data. It identifies compliance deficiencies, generates management-level metrics, and provides a foundation for a future PostgreSQL-backed compliance operations platform.

---

## Current Features

- Attorney, license, CLE, matter, and matter assignment datasets
- SQL-based compliance checks
- Python analytics layer using pandas
- Streamlit dashboard
- Executive Summary view
- Attorney Directory
- Matters Directory
- CLE Compliance view
- Compliance assistant prototype
- Sign In / Register workflow foundation
- Role-based permission foundation
- Automated tests with pytest
- GitHub Actions CI workflow

---

## Dashboard Views

| View | Purpose |
|---|---|
| Executive Summary | Displays key management metrics |
| Attorney Directory | Reviews attorney profile and compliance-related data |
| Matters Directory | Reviews matter assignments and jurisdiction eligibility |
| CLE Compliance | Tracks required and completed CLE hours |
| Sign In / Register | Provides authentication workflow foundation |

---

## Data Model

Core datasets:

| Dataset | Description |
|---|---|
| `attorneys.csv` | Attorney demographic and employment information |
| `licenses.csv` | Attorney licensing and registration records |
| `cle_records.csv` | CLE completion and compliance data |
| `jurisdiction_rules.csv` | Jurisdiction-specific compliance requirements |
| `matters.csv` | Matter-level business information |
| `matter_assignments.csv` | Attorney assignments to matters |

Additional documentation:

- `docs/product_plan.md`
- `docs/roadmap.md`
- `docs/architecture.md`
- `docs/data_dictionary.md`
- `docs/ERD.md`

---

## Compliance Checks

The current analytics layer reviews:

- Expired licenses
- Suspended licenses
- CLE deficient records
- Attorneys assigned to matters without an active license in the matter jurisdiction
- Revenue exposure connected to compliance review items
- Data quality issues across source datasets

---

## SQL Modules

| File | Purpose |
|---|---|
| `sql/01_create_tables.sql` | Creates base SQL tables |
| `sql/02_license_monitoring.sql` | License compliance monitoring |
| `sql/03_cle_compliance_checks.sql` | CLE validation checks |
| `sql/04_attorney_compliance_summary.sql` | Attorney-level compliance summary |
| `sql/05_data_quality_checks.sql` | Data quality and integrity validation |
| `sql/06_management_dashboard.sql` | Executive dashboard metrics |
| `sql/07_risk_metrics.sql` | Scoring and exposure analysis |
| `sql/08_postgres_schema.sql` | Planned PostgreSQL schema |

---

## Python Modules

| Module | Purpose |
|---|---|
| `src/analysis/load_data.py` | Loads source datasets |
| `src/analysis/matter_license_check.py` | Reviews matter assignment licensing alignment |
| `src/analysis/risk_scoring.py` | Calculates attorney-level compliance scoring |
| `src/dashboard/dashboard_summary.py` | Generates executive dashboard metrics |
| `src/assistant/compliance_assistant.py` | Provides command-line compliance assistant prototype |

---

## Run the Project Locally

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate