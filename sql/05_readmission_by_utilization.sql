-- ============================================================
-- Patient Readmission Analysis
-- SQL Analysis: Prior Healthcare Utilization
-- ============================================================

USE patient_readmission;


-- ============================================================
-- Query 1: Early-readmission rate by prior inpatient visits
-- ============================================================

SELECT
    inpatient_visits_group,
    COUNT(*) AS total_encounters,
    SUM(early_readmission) AS early_readmissions,
    ROUND(
        100.0 * SUM(early_readmission) / COUNT(*),
        2
    ) AS early_readmission_rate
FROM patient_readmission_analysis
GROUP BY inpatient_visits_group
ORDER BY
    CASE inpatient_visits_group
        WHEN '0' THEN 1
        WHEN '1' THEN 2
        WHEN '2' THEN 3
        WHEN '3+' THEN 4
        ELSE 5
    END;


-- ============================================================
-- Query 2: Early-readmission rate by prior emergency visits
-- ============================================================

SELECT
    emergency_visits_group,
    COUNT(*) AS total_encounters,
    SUM(early_readmission) AS early_readmissions,
    ROUND(
        100.0 * SUM(early_readmission) / COUNT(*),
        2
    ) AS early_readmission_rate
FROM patient_readmission_analysis
GROUP BY emergency_visits_group
ORDER BY
    CASE emergency_visits_group
        WHEN '0' THEN 1
        WHEN '1' THEN 2
        WHEN '2' THEN 3
        WHEN '3+' THEN 4
        ELSE 5
    END;


-- ============================================================
-- Query 3: Early-readmission rate by prior outpatient visits
-- ============================================================

SELECT
    outpatient_visits_group,
    COUNT(*) AS total_encounters,
    SUM(early_readmission) AS early_readmissions,
    ROUND(
        100.0 * SUM(early_readmission) / COUNT(*),
        2
    ) AS early_readmission_rate
FROM patient_readmission_analysis
GROUP BY outpatient_visits_group
ORDER BY
    CASE outpatient_visits_group
        WHEN '0' THEN 1
        WHEN '1' THEN 2
        WHEN '2' THEN 3
        WHEN '3+' THEN 4
        ELSE 5
    END;


-- ============================================================
-- Query 4: Combined utilization comparison
-- ============================================================

SELECT
    'Outpatient' AS utilization_type,
    outpatient_visits_group AS utilization_group,
    COUNT(*) AS total_encounters,
    SUM(early_readmission) AS early_readmissions,
    ROUND(
        100.0 * SUM(early_readmission) / COUNT(*),
        2
    ) AS early_readmission_rate
FROM patient_readmission_analysis
GROUP BY outpatient_visits_group

UNION ALL

SELECT
    'Emergency' AS utilization_type,
    emergency_visits_group AS utilization_group,
    COUNT(*) AS total_encounters,
    SUM(early_readmission) AS early_readmissions,
    ROUND(
        100.0 * SUM(early_readmission) / COUNT(*),
        2
    ) AS early_readmission_rate
FROM patient_readmission_analysis
GROUP BY emergency_visits_group

UNION ALL

SELECT
    'Inpatient' AS utilization_type,
    inpatient_visits_group AS utilization_group,
    COUNT(*) AS total_encounters,
    SUM(early_readmission) AS early_readmissions,
    ROUND(
        100.0 * SUM(early_readmission) / COUNT(*),
        2
    ) AS early_readmission_rate
FROM patient_readmission_analysis
GROUP BY inpatient_visits_group

ORDER BY
    utilization_type,
    CASE utilization_group
        WHEN '0' THEN 1
        WHEN '1' THEN 2
        WHEN '2' THEN 3
        WHEN '3+' THEN 4
        ELSE 5
    END;