# ============================================================
# Patient Readmission Analysis
# Stage 6C: Readmission by Demographics
# ============================================================

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ------------------------------------------------------------
# 1. File paths
# ------------------------------------------------------------

DATA_PATH = "data/processed/diabetic_data_decoded.csv"

FIGURE_PATH_GENDER = (
    "results/figures/"
    "early_readmission_rate_by_gender.png"
)

FIGURE_PATH_RACE = (
    "results/figures/"
    "early_readmission_rate_by_race.png"
)

RESULT_PATH = (
    "results/analysis_results/"
    "readmission_by_demographics.txt"
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
print("STAGE 6C: READMISSION BY DEMOGRAPHICS")
print("=" * 70)

print(
    f"\nDataset shape: {df.shape}"
)


# ------------------------------------------------------------
# 4. Overall early readmission rate
# ------------------------------------------------------------

overall_rate = (
    df["early_readmission"].mean() * 100
)

print("\n" + "=" * 70)
print("OVERALL EARLY READMISSION RATE")
print("=" * 70)

print(
    f"{overall_rate:.2f}%"
)


# ============================================================
# 5. GENDER ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("GENDER ANALYSIS")
print("=" * 70)


gender_summary = (
    df.groupby(
        "gender",
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
)


# ------------------------------------------------------------
# 6. Calculate gender readmission rate
# ------------------------------------------------------------

gender_summary["early_readmission_rate"] = (
    gender_summary["early_readmissions"]
    / gender_summary["total_encounters"]
    * 100
).round(2)


gender_summary["non_early_readmissions"] = (
    gender_summary["total_encounters"]
    - gender_summary["early_readmissions"]
)


gender_summary["difference_from_overall_rate"] = (
    gender_summary["early_readmission_rate"]
    - overall_rate
).round(2)


# ------------------------------------------------------------
# 7. Display gender results
# ------------------------------------------------------------

print("\nGender readmission summary:")

print(
    gender_summary.to_string()
)


# ------------------------------------------------------------
# 8. Gender plot
# ------------------------------------------------------------

gender_plot_df = (
    gender_summary
    .reset_index()
)

plt.figure(
    figsize=(7, 5)
)

sns.barplot(
    data=gender_plot_df,
    x="gender",
    y="early_readmission_rate"
)

plt.title(
    "Early Readmission Rate by Gender"
)

plt.xlabel(
    "Gender"
)

plt.ylabel(
    "Early Readmission Rate (%)"
)

plt.tight_layout()

plt.savefig(
    FIGURE_PATH_GENDER,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 9. RACE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("RACE ANALYSIS")
print("=" * 70)


race_summary = (
    df.groupby(
        "race",
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
)


# ------------------------------------------------------------
# 10. Calculate race readmission rate
# ------------------------------------------------------------

race_summary["early_readmission_rate"] = (
    race_summary["early_readmissions"]
    / race_summary["total_encounters"]
    * 100
).round(2)


race_summary["non_early_readmissions"] = (
    race_summary["total_encounters"]
    - race_summary["early_readmissions"]
)


race_summary["difference_from_overall_rate"] = (
    race_summary["early_readmission_rate"]
    - overall_rate
).round(2)


# ------------------------------------------------------------
# 11. Display race results
# ------------------------------------------------------------

print("\nRace readmission summary:")

print(
    race_summary.to_string()
)


# ------------------------------------------------------------
# 12. Race plot
# ------------------------------------------------------------

race_plot_df = (
    race_summary
    .reset_index()
    .sort_values(
        "early_readmission_rate",
        ascending=False
    )
)

plt.figure(
    figsize=(9, 6)
)

sns.barplot(
    data=race_plot_df,
    x="race",
    y="early_readmission_rate"
)

plt.title(
    "Early Readmission Rate by Race"
)

plt.xlabel(
    "Race"
)

plt.ylabel(
    "Early Readmission Rate (%)"
)

plt.xticks(
    rotation=30,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    FIGURE_PATH_RACE,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 13. Identify observed highest/lowest rates
# ============================================================

highest_gender = (
    gender_summary["early_readmission_rate"]
    .idxmax()
)

highest_gender_rate = (
    gender_summary["early_readmission_rate"]
    .max()
)

lowest_gender = (
    gender_summary["early_readmission_rate"]
    .idxmin()
)

lowest_gender_rate = (
    gender_summary["early_readmission_rate"]
    .min()
)


highest_race = (
    race_summary["early_readmission_rate"]
    .idxmax()
)

highest_race_rate = (
    race_summary["early_readmission_rate"]
    .max()
)

lowest_race = (
    race_summary["early_readmission_rate"]
    .idxmin()
)

lowest_race_rate = (
    race_summary["early_readmission_rate"]
    .min()
)


print("\n" + "=" * 70)
print("OBSERVED RATE RANGE")
print("=" * 70)

print(
    f"Gender highest observed rate: "
    f"{highest_gender} "
    f"({highest_gender_rate:.2f}%)"
)

print(
    f"Gender lowest observed rate: "
    f"{lowest_gender} "
    f"({lowest_gender_rate:.2f}%)"
)

print(
    f"Race highest observed rate: "
    f"{highest_race} "
    f"({highest_race_rate:.2f}%)"
)

print(
    f"Race lowest observed rate: "
    f"{lowest_race} "
    f"({lowest_race_rate:.2f}%)"
)


# ============================================================
# 14. Save results
# ============================================================

with open(
    RESULT_PATH,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "STAGE 6C: READMISSION BY DEMOGRAPHICS\n"
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
        "GENDER ANALYSIS\n"
    )

    file.write(
        "-" * 50 + "\n"
    )

    file.write(
        gender_summary.to_string()
    )

    file.write("\n\n")

    file.write(
        "RACE ANALYSIS\n"
    )

    file.write(
        "-" * 50 + "\n"
    )

    file.write(
        race_summary.to_string()
    )

    file.write("\n\n")

    file.write(
        "OBSERVED RATE RANGE\n"
    )

    file.write(
        "-" * 50 + "\n"
    )

    file.write(
        f"Gender highest observed rate: "
        f"{highest_gender} "
        f"({highest_gender_rate:.2f}%)\n"
    )

    file.write(
        f"Gender lowest observed rate: "
        f"{lowest_gender} "
        f"({lowest_gender_rate:.2f}%)\n"
    )

    file.write(
        f"Race highest observed rate: "
        f"{highest_race} "
        f"({highest_race_rate:.2f}%)\n"
    )

    file.write(
        f"Race lowest observed rate: "
        f"{lowest_race} "
        f"({lowest_race_rate:.2f}%)\n"
    )


# ============================================================
# 15. Completion message
# ============================================================

print("\n" + "=" * 70)
print("OUTPUT FILES")
print("=" * 70)

print(
    f"\nGender figure:\n{FIGURE_PATH_GENDER}"
)

print(
    f"\nRace figure:\n{FIGURE_PATH_RACE}"
)

print(
    f"\nAnalysis results:\n{RESULT_PATH}"
)

print("\n" + "=" * 70)
print("STAGE 6C COMPLETE")
print("=" * 70)