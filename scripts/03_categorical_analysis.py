# ============================================================
# Patient Readmission Analysis
# Stage 3: Categorical Variable Exploration
# ============================================================

import pandas as pd

# ------------------------------------------------------------
# 1. Load the raw dataset
# ------------------------------------------------------------

DATA_PATH = "data/raw/diabetic_data.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 70)
print("STAGE 3: CATEGORICAL VARIABLE EXPLORATION")
print("=" * 70)

print(f"\nDataset shape: {df.shape}")


# ------------------------------------------------------------
# 2. Explore important categorical variables
# ------------------------------------------------------------

categorical_columns = [
    "race",
    "gender",
    "age",
    "weight",
    "payer_code",
    "medical_specialty",
    "max_glu_serum",
    "A1Cresult",
    "change",
    "diabetesMed",
    "readmitted"
]

for column in categorical_columns:

    print("\n" + "=" * 70)
    print(f"COLUMN: {column}")
    print("=" * 70)

    print(f"Number of unique values: {df[column].nunique(dropna=False)}")

    print("\nValue counts:")
    print(df[column].value_counts(dropna=False).head(30))


# ------------------------------------------------------------
# 3. Explore coded categorical variables
# ------------------------------------------------------------

coded_columns = [
    "admission_type_id",
    "discharge_disposition_id",
    "admission_source_id"
]

for column in coded_columns:

    print("\n" + "=" * 70)
    print(f"CODED COLUMN: {column}")
    print("=" * 70)

    print(f"Number of unique values: {df[column].nunique()}")

    print("\nValue counts:")
    print(df[column].value_counts().sort_index())


# ------------------------------------------------------------
# 4. Completion message
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("CATEGORICAL ANALYSIS COMPLETE")
print("=" * 70)