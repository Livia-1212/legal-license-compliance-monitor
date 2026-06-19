-- Module 4: Attorney Compliance Findings Summary
-- Purpose: Provide attorney-level compliance findings with clear issue descriptions for legal and compliance stakeholders.

WITH license_findings AS (
    SELECT
        attorney_id,
        GROUP_CONCAT(
            CASE
                WHEN license_status = 'Suspended'
                    THEN CONCAT('Suspended ', jurisdiction, ' license')
                WHEN license_status = 'Expired'
                    THEN CONCAT('Expired ', jurisdiction, ' registration')
            END
            SEPARATOR '; '
        ) AS license_issue
    FROM licenses
    WHERE license_status <> 'Active'
    GROUP BY attorney_id
),

cle_findings AS (
    SELECT
        attorney_id,
        GROUP_CONCAT(
            CONCAT('Missing ', required_hours - completed_hours, ' CLE hours in ', jurisdiction)
            SEPARATOR '; '
        ) AS cle_issue,
        SUM(required_hours - completed_hours) AS total_missing_cle_hours
    FROM cle_records
    WHERE completed_hours < required_hours
    GROUP BY attorney_id
),

matter_findings AS (
    SELECT
        ma.attorney_id,
        GROUP_CONCAT(
            CONCAT(
                'Assigned to ', m.matter_name,
                ' (', m.jurisdiction, ') for ', m.client
            )
            SEPARATOR '; '
        ) AS matter_issue,
        COUNT(*) AS affected_matter_count,
        SUM(m.revenue) AS revenue_exposure
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

    COALESCE(lf.license_issue, 'No license issue') AS license_findings,
    COALESCE(cf.cle_issue, 'No CLE issue') AS cle_findings,
    COALESCE(mf.matter_issue, 'No matter assignment issue') AS matter_assignment_findings,

    COALESCE(cf.total_missing_cle_hours, 0) AS total_missing_cle_hours,
    COALESCE(mf.affected_matter_count, 0) AS affected_matter_count,
    COALESCE(mf.revenue_exposure, 0) AS revenue_exposure,

    CASE
        WHEN lf.license_issue LIKE '%Suspended%'
            OR mf.affected_matter_count > 0
            THEN 'Critical'
        WHEN lf.license_issue IS NOT NULL
            OR cf.total_missing_cle_hours > 0
            THEN 'High'
        ELSE 'No Current Finding'
    END AS overall_assessment

FROM attorneys a
LEFT JOIN license_findings lf
    ON a.attorney_id = lf.attorney_id
LEFT JOIN cle_findings cf
    ON a.attorney_id = cf.attorney_id
LEFT JOIN matter_findings mf
    ON a.attorney_id = mf.attorney_id

WHERE
    lf.license_issue IS NOT NULL
    OR cf.cle_issue IS NOT NULL
    OR mf.matter_issue IS NOT NULL

ORDER BY
    CASE
        WHEN overall_assessment = 'Critical' THEN 1
        WHEN overall_assessment = 'High' THEN 2
        ELSE 3
    END,
    revenue_exposure DESC,
    total_missing_cle_hours DESC;
