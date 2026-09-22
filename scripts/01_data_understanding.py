# ============================================================
# Patient Readmission Analysis
# Stage 1: Data Understanding
# ============================================================

import pandas as pd


# ------------------------------------------------------------
# 1. Load the dataset
# ------------------------------------------------------------

DATA_PATH = "data/raw/diabetic_data.csv"

df = pd.read_csv(DATA_PATH)


# ------------------------------------------------------------
# 2. Basic dataset dimensions
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("1. DATASET DIMENSIONS")
print("=" * 60)

print(f"Number of rows    : {df.shape[0]}")
print(f"Number of columns : {df.shape[1]}")


# ------------------------------------------------------------
# 3. Display the first 5 rows
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("2. FIRST 5 ROWS")
print("=" * 60)

print(df.head())


# ------------------------------------------------------------
# 4. Display all column names
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("3. COLUMN NAMES")
print("=" * 60)

for i, column in enumerate(df.columns, start=1):
    print(f"{i:2}. {column}")


# ------------------------------------------------------------
# 5. Data types
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("4. DATA TYPES")
print("=" * 60)

print(df.dtypes)


# ------------------------------------------------------------
# 6. Dataset information
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("5. DATASET INFORMATION")
print("=" * 60)

df.info()


# ------------------------------------------------------------
# 7. Number of unique patients
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("6. UNIQUE IDENTIFIERS")
print("=" * 60)

print(f"Unique encounter IDs : {df['encounter_id'].nunique()}")
print(f"Unique patient IDs   : {df['patient_nbr'].nunique()}")


# ------------------------------------------------------------
# 8. Check duplicate rows
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("7. DUPLICATE CHECK")
print("=" * 60)

duplicate_rows = df.duplicated().sum()

print(f"Duplicate rows : {duplicate_rows}")


# ------------------------------------------------------------
# 9. Missing values represented by '?'
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("8. '?' VALUES")
print("=" * 60)

question_mark_counts = (df == "?").sum()

question_mark_counts = question_mark_counts[
    question_mark_counts > 0
].sort_values(ascending=False)

print(question_mark_counts)


# ------------------------------------------------------------
# 10. Standard missing-value counts
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("9. NaN / NULL VALUES")
print("=" * 60)

missing_values = df.isnull().sum()

missing_values = missing_values[
    missing_values > 0
].sort_values(ascending=False)

if missing_values.empty:
    print("No standard NaN values found.")
else:
    print(missing_values)


# ------------------------------------------------------------
# 11. Readmission categories
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("10. READMISSION CATEGORIES")
print("=" * 60)

print(df["readmitted"].value_counts())

print("\nReadmission percentages:")
print(df["readmitted"].value_counts(normalize=True).mul(100).round(2))


# ------------------------------------------------------------
# 12. Basic numerical summary
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("11. NUMERICAL SUMMARY")
print("=" * 60)

print(df.describe())


# ------------------------------------------------------------
# 13. Final confirmation
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DATA UNDERSTANDING COMPLETE")
print("=" * 60)

print("The raw dataset has been loaded successfully.")
print("No changes have been made to the original dataset.")