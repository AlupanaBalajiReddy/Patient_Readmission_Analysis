# Patient Readmission Analysis (Python • MySQL • Power BI)

[![Python](https://img.shields.io/badge/Python-Data%20Cleaning%20%26%20EDA-3776AB?logo=python&logoColor=white)](#)
[![MySQL](https://img.shields.io/badge/MySQL-SQL%20Analytics-4479A1?logo=mysql&logoColor=white)](#)
[![Power BI](https://img.shields.io/badge/Power%20BI-Interactive%20Dashboard-F2C811?logo=powerbi&logoColor=black)](#)

An end-to-end healthcare data analytics project investigating clinical, demographic, and operational factors associated with **30-day hospital readmissions** among diabetic patients. Built using **Python** for data cleaning and exploratory analysis, **MySQL** for relational querying and cohort aggregation, and **Power BI** (`projectk.pbix`) for interactive executive reporting.

---

## About the Project

Hospital readmissions increase healthcare costs and place substantial strain on inpatient capacity and clinical resources. In this project, I analyzed **101,766 inpatient encounters** involving diabetic patients to evaluate:

* **Baseline Readmission Burden:** How prevalent `<30-day` readmissions are relative to `>30-day` and non-readmitted (`NO`) encounters.
* **Prior Utilization Impact:** Whether prior inpatient, emergency, and outpatient visits correlate with higher early readmission rates.
* **Demographic Disparities:** How 30-day readmission rates vary across **age brackets**, **gender**, and **race**.
* **Clinical & Medication Factors:** How primary diagnosis categories, number of diagnoses, lab/procedure counts, and diabetes medication adjustments relate to readmission.
* **Care-Transition Characteristics:** How admission sources and discharge dispositions differ across readmitted vs. non-readmitted encounters.

> **Methodological Note:** Because this study uses retrospective observational hospital records, findings represent statistical associations rather than causal relationships.

---

## Dataset Overview

* **Source:** Diabetes 130-US Hospitals for Years 1999–2008 (UCI Machine Learning Repository)
* **Scale:** **101,766 hospital encounters** across 130 U.S. hospitals over a 10-year period.
* **Granularity:** Each row represents an individual **hospital encounter** (`encounter_id`), not necessarily a unique patient (`patient_nbr`), as individual patients may have multiple admissions across the study window.

---

## Target Variable Engineering

The raw `readmitted` field categorizes encounters into three outcomes:
* `NO` — No recorded readmission
* `>30` — Readmitted more than 30 days after discharge
* `<30` — Readmitted within 30 days of discharge

To align with standard hospital quality benchmarks (such as CMS 30-day readmission metrics), I engineered a binary target flag:
* **`early_readmission`**: Coded as `1` when `readmitted == '<30'` (early readmission within 30 days) and `0` otherwise (`'>30'` or `'NO'`).

---

## End-to-End Analytics Workflow

### 1. Data Cleaning & Preprocessing (`Python`)
* Audited missing values (`?` placeholders across fields such as `race`, `weight`, `payer_code`, and `medical_specialty`) and standardized categorical labels.
* Removed invalid/expired discharge dispositions (e.g., hospice or deceased patients) where 30-day readmission is clinically non-applicable.
* Engineered the binary `early_readmission` target flag, grouped ICD-9 diagnosis codes into clinical categories, and exported a clean analytical dataset for relational querying.

### 2. SQL Cohort & Driver Analysis (`MySQL`)
* Loaded the cleaned encounter table into **MySQL** to perform structured aggregations across patient demographics, prior utilization (`number_inpatient`, `number_emergency`), and clinical complexity.
* Computed segmented 30-day readmission rates (`SUM(early_readmission) / COUNT(*)`) using `GROUP BY`, `CASE WHEN` risk bucketing, and window functions to rank high-risk admission and discharge pathways.

### 3. Interactive BI Reporting (`Power BI` — `projectk.pbix`)
* Built an interactive multi-page dashboard in **Power BI Desktop** featuring custom **DAX** measures (`Total Encounters`, `Unique Patients`, `Early Readmission Rate (%)`, `Avg Time in Hospital`).
* Enabled cross-filtering across age cohorts, primary diagnosis categories, medication changes, and discharge dispositions for self-service exploration.

---

## Key Insights & Takeaways

*(Fill in the exact percentages from your SQL queries / Power BI cards before finalizing)*
* **Overall 30-Day Readmission Rate:** **[~11.2%]** of valid encounters resulted in an early readmission (`<30 days`).
* **Prior Inpatient History:** Prior inpatient utilization emerged as the strongest indicator of early readmission—patients with multiple prior inpatient visits exhibited significantly higher `early_readmission` rates than first-time encounters.
* **Discharge Disposition:** Patients discharged to post-acute care facilities (such as skilled nursing or rehabilitation facilities) experienced substantially higher 30-day readmission rates than routine home discharges.
* **Clinical & Medication Complexity:** Encounters involving higher diagnosis counts and active diabetes medication adjustments showed elevated readmission associations.

---

## Repository Structure

```text
Patient_Readmission_Analysis/
├── projectk.pbix          # Power BI Desktop dashboard (data model, DAX measures, and visuals)
└── README.md              # Project overview, methodology, and analytical documentation
```
*(Note: If you also plan to upload your Python `.ipynb`/`.py` scripts and `.sql` query files later, add them to this repository to showcase the full 3-tool pipeline).*

---

## How to Explore the Dashboard

1. Clone this repository or download `projectk.pbix`:
   ```bash
   git clone [https://github.com/AlupanaBalajiReddy/Patient_Readmission_Analysis.git](https://github.com/AlupanaBalajiReddy/Patient_Readmission_Analysis.git)
   ```
2. Open `projectk.pbix` in **Microsoft Power BI Desktop**.
3. Use the interactive slicers to filter readmission metrics by **Age**, **Race**, **Gender**, **Diagnosis Category**, and **Discharge Disposition**.

---

## Author

**Alupana Balaji Reddy**  
M.Tech in Medical Biotechnology — Indian Institute of Technology Hyderabad  
[GitHub](https://github.com/AlupanaBalajiReddy) • [Email](mailto:bt25mtech11001@iith.ac.in)