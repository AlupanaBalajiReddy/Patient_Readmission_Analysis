# ============================================================
# Patient Readmission Analysis
# Stage 2: Missing Data Analysis
# ============================================================

import pandas as pd


# ------------------------------------------------------------
# 1. Load raw dataset
# ------------------------------------------------------------

DATA_PATH = "data/raw/diabetic_data.csv"

df = pd.read_csv(DATA_PATH)


# ------------------------------------------------------------
# 2. Calculate '?' counts
# ------------------------------------------------------------

question_mark_counts = (df == "?").sum()


# ------------------------------------------------------------
# 3. Calculate NaN counts
# ------------------------------------------------------------

nan_counts = df.isna().sum()


# ------------------------------------------------------------
# 4. Combine both types of missing values
# ------------------------------------------------------------

missing_summary = pd.DataFrame({
    "question_mark_count": question_mark_counts,
    "nan_count": nan_counts
})


# ------------------------------------------------------------
# 5. Total missing values
# ------------------------------------------------------------

missing_summary["total_missing"] = (
    missing_summary["question_mark_count"]
    + missing_summary["nan_count"]
)


# ------------------------------------------------------------
# 6. Missing percentage
# ------------------------------------------------------------

missing_summary["missing_percentage"] = (
    missing_summary["total_missing"]
    / len(df)
    * 100
)


# ------------------------------------------------------------
# 7. Keep only columns containing missing values
# ------------------------------------------------------------

missing_summary = missing_summary[
    missing_summary["total_missing"] > 0
].sort_values(
    by="missing_percentage",
    ascending=False
)


# ------------------------------------------------------------
# 8. Display results
# ------------------------------------------------------------

print("\n" + "=" * 80)
print("MISSING DATA SUMMARY")
print("=" * 80)

print(
    missing_summary.to_string(
        float_format=lambda x: f"{x:.2f}"
    )
)


# ------------------------------------------------------------
# 9. Save results
# ------------------------------------------------------------

OUTPUT_PATH = "results/analysis_results/missing_data_summary.csv"

missing_summary.to_csv(OUTPUT_PATH)

print("\n" + "=" * 80)
print("RESULT SAVED")
print("=" * 80)

print(f"Saved to: {OUTPUT_PATH}")