-- ============================================================
-- Patient Readmission Analysis
-- SQL: Database and Table Setup
-- ============================================================

-- ============================================================
-- 1. Create the project database
-- ============================================================

CREATE DATABASE IF NOT EXISTS patient_readmission;

USE patient_readmission;


-- ============================================================
-- 2. Create the analysis table
-- ============================================================

CREATE TABLE IF NOT EXISTS patient_readmission_analysis (

    race VARCHAR(50),
    gender VARCHAR(30),
    age VARCHAR(20),
    time_in_hospital INT,
    payer_code VARCHAR(20),
    medical_specialty VARCHAR(100),

    num_lab_procedures INT,
    num_procedures INT,
    num_medications INT,

    number_outpatient INT,
    number_emergency INT,
    number_inpatient INT,
    number_diagnoses INT,

    metformin VARCHAR(20),
    repaglinide VARCHAR(20),
    nateglinide VARCHAR(20),
    chlorpropamide VARCHAR(20),
    glimepiride VARCHAR(20),
    acetohexamide VARCHAR(20),
    glipizide VARCHAR(20),
    glyburide VARCHAR(20),
    tolbutamide VARCHAR(20),
    pioglitazone VARCHAR(20),
    rosiglitazone VARCHAR(20),
    acarbose VARCHAR(20),
    miglitol VARCHAR(20),
    troglitazone VARCHAR(20),
    tolazamide VARCHAR(20),
    insulin VARCHAR(20),

    glyburide_metformin VARCHAR(20),
    glipizide_metformin VARCHAR(20),
    glimepiride_pioglitazone VARCHAR(20),
    metformin_rosiglitazone VARCHAR(20),
    metformin_pioglitazone VARCHAR(20),

    `change` VARCHAR(20),
    diabetesMed VARCHAR(20),

    readmitted VARCHAR(20),
    early_readmission TINYINT,

    admission_type VARCHAR(50),
    discharge_disposition VARCHAR(100),
    admission_source VARCHAR(100),

    outpatient_visits_group VARCHAR(10),
    emergency_visits_group VARCHAR(10),
    inpatient_visits_group VARCHAR(10),

    primary_diagnosis_category VARCHAR(50),
    secondary_diagnosis_category VARCHAR(50),
    tertiary_diagnosis_category VARCHAR(50)
);


-- ============================================================
-- 3. Verify table structure
-- ============================================================

DESCRIBE patient_readmission_analysis;


-- ============================================================
-- 4. Verify that the table exists
-- ============================================================

SHOW TABLES;