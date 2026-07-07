# Product Plan

## Legal License Compliance Monitor

The Legal License Compliance Monitor is a legal operations and compliance analytics platform designed to help law firms and legal departments monitor attorney licensing status, CLE compliance, matter assignment eligibility, and revenue exposure across multiple jurisdictions.

This project demonstrates how legal-domain knowledge can be translated into a structured data product using SQL, Python, Streamlit, testing, and a planned PostgreSQL persistence layer.

---

## Product Objective

The goal of this project is to move beyond static compliance tracking and create an operational platform that can:

- Centralize attorney, license, CLE, matter, and assignment data
- Identify license and CLE compliance deficiencies
- Review whether attorneys are properly licensed for assigned matters
- Quantify revenue exposure associated with compliance issues
- Provide executive-level compliance metrics
- Support future administrative data entry, audit logging, and AI-assisted compliance workflows

---

## Business Problem

Law firms and legal departments must ensure that attorneys remain properly licensed and compliant with jurisdiction-specific CLE requirements. Manual tracking through spreadsheets can create operational gaps, especially when attorneys work across multiple offices, jurisdictions, practice areas, and client matters.

Common compliance concerns include:

- Expired or suspended attorney licenses
- Incomplete CLE requirements
- Attorneys assigned to matters in jurisdictions where they lack an active license
- Lack of centralized visibility into compliance status
- Difficulty connecting compliance deficiencies to business exposure
- Limited auditability of compliance review decisions

---

## Target Users

| User Group | Need |
|---|---|
| Legal Operations | Monitor attorney and matter-level compliance status |
| Compliance Team | Identify license, CLE, and assignment deficiencies |
| Firm Management | Review executive metrics and revenue exposure |
| Practice Group Leaders | Understand attorney eligibility by jurisdiction |
| Admin Users | Maintain attorney, license, CLE, and matter records |

---

## Current Product Scope

The current version includes:

- Synthetic CSV-based datasets
- SQL compliance checks
- Python analytics layer
- Streamlit dashboard
- Executive Summary view
- Attorney Directory
- Matters Directory
- CLE Compliance view
- Compliance assistant prototype
- Sign In / Register workflow foundation
- Role-based permission foundation
- Pytest test coverage
- GitHub Actions CI workflow

The current runtime data source remains CSV-based. CSV files will become seed/import data after the PostgreSQL persistence layer is implemented.

---

## Key Features

### Executive Summary

Provides management-level metrics, including:

- Total attorneys
- Expired licenses
- CLE deficient records
- Total revenue exposure

### Attorney Directory

Displays attorney demographic, employment, license, and compliance-related information in a searchable dashboard view.

### Matters Directory

Reviews matter assignments against attorney licensing data to identify matters that may require compliance review.

### CLE Compliance

Tracks required CLE hours, completed CLE hours, deadlines, and deficiency status.

### Compliance Analytics

Uses SQL and Python logic to generate attorney-level compliance metrics, assignment review outputs, and revenue exposure indicators.

### Authentication Foundation

Supports a basic Sign In / Register workflow with planned PostgreSQL-backed users and role-based access controls.

---

## Product Direction

The product is evolving from a CSV-backed analytics dashboard into a PostgreSQL-backed legal compliance operations platform.

Near-term product direction:

- PostgreSQL persistence layer
- Database-backed authentication
- Role-based page access
- Admin data entry and editing workflows
- Audit logging
- CSV upload/import and export
- Improved compliance review workflow

Long-term product direction:

- BigQuery analytics warehouse
- PDF and OCR document intake
- CLE certificate extraction
- Attorney registration document parsing
- Human review queue
- Agentic AI compliance workflow
- Evidence-backed compliance findings

---

## Design Principles

This project follows several product design principles:

- Treat compliance findings as review items, not automatic legal conclusions
- Preserve human review for sensitive legal or compliance decisions
- Use clear legal operations terminology
- Avoid unnecessary “risk” labels where “deficiency,” “review,” or “exposure” is more precise
- Separate operational application workflows from optional BI dashboards
- Maintain auditability for future data changes and AI-assisted outputs

---

## Out of Scope for Current Version

The current version does not provide legal advice or make binding compliance determinations.

The following items are planned for later phases but are not part of the current runtime system:

- Production authentication security
- Live regulator integrations
- Automated attorney disciplinary record checks
- Real-time alerts
- Full document automation
- AI agent execution
- Production cloud deployment
