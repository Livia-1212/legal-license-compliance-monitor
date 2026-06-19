-- 05_data_quality_checks.sql
-- Purpose: Identify data quality issues across attorney, license, CLE, jurisdiction, matter, and assignment datasets.

-- 1. Duplicate attorney IDs
SELECT
    attorney_id,
    COUNT(*) AS record_count
FROM attorneys
GROUP BY attorney_id
HAVING COUNT(*) > 1;

-- 2. Missing attorney IDs in attorneys table
SELECT *
FROM attorneys
WHERE attorney_id IS NULL;

-- 3. Licenses linked to attorneys that do not exist
SELECT l.*
FROM licenses l
LEFT JOIN attorneys a
    ON l.attorney_id = a.attorney_id
WHERE a.attorney_id IS NULL;

-- 4. CLE records linked to attorneys that do not exist
SELECT c.*
FROM cle_records c
LEFT JOIN attorneys a
    ON c.attorney_id = a.attorney_id
WHERE a.attorney_id IS NULL;

-- 5. Matter assignments linked to attorneys that do not exist
SELECT ma.*
FROM matter_assignments ma
LEFT JOIN attorneys a
    ON ma.attorney_id = a.attorney_id
WHERE a.attorney_id IS NULL;

-- 6. Matter assignments linked to matters that do not exist
SELECT ma.*
FROM matter_assignments ma
LEFT JOIN matters m
    ON ma.matter_id = m.matter_id
WHERE m.matter_id IS NULL;

-- 7. Invalid jurisdictions in licenses
SELECT l.*
FROM licenses l
LEFT JOIN jurisdiction_rules jr
    ON l.jurisdiction = jr.jurisdiction
WHERE jr.jurisdiction IS NULL;

-- 8. Invalid jurisdictions in CLE records
SELECT c.*
FROM cle_records c
LEFT JOIN jurisdiction_rules jr
    ON c.jurisdiction = jr.jurisdiction
WHERE jr.jurisdiction IS NULL;

-- 9. Invalid jurisdictions in matters
SELECT m.*
FROM matters m
LEFT JOIN jurisdiction_rules jr
    ON m.jurisdiction = jr.jurisdiction
WHERE jr.jurisdiction IS NULL;

-- 10. Invalid license status values
SELECT *
FROM licenses
WHERE license_status NOT IN ('Active', 'Expired', 'Suspended');

-- 11. CLE completed hours greater than required hours
SELECT *
FROM cle_records
WHERE completed_hours > required_hours;

-- 12. CLE completed hours below zero
SELECT *
FROM cle_records
WHERE completed_hours < 0
   OR required_hours < 0;

-- 13. Missing registration expiry dates
SELECT *
FROM licenses
WHERE registration_expiry IS NULL;

-- 14. Missing CLE deadlines
SELECT *
FROM cle_records
WHERE deadline IS NULL;

-- 15. Duplicate matter IDs
SELECT
    matter_id,
    COUNT(*) AS record_count
FROM matters
GROUP BY matter_id
HAVING COUNT(*) > 1;

-- 16. Duplicate assignment records
SELECT
    matter_id,
    attorney_id,
    role,
    assignment_date,
    COUNT(*) AS record_count
FROM matter_assignments
GROUP BY matter_id, attorney_id, role, assignment_date
HAVING COUNT(*) > 1;