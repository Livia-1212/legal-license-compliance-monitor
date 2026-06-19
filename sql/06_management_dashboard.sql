-- 06_management_dashboard.sql
-- Purpose: Generate management-level compliance dashboard metrics.

-- 1. Attorney population overview
SELECT
    COUNT(*) AS total_attorneys,
    COUNT(CASE WHEN employment_status = 'Active' THEN 1 END) AS active_attorneys
FROM attorneys;

-- 2. License status summary
SELECT
    license_status,
    COUNT(*) AS license_count
FROM licenses
GROUP BY license_status
ORDER BY license_count DESC;

-- 3. CLE compliance summary
SELECT
    CASE
        WHEN completed_hours >= required_hours THEN 'Compliant'
        ELSE 'Deficient'
    END AS cle_status,
    COUNT(*) AS attorney_count
FROM cle_records
GROUP BY cle_status
ORDER BY attorney_count DESC;

-- 4. License expiration risk summary
SELECT
    CASE
        WHEN registration_expiry < CURRENT_DATE THEN 'Expired'
        WHEN registration_expiry <= CURRENT_DATE + INTERVAL '90 days' THEN 'Expiring Within 90 Days'
        ELSE 'Current'
    END AS registration_risk_status,
    COUNT(*) AS license_count
FROM licenses
GROUP BY registration_risk_status
ORDER BY license_count DESC;

-- 5. Matter exposure by jurisdiction
SELECT
    jurisdiction,
    COUNT(*) AS matter_count,
    SUM(revenue) AS total_revenue_exposure
FROM matters
GROUP BY jurisdiction
ORDER BY total_revenue_exposure DESC;

-- 6. Matter exposure by matter type
SELECT
    matter_type,
    COUNT(*) AS matter_count,
    SUM(revenue) AS total_revenue_exposure
FROM matters
GROUP BY matter_type
ORDER BY total_revenue_exposure DESC;

-- 7. Attorney matter assignment summary
SELECT
    a.attorney_id,
    a.name,
    a.title,
    a.office,
    COUNT(ma.matter_id) AS assigned_matter_count,
    COALESCE(SUM(m.revenue), 0) AS assigned_revenue_exposure
FROM attorneys a
LEFT JOIN matter_assignments ma
    ON a.attorney_id = ma.attorney_id
LEFT JOIN matters m
    ON ma.matter_id = m.matter_id
GROUP BY
    a.attorney_id,
    a.name,
    a.title,
    a.office
ORDER BY assigned_revenue_exposure DESC;

-- 8. High-level compliance dashboard
SELECT
    (SELECT COUNT(*) FROM attorneys) AS total_attorneys,

    (SELECT COUNT(*)
     FROM licenses
     WHERE license_status = 'Active') AS active_licenses,

    (SELECT COUNT(*)
     FROM licenses
     WHERE license_status = 'Expired') AS expired_licenses,

    (SELECT COUNT(*)
     FROM licenses
     WHERE license_status = 'Suspended') AS suspended_licenses,

    (SELECT COUNT(*)
     FROM cle_records
     WHERE completed_hours >= required_hours) AS cle_compliant_records,

    (SELECT COUNT(*)
     FROM cle_records
     WHERE completed_hours < required_hours) AS cle_deficient_records,

    (SELECT COUNT(DISTINCT attorney_id)
     FROM matter_assignments) AS attorneys_assigned_to_matters,

    (SELECT SUM(revenue)
     FROM matters) AS total_matter_revenue_exposure;
     