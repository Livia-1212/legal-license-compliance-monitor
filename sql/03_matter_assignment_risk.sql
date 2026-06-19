-- Module 3: Matter Assignment Risk Detection
-- Purpose: Identify matters assigned to attorneys who do not hold an active license in the matter jurisdiction.

SELECT
    m.matter_id,
    m.matter_name,
    m.client,
    m.revenue,
    m.jurisdiction AS matter_jurisdiction,
    ma.role,

    a.attorney_id,
    a.name,
    a.email,
    a.title,
    a.office,
    a.practice_group,

    l.jurisdiction AS licensed_jurisdiction,
    l.license_status,

    CASE
        WHEN l.attorney_id IS NULL THEN 'No Active License in Matter Jurisdiction'
        WHEN l.license_status <> 'Active' THEN 'Inactive License in Matter Jurisdiction'
        ELSE 'Compliant'
    END AS assignment_risk_category,

    CASE
        WHEN l.attorney_id IS NULL THEN 100
        WHEN l.license_status = 'Suspended' THEN 100
        WHEN l.license_status = 'Expired' THEN 75
        ELSE 0
    END AS assignment_risk_score

FROM matter_assignments ma
JOIN matters m
    ON ma.matter_id = m.matter_id
JOIN attorneys a
    ON ma.attorney_id = a.attorney_id
LEFT JOIN licenses l
    ON a.attorney_id = l.attorney_id
    AND l.jurisdiction = m.jurisdiction
    AND l.license_status = 'Active'

WHERE l.attorney_id IS NULL

ORDER BY
    assignment_risk_score DESC,
    m.revenue DESC;
