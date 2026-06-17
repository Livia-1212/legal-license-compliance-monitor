-- Module 3: Attorney Compliance Summary
-- Purpose: Summarize attorney license and CLE compliance status for follow-up review.

SELECT
    a.attorney_id,
    a.name,
    a.email,
    a.date_of_birth,
    a.title,
    a.office,
    a.practice_area,
    l.jurisdiction,
    l.admission_date,
    l.admission_year,
    l.license_status,
    l.registration_expiry,
    c.required_hours,
    c.completed_hours,
    (c.required_hours - c.completed_hours) AS missing_cle_hours,

    CASE
        WHEN l.license_status = 'Active' THEN 'Clear'
        ELSE 'Review Required'
    END AS license_status_flag,

    CASE
        WHEN c.completed_hours >= c.required_hours THEN 'Clear'
        ELSE 'Review Required'
    END AS cle_status_flag,

    CASE
        WHEN l.license_status = 'Suspended' THEN 'Non-Compliant'
        WHEN l.license_status = 'Expired' THEN 'Needs Attention'
        WHEN c.completed_hours < c.required_hours THEN 'Needs Attention'
        ELSE 'Compliant'
    END AS overall_compliance_status,

    CASE
        WHEN l.license_status = 'Suspended' THEN 'Immediate Review'
        WHEN l.license_status = 'Expired' THEN 'Priority Follow-Up'
        WHEN c.completed_hours < c.required_hours THEN 'Standard Follow-Up'
        ELSE 'No Follow-Up Needed'
    END AS compliance_priority

FROM attorneys a
JOIN licenses l
    ON a.attorney_id = l.attorney_id
JOIN cle_records c
    ON a.attorney_id = c.attorney_id
    AND l.jurisdiction = c.jurisdiction
ORDER BY
    CASE
        WHEN l.license_status = 'Suspended' THEN 1
        WHEN l.license_status = 'Expired' THEN 2
        WHEN c.completed_hours < c.required_hours THEN 3
        ELSE 4
    END,
    a.name;