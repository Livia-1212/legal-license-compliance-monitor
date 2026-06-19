# Entity Relationship Diagram

## Current CSV-Based Data Model

### attorneys
Primary key: `attorney_id`

### licenses
Foreign keys:
- `attorney_id` → `attorneys.attorney_id`
- `jurisdiction` → `jurisdiction_rules.jurisdiction`

### cle_records
Foreign keys:
- `attorney_id` → `attorneys.attorney_id`
- `jurisdiction` → `jurisdiction_rules.jurisdiction`

### jurisdiction_rules
Primary key: `jurisdiction`

### matters
Primary key: `matter_id`

Current issue: `matters.csv` duplicates `matter_assignments.csv`. It should be redesigned to store matter-level information only.

### matter_assignments
Foreign keys:
- `matter_id` → `matters.matter_id`
- `attorney_id` → `attorneys.attorney_id`

## Relationships

- One attorney can hold many licenses.
- One attorney can have many CLE records.
- One jurisdiction rule can apply to many licenses.
- One jurisdiction rule can apply to many CLE records.
- One matter can have many attorney assignments.
- One attorney can be assigned to many matters.