# Patient Readmission Analysis

An end-to-end data analytics project to understand the factors associated with **hospital readmission within 30 days**.

I used Python for data cleaning and analysis, MySQL for SQL-based analysis, and Power BI to build an interactive dashboard.

---

## About the Project

Hospital readmissions can increase healthcare costs and put additional pressure on hospital resources.

In this project, I analyzed hospital encounters involving diabetic patients to understand:

- How common 30-day readmissions are
- Whether previous hospital visits are associated with readmission
- How readmission varies across age, gender, and race
- How medications and diagnosis categories relate to readmission
- How admission and discharge characteristics differ

> This is an observational analysis, so the findings show associations rather than causes.

---

## Dataset

**Diabetes 130-US Hospitals for Years 1999-2008**

The dataset contains **101,766 hospital encounters** from U.S. hospitals.

Some patients have multiple encounters, so one row represents a **hospital encounter**, not necessarily a unique patient.

### Target

The original dataset contains three readmission categories:

- `NO` — No readmission
- `>30` — Readmitted after 30 days
- `<30` — Readmitted within 30 days

For this project, I created:

```text
early_readmission
