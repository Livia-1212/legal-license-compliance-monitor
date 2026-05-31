# Data Dictionary

## attorneys.csv

| Column | Description |
|---|---|
| attorney_id | Unique attorney identifier |
| name | Attorney full name |
| title | Attorney role or seniority level |
| office | Primary office location |
| practice_group | Attorney's primary practice group |
| employment_status | Whether the attorney is currently active with the firm |

## licenses.csv

| Column | Description |
|---|---|
| attorney_id | Links license record to attorney |
| jurisdiction | State or jurisdiction of bar admission |
| admission_date | Date of admission |
| license_status | Current license status: Active, Expired, Suspended |
| registration_expiry | Date when attorney registration expires |

## cle_records.csv

| Column | Description |
|---|---|
| attorney_id | Links CLE record to attorney |
| jurisdiction | Jurisdiction where CLE requirement applies |
| required_hours | Required CLE hours |
| completed_hours | Completed CLE hours |
| deadline | CLE completion deadline |

## matters.csv

| Column | Description |
|---|---|
| matter_id | Unique legal matter identifier |
| matter_name | Matter description |
| jurisdiction | Governing or active matter jurisdiction |
| client | Client name |
| revenue | Estimated matter revenue |
| matter_type | Litigation, transaction, regulatory, finance, or commercial |
| status | Matter status |

## matter_assignments.csv

| Column | Description |
|---|---|
| matter_id | Links assignment to matter |
| attorney_id | Links assignment to attorney |
| role | Attorney role on the matter |
| assignment_date | Date attorney was assigned |

## jurisdiction_rules.csv

| Column | Description |
|---|---|
| jurisdiction | State or jurisdiction |
| cle_required_hours | Required CLE hours for that jurisdiction |
| registration_cycle | Registration cycle frequency |
