-- ============================================================
-- Patient Readmission Analysis
-- SQL Analysis: Medication-Related Factors
-- ============================================================

USE patient_readmission;

-- ============================================================
-- Query 1: Early-readmission rate by diabetes medication use
-- ============================================================

SELECT
    diabetesMed,
    COUNT(*) AS total_encounters,
    SUM(early_readmission) AS early_readmissions,
    ROUND(
        100.0 * SUM(early_readmission) / COUNT(*),
        2
    ) AS early_readmission_rate
FROM patient_readmission_analysis
GROUP BY diabetesMed
ORDER BY early_readmission_rate DESC;


-- ============================================================
-- Query 2: Early-readmission rate by medication change
-- ============================================================

SELECT
    `change`,
    COUNT(*) AS total_encounters,
    SUM(early_readmission) AS early_readmissions,
    ROUND(
        100.0 * SUM(early_readmission) / COUNT(*),
        2
    ) AS early_readmission_rate
FROM patient_readmission_analysis
GROUP BY `change`
ORDER BY early_readmission_rate DESC;


-- ============================================================
-- Query 3: Early-readmission rate by insulin treatment status
-- ============================================================

SELECT
    insulin,
    COUNT(*) AS total_encounters,
    SUM(early_readmission) AS early_readmissions,
    ROUND(
        100.0 * SUM(early_readmission) / COUNT(*),
        2
    ) AS early_readmission_rate
FROM patient_readmission_analysis
GROUP BY insulin
ORDER BY early_readmission_rate DESC;