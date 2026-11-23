# ============================================================
# Patient Readmission Analysis
# Stage 4: Numerical Variable Exploration
# ============================================================

import pandas as pd

# ------------------------------------------------------------
# 1. Load the raw dataset
# ------------------------------------------------------------

DATA_PATH = "data/raw/diabetic_data.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 70)
print("STAGE 4: NUMERICAL VARIABLE EXPLORATION")
print("=" * 70)

print(f"\nDataset shape: {df.shape}")


# ------------------------------------------------------------
# 2. Identify numerical columns
# ------------------------------------------------------------

numerical_columns = [
    "encounter_id",
    "patient_nbr",
    "time_in_hospital",
    "num_lab_procedures",
    "num_procedures",
    "num_medications",
    "number_outpatient",
    "number_emergency",
    "number_inpatient",
    "number_diagnoses"
]


# ------------------------------------------------------------
# 3. Basic statistical summary
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("NUMERICAL VARIABLE SUMMARY")
print("=" * 70)

print(
    df[numerical_columns]
    .describe()
    .T
    .to_string()
)


# ------------------------------------------------------------
# 4. Median and missing values
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("MEDIAN AND MISSING VALUES")
print("=" * 70)

summary = pd.DataFrame({
    "mean": df[numerical_columns].mean(),
    "median": df[numerical_columns].median(),
    "std": df[numerical_columns].std(),
    "min": df[numerical_columns].min(),
    "max": df[numerical_columns].max(),
    "missing": df[numerical_columns].isna().sum()
})

print(summary.to_string())


# ------------------------------------------------------------
# 5. Unique values
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("NUMBER OF UNIQUE VALUES")
print("=" * 70)

for column in numerical_columns:

    print(
        f"{column:25s} : "
        f"{df[column].nunique(dropna=False)} unique values"
    )


# ------------------------------------------------------------
# 6. Detailed value counts for discrete variables
# ------------------------------------------------------------

count_columns = [
    "time_in_hospital",
    "num_procedures",
    "number_outpatient",
    "number_emergency",
    "number_inpatient",
    "number_diagnoses"
]

for column in count_columns:

    print("\n" + "=" * 70)
    print(f"VALUE COUNTS: {column}")
    print("=" * 70)

    print(df[column].value_counts().sort_index().to_string())


# ------------------------------------------------------------
# 7. Check potentially important ranges
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("RANGE CHECK")
print("=" * 70)

for column in numerical_columns:

    print(
        f"{column:25s} | "
        f"Min: {df[column].min()} | "
        f"Max: {df[column].max()}"
    )


# ------------------------------------------------------------
# 8. Completion message
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("NUMERICAL ANALYSIS COMPLETE")
print("=" * 70)