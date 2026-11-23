# ============================================================
# Patient Readmission Analysis
# Stage 5D: Final Data Quality Audit
# ============================================================

import pandas as pd


# ------------------------------------------------------------
# 1. File paths
# ------------------------------------------------------------

DATA_PATH = "data/processed/diabetic_data_decoded.csv"
OUTPUT_PATH = "results/analysis_results/final_data_quality_audit.txt"


# ------------------------------------------------------------
# 2. Load decoded dataset
# ------------------------------------------------------------

# keep_default_na=False is important.
# The dataset intentionally contains the literal category "NULL"
# in the decoded administrative variables.
df = pd.read_csv(
    DATA_PATH,
    keep_default_na=False
)

print("=" * 70)
print("STAGE 5D: FINAL DATA QUALITY AUDIT")
print("=" * 70)

print(f"\nDataset shape: {df.shape}")


# ------------------------------------------------------------
# 3. Dataset structure
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("DATASET STRUCTURE")
print("=" * 70)

print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")

print("\nColumn names:")

for column in df.columns:
    print(column)


# ------------------------------------------------------------
# 4. Data types
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("DATA TYPES")
print("=" * 70)

print(df.dtypes.to_string())


# ------------------------------------------------------------
# 5. Missing-value audit
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("MISSING VALUE AUDIT")
print("=" * 70)

missing_summary = pd.DataFrame({
    "missing_values": df.isna().sum(),
    "missing_percentage": (
        df.isna().mean() * 100
    ).round(2)
})

missing_summary = missing_summary[
    missing_summary["missing_values"] > 0
].sort_values(
    "missing_values",
    ascending=False
)

if missing_summary.empty:
    print("No NaN values found.")
else:
    print(missing_summary.to_string())


# ------------------------------------------------------------
# 6. Question-mark audit
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("QUESTION-MARK AUDIT")
print("=" * 70)

question_mark_summary = {}

for column in df.columns:

    count = (
        df[column]
        .astype(str)
        .eq("?")
        .sum()
    )

    if count > 0:
        question_mark_summary[column] = count


if question_mark_summary:

    for column, count in question_mark_summary.items():
        print(f"{column}: {count}")

else:
    print("No '?' values found.")


# ------------------------------------------------------------
# 7. Encounter uniqueness
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("ENCOUNTER ID CHECK")
print("=" * 70)

unique_encounters = df["encounter_id"].nunique()

duplicate_encounters = (
    df["encounter_id"].duplicated().sum()
)

print(
    f"Total encounter records: {len(df):,}"
)

print(
    f"Unique encounter IDs: {unique_encounters:,}"
)

print(
    f"Duplicate encounter IDs: {duplicate_encounters:,}"
)


# ------------------------------------------------------------
# 8. Patient uniqueness
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("PATIENT ID CHECK")
print("=" * 70)

unique_patients = df["patient_nbr"].nunique()

print(
    f"Unique patients: {unique_patients:,}"
)

print(
    f"Encounters per patient: "
    f"{len(df) / unique_patients:.2f}"
)


# ------------------------------------------------------------
# 9. Complete duplicate-row check
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("DUPLICATE ROW CHECK")
print("=" * 70)

duplicate_rows = df.duplicated().sum()

print(
    f"Duplicate complete rows: {duplicate_rows:,}"
)


# ------------------------------------------------------------
# 10. Early-readmission target audit
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("EARLY READMISSION TARGET AUDIT")
print("=" * 70)

print("\nOriginal readmitted values:")

print(
    df["readmitted"]
    .value_counts(dropna=False)
    .to_string()
)

print("\nEarly readmission values:")

print(
    df["early_readmission"]
    .value_counts(dropna=False)
    .sort_index()
    .to_string()
)

print("\nEarly readmission percentage:")

early_rate = (
    df["early_readmission"].mean() * 100
)

print(f"{early_rate:.2f}%")


# ------------------------------------------------------------
# 11. Verify target logic
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TARGET LOGIC CHECK")
print("=" * 70)

expected_target = (
    df["readmitted"] == "<30"
).astype(int)

target_mismatches = (
    df["early_readmission"] != expected_target
).sum()

print(
    f"Target mismatches: {target_mismatches:,}"
)


# ------------------------------------------------------------
# 12. Numerical range audit
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("NUMERICAL RANGE AUDIT")
print("=" * 70)

numerical_columns = [
    "time_in_hospital",
    "num_lab_procedures",
    "num_procedures",
    "num_medications",
    "number_outpatient",
    "number_emergency",
    "number_inpatient",
    "number_diagnoses"
]

range_summary = pd.DataFrame({
    "min": df[numerical_columns].min(),
    "max": df[numerical_columns].max(),
    "mean": df[numerical_columns].mean().round(2),
    "median": df[numerical_columns].median()
})

print(
    range_summary.to_string()
)


# ------------------------------------------------------------
# 13. Important categorical audit
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("IMPORTANT CATEGORICAL VARIABLES")
print("=" * 70)

categorical_columns = [
    "race",
    "gender",
    "age",
    "payer_code",
    "medical_specialty",
    "change",
    "diabetesMed",
    "readmitted",
    "early_readmission",
    "admission_type",
    "discharge_disposition",
    "admission_source"
]

for column in categorical_columns:

    print("\n" + "-" * 70)
    print(column)
    print("-" * 70)

    print(
        df[column]
        .value_counts(dropna=False)
        .head(20)
        .to_string()
    )


# ------------------------------------------------------------
# 14. Verify decoded administrative columns
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("ADMINISTRATIVE MAPPING CHECK")
print("=" * 70)

mapping_columns = [
    "admission_type",
    "discharge_disposition",
    "admission_source"
]

for column in mapping_columns:

    missing_count = df[column].isna().sum()

    print(
        f"{column}: "
        f"{missing_count} actual NaN values"
    )


# ------------------------------------------------------------
# 15. Verify literal NULL categories
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("LITERAL NULL CATEGORY CHECK")
print("=" * 70)

for column in mapping_columns:

    null_count = (
        df[column] == "NULL"
    ).sum()

    print(
        f"{column}: "
        f"{null_count:,} literal NULL values"
    )


# ------------------------------------------------------------
# 16. Final quality summary
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("FINAL QUALITY SUMMARY")
print("=" * 70)

checks = {
    "Rows present": len(df) == 101766,

    "Unique encounter IDs":
        unique_encounters == 101766,

    "Duplicate encounter IDs":
        duplicate_encounters == 0,

    "Duplicate complete rows":
        duplicate_rows == 0,

    "Target mismatches":
        target_mismatches == 0,

    "Unintended NaN values":
        df.isna().sum().sum() == 0,

    "Unmapped admission types":
        df["admission_type"].isna().sum() == 0,

    "Unmapped discharge dispositions":
        df["discharge_disposition"].isna().sum() == 0,

    "Unmapped admission sources":
        df["admission_source"].isna().sum() == 0
}

for check, result in checks.items():

    status = "PASS" if result else "REVIEW"

    print(
        f"{check:35s}: {status}"
    )


# ------------------------------------------------------------
# 17. Final completion message
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("FINAL DATA QUALITY AUDIT COMPLETE")
print("=" * 70)