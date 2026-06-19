-- Module 4: Attorney Compliance Summary
-- Purpose: Create an attorney-level compliance risk summary by combining license status, CLE status, and matter assignment risk.

WITH license_risk AS (
    SELECT
        attorney_id,
        MAX(
            CASE
                WHEN license_status = 'Suspended' THEN 100
                WHEN license_status = 'Expired' THEN 75
                ELSE 0
            END
        ) AS license_risk_score
    FROM licenses
    GROUP BY attorney_id
),

cle_risk AS (
    SELECT
        attorney_id,
        MAX(
            CASE
                WHEN completed_hours < required_hours THEN 25
                ELSE 0
            END
        ) AS cle_risk_score,
        SUM(
            CASE
                WHEN completed_hours < required_hours
                THEN required_hours - completed_hours
                ELSE 0
            END
        ) AS total_missing_cle_hours
    FROM cle_records
    GROUP BY attorney_id
),

matter_risk AS (
    SELECT
        ma.attorney_id,
        COUNT(*) AS risky_matter_count,
        SUM(m.revenue) AS revenue_at_risk,
        MAX(100) AS matter_assignment_risk_score
    FROM matter_assignments ma
    JOIN matters m
        ON ma.matter_id = m.matter_id
    LEFT JOIN licenses l
        ON ma.attorney_id = l.attorney_id
        AND m.jurisdiction = l.jurisdiction
        AND l.license_status = 'Active'
    WHERE l.attorney_id IS NULL
    GROUP BY ma.attorney_id
)

SELECT
    a.attorney_id,
    a.name,
    a.email,
    a.title,
    a.office,
    a.practice_group,

    COALESCE(lr.license_risk_score, 0) AS license_risk_score,
    COALESCE(cr.cle_risk_score, 0) AS cle_risk_score,
    COALESCE(cr.total_missing_cle_hours, 0) AS total_missing_cle_hours,
    COALESCE(mr.matter_assignment_risk_score, 0) AS matter_assignment_risk_score,
    COALESCE(mr.risky_matter_count, 0) AS risky_matter_count,
    COALESCE(mr.revenue_at_risk, 0) AS revenue_at_risk,

    (
        COALESCE(lr.license_risk_score, 0)
        + COALESCE(cr.cle_risk_score, 0)
        + COALESCE(mr.matter_assignment_risk_score, 0)
    ) AS total_compliance_risk_score,

    CASE
        WHEN (
            COALESCE(lr.license_risk_score, 0)
            + COALESCE(cr.cle_risk_score, 0)
            + COALESCE(mr.matter_assignment_risk_score, 0)
        ) >= 150 THEN 'Critical'
        WHEN (
            COALESCE(lr.license_risk_score, 0)
            + COALESCE(cr.cle_risk_score, 0)
            + COALESCE(mr.matter_assignment_risk_score, 0)
        ) >= 75 THEN 'High'
        WHEN (
            COALESCE(lr.license_risk_score, 0)
            + COALESCE(cr.cle_risk_score, 0)
            + COALESCE(mr.matter_assignment_risk_score, 0)
        ) > 0 THEN 'Moderate'
        ELSE 'Low'
    END AS overall_risk_level

FROM attorneys a
LEFT JOIN license_risk lr
    ON a.attorney_id = lr.attorney_id
LEFT JOIN cle_risk cr
    ON a.attorney_id = cr.attorney_id
LEFT JOIN matter_risk mr
    ON a.attorney_id = mr.attorney_id

ORDER BY
    total_compliance_risk_score DESC,
    revenue_at_risk DESC;
