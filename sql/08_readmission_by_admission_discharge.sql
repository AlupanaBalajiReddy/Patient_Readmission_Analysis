-- ============================================================
-- Patient Readmission Analysis
-- SQL Analysis: Admission and Discharge Factors
-- ============================================================

USE patient_readmission;

-- ============================================================
-- Query 1: Early-readmission rate by admission type
-- ============================================================

SELECT
    admission_type,
    COUNT(*) AS total_encounters,
    SUM(early_readmission) AS early_readmissions,
    ROUND(
        100.0 * SUM(early_readmission) / COUNT(*),
        2
    ) AS early_readmission_rate
FROM patient_readmission_analysis
GROUP BY admission_type
HAVING COUNT(*) >= 100
ORDER BY early_readmission_rate DESC;


-- ============================================================
-- Query 2: Early-readmission rate by discharge disposition
-- ============================================================

SELECT
    discharge_disposition,
    COUNT(*) AS total_encounters,
    SUM(early_readmission) AS early_readmissions,
    ROUND(
        100.0 * SUM(early_readmission) / COUNT(*),
        2
    ) AS early_readmission_rate
FROM patient_readmission_analysis
GROUP BY discharge_disposition
HAVING COUNT(*) >= 100
ORDER BY early_readmission_rate DESC;


-- ============================================================
-- Query 3: Early-readmission rate by admission source
-- ============================================================

SELECT
    admission_source,
    COUNT(*) AS total_encounters,
    SUM(early_readmission) AS early_readmissions,
    ROUND(
        100.0 * SUM(early_readmission) / COUNT(*),
        2
    ) AS early_readmission_rate
FROM patient_readmission_analysis
GROUP BY admission_source
HAVING COUNT(*) >= 100
ORDER BY early_readmission_rate DESC;