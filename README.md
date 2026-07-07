# Legal License Compliance Monitor

A legal compliance analytics platform for monitoring attorney license status, CLE completion, matter assignment eligibility, and revenue exposure across multiple jurisdictions.

This project combines legal-domain knowledge with SQL, Python analytics, PostgreSQL persistence, Streamlit dashboarding, authentication workflow foundations, and automated testing.

---

## Overview

Law firms and legal departments need reliable ways to track whether attorneys remain properly licensed, satisfy CLE requirements, and are eligible to work on client matters in specific jurisdictions.

This project simulates that workflow using synthetic legal operations data. It identifies compliance deficiencies, generates management-level metrics, and provides a foundation for a PostgreSQL-backed compliance operations platform.

The project currently supports two data source modes:

- `csv` mode for lightweight local development and testing
- `postgres` mode for database-backed persistence using PostgreSQL

---

## Current Features

- Attorney, license, CLE, matter, and matter assignment datasets
- SQL-based compliance checks
- Python analytics layer using pandas
- PostgreSQL schema and repository layer
- CSV-to-PostgreSQL seed/import workflow
- Configurable data source switch using `.env`
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
| `sql/01_create_tables.sql` | Creates base SQL tables for the initial SQL prototype |
| `sql/02_license_monitoring.sql` | License compliance monitoring |
| `sql/03_cle_compliance_checks.sql` | CLE validation checks |
| `sql/04_attorney_compliance_summary.sql` | Attorney-level compliance summary |
| `sql/05_data_quality_checks.sql` | Data quality and integrity validation |
| `sql/06_management_dashboard.sql` | Executive dashboard metrics |
| `sql/07_risk_metrics.sql` | Scoring and exposure analysis |
| `sql/08_postgres_schema.sql` | PostgreSQL schema for persistent application data |

---

## Python Modules

| Module | Purpose |
|---|---|
| `src/analysis/load_data.py` | Loads source CSV datasets |
| `src/analysis/matter_license_check.py` | Reviews matter assignment licensing alignment |
| `src/analysis/risk_scoring.py` | Calculates attorney-level compliance scoring |
| `src/dashboard/dashboard_summary.py` | Generates executive dashboard metrics |
| `src/assistant/compliance_assistant.py` | Provides command-line compliance assistant prototype |
| `src/db/connection.py` | Creates PostgreSQL database connections |
| `src/db/data_import.py` | Seeds PostgreSQL tables from CSV source files |
| `src/db/repositories.py` | Loads PostgreSQL tables into pandas DataFrames |
| `src/db/data_source.py` | Switches between CSV and PostgreSQL data sources |

---

## Project Structure

```text
legal-license-compliance-monitor/
├── assets/
├── data/
│   └── raw/
├── docs/
├── scripts/
│   └── seed_postgres_from_csv.py
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_license_monitoring.sql
│   ├── 03_cle_compliance_checks.sql
│   ├── 04_attorney_compliance_summary.sql
│   ├── 05_data_quality_checks.sql
│   ├── 06_management_dashboard.sql
│   ├── 07_risk_metrics.sql
│   └── 08_postgres_schema.sql
├── src/
│   ├── analysis/
│   ├── assistant/
│   ├── auth/
│   ├── dashboard/
│   └── db/
├── tests/
├── streamlit_app.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## Data Source Modes

The application supports two data source modes.

| Mode | Description |
|---|---|
| `csv` | Loads data directly from `data/raw/*.csv` |
| `postgres` | Loads data from a local PostgreSQL database |

The selected mode is controlled by the `DATA_SOURCE` environment variable.

Example:

```env
DATA_SOURCE=csv
```

or:

```env
DATA_SOURCE=postgres
```

The default mode is `csv`.

---

## Run the Project Locally

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
python -m pytest
```

Run the Streamlit dashboard:

```bash
streamlit run streamlit_app.py
```

---

## Run in CSV Mode

CSV mode is the simplest local development option.

Create a local environment file:

```bash
cp .env.example .env
```

Set:

```env
DATA_SOURCE=csv
```

Then run:

```bash
streamlit run streamlit_app.py
```

---

## PostgreSQL Local Setup with Docker

This project also supports PostgreSQL as the application data layer.

### 1. Start PostgreSQL with Docker

```bash
docker run --name legal-license-postgres \
  -e POSTGRES_DB=legal_license_compliance \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -d postgres:16
```

If the container already exists but is stopped, start it with:

```bash
docker start legal-license-postgres
```

Check that it is running:

```bash
docker ps
```

---

### 2. Configure Local Environment

Copy the example environment file:

```bash
cp .env.example .env
```

For Docker PostgreSQL, use:

```env
DATA_SOURCE=postgres

POSTGRES_DB=legal_license_compliance
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

The `.env` file should stay local and should not be committed.

---

### 3. Apply PostgreSQL Schema

Create the PostgreSQL tables:

```bash
docker exec -i legal-license-postgres psql -U postgres -d legal_license_compliance < sql/08_postgres_schema.sql
```

---

### 4. Seed PostgreSQL from CSV Files

Import the source CSV files into PostgreSQL:

```bash
PYTHONPATH=. python scripts/seed_postgres_from_csv.py
```

Expected output:

```text
PostgreSQL database seeded successfully from CSV files.
```

---

### 5. Verify PostgreSQL Reads

Run:

```bash
PYTHONPATH=. python - <<'PY'
from src.db.repositories import load_all_data_from_db

data = load_all_data_from_db()

for name, df in data.items():
    print(name, df.shape)
PY
```

Expected output:

```text
attorneys (8, 8)
licenses (9, 7)
cle_records (8, 6)
jurisdiction_rules (6, 3)
matters (8, 7)
matter_assignments (8, 5)
```

---

### 6. Run Streamlit in PostgreSQL Mode

Make sure `.env` contains:

```env
DATA_SOURCE=postgres
```

Then run:

```bash
streamlit run streamlit_app.py
```

The dashboard will load application data from PostgreSQL.

---

## Common PostgreSQL Commands

Start the PostgreSQL container:

```bash
docker start legal-license-postgres
```

Stop the PostgreSQL container:

```bash
docker stop legal-license-postgres
```

Open a PostgreSQL shell inside Docker:

```bash
docker exec -it legal-license-postgres psql -U postgres -d legal_license_compliance
```

List tables inside the PostgreSQL shell:

```sql
\dt
```

Exit the PostgreSQL shell:

```sql
\q
```

Re-apply schema:

```bash
docker exec -i legal-license-postgres psql -U postgres -d legal_license_compliance < sql/08_postgres_schema.sql
```

Re-seed database:

```bash
PYTHONPATH=. python scripts/seed_postgres_from_csv.py
```

---

## Testing

Run all tests:

```bash
python -m pytest
```

The test suite currently covers:

- Analytics calculations
- Authentication helper logic
- Configurable data source behavior

The data source tests are designed so that CI can run without requiring a live PostgreSQL database.

---

## Development Workflow

Recommended workflow:

```bash
git checkout -b feature/your-feature-name
python -m pytest
git status
git add .
git commit -m "Describe your change"
git push
```

Before opening a pull request or merging:

```bash
python -m pytest
git status
```

Expected result:

```text
working tree clean
```

---

## Technology Stack

| Area | Tools |
|---|---|
| Language | Python |
| Data analysis | pandas |
| Database | PostgreSQL |
| Local database runtime | Docker |
| Dashboard | Streamlit |
| Testing | pytest |
| CI | GitHub Actions |
| Configuration | python-dotenv |
| SQL execution | psycopg2 |

---

## Project Roadmap

Completed foundations:

- Synthetic legal compliance datasets
- SQL compliance checks
- Python analytics layer
- Streamlit dashboard
- Authentication workflow foundation
- PostgreSQL schema
- CSV-to-PostgreSQL import workflow
- Repository layer
- Configurable CSV/PostgreSQL data source switch
- Automated tests

Potential next phases:

- Admin CRUD forms connected to PostgreSQL
- Editable attorney, license, CLE, matter, and assignment records
- SQLAlchemy-based database access layer
- Expanded role-based permissions
- Audit trail for data changes
- Production deployment planning
- AI assistant connected to PostgreSQL-backed compliance data

---

## Notes

This project uses synthetic data for demonstration and portfolio purposes. It is not intended to provide legal advice or determine actual attorney eligibility.