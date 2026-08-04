# Attorney License Compliance Monitor

A legal operations and compliance management platform that centralizes attorney licensing, Continuing Legal Education (CLE), jurisdiction-specific eligibility, and matter assignments into a unified compliance dashboard.

The project demonstrates how legal and regulatory requirements can be translated into structured data models, compliance workflows, and operational controls using Python, PostgreSQL, SQL, and Streamlit.

---

## Why This Project?

Law firms and legal departments often manage attorney licenses, CLE requirements, renewal deadlines, and jurisdiction-specific practice eligibility across spreadsheets, emails, and disconnected internal records.

As organizations grow, these manual processes increase the risk of:

- Missed license renewal deadlines
- Incomplete CLE records
- Incorrect matter assignments
- Inconsistent jurisdiction eligibility checks
- Limited compliance visibility
- Administrative inefficiencies

The Attorney License Compliance Monitor explores how these operational challenges can be addressed through centralized compliance workflows and structured data management.

For a detailed business overview, see:

**➡️ [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)**

---

## Features

### Attorney Management

- Attorney directory
- Attorney profile management
- Multi-jurisdiction license records
- Searchable attorney records

### License & CLE Compliance

- License status tracking
- License expiration monitoring
- CLE requirement tracking
- Compliance status monitoring
- Jurisdiction-specific compliance rules

### Matter Management

- Matter records
- Attorney matter assignments
- Jurisdiction eligibility validation
- Compliance risk identification

### Administration

- Administrative data entry
- Role-based access control
- Interactive Streamlit dashboard
- PostgreSQL-backed persistence

---

## Technology Stack

| Area | Technologies |
|------|--------------|
| Language | Python |
| Database | PostgreSQL |
| Query Language | SQL |
| Data Analysis | pandas |
| Dashboard | Streamlit |
| Testing | Pytest |
| CI/CD | GitHub Actions |
| Local Database | Docker |

---

## Project Documentation

Additional project documentation is organized by topic.

| Document | Description |
|----------|-------------|
| **PROJECT_OVERVIEW.md** | Business problem, intended users, solution, and project value |
| **SYSTEM_ARCHITECTURE.md** *(Coming Soon)* | Application architecture and system design |
| **DATABASE_SCHEMA.md** *(Coming Soon)* | Relational database design and schema documentation |
| **USER_GUIDE.md** *(Coming Soon)* | Application walkthrough and usage guide |
| **CASE_STUDY.md** *(Coming Soon)* | Design decisions, implementation process, and lessons learned |
| **FUTURE_ROADMAP.md** *(Coming Soon)* | Planned enhancements and future development roadmap |

---

## Quick Start

Clone the repository:

```bash
git clone https://github.com/yourusername/legal-license-compliance-monitor.git
cd legal-license-compliance-monitor
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run streamlit_app.py
```

Run automated tests:

```bash
python -m pytest
```

---

## Current Development Status

### Completed

- Attorney management
- License compliance monitoring
- CLE compliance tracking
- Matter assignment management
- Administrative CRUD workflows
- PostgreSQL persistence layer
- Authentication workflow
- Role-based access foundation
- Automated testing with Pytest
- GitHub Actions CI

### In Progress

- User experience improvements
- Search enhancements
- Data validation improvements

### Planned

- Audit logging
- Advanced reporting
- AI-assisted compliance workflows
- External licensing database integration
- Enterprise authentication

---

## Repository Structure

```text
legal-license-compliance-monitor/
├── assets/
├── data/
├── docs/
├── scripts/
├── sql/
├── src/
├── tests/
├── streamlit_app.py
├── requirements.txt
├── README.md
└── PROJECT_OVERVIEW.md
```

---

## License

This project is provided for educational and portfolio purposes.

It uses synthetic data and is intended to demonstrate legal operations, regulatory compliance workflows, relational database design, and software engineering concepts. It is **not** intended to provide legal advice or determine actual attorney licensing eligibility.

---

## Author

**Livia Weiyu Lee**

NY-Admitted Attorney | M.S. Computer Science Candidate

Building technology solutions at the intersection of legal operations, regulatory compliance, data, and technology governance.