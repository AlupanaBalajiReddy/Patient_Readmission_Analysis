# ============================================================
# Patient Readmission Analysis
# Stage 6A: Overall Readmission Profile
# ============================================================

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ------------------------------------------------------------
# 1. File paths
# ------------------------------------------------------------

DATA_PATH = "data/processed/diabetic_data_decoded.csv"
FIGURE_PATH_1 = "results/figures/readmission_distribution.png"
FIGURE_PATH_2 = "results/figures/early_readmission_distribution.png"
RESULT_PATH = "results/analysis_results/readmission_overview.txt"


# ------------------------------------------------------------
# 2. Create output directories if necessary
# ------------------------------------------------------------

os.makedirs("results/figures", exist_ok=True)
os.makedirs("results/analysis_results", exist_ok=True)


# ------------------------------------------------------------
# 3. Load dataset
# ------------------------------------------------------------

df = pd.read_csv(
    DATA_PATH,
    keep_default_na=False
)

print("=" * 70)
print("STAGE 6A: OVERALL READMISSION PROFILE")
print("=" * 70)

print(f"\nDataset shape: {df.shape}")


# ------------------------------------------------------------
# 4. Analyze original readmission categories
# ------------------------------------------------------------

readmission_counts = (
    df["readmitted"]
    .value_counts()
)

readmission_percentages = (
    df["readmitted"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)


print("\n" + "=" * 70)
print("ORIGINAL READMISSION DISTRIBUTION")
print("=" * 70)

print("\nCounts:")

print(
    readmission_counts.to_string()
)

print("\nPercentages:")

print(
    readmission_percentages.to_string()
)


# ------------------------------------------------------------
# 5. Analyze early readmission
# ------------------------------------------------------------

early_counts = (
    df["early_readmission"]
    .value_counts()
    .sort_index()
)

early_percentages = (
    df["early_readmission"]
    .value_counts(normalize=True)
    .sort_index()
    .mul(100)
    .round(2)
)


print("\n" + "=" * 70)
print("EARLY READMISSION DISTRIBUTION")
print("=" * 70)

print("\nCounts:")

print(
    early_counts.to_string()
)

print("\nPercentages:")

print(
    early_percentages.to_string()
)


# ------------------------------------------------------------
# 6. Create summary table
# ------------------------------------------------------------

summary = pd.DataFrame({
    "count": readmission_counts,
    "percentage": readmission_percentages
})

summary.index.name = "readmission_category"


print("\n" + "=" * 70)
print("READMISSION SUMMARY TABLE")
print("=" * 70)

print(
    summary.to_string()
)


# ------------------------------------------------------------
# 7. Create original readmission bar chart
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

order = ["NO", ">30", "<30"]

sns.countplot(
    data=df,
    x="readmitted",
    order=order
)

plt.title("Distribution of Hospital Readmission Categories")
plt.xlabel("Readmission Category")
plt.ylabel("Number of Encounters")

plt.tight_layout()

plt.savefig(
    FIGURE_PATH_1,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ------------------------------------------------------------
# 8. Create early-readmission bar chart
# ------------------------------------------------------------

early_plot_df = pd.DataFrame({
    "Early Readmission": [
        "No",
        "Yes"
    ],
    "Count": [
        early_counts.get(0, 0),
        early_counts.get(1, 0)
    ]
})


plt.figure(figsize=(7, 5))

sns.barplot(
    data=early_plot_df,
    x="Early Readmission",
    y="Count"
)

plt.title("Early Readmission (<30 Days)")
plt.xlabel("Early Readmission")
plt.ylabel("Number of Encounters")

plt.tight_layout()

plt.savefig(
    FIGURE_PATH_2,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ------------------------------------------------------------
# 9. Calculate key metrics
# ------------------------------------------------------------

total_encounters = len(df)

early_readmissions = (
    df["early_readmission"] == 1
).sum()

not_early_readmissions = (
    df["early_readmission"] == 0
).sum()

early_readmission_rate = (
    early_readmissions /
    total_encounters *
    100
)

print("\n" + "=" * 70)
print("KEY METRICS")
print("=" * 70)

print(
    f"Total encounters: "
    f"{total_encounters:,}"
)

print(
    f"Early readmission encounters: "
    f"{early_readmissions:,}"
)

print(
    f"Non-early-readmission encounters: "
    f"{not_early_readmissions:,}"
)

print(
    f"Early readmission rate: "
    f"{early_readmission_rate:.2f}%"
)


# ------------------------------------------------------------
# 10. Save analysis results
# ------------------------------------------------------------

with open(
    RESULT_PATH,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "STAGE 6A: OVERALL READMISSION PROFILE\n"
    )

    file.write(
        "=" * 70 + "\n\n"
    )

    file.write(
        f"Total encounters: {total_encounters:,}\n"
    )

    file.write(
        f"Early readmission encounters: "
        f"{early_readmissions:,}\n"
    )

    file.write(
        f"Non-early-readmission encounters: "
        f"{not_early_readmissions:,}\n"
    )

    file.write(
        f"Early readmission rate: "
        f"{early_readmission_rate:.2f}%\n\n"
    )

    file.write(
        "Original readmission distribution\n"
    )

    file.write(
        "-" * 50 + "\n"
    )

    file.write(
        summary.to_string()
    )

    file.write("\n\n")

    file.write(
        "Early readmission distribution\n"
    )

    file.write(
        "-" * 50 + "\n"
    )

    early_summary = pd.DataFrame({
        "count": early_counts,
        "percentage": early_percentages
    })

    early_summary.index.name = "early_readmission"

    file.write(
        early_summary.to_string()
    )


# ------------------------------------------------------------
# 11. Completion message
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("OUTPUT FILES")
print("=" * 70)

print(
    f"\nFigure 1:\n{FIGURE_PATH_1}"
)

print(
    f"\nFigure 2:\n{FIGURE_PATH_2}"
)

print(
    f"\nAnalysis results:\n{RESULT_PATH}"
)

print("\n" + "=" * 70)
print("STAGE 6A COMPLETE")
print("=" * 70)