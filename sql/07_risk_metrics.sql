-- 07_risk_metrics.sql
-- Purpose: Calculate portfolio-level and attorney-level compliance risk metrics.

-- 1. License compliance rate
SELECT
    COUNT(*) AS total_licenses,
    COUNT(CASE WHEN license_status = 'Active' THEN 1 END) AS active_licenses,
    ROUND(
        COUNT(CASE WHEN license_status = 'Active' THEN 1 END) * 100.0 / COUNT(*),
        2
    ) AS license_compliance_rate_pct
FROM licenses;

-- 2. CLE compliance rate
SELECT
    COUNT(*) AS total_cle_records,
    COUNT(CASE WHEN completed_hours >= required_hours THEN 1 END) AS compliant_cle_records,
    ROUND(
        COUNT(CASE WHEN completed_hours >= required_hours THEN 1 END) * 100.0 / COUNT(*),
        2
    ) AS cle_compliance_rate_pct
FROM cle_records;

-- 3. Revenue exposure by license status
SELECT
    l.license_status,
    COUNT(DISTINCT a.attorney_id) AS attorney_count,
    COUNT(DISTINCT m.matter_id) AS matter_count,
    COALESCE(SUM(m.revenue), 0) AS revenue_exposure
FROM attorneys a
JOIN licenses l
    ON a.attorney_id = l.attorney_id
LEFT JOIN matter_assignments ma
    ON a.attorney_id = ma.attorney_id
LEFT JOIN matters m
    ON ma.matter_id = m.matter_id
GROUP BY l.license_status
ORDER BY revenue_exposure DESC;

-- 4. Revenue exposure by CLE status
SELECT
    CASE
        WHEN c.completed_hours >= c.required_hours THEN 'CLE Compliant'
        ELSE 'CLE Deficient'
    END AS cle_status,
    COUNT(DISTINCT a.attorney_id) AS attorney_count,
    COUNT(DISTINCT m.matter_id) AS matter_count,
    COALESCE(SUM(m.revenue), 0) AS revenue_exposure
FROM attorneys a
JOIN cle_records c
    ON a.attorney_id = c.attorney_id
LEFT JOIN matter_assignments ma
    ON a.attorney_id = ma.attorney_id
LEFT JOIN matters m
    ON ma.matter_id = m.matter_id
GROUP BY cle_status
ORDER BY revenue_exposure DESC;

-- 5. Attorney-level risk scoring
SELECT
    a.attorney_id,
    a.name,
    a.title,
    a.office,
    a.practice_area,

    MAX(
        CASE
            WHEN l.license_status = 'Suspended' THEN 50
            WHEN l.license_status = 'Expired' THEN 40
            WHEN l.registration_expiry < CURRENT_DATE THEN 35
            WHEN l.registration_expiry <= CURRENT_DATE + INTERVAL '90 days' THEN 20
            ELSE 0
        END
    ) AS license_risk_score,

    MAX(
        CASE
            WHEN c.completed_hours < c.required_hours THEN 25
            ELSE 0
        END
    ) AS cle_risk_score,

    COUNT(DISTINCT ma.matter_id) AS assigned_matter_count,
    COALESCE(SUM(DISTINCT m.revenue), 0) AS revenue_exposure,

    CASE
        WHEN COALESCE(SUM(DISTINCT m.revenue), 0) >= 200000 THEN 20
        WHEN COALESCE(SUM(DISTINCT m.revenue), 0) >= 100000 THEN 10
        ELSE 0
    END AS revenue_exposure_risk_score,

    (
        MAX(
            CASE
                WHEN l.license_status = 'Suspended' THEN 50
                WHEN l.license_status = 'Expired' THEN 40
                WHEN l.registration_expiry < CURRENT_DATE THEN 35
                WHEN l.registration_expiry <= CURRENT_DATE + INTERVAL '90 days' THEN 20
                ELSE 0
            END
        )
        +
        MAX(
            CASE
                WHEN c.completed_hours < c.required_hours THEN 25
                ELSE 0
            END
        )
        +
        CASE
            WHEN COALESCE(SUM(DISTINCT m.revenue), 0) >= 200000 THEN 20
            WHEN COALESCE(SUM(DISTINCT m.revenue), 0) >= 100000 THEN 10
            ELSE 0
        END
    ) AS total_risk_score,

    CASE
        WHEN (
            MAX(
                CASE
                    WHEN l.license_status = 'Suspended' THEN 50
                    WHEN l.license_status = 'Expired' THEN 40
                    WHEN l.registration_expiry < CURRENT_DATE THEN 35
                    WHEN l.registration_expiry <= CURRENT_DATE + INTERVAL '90 days' THEN 20
                    ELSE 0
                END
            )
            +
            MAX(
                CASE
                    WHEN c.completed_hours < c.required_hours THEN 25
                    ELSE 0
                END
            )
            +
            CASE
                WHEN COALESCE(SUM(DISTINCT m.revenue), 0) >= 200000 THEN 20
                WHEN COALESCE(SUM(DISTINCT m.revenue), 0) >= 100000 THEN 10
                ELSE 0
            END
        ) >= 70 THEN 'High Risk'

        WHEN (
            MAX(
                CASE
                    WHEN l.license_status = 'Suspended' THEN 50
                    WHEN l.license_status = 'Expired' THEN 40
                    WHEN l.registration_expiry < CURRENT_DATE THEN 35
                    WHEN l.registration_expiry <= CURRENT_DATE + INTERVAL '90 days' THEN 20
                    ELSE 0
                END
            )
            +
            MAX(
                CASE
                    WHEN c.completed_hours < c.required_hours THEN 25
                    ELSE 0
                END
            )
            +
            CASE
                WHEN COALESCE(SUM(DISTINCT m.revenue), 0) >= 200000 THEN 20
                WHEN COALESCE(SUM(DISTINCT m.revenue), 0) >= 100000 THEN 10
                ELSE 0
            END
        ) >= 40 THEN 'Medium Risk'

        ELSE 'Low Risk'
    END AS risk_tier

FROM attorneys a
LEFT JOIN licenses l
    ON a.attorney_id = l.attorney_id
LEFT JOIN cle_records c
    ON a.attorney_id = c.attorney_id
LEFT JOIN matter_assignments ma
    ON a.attorney_id = ma.attorney_id
LEFT JOIN matters m
    ON ma.matter_id = m.matter_id
GROUP BY
    a.attorney_id,
    a.name,
    a.title,
    a.office,
    a.practice_area
ORDER BY total_risk_score DESC;

-- 6. Risk tier distribution
WITH attorney_risk AS (
    SELECT
        a.attorney_id,

        (
            MAX(
                CASE
                    WHEN l.license_status = 'Suspended' THEN 50
                    WHEN l.license_status = 'Expired' THEN 40
                    WHEN l.registration_expiry < CURRENT_DATE THEN 35
                    WHEN l.registration_expiry <= CURRENT_DATE + INTERVAL '90 days' THEN 20
                    ELSE 0
                END
            )
            +
            MAX(
                CASE
                    WHEN c.completed_hours < c.required_hours THEN 25
                    ELSE 0
                END
            )
            +
            CASE
                WHEN COALESCE(SUM(DISTINCT m.revenue), 0) >= 200000 THEN 20
                WHEN COALESCE(SUM(DISTINCT m.revenue), 0) >= 100000 THEN 10
                ELSE 0
            END
        ) AS total_risk_score

    FROM attorneys a
    LEFT JOIN licenses l
        ON a.attorney_id = l.attorney_id
    LEFT JOIN cle_records c
        ON a.attorney_id = c.attorney_id
    LEFT JOIN matter_assignments ma
        ON a.attorney_id = ma.attorney_id
    LEFT JOIN matters m
        ON ma.matter_id = m.matter_id
    GROUP BY a.attorney_id
)

SELECT
    CASE
        WHEN total_risk_score >= 70 THEN 'High Risk'
        WHEN total_risk_score >= 40 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END AS risk_tier,
    COUNT(*) AS attorney_count
FROM attorney_risk
GROUP BY risk_tier
ORDER BY attorney_count DESC;
