-- Module 5: Executive Dashboard Summary
-- Purpose: Provide firm-level compliance metrics for legal, compliance, and management stakeholders.

WITH inactive_license_summary AS (
    SELECT
        COUNT(*) AS inactive_license_count,
        SUM(CASE WHEN license_status = 'Suspended' THEN 1 ELSE 0 END) AS suspended_license_count,
        SUM(CASE WHEN license_status = 'Expired' THEN 1 ELSE 0 END) AS expired_registration_count
    FROM licenses
    WHERE license_status <> 'Active'
),

cle_summary AS (
    SELECT
        COUNT(DISTINCT attorney_id) AS cle_deficient_attorney_count,
        SUM(required_hours - completed_hours) AS total_missing_cle_hours
    FROM cle_records
    WHERE completed_hours < required_hours
),

matter_risk_summary AS (
    SELECT
        COUNT(DISTINCT ma.matter_id) AS affected_matter_count,
        COUNT(DISTINCT ma.attorney_id) AS affected_attorney_count,
        SUM(m.revenue) AS total_revenue_exposure
    FROM matter_assignments ma
    JOIN matters m
        ON ma.matter_id = m.matter_id
    LEFT JOIN licenses l
        ON ma.attorney_id = l.attorney_id
        AND m.jurisdiction = l.jurisdiction
        AND l.license_status = 'Active'
    WHERE l.attorney_id IS NULL
),

attorney_summary AS (
    SELECT
        COUNT(*) AS total_active_attorneys
    FROM attorneys
    WHERE employment_status = 'Active'
)

SELECT
    a.total_active_attorneys,

    i.inactive_license_count,
    i.suspended_license_count,
    i.expired_registration_count,

    c.cle_deficient_attorney_count,
    c.total_missing_cle_hours,

    m.affected_attorney_count AS attorneys_with_matter_assignment_issues,
    m.affected_matter_count AS matters_with_jurisdiction_issues,
    m.total_revenue_exposure,

    CASE
        WHEN i.suspended_license_count > 0
            OR m.affected_matter_count > 0
            THEN 'Immediate Review Required'
        WHEN i.expired_registration_count > 0
            OR c.cle_deficient_attorney_count > 0
            THEN 'Follow-Up Required'
        ELSE 'No Material Findings'
    END AS executive_assessment

FROM attorney_summary a
CROSS JOIN inactive_license_summary i
CROSS JOIN cle_summary c
CROSS JOIN matter_risk_summary m;
