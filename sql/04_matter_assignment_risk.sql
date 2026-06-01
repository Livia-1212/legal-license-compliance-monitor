-- Module 2: Matter Assignment Risk Detection
-- Purpose: Identify attorneys assigned to matters in jurisdictions where they do not hold an active license.

SELECT
    m.matter_id,
    m.matter_name,
    m.client,
    m.revenue,
    m.jurisdiction AS matter_jurisdiction,

    a.attorney_id,
    a.name,
    a.email,
    a.title,

    l.jurisdiction AS licensed_jurisdiction,
    l.license_status,

    CASE
        WHEN l.jurisdiction IS NULL THEN 'No License Found'
        WHEN l.license_status <> 'Active' THEN 'Inactive License'
        WHEN l.jurisdiction <> m.jurisdiction THEN 'Jurisdiction Mismatch'
        ELSE 'Compliant'
    END AS assignment_risk

FROM matter_assignments ma

JOIN matters m
    ON ma.matter_id = m.matter_id

JOIN attorneys a
    ON ma.attorney_id = a.attorney_id

LEFT JOIN licenses l
    ON a.attorney_id = l.attorney_id
    AND l.jurisdiction = m.jurisdiction

WHERE
    l.attorney_id IS NULL
    OR l.license_status <> 'Active';