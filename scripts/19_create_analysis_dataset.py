"""
Stage 8: Create Final Analysis Dataset

Purpose:
    Create a clean, analysis-ready dataset from the decoded dataset.

The analysis dataset:
    - Removes technical identifiers
    - Keeps clinically/business-relevant variables
    - Creates useful utilization categories
    - Creates broad ICD-9 diagnosis categories
    - Preserves the original readmission target
    - Preserves the binary early_readmission target
    - Performs final validation
    - Saves the final dataset separately

Important:
    Duplicate analytical rows can exist because encounter_id and
    patient_nbr are intentionally removed from this dataset.

    Source-level encounter uniqueness was already validated before
    creating this analysis dataset.
"""

import os
import pandas as pd


# ============================================================
# 1. PATHS
# ============================================================

INPUT_FILE = "data/processed/diabetic_data_decoded.csv"

OUTPUT_DIR = "data/processed"

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "patient_readmission_analysis.csv"
)

QUALITY_FILE = (
    "results/analysis_results/"
    "final_analysis_dataset_quality.txt"
)


# ============================================================
# 2. LOAD DATA
# ============================================================

print("=" * 70)
print("STAGE 8: CREATE FINAL ANALYSIS DATASET")
print("=" * 70)

df = pd.read_csv(
    INPUT_FILE,
    keep_default_na=False
)

print(f"\nInput dataset shape: {df.shape}")


# ============================================================
# 3. CREATE OUTPUT DIRECTORIES
# ============================================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

os.makedirs(
    "results/analysis_results",
    exist_ok=True
)


# ============================================================
# 4. CREATE UTILIZATION CATEGORIES
# ============================================================

print("\nCreating utilization categories...")


df["outpatient_visits_group"] = pd.cut(
    df["number_outpatient"],
    bins=[-1, 0, 1, 2, float("inf")],
    labels=["0", "1", "2", "3+"]
)

df["emergency_visits_group"] = pd.cut(
    df["number_emergency"],
    bins=[-1, 0, 1, 2, float("inf")],
    labels=["0", "1", "2", "3+"]
)

df["inpatient_visits_group"] = pd.cut(
    df["number_inpatient"],
    bins=[-1, 0, 1, 2, float("inf")],
    labels=["0", "1", "2", "3+"]
)


# ============================================================
# 5. CREATE BROAD ICD-9 DIAGNOSIS CATEGORIES
# ============================================================

print("Creating broad diagnosis categories...")


def classify_icd9(code):
    """
    Classify an ICD-9 diagnosis code into a broad category.
    """

    if code in ["", "?", "Unknown", "NULL"]:
        return "Unknown / Other"

    code = str(code).strip()

    # V-codes
    if code.startswith("V"):
        return "Supplementary / External Factors"

    # E-codes
    if code.startswith("E"):
        return "Injury / External Causes"

    # Numeric ICD-9 codes
    try:
        number = float(code)
    except ValueError:
        return "Unknown / Other"

    # 001-139
    if 1 <= number < 140:
        return "Infectious / Parasitic"

    # 140-239
    if 140 <= number < 240:
        return "Neoplasms"

    # 240-279
    if 240 <= number < 280:
        return "Endocrine / Metabolic"

    # 280-289
    if 280 <= number < 290:
        return "Blood / Blood-forming Organs"

    # 290-319
    if 290 <= number < 320:
        return "Mental Disorders"

    # 320-359
    if 320 <= number < 360:
        return "Nervous System"

    # 360-389
    if 360 <= number < 390:
        return "Sense Organs"

    # 390-459
    if 390 <= number < 460:
        return "Circulatory"

    # 460-519
    if 460 <= number < 520:
        return "Respiratory"

    # 520-579
    if 520 <= number < 580:
        return "Digestive"

    # 580-629
    if 580 <= number < 630:
        return "Genitourinary"

    # 630-679
    if 630 <= number < 680:
        return "Pregnancy / Childbirth"

    # 680-709
    if 680 <= number < 710:
        return "Skin / Subcutaneous Tissue"

    # 710-739
    if 710 <= number < 740:
        return "Musculoskeletal"

    # 740-759
    if 740 <= number < 760:
        return "Congenital Conditions"

    # 760-779
    if 760 <= number < 780:
        return "Perinatal Conditions"

    # 780-799
    if 780 <= number < 800:
        return "Symptoms / Signs / Abnormal Findings"

    # 800-999
    if 800 <= number < 1000:
        return "Injury / Poisoning"

    return "Unknown / Other"


df["primary_diagnosis_category"] = (
    df["diag_1"].apply(classify_icd9)
)

df["secondary_diagnosis_category"] = (
    df["diag_2"].apply(classify_icd9)
)

df["tertiary_diagnosis_category"] = (
    df["diag_3"].apply(classify_icd9)
)


# ============================================================
# 6. REMOVE TECHNICAL IDENTIFIERS
# ============================================================

print("Removing technical identifiers...")


technical_identifier_columns = [
    "encounter_id",
    "patient_nbr"
]

df_analysis = df.drop(
    columns=technical_identifier_columns,
    errors="ignore"
).copy()


# ============================================================
# 7. REMOVE RAW ADMINISTRATIVE ID CODES
# ============================================================

administrative_id_columns = [
    "admission_type_id",
    "discharge_disposition_id",
    "admission_source_id"
]

df_analysis = df_analysis.drop(
    columns=administrative_id_columns,
    errors="ignore"
)


# ============================================================
# 8. REMOVE RAW DIAGNOSIS CODE COLUMNS
# ============================================================

raw_diagnosis_columns = [
    "diag_1",
    "diag_2",
    "diag_3"
]

df_analysis = df_analysis.drop(
    columns=raw_diagnosis_columns,
    errors="ignore"
)


# ============================================================
# 9. REMOVE ZERO-VARIANCE MEDICATION VARIABLES
# ============================================================

zero_variance_columns = [
    "examide",
    "citoglipton"
]

df_analysis = df_analysis.drop(
    columns=zero_variance_columns,
    errors="ignore"
)


# ============================================================
# 10. CHECK TARGET VARIABLES
# ============================================================

print("Checking target variables...")


if "readmitted" not in df_analysis.columns:
    raise ValueError(
        "Target column 'readmitted' is missing."
    )

if "early_readmission" not in df_analysis.columns:
    raise ValueError(
        "Target column 'early_readmission' is missing."
    )


# ============================================================
# 11. CHECK EXPECTED ANALYSIS COLUMNS
# ============================================================

expected_columns = [
    "race",
    "gender",
    "age",
    "time_in_hospital",
    "payer_code",
    "medical_specialty",
    "num_lab_procedures",
    "num_procedures",
    "num_medications",
    "number_outpatient",
    "number_emergency",
    "number_inpatient",
    "number_diagnoses",
    "change",
    "diabetesMed",
    "insulin",
    "readmitted",
    "early_readmission",
    "admission_type",
    "discharge_disposition",
    "admission_source"
]

missing_expected_columns = [
    column
    for column in expected_columns
    if column not in df_analysis.columns
]

if missing_expected_columns:
    raise ValueError(
        "Missing expected analysis columns: "
        + ", ".join(missing_expected_columns)
    )


# ============================================================
# 12. CONVERT UTILIZATION GROUPS TO STRING
# ============================================================

category_columns = [
    "outpatient_visits_group",
    "emergency_visits_group",
    "inpatient_visits_group"
]

for column in category_columns:

    if column in df_analysis.columns:

        df_analysis[column] = (
            df_analysis[column]
            .astype(str)
        )


# ============================================================
# 13. FINAL MISSING-VALUE CHECK
# ============================================================

print("Performing final quality checks...")


total_missing = (
    df_analysis.isna()
    .sum()
    .sum()
)

if total_missing != 0:

    missing_columns = (
        df_analysis.isna()
        .sum()
    )

    missing_columns = (
        missing_columns[
            missing_columns > 0
        ]
        .sort_values(
            ascending=False
        )
    )

    raise ValueError(
        "Unexpected NaN values found:\n"
        + missing_columns.to_string()
    )


# ============================================================
# 14. CHECK QUESTION-MARK VALUES
# ============================================================

question_mark_counts = {}

for column in df_analysis.columns:

    count = (
        df_analysis[column]
        .astype(str)
        .eq("?")
        .sum()
    )

    if count > 0:

        question_mark_counts[column] = int(
            count
        )


# ============================================================
# 15. CHECK ANALYSIS-LEVEL DUPLICATES
# ============================================================

analysis_duplicate_rows = (
    df_analysis
    .duplicated()
    .sum()
)

print(
    f"Analysis-level duplicate rows: "
    f"{analysis_duplicate_rows}"
)

print(
    "Note: These duplicates are allowed because "
    "encounter_id and patient_nbr were removed."
)


# ============================================================
# 16. CHECK TARGET DISTRIBUTION
# ============================================================

target_counts = (
    df_analysis["early_readmission"]
    .value_counts()
    .sort_index()
)

target_rate = (
    df_analysis["early_readmission"]
    .mean()
    * 100
)


# ============================================================
# 17. CHECK TARGET CONSISTENCY
# ============================================================

expected_target = (
    df_analysis["readmitted"]
    .eq("<30")
    .astype(int)
)

target_mismatches = (
    df_analysis["early_readmission"]
    != expected_target
).sum()


# ============================================================
# 18. FINAL DATASET SUMMARY
# ============================================================

print("\nFinal analysis dataset")
print("-" * 70)

print(
    f"Rows: {len(df_analysis):,}"
)

print(
    f"Columns: {len(df_analysis.columns)}"
)

print(
    f"Analysis-level duplicate rows: "
    f"{analysis_duplicate_rows}"
)

print(
    f"Total missing values: {total_missing}"
)

print(
    f"Target mismatches: {target_mismatches}"
)

print(
    f"Early-readmission rate: {target_rate:.2f}%"
)


# ============================================================
# 19. SAVE FINAL ANALYSIS DATASET
# ============================================================

df_analysis.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# 20. CREATE QUALITY REPORT
# ============================================================

quality_lines = []

quality_lines.append(
    "STAGE 8: FINAL ANALYSIS DATASET QUALITY REPORT"
)

quality_lines.append("=" * 70)

quality_lines.append(
    f"Input file: {INPUT_FILE}"
)

quality_lines.append(
    f"Output file: {OUTPUT_FILE}"
)

quality_lines.append("")

quality_lines.append(
    f"Rows: {len(df_analysis):,}"
)

quality_lines.append(
    f"Columns: {len(df_analysis.columns)}"
)

quality_lines.append("")

quality_lines.append(
    f"Analysis-level duplicate rows: "
    f"{analysis_duplicate_rows}"
)

quality_lines.append(
    "Duplicate interpretation: "
    "Allowed because encounter_id and patient_nbr "
    "were intentionally removed."
)

quality_lines.append(
    "Source-level encounter uniqueness was validated "
    "before creating this analysis dataset."
)

quality_lines.append("")

quality_lines.append(
    f"Total NaN values: {total_missing}"
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
        / len(df_analysis)
        * 100
    )

    quality_lines.append(
        f"  {value}: {count:,} "
        f"({percentage:.2f}%)"
    )


# ============================================================
# 21. QUESTION-MARK REPORT
# ============================================================

quality_lines.append("")

quality_lines.append(
    "Question-mark values remaining:"
)

if question_mark_counts:

    for column, count in question_mark_counts.items():

        quality_lines.append(
            f"  {column}: {count:,}"
        )

else:

    quality_lines.append(
        "  None"
    )


# ============================================================
# 22. FINAL COLUMN LIST
# ============================================================

quality_lines.append("")

quality_lines.append(
    "Final analysis columns:"
)

for i, column in enumerate(
    df_analysis.columns,
    start=1
):

    quality_lines.append(
        f"  {i:02d}. {column}"
    )


# ============================================================
# 23. FINAL QUALITY STATUS
# ============================================================

quality_lines.append("")

quality_lines.append(
    "=" * 70
)


if (
    total_missing == 0
    and target_mismatches == 0
):

    quality_lines.append(
        "FINAL QUALITY STATUS: PASS"
    )

else:

    quality_lines.append(
        "FINAL QUALITY STATUS: REVIEW REQUIRED"
    )


# ============================================================
# 24. SAVE QUALITY REPORT
# ============================================================

with open(
    QUALITY_FILE,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "\n".join(quality_lines)
    )


# ============================================================
# 25. FINAL MESSAGE
# ============================================================

print(
    f"\nFinal analysis dataset saved to:"
    f"\n{OUTPUT_FILE}"
)

print(
    f"Quality report saved to:"
    f"\n{QUALITY_FILE}"
)

print("\nStage 8 completed successfully.")