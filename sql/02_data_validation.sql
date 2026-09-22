-- ============================================================
-- Patient Readmission Analysis
-- SQL: Data Validation
-- ============================================================

USE patient_readmission;


-- ============================================================
-- Query 1: Check total number of records
-- Expected: 101,766
-- ============================================================

SELECT
    COUNT(*) AS total_rows
FROM patient_readmission_analysis;


-- ============================================================
-- Query 2: Check early-readmission distribution
-- Expected:
-- 0 = 90,409
-- 1 = 11,357
-- ============================================================

SELECT
    early_readmission,
    COUNT(*) AS total_encounters
FROM patient_readmission_analysis
GROUP BY early_readmission
ORDER BY early_readmission;


-- ============================================================
-- Query 3: Calculate overall early-readmission rate
-- Expected: approximately 11.16%
-- ============================================================

SELECT
    COUNT(*) AS total_encounters,
    SUM(early_readmission) AS early_readmissions,
    ROUND(
        100.0 * SUM(early_readmission) / COUNT(*),
        2
    ) AS early_readmission_rate
FROM patient_readmission_analysis;


-- ============================================================
-- Query 4: Check for NULL values in important fields
-- Expected: 0
-- ============================================================

SELECT
    COUNT(*) AS rows_with_nulls
FROM patient_readmission_analysis
WHERE
    race IS NULL
    OR gender IS NULL
    OR age IS NULL
    OR time_in_hospital IS NULL
    OR num_lab_procedures IS NULL
    OR num_procedures IS NULL
    OR num_medications IS NULL
    OR number_outpatient IS NULL
    OR number_emergency IS NULL
    OR number_inpatient IS NULL
    OR number_diagnoses IS NULL
    OR readmitted IS NULL
    OR early_readmission IS NULL;


-- ============================================================
-- Query 5: Check target consistency
-- early_readmission should be 1 only when readmitted = '<30'
-- ============================================================

SELECT
    COUNT(*) AS target_mismatches
FROM patient_readmission_analysis
WHERE
    (readmitted = '<30' AND early_readmission <> 1)
    OR
    (readmitted <> '<30' AND early_readmission <> 0);


-- ============================================================
-- Query 6: Check distinct target values
-- ============================================================

SELECT DISTINCT
    early_readmission
FROM patient_readmission_analysis
ORDER BY early_readmission;


-- ============================================================
-- Query 7: Check minimum and maximum values of numerical fields
-- ============================================================

SELECT
    MIN(time_in_hospital) AS min_time_in_hospital,
    MAX(time_in_hospital) AS max_time_in_hospital,

    MIN(num_lab_procedures) AS min_lab_procedures,
    MAX(num_lab_procedures) AS max_lab_procedures,

    MIN(num_procedures) AS min_procedures,
    MAX(num_procedures) AS max_procedures,

    MIN(num_medications) AS min_medications,
    MAX(num_medications) AS max_medications,

    MIN(number_outpatient) AS min_outpatient,
    MAX(number_outpatient) AS max_outpatient,

    MIN(number_emergency) AS min_emergency,
    MAX(number_emergency) AS max_emergency,

    MIN(number_inpatient) AS min_inpatient,
    MAX(number_inpatient) AS max_inpatient,

    MIN(number_diagnoses) AS min_diagnoses,
    MAX(number_diagnoses) AS max_diagnoses

FROM patient_readmission_analysis;


-- ============================================================
-- Query 8: Check for unexpected early_readmission values
-- Expected: 0 unexpected values
-- ============================================================

SELECT
    COUNT(*) AS invalid_target_values
FROM patient_readmission_analysis
WHERE early_readmission NOT IN (0, 1);


-- ============================================================
-- Query 9: Check row counts by original readmission category
-- ============================================================

SELECT
    readmitted,
    COUNT(*) AS total_encounters
FROM patient_readmission_analysis
GROUP BY readmitted
ORDER BY total_encounters DESC;


-- ============================================================
-- Query 10: Final validation summary
-- ============================================================

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT early_readmission) AS distinct_target_values,
    SUM(early_readmission) AS early_readmissions,
    ROUND(
        100.0 * SUM(early_readmission) / COUNT(*),
        2
    ) AS early_readmission_rate
FROM patient_readmission_analysis;