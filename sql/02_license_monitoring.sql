-- Module 1: Attorney License Monitoring
-- Purpose: Identify attorneys with inactive, expired, or suspended bar licenses.

SELECT
    a.attorney_id,
    a.name,
    a.email,
    a.title,
    a.office,
    a.practice_area,
    l.jurisdiction,
    l.license_status,
    l.registration_expiry,
    CASE
        WHEN l.license_status = 'Active' THEN 'Compliant'
        WHEN l.license_status = 'Expired' THEN 'Registration Issue'
        WHEN l.license_status = 'Suspended' THEN 'License Status Issue'
        ELSE 'Review Required'
    END AS license_compliance_issue
FROM attorneys a
JOIN licenses l
    ON a.attorney_id = l.attorney_id
WHERE l.license_status <> 'Active'
ORDER BY
    CASE
        WHEN l.license_status = 'Suspended' THEN 1
        WHEN l.license_status = 'Expired' THEN 2
        ELSE 3
    END,
    a.name;
