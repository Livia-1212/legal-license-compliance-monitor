````markdown
# Legal License Compliance Monitor

## Overview

The Legal License Compliance Monitor is a compliance analytics platform designed to monitor attorney licensing status, Continuing Legal Education (CLE) compliance, and matter assignment risk across multiple jurisdictions.

The project simulates a legal operations and regulatory compliance environment where attorneys must maintain active licenses and satisfy CLE requirements before being assigned to client matters. The system identifies compliance deficiencies, quantifies business risk exposure, and generates management-level reporting through SQL and Python analytics.

---

## Business Problem

Law firms and legal departments face regulatory, operational, and reputational risks when attorneys:

- Practice with expired or suspended licenses
- Fail to complete mandatory CLE requirements
- Work on matters in jurisdictions where they are not licensed
- Generate revenue exposure while non-compliant

This project provides a framework for detecting these risks and supporting compliance oversight.

---

## Project Architecture

```text
Raw Data (CSV)
        ↓
Data Quality Validation
        ↓
Compliance Monitoring
        ↓
Risk Scoring Engine
        ↓
Management Dashboard Metrics
        ↓
Compliance Assistant
````

---

## Data Model

Core datasets:

| Dataset                | Description                                     |
| ---------------------- | ----------------------------------------------- |
| attorneys.csv          | Attorney demographic and employment information |
| licenses.csv           | Attorney licensing and registration records     |
| cle_records.csv        | CLE completion and compliance data              |
| jurisdiction_rules.csv | Jurisdiction-specific regulatory requirements   |
| matters.csv            | Matter-level business information               |
| matter_assignments.csv | Attorney assignments to matters                 |

Documentation:

* docs/ERD.md
* docs/architecture.md
* docs/data_dictionary.md

---

## Compliance Controls

### License Monitoring

Detects:

* Expired licenses
* Suspended licenses
* Registration expiration risk

### CLE Compliance

Detects:

* CLE deficiencies
* Incomplete CLE requirements
* Jurisdiction-specific compliance gaps

### Matter Assignment Risk

Detects:

* Attorneys assigned to matters while unlicensed in the matter jurisdiction
* Attorneys assigned while holding expired or suspended licenses

---

## SQL Analytics Modules

| File                               | Purpose                               |
| ---------------------------------- | ------------------------------------- |
| 02_license_monitoring.sql          | License compliance monitoring         |
| 03_cle_compliance_checks.sql       | CLE validation checks                 |
| 04_attorney_compliance_summary.sql | Attorney-level compliance summary     |
| 05_data_quality_checks.sql         | Data quality and integrity validation |
| 06_management_dashboard.sql        | Executive dashboard metrics           |
| 07_risk_metrics.sql                | Risk scoring and exposure analysis    |

---

## Python Analytics Layer

### Data Loading

```bash
python src/analysis/load_data.py
```

Loads all source datasets into pandas DataFrames.

### Matter License Validation

```bash
python src/analysis/matter_license_check.py
```

Identifies attorneys assigned to matters without appropriate jurisdictional licensing.

### Risk Scoring

```bash
python src/analysis/risk_scoring.py
```

Calculates attorney-level compliance risk scores and risk tiers.

### Executive Dashboard

```bash
python src/dashboard/dashboard_summary.py
```

Generates management-level compliance metrics.

### Compliance Assistant

```bash
python src/assistant/compliance_assistant.py
```

Interactive command-line assistant for compliance reporting.

---

## Sample Risk Scoring Methodology

Risk factors include:

| Risk Factor                 | Score |
| --------------------------- | ----- |
| Suspended License           | 50    |
| Expired License             | 40    |
| CLE Deficiency              | 25    |
| Revenue Exposure > $200,000 | 20    |
| Revenue Exposure > $100,000 | 10    |

Risk tiers:

| Tier        | Score Range |
| ----------- | ----------- |
| High Risk   | 70+         |
| Medium Risk | 40–69       |
| Low Risk    | Below 40    |

---

## Testing & CI/CD

Automated testing is implemented using:

* pytest
* GitHub Actions

Current test coverage validates:

* Data loading
* Risk scoring
* Dashboard generation
* Matter license risk detection

GitHub Actions automatically executes tests on every push and pull request.

---

## Repository Structure

```text
legal-license-compliance-monitor
│
├── data/
│   └── raw/
│       ├── attorneys.csv
│       ├── licenses.csv
│       ├── cle_records.csv
│       ├── jurisdiction_rules.csv
│       ├── matters.csv
│       └── matter_assignments.csv
│
├── docs/
│   ├── ERD.md
│   ├── architecture.md
│   └── data_dictionary.md
│
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_license_monitoring.sql
│   ├── 03_cle_compliance_checks.sql
│   ├── 04_attorney_compliance_summary.sql
│   ├── 05_data_quality_checks.sql
│   ├── 06_management_dashboard.sql
│   └── 07_risk_metrics.sql
│
├── src/
│   ├── analysis/
│   ├── assistant/
│   └── dashboard/
│
├── tests/
├── requirements.txt
└── .github/workflows/python-ci.yml
```

---

## Technologies Used

* Python
* Pandas
* SQL
* Git
* GitHub Actions
* Pytest

---

## Future Enhancements

### Phase 8

* PostgreSQL migration
* Streamlit dashboard
* Interactive risk visualization
* Automated compliance alerts

### Long-Term Roadmap

* REST API using FastAPI
* Cloud deployment
* Multi-jurisdiction compliance engine
* Real-time compliance monitoring

---

## Author

**Livia Weiyu Lee**

* New York Attorney
* M.S. Computer Science Candidate (NJIT)
* Legal Technology, Compliance Analytics, and Risk Data Enthusiast

## License

This project is provided for educational and portfolio purposes.
```
```
