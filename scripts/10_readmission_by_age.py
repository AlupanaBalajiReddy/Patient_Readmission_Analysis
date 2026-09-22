# ============================================================
# Patient Readmission Analysis
# Stage 6B: Readmission by Age Group
# ============================================================

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ------------------------------------------------------------
# 1. File paths
# ------------------------------------------------------------

DATA_PATH = "data/processed/diabetic_data_decoded.csv"

FIGURE_PATH = (
    "results/figures/"
    "early_readmission_rate_by_age.png"
)

RESULT_PATH = (
    "results/analysis_results/"
    "readmission_by_age.txt"
)


# ------------------------------------------------------------
# 2. Create output directories
# ------------------------------------------------------------

os.makedirs(
    "results/figures",
    exist_ok=True
)

os.makedirs(
    "results/analysis_results",
    exist_ok=True
)


# ------------------------------------------------------------
# 3. Load dataset
# ------------------------------------------------------------

df = pd.read_csv(
    DATA_PATH,
    keep_default_na=False
)

print("=" * 70)
print("STAGE 6B: READMISSION BY AGE GROUP")
print("=" * 70)

print(
    f"\nDataset shape: {df.shape}"
)


# ------------------------------------------------------------
# 4. Define correct age-group order
# ------------------------------------------------------------

age_order = [
    "[0-10)",
    "[10-20)",
    "[20-30)",
    "[30-40)",
    "[40-50)",
    "[50-60)",
    "[60-70)",
    "[70-80)",
    "[80-90)",
    "[90-100)"
]


# ------------------------------------------------------------
# 5. Verify age categories
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("AGE GROUP CHECK")
print("=" * 70)

print("\nAge groups present in dataset:")

print(
    df["age"]
    .value_counts()
    .reindex(age_order)
    .to_string()
)


# ------------------------------------------------------------
# 6. Calculate age-group summary
# ------------------------------------------------------------

age_summary = (
    df.groupby(
        "age",
        observed=False
    )
    .agg(
        total_encounters=(
            "encounter_id",
            "count"
        ),
        early_readmissions=(
            "early_readmission",
            "sum"
        )
    )
    .reindex(age_order)
)


# ------------------------------------------------------------
# 7. Calculate early readmission rate
# ------------------------------------------------------------

age_summary["early_readmission_rate"] = (
    age_summary["early_readmissions"]
    / age_summary["total_encounters"]
    * 100
).round(2)


# ------------------------------------------------------------
# 8. Calculate non-early-readmission encounters
# ------------------------------------------------------------

age_summary["non_early_readmissions"] = (
    age_summary["total_encounters"]
    - age_summary["early_readmissions"]
)


# ------------------------------------------------------------
# 9. Display summary
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("READMISSION BY AGE GROUP")
print("=" * 70)

print(
    age_summary.to_string()
)


# ------------------------------------------------------------
# 10. Identify highest and lowest observed rates
# ------------------------------------------------------------

highest_rate_age = (
    age_summary["early_readmission_rate"]
    .idxmax()
)

highest_rate = (
    age_summary["early_readmission_rate"]
    .max()
)

lowest_rate_age = (
    age_summary["early_readmission_rate"]
    .idxmin()
)

lowest_rate = (
    age_summary["early_readmission_rate"]
    .min()
)


print("\n" + "=" * 70)
print("OBSERVED AGE-GROUP RATES")
print("=" * 70)

print(
    f"Highest observed early readmission rate: "
    f"{highest_rate_age} ({highest_rate:.2f}%)"
)

print(
    f"Lowest observed early readmission rate: "
    f"{lowest_rate_age} ({lowest_rate:.2f}%)"
)


# ------------------------------------------------------------
# 11. Plot early readmission rate by age
# ------------------------------------------------------------

plot_df = (
    age_summary
    .reset_index()
)

plt.figure(
    figsize=(10, 6)
)

sns.barplot(
    data=plot_df,
    x="age",
    y="early_readmission_rate",
    order=age_order
)

plt.title(
    "Early Readmission Rate by Age Group"
)

plt.xlabel(
    "Age Group"
)

plt.ylabel(
    "Early Readmission Rate (%)"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()

plt.savefig(
    FIGURE_PATH,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ------------------------------------------------------------
# 12. Compare each age group with overall rate
# ------------------------------------------------------------

overall_rate = (
    df["early_readmission"].mean()
    * 100
)

age_summary["difference_from_overall_rate"] = (
    age_summary["early_readmission_rate"]
    - overall_rate
).round(2)


print("\n" + "=" * 70)
print("COMPARISON WITH OVERALL EARLY READMISSION RATE")
print("=" * 70)

print(
    f"\nOverall early readmission rate: "
    f"{overall_rate:.2f}%"
)

print(
    age_summary[
        [
            "total_encounters",
            "early_readmissions",
            "early_readmission_rate",
            "difference_from_overall_rate"
        ]
    ].to_string()
)


# ------------------------------------------------------------
# 13. Save analysis results
# ------------------------------------------------------------

with open(
    RESULT_PATH,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "STAGE 6B: READMISSION BY AGE GROUP\n"
    )

    file.write(
        "=" * 70 + "\n\n"
    )

    file.write(
        f"Total encounters: {len(df):,}\n"
    )

    file.write(
        f"Overall early readmission rate: "
        f"{overall_rate:.2f}%\n\n"
    )

    file.write(
        "Age-group summary\n"
    )

    file.write(
        "-" * 50 + "\n"
    )

    file.write(
        age_summary.to_string()
    )

    file.write("\n\n")

    file.write(
        f"Highest observed early readmission rate: "
        f"{highest_rate_age} ({highest_rate:.2f}%)\n"
    )

    file.write(
        f"Lowest observed early readmission rate: "
        f"{lowest_rate_age} ({lowest_rate:.2f}%)\n"
    )

    file.write("\n")

    file.write(
        "Comparison with overall rate\n"
    )

    file.write(
        "-" * 50 + "\n"
    )

    file.write(
        age_summary[
            [
                "total_encounters",
                "early_readmissions",
                "early_readmission_rate",
                "difference_from_overall_rate"
            ]
        ].to_string()
    )


# ------------------------------------------------------------
# 14. Completion message
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("OUTPUT FILES")
print("=" * 70)

print(
    f"\nFigure:\n{FIGURE_PATH}"
)

print(
    f"\nAnalysis results:\n{RESULT_PATH}"
)

print("\n" + "=" * 70)
print("STAGE 6B COMPLETE")
print("=" * 70)