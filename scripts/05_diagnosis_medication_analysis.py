# ============================================================
# Patient Readmission Analysis
# Stage 5A: Diagnosis & Medication Structure Exploration
# ============================================================

import pandas as pd

# ------------------------------------------------------------
# 1. Load the raw dataset
# ------------------------------------------------------------

DATA_PATH = "data/raw/diabetic_data.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 70)
print("STAGE 5A: DIAGNOSIS & MEDICATION STRUCTURE EXPLORATION")
print("=" * 70)

print(f"\nDataset shape: {df.shape}")


# ------------------------------------------------------------
# 2. Explore diagnosis columns
# ------------------------------------------------------------

diagnosis_columns = [
    "diag_1",
    "diag_2",
    "diag_3"
]

for column in diagnosis_columns:

    print("\n" + "=" * 70)
    print(f"DIAGNOSIS COLUMN: {column}")
    print("=" * 70)

    print(f"Data type: {df[column].dtype}")

    print(
        f"Number of unique values: "
        f"{df[column].nunique(dropna=False)}"
    )

    print(
        f"Missing values (NaN): "
        f"{df[column].isna().sum()}"
    )

    print(
        f"Question-mark values: "
        f"{(df[column] == '?').sum()}"
    )

    print("\nTop 30 values:")
    print(df[column].value_counts(dropna=False).head(30))


# ------------------------------------------------------------
# 3. Identify medication columns
# ------------------------------------------------------------

medication_columns = [
    "metformin",
    "repaglinide",
    "nateglinide",
    "chlorpropamide",
    "glimepiride",
    "acetohexamide",
    "glipizide",
    "glyburide",
    "tolbutamide",
    "pioglitazone",
    "rosiglitazone",
    "acarbose",
    "miglitol",
    "troglitazone",
    "tolazamide",
    "examide",
    "citoglipton",
    "insulin",
    "glyburide-metformin",
    "glipizide-metformin",
    "glimepiride-pioglitazone",
    "metformin-rosiglitazone",
    "metformin-pioglitazone"
]


# ------------------------------------------------------------
# 4. Verify medication columns exist
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("MEDICATION COLUMNS")
print("=" * 70)

existing_medication_columns = []

for column in medication_columns:

    if column in df.columns:
        existing_medication_columns.append(column)
        print(f"{column:30s} : FOUND")
    else:
        print(f"{column:30s} : NOT FOUND")


# ------------------------------------------------------------
# 5. Explore medication values
# ------------------------------------------------------------

for column in existing_medication_columns:

    print("\n" + "=" * 70)
    print(f"MEDICATION: {column}")
    print("=" * 70)

    print(
        f"Number of unique values: "
        f"{df[column].nunique(dropna=False)}"
    )

    print("\nValue counts:")
    print(df[column].value_counts(dropna=False).to_string())


# ------------------------------------------------------------
# 6. Create medication structure summary
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("MEDICATION STRUCTURE SUMMARY")
print("=" * 70)

medication_summary = pd.DataFrame({
    "unique_values": [
        df[column].nunique(dropna=False)
        for column in existing_medication_columns
    ],
    "missing_values": [
        df[column].isna().sum()
        for column in existing_medication_columns
    ],
    "question_mark_values": [
        (df[column] == "?").sum()
        for column in existing_medication_columns
    ]
}, index=existing_medication_columns)

print(medication_summary.to_string())


# ------------------------------------------------------------
# 7. Explore the overall medication-count variable
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("NUM_MEDICATIONS")
print("=" * 70)

print(f"Mean: {df['num_medications'].mean():.2f}")
print(f"Median: {df['num_medications'].median():.2f}")
print(f"Minimum: {df['num_medications'].min()}")
print(f"Maximum: {df['num_medications'].max()}")

print("\nValue counts:")
print(
    df["num_medications"]
    .value_counts()
    .sort_index()
    .to_string()
)


# ------------------------------------------------------------
# 8. Completion message
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("DIAGNOSIS & MEDICATION ANALYSIS COMPLETE")
print("=" * 70)