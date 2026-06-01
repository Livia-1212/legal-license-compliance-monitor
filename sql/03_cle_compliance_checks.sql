-- Module 1 / Module 3: CLE Compliance Checks
-- Purpose: Identify attorneys who have not completed required CLE hours.

SELECT
    a.attorney_id,
    a.name,
    a.email,
    a.title,
    a.office,
    a.practice_group,
    c.jurisdiction,
    c.required_hours,
    c.completed_hours,
    (c.required_hours - c.completed_hours) AS missing_hours,
    c.deadline,
    CASE
        WHEN c.completed_hours >= c.required_hours THEN 'CLE Compliant'
        WHEN c.completed_hours < c.required_hours THEN 'CLE Deficient'
        ELSE 'Review Required'
    END AS cle_status
FROM attorneys a
JOIN cle_records c
    ON a.attorney_id = c.attorney_id
WHERE c.completed_hours < c.required_hours
ORDER BY missing_hours DESC, c.deadline ASC;
