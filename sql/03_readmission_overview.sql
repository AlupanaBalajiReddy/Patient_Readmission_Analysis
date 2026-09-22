-- ============================================================
-- Patient Readmission Analysis
-- SQL Analysis: Readmission Overview
-- ============================================================

USE patient_readmission;


-- ============================================================
-- Query 1: Overall early-readmission summary
-- ============================================================

SELECT
    COUNT(*) AS total_encounters,
    SUM(early_readmission) AS early_readmissions,
    COUNT(*) - SUM(early_readmission) AS non_early_readmissions,
    ROUND(
        100.0 * SUM(early_readmission) / COUNT(*),
        2
    ) AS early_readmission_rate
FROM patient_readmission_analysis;


-- ============================================================
-- Query 2: Original readmission categories
-- ============================================================

SELECT
    readmitted,
    COUNT(*) AS total_encounters,
    ROUND(
        100.0 * COUNT(*) / (
            SELECT COUNT(*)
            FROM patient_readmission_analysis
        ),
        2
    ) AS percentage_of_encounters
FROM patient_readmission_analysis
GROUP BY readmitted
ORDER BY total_encounters DESC;


-- ============================================================
-- Query 3: Early-readmission distribution
-- ============================================================

SELECT
    early_readmission,
    COUNT(*) AS encounters,
    ROUND(
        100.0 * COUNT(*) / (
            SELECT COUNT(*)
            FROM patient_readmission_analysis
        ),
        2
    ) AS percentage_of_encounters
FROM patient_readmission_analysis
GROUP BY early_readmission
ORDER BY early_readmission;