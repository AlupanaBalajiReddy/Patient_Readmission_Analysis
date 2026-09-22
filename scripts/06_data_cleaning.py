# ============================================================
# Patient Readmission Analysis
# Stage 5B: Data Cleaning
# ============================================================

import pandas as pd

# ------------------------------------------------------------
# 1. File paths
# ------------------------------------------------------------

RAW_DATA_PATH = "data/raw/diabetic_data.csv"
CLEANED_DATA_PATH = "data/processed/diabetic_data_cleaned.csv"


# ------------------------------------------------------------
# 2. Load raw dataset
# ------------------------------------------------------------

df = pd.read_csv(RAW_DATA_PATH)

print("=" * 70)
print("STAGE 5B: DATA CLEANING")
print("=" * 70)

print(f"\nOriginal dataset shape: {df.shape}")


# ------------------------------------------------------------
# 3. Create a copy
# ------------------------------------------------------------

cleaned_df = df.copy()


# ------------------------------------------------------------
# 4. Standardize selected missing-value representations
# ------------------------------------------------------------

# In these categorical columns, "?" represents an
# unavailable/unknown category.
unknown_columns = [
    "race",
    "payer_code",
    "medical_specialty"
]

for column in unknown_columns:
    cleaned_df[column] = cleaned_df[column].replace("?", "Unknown")


# Handle the three invalid gender records explicitly.
cleaned_df["gender"] = cleaned_df["gender"].replace(
    "Unknown/Invalid",
    "Unknown"
)


# ------------------------------------------------------------
# 5. Remove variables excluded from primary analysis
# ------------------------------------------------------------

columns_to_remove = [
    "weight",
    "max_glu_serum",
    "A1Cresult",
    "examide",
    "citoglipton"
]

cleaned_df = cleaned_df.drop(
    columns=columns_to_remove
)


# ------------------------------------------------------------
# 6. Create binary early-readmission target
# ------------------------------------------------------------

# <30 means readmission occurred within 30 days.
# NO and >30 are treated as not early-readmitted.

cleaned_df["early_readmission"] = (
    cleaned_df["readmitted"] == "<30"
).astype(int)


# ------------------------------------------------------------
# 7. Verify target creation
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("EARLY READMISSION TARGET")
print("=" * 70)

print("\nOriginal readmitted distribution:")
print(
    cleaned_df["readmitted"]
    .value_counts()
    .sort_index()
)

print("\nNew early_readmission distribution:")
print(
    cleaned_df["early_readmission"]
    .value_counts()
    .sort_index()
)

print("\nEarly readmission percentage:")
print(
    f"{cleaned_df['early_readmission'].mean() * 100:.2f}%"
)


# ------------------------------------------------------------
# 8. Check missing values after cleaning
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("MISSING VALUES AFTER CLEANING")
print("=" * 70)

missing_summary = (
    cleaned_df.isna()
    .sum()
    .sort_values(ascending=False)
)

print(
    missing_summary[
        missing_summary > 0
    ].to_string()
    if (missing_summary > 0).any()
    else "No NaN values remain."
)


# ------------------------------------------------------------
# 9. Check remaining question marks
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("QUESTION MARK CHECK")
print("=" * 70)

question_mark_counts = {}

for column in cleaned_df.columns:
    count = (cleaned_df[column] == "?").sum()

    if count > 0:
        question_mark_counts[column] = count

if question_mark_counts:
    for column, count in question_mark_counts.items():
        print(f"{column}: {count}")
else:
    print("No '?' values remain.")


# ------------------------------------------------------------
# 10. Check duplicate rows
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("DUPLICATE CHECK")
print("=" * 70)

duplicate_count = cleaned_df.duplicated().sum()

print(f"Duplicate complete rows: {duplicate_count}")


# ------------------------------------------------------------
# 11. Verify encounter count
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("ROW COUNT CHECK")
print("=" * 70)

print(f"Original rows: {len(df):,}")
print(f"Cleaned rows:  {len(cleaned_df):,}")

if len(df) == len(cleaned_df):
    print("Row count preserved: YES")
else:
    print("Row count preserved: NO")


# ------------------------------------------------------------
# 12. Verify important columns
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("CLEANED DATASET COLUMNS")
print("=" * 70)

print(f"Number of columns: {len(cleaned_df.columns)}")

for column in cleaned_df.columns:
    print(column)


# ------------------------------------------------------------
# 13. Save cleaned dataset
# ------------------------------------------------------------

cleaned_df.to_csv(
    CLEANED_DATA_PATH,
    index=False
)

print("\n" + "=" * 70)
print("CLEANED DATASET SAVED")
print("=" * 70)

print(f"Output file: {CLEANED_DATA_PATH}")
print(f"Final shape: {cleaned_df.shape}")


# ------------------------------------------------------------
# 14. Completion message
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("DATA CLEANING COMPLETE")
print("=" * 70)