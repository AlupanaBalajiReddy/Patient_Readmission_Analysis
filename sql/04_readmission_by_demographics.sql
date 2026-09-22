-- ============================================================
-- Patient Readmission Analysis
-- SQL Analysis: Demographics
-- ============================================================

USE patient_readmission;


-- ============================================================
-- Query 1: Early-readmission rate by age group
-- ============================================================

SELECT
    age,
    COUNT(*) AS total_encounters,
    SUM(early_readmission) AS early_readmissions,
    ROUND(
        100.0 * SUM(early_readmission) / COUNT(*),
        2
    ) AS early_readmission_rate
FROM patient_readmission_analysis
GROUP BY age
ORDER BY early_readmission_rate DESC;


-- ============================================================
-- Query 2: Early-readmission rate by gender
-- ============================================================

SELECT
    gender,
    COUNT(*) AS total_encounters,
    SUM(early_readmission) AS early_readmissions,
    ROUND(
        100.0 * SUM(early_readmission) / COUNT(*),
        2
    ) AS early_readmission_rate
FROM patient_readmission_analysis
GROUP BY gender
HAVING COUNT(*) >= 100
ORDER BY early_readmission_rate DESC;


-- ============================================================
-- Query 3: Early-readmission rate by race
-- ============================================================

SELECT
    race,
    COUNT(*) AS total_encounters,
    SUM(early_readmission) AS early_readmissions,
    ROUND(
        100.0 * SUM(early_readmission) / COUNT(*),
        2
    ) AS early_readmission_rate
FROM patient_readmission_analysis
GROUP BY race
HAVING COUNT(*) >= 100
ORDER BY early_readmission_rate DESC;