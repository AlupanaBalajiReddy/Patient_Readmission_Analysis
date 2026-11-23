-- ============================================================
-- Patient Readmission Analysis
-- SQL Analysis: Business Insights
-- ============================================================

USE patient_readmission;


-- ============================================================
-- Query 1: Overall early-readmission rate
-- Business Question:
-- What proportion of hospital encounters resulted in
-- readmission within 30 days?
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
-- Query 2: Compare patients with no prior inpatient visits
-- against patients with 3+ prior inpatient visits
-- Business Question:
-- How does prior inpatient utilization relate to
-- early readmission?
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
WHERE inpatient_visits_group IN ('0', '3+')
GROUP BY inpatient_visits_group
ORDER BY
    CASE inpatient_visits_group
        WHEN '0' THEN 1
        WHEN '3+' THEN 2
    END;


-- ============================================================
-- Query 3: Compare patients with no prior emergency visits
-- against patients with 3+ prior emergency visits
-- Business Question:
-- How does prior emergency utilization relate to
-- early readmission?
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
WHERE emergency_visits_group IN ('0', '3+')
GROUP BY emergency_visits_group
ORDER BY
    CASE emergency_visits_group
        WHEN '0' THEN 1
        WHEN '3+' THEN 2
    END;


-- ============================================================
-- Query 4: Compare diabetes medication use
-- Business Question:
-- Is early-readmission rate different between encounters
-- with and without diabetes medication?
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
-- Query 5: Compare medication change status
-- Business Question:
-- Is early-readmission rate different when diabetes
-- medication was changed?
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
-- Query 6: Highest-volume discharge dispositions
-- Business Question:
-- Which discharge destinations have both substantial
-- encounter volume and elevated early-readmission rates?
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
HAVING COUNT(*) >= 1000
ORDER BY early_readmission_rate DESC;


-- ============================================================
-- Query 7: Primary diagnosis categories with substantial
-- encounter volume
-- Business Question:
-- Which diagnosis categories show different levels of
-- early readmission?
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
HAVING COUNT(*) >= 1000
ORDER BY early_readmission_rate DESC;


-- ============================================================
-- Query 8: Identify high-utilization groups with elevated
-- early-readmission rates
-- Business Question:
-- What happens when prior inpatient and emergency
-- utilization are both high?
-- ============================================================

SELECT
    inpatient_visits_group,
    emergency_visits_group,
    COUNT(*) AS total_encounters,
    SUM(early_readmission) AS early_readmissions,
    ROUND(
        100.0 * SUM(early_readmission) / COUNT(*),
        2
    ) AS early_readmission_rate
FROM patient_readmission_analysis
WHERE inpatient_visits_group IN ('0', '3+')
  AND emergency_visits_group IN ('0', '3+')
GROUP BY
    inpatient_visits_group,
    emergency_visits_group
HAVING COUNT(*) >= 100
ORDER BY early_readmission_rate DESC;