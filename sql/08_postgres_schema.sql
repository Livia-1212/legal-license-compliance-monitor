DROP TABLE IF EXISTS matter_assignments CASCADE;
DROP TABLE IF EXISTS cle_records CASCADE;
DROP TABLE IF EXISTS licenses CASCADE;
DROP TABLE IF EXISTS matters CASCADE;
DROP TABLE IF EXISTS attorneys CASCADE;
DROP TABLE IF EXISTS jurisdiction_rules CASCADE;

CREATE TABLE jurisdiction_rules (
    jurisdiction VARCHAR(10) PRIMARY KEY,
    cle_required_hours INTEGER NOT NULL,
    registration_cycle VARCHAR(50)
);

CREATE TABLE attorneys (
    attorney_id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    date_of_birth DATE,
    title VARCHAR(100),
    office VARCHAR(100),
    practice_area VARCHAR(100),
    employment_status VARCHAR(50)
);

CREATE TABLE licenses (
    license_id SERIAL PRIMARY KEY,
    attorney_id INTEGER NOT NULL REFERENCES attorneys(attorney_id),
    jurisdiction VARCHAR(10) NOT NULL REFERENCES jurisdiction_rules(jurisdiction),
    admission_date DATE,
    admission_year INTEGER,
    license_status VARCHAR(50),
    registration_expiry DATE
);

CREATE TABLE cle_records (
    cle_record_id SERIAL PRIMARY KEY,
    attorney_id INTEGER NOT NULL REFERENCES attorneys(attorney_id),
    jurisdiction VARCHAR(10) NOT NULL REFERENCES jurisdiction_rules(jurisdiction),
    required_hours NUMERIC(5, 2),
    completed_hours NUMERIC(5, 2),
    deadline DATE
);

CREATE TABLE matters (
    matter_id VARCHAR(20) PRIMARY KEY,
    matter_name VARCHAR(255) NOT NULL,
    jurisdiction VARCHAR(10) REFERENCES jurisdiction_rules(jurisdiction),
    client VARCHAR(255),
    revenue NUMERIC(12, 2),
    matter_type VARCHAR(100),
    status VARCHAR(50)
);

CREATE TABLE matter_assignments (
    assignment_id SERIAL PRIMARY KEY,
    matter_id VARCHAR(20) NOT NULL REFERENCES matters(matter_id),
    attorney_id INTEGER NOT NULL REFERENCES attorneys(attorney_id),
    role VARCHAR(100),
    assignment_date DATE
);
