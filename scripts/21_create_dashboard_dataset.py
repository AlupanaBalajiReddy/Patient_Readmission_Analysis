"""
Stage 9: Create Dashboard-Ready Dataset

Purpose:
    Create a focused dataset for the Power BI dashboard.

Important:
    The original analysis dataset is not modified.
    This creates a separate dashboard-specific dataset.
"""

import os
import pandas as pd


# ============================================================
# 1. PATHS
# ============================================================

INPUT_FILE = (
    "data/processed/"
    "patient_readmission_analysis.csv"
)

OUTPUT_DIR = "data/processed"

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "patient_readmission_dashboard.csv"
)

QUALITY_FILE = (
    "results/analysis_results/"
    "dashboard_dataset_quality.txt"
)


# ============================================================
# 2. LOAD DATA
# ============================================================

print("=" * 70)
print("STAGE 9: CREATE DASHBOARD-READY DATASET")
print("=" * 70)

df = pd.read_csv(
    INPUT_FILE,
    keep_default_na=False
)

print(
    f"\nInput dataset shape: {df.shape}"
)


# ============================================================
# 3. DASHBOARD COLUMNS
# ============================================================

dashboard_columns = [

    # Target
    "readmitted",
    "early_readmission",

    # Patient profile
    "race",
    "gender",
    "age",

    # Clinical activity
    "time_in_hospital",
    "num_lab_procedures",
    "num_procedures",
    "num_medications",
    "number_diagnoses",

    # Healthcare utilization
    "number_outpatient",
    "number_emergency",
    "number_inpatient",
    "outpatient_visits_group",
    "emergency_visits_group",
    "inpatient_visits_group",

    # Medication
    "diabetesMed",
    "change",
    "insulin",

    # Hospital operations
    "admission_type",
    "discharge_disposition",
    "admission_source",

    # Diagnosis
    "primary_diagnosis_category",
    "secondary_diagnosis_category",
    "tertiary_diagnosis_category"
]


# ============================================================
# 4. CHECK REQUIRED COLUMNS
# ============================================================

missing_columns = [
    column
    for column in dashboard_columns
    if column not in df.columns
]

if missing_columns:

    raise ValueError(
        "The following dashboard columns are missing:\n"
        + "\n".join(missing_columns)
    )


# ============================================================
# 5. CREATE DASHBOARD DATASET
# ============================================================

df_dashboard = df[
    dashboard_columns
].copy()


# ============================================================
# 6. FINAL VALIDATION
# ============================================================

print("\nPerforming dashboard dataset validation...")

total_missing = (
    df_dashboard.isna()
    .sum()
    .sum()
)

if total_missing != 0:

    missing_summary = (
        df_dashboard.isna()
        .sum()
    )

    missing_summary = (
        missing_summary[
            missing_summary > 0
        ]
        .sort_values(
            ascending=False
        )
    )

    raise ValueError(
        "Unexpected missing values found:\n"
        + missing_summary.to_string()
    )


# ============================================================
# 7. TARGET VALIDATION
# ============================================================

expected_target = (
    df_dashboard["readmitted"]
    .eq("<30")
    .astype(int)
)

target_mismatches = (
    df_dashboard["early_readmission"]
    != expected_target
).sum()


if target_mismatches != 0:

    raise ValueError(
        f"Target mismatches found: "
        f"{target_mismatches}"
    )


# ============================================================
# 8. DUPLICATE CHECK
# ============================================================

duplicate_rows = (
    df_dashboard
    .duplicated()
    .sum()
)


# ============================================================
# 9. TARGET SUMMARY
# ============================================================

target_counts = (
    df_dashboard["early_readmission"]
    .value_counts()
    .sort_index()
)

early_readmission_rate = (
    df_dashboard["early_readmission"]
    .mean()
    * 100
)


# ============================================================
# 10. SAVE DATASET
# ============================================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

os.makedirs(
    "results/analysis_results",
    exist_ok=True
)

df_dashboard.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# 11. CREATE QUALITY REPORT
# ============================================================

quality_lines = []

quality_lines.append(
    "DASHBOARD DATASET QUALITY REPORT"
)

quality_lines.append(
    "=" * 70
)

quality_lines.append(
    f"Source dataset: {INPUT_FILE}"
)

quality_lines.append(
    f"Dashboard dataset: {OUTPUT_FILE}"
)

quality_lines.append("")

quality_lines.append(
    f"Rows: {len(df_dashboard):,}"
)

quality_lines.append(
    f"Columns: {len(df_dashboard.columns)}"
)

quality_lines.append(
    f"Missing values: {total_missing}"
)

quality_lines.append(
    f"Duplicate analytical rows: {duplicate_rows}"
)

quality_lines.append(
    f"Target mismatches: {target_mismatches}"
)

quality_lines.append("")

quality_lines.append(
    "Early-readmission distribution:"
)

for value, count in target_counts.items():

    percentage = (
        count
        / len(df_dashboard)
        * 100
    )

    quality_lines.append(
        f"  {value}: {count:,} "
        f"({percentage:.2f}%)"
    )

quality_lines.append("")

quality_lines.append(
    f"Early-readmission rate: "
    f"{early_readmission_rate:.2f}%"
)

quality_lines.append("")

quality_lines.append(
    "Dashboard columns:"
)

for index, column in enumerate(
    df_dashboard.columns,
    start=1
):

    quality_lines.append(
        f"  {index:02d}. {column}"
    )

quality_lines.append("")

quality_lines.append(
    "=" * 70
)

if (
    total_missing == 0
    and target_mismatches == 0
):

    quality_lines.append(
        "DASHBOARD DATASET STATUS: PASS"
    )

else:

    quality_lines.append(
        "DASHBOARD DATASET STATUS: REVIEW REQUIRED"
    )


with open(
    QUALITY_FILE,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "\n".join(quality_lines)
    )


# ============================================================
# 12. FINAL OUTPUT
# ============================================================

print("\nDashboard dataset created successfully.")

print(
    f"Rows: {len(df_dashboard):,}"
)

print(
    f"Columns: {len(df_dashboard.columns)}"
)

print(
    f"Missing values: {total_missing}"
)

print(
    f"Duplicate analytical rows: "
    f"{duplicate_rows}"
)

print(
    f"Early-readmission rate: "
    f"{early_readmission_rate:.2f}%"
)

print(
    f"\nDashboard dataset saved to:"
    f"\n{OUTPUT_FILE}"
)

print(
    f"\nQuality report saved to:"
    f"\n{QUALITY_FILE}"
)

print("\n" + "=" * 70)