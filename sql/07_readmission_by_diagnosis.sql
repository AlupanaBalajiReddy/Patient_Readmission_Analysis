-- ============================================================
-- Patient Readmission Analysis
-- SQL Analysis: Diagnosis-Related Factors
-- ============================================================

USE patient_readmission;

-- ============================================================
-- Query 1: Early-readmission rate by primary diagnosis category
-- ============================================================

SELECT
    primary_diagnosis_category,
    COUNT(*) AS total_encounters,
    SUM(early_readmission) AS early_readmissions,
    ROUND(
        100.0 * SUM(early_readmission) / COUNT(*),
        2
    ) AS early_readmission_rate
FROM patient_readmission_analysis
GROUP BY primary_diagnosis_category
HAVING COUNT(*) >= 100
ORDER BY early_readmission_rate DESC;


-- ============================================================
-- Query 2: Early-readmission rate by secondary diagnosis category
-- ============================================================

SELECT
    secondary_diagnosis_category,
    COUNT(*) AS total_encounters,
    SUM(early_readmission) AS early_readmissions,
    ROUND(
        100.0 * SUM(early_readmission) / COUNT(*),
        2
    ) AS early_readmission_rate
FROM patient_readmission_analysis
GROUP BY secondary_diagnosis_category
HAVING COUNT(*) >= 100
ORDER BY early_readmission_rate DESC;


-- ============================================================
-- Query 3: Early-readmission rate by tertiary diagnosis category
-- ============================================================

SELECT
    tertiary_diagnosis_category,
    COUNT(*) AS total_encounters,
    SUM(early_readmission) AS early_readmissions,
    ROUND(
        100.0 * SUM(early_readmission) / COUNT(*),
        2
    ) AS early_readmission_rate
FROM patient_readmission_analysis
GROUP BY tertiary_diagnosis_category
HAVING COUNT(*) >= 100
ORDER BY early_readmission_rate DESC;