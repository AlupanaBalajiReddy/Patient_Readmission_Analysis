"""
Stage 6E: Early Readmission vs Hospital Stay & Clinical Activity

Purpose:
    Compare hospital stay and clinical activity between encounters
    with and without early readmission (<30 days).

Variables analyzed:
    - time_in_hospital
    - num_lab_procedures
    - num_procedures
    - num_medications
    - number_diagnoses

Outputs:
    - results/analysis_results/readmission_by_clinical_activity.txt
    - results/figures/early_readmission_by_time_in_hospital.png
    - results/figures/early_readmission_by_lab_procedures.png
    - results/figures/early_readmission_by_procedures.png
    - results/figures/early_readmission_by_medications.png
    - results/figures/early_readmission_by_diagnoses.png
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# 1. Paths
# ============================================================

INPUT_FILE = "data/processed/diabetic_data_decoded.csv"

OUTPUT_DIR = "results/analysis_results"
FIGURE_DIR = "results/figures"

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "readmission_by_clinical_activity.txt"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FIGURE_DIR, exist_ok=True)


# ============================================================
# 2. Load dataset
# ============================================================

df = pd.read_csv(INPUT_FILE, keep_default_na=False)

print("=" * 70)
print("STAGE 6E: READMISSION VS HOSPITAL STAY & CLINICAL ACTIVITY")
print("=" * 70)

print(f"\nDataset shape: {df.shape}")


# ============================================================
# 3. Variables to analyze
# ============================================================

clinical_variables = [
    "time_in_hospital",
    "num_lab_procedures",
    "num_procedures",
    "num_medications",
    "number_diagnoses"
]

print("\nClinical activity variables:")
for variable in clinical_variables:
    print(f"- {variable}")


# ============================================================
# 4. Validate required columns
# ============================================================

required_columns = clinical_variables + ["early_readmission"]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )


# ============================================================
# 5. Overall descriptive statistics
# ============================================================

print("\n" + "=" * 70)
print("OVERALL CLINICAL ACTIVITY")
print("=" * 70)

overall_stats = []

for variable in clinical_variables:

    series = pd.to_numeric(df[variable], errors="coerce")

    stats = {
        "variable": variable,
        "count": series.count(),
        "mean": series.mean(),
        "median": series.median(),
        "q25": series.quantile(0.25),
        "q75": series.quantile(0.75),
        "min": series.min(),
        "max": series.max()
    }

    overall_stats.append(stats)

    print(f"\n{variable}")
    print(f"  Count   : {stats['count']}")
    print(f"  Mean    : {stats['mean']:.2f}")
    print(f"  Median  : {stats['median']:.2f}")
    print(f"  Q25     : {stats['q25']:.2f}")
    print(f"  Q75     : {stats['q75']:.2f}")
    print(f"  Minimum : {stats['min']}")
    print(f"  Maximum : {stats['max']}")


# ============================================================
# 6. Compare early vs non-early readmission
# ============================================================

print("\n" + "=" * 70)
print("COMPARISON: EARLY VS NON-EARLY READMISSION")
print("=" * 70)

comparison_stats = []

for variable in clinical_variables:

    grouped = (
        df.groupby("early_readmission")[variable]
        .agg(
            count="count",
            mean="mean",
            median="median",
            q25=lambda x: x.quantile(0.25),
            q75=lambda x: x.quantile(0.75),
            min="min",
            max="max"
        )
    )

    print(f"\n{variable}")

    for target_value in [0, 1]:

        if target_value not in grouped.index:
            continue

        row = grouped.loc[target_value]

        label = (
            "Non-early readmission"
            if target_value == 0
            else "Early readmission"
        )

        print(f"\n  {label}")
        print(f"    Count   : {int(row['count'])}")
        print(f"    Mean    : {row['mean']:.2f}")
        print(f"    Median  : {row['median']:.2f}")
        print(f"    Q25     : {row['q25']:.2f}")
        print(f"    Q75     : {row['q75']:.2f}")
        print(f"    Minimum : {row['min']}")
        print(f"    Maximum : {row['max']}")

        comparison_stats.append({
            "variable": variable,
            "early_readmission": target_value,
            "group": label,
            "count": int(row["count"]),
            "mean": row["mean"],
            "median": row["median"],
            "q25": row["q25"],
            "q75": row["q75"],
            "min": row["min"],
            "max": row["max"]
        })


# ============================================================
# 7. Calculate mean and median differences
# ============================================================

print("\n" + "=" * 70)
print("DIFFERENCE BETWEEN EARLY AND NON-EARLY GROUPS")
print("=" * 70)

difference_results = []

for variable in clinical_variables:

    non_early = df.loc[
        df["early_readmission"] == 0,
        variable
    ]

    early = df.loc[
        df["early_readmission"] == 1,
        variable
    ]

    non_early_mean = non_early.mean()
    early_mean = early.mean()

    non_early_median = non_early.median()
    early_median = early.median()

    mean_difference = early_mean - non_early_mean
    median_difference = early_median - non_early_median

    mean_percent_difference = (
        (mean_difference / non_early_mean) * 100
        if non_early_mean != 0
        else None
    )

    print(f"\n{variable}")
    print(f"  Non-early mean : {non_early_mean:.2f}")
    print(f"  Early mean     : {early_mean:.2f}")
    print(f"  Mean difference: {mean_difference:.2f}")

    if mean_percent_difference is not None:
        print(
            f"  Mean difference (%): "
            f"{mean_percent_difference:.2f}%"
        )

    print(f"  Non-early median : {non_early_median:.2f}")
    print(f"  Early median     : {early_median:.2f}")
    print(f"  Median difference: {median_difference:.2f}")

    difference_results.append({
        "variable": variable,
        "non_early_mean": non_early_mean,
        "early_mean": early_mean,
        "mean_difference": mean_difference,
        "mean_percent_difference": mean_percent_difference,
        "non_early_median": non_early_median,
        "early_median": early_median,
        "median_difference": median_difference
    })


# ============================================================
# 8. Create boxplots
# ============================================================

print("\n" + "=" * 70)
print("CREATING FIGURES")
print("=" * 70)

plot_labels = {
    "time_in_hospital": "Time in Hospital (days)",
    "num_lab_procedures": "Number of Lab Procedures",
    "num_procedures": "Number of Procedures",
    "num_medications": "Number of Medications",
    "number_diagnoses": "Number of Diagnoses"
}

plot_files = {}

for variable in clinical_variables:

    plot_data = df[
        ["early_readmission", variable]
    ].copy()

    plot_data["Readmission Group"] = plot_data[
        "early_readmission"
    ].map({
        0: "No Early Readmission",
        1: "Early Readmission"
    })

    plt.figure(figsize=(8, 6))

    sns.boxplot(
        data=plot_data,
        x="Readmission Group",
        y=variable
    )

    plt.title(
        f"{plot_labels[variable]} by Early Readmission Status"
    )

    plt.xlabel("Readmission Group")
    plt.ylabel(plot_labels[variable])

    plt.tight_layout()

    figure_filename = (
        f"early_readmission_by_{variable}.png"
    )

    figure_path = os.path.join(
        FIGURE_DIR,
        figure_filename
    )

    plt.savefig(
        figure_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    plot_files[variable] = figure_path

    print(f"Saved: {figure_path}")


# ============================================================
# 9. Save detailed results
# ============================================================

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

    file.write(
        "STAGE 6E: READMISSION VS HOSPITAL STAY & "
        "CLINICAL ACTIVITY\n"
    )

    file.write("=" * 70 + "\n\n")

    file.write(f"Dataset shape: {df.shape}\n\n")

    file.write(
        "Purpose:\n"
        "Compare hospital stay and clinical activity between "
        "encounters with and without early readmission (<30 days).\n\n"
    )

    file.write(
        "Important interpretation note:\n"
        "These are descriptive encounter-level associations. "
        "They do not establish causality.\n\n"
    )

    # Overall statistics
    file.write("=" * 70 + "\n")
    file.write("OVERALL CLINICAL ACTIVITY\n")
    file.write("=" * 70 + "\n\n")

    for row in overall_stats:

        file.write(f"{row['variable']}\n")
        file.write(f"  Count   : {row['count']}\n")
        file.write(f"  Mean    : {row['mean']:.2f}\n")
        file.write(f"  Median  : {row['median']:.2f}\n")
        file.write(f"  Q25     : {row['q25']:.2f}\n")
        file.write(f"  Q75     : {row['q75']:.2f}\n")
        file.write(f"  Minimum : {row['min']}\n")
        file.write(f"  Maximum : {row['max']}\n\n")

    # Group comparison
    file.write("=" * 70 + "\n")
    file.write("COMPARISON: EARLY VS NON-EARLY READMISSION\n")
    file.write("=" * 70 + "\n\n")

    current_variable = None

    for row in comparison_stats:

        if row["variable"] != current_variable:

            current_variable = row["variable"]

            file.write(
                f"{current_variable}\n"
            )

        file.write(
            f"  {row['group']}\n"
        )

        file.write(
            f"    Count   : {row['count']}\n"
            f"    Mean    : {row['mean']:.2f}\n"
            f"    Median  : {row['median']:.2f}\n"
            f"    Q25     : {row['q25']:.2f}\n"
            f"    Q75     : {row['q75']:.2f}\n"
            f"    Minimum : {row['min']}\n"
            f"    Maximum : {row['max']}\n\n"
        )

    # Differences
    file.write("=" * 70 + "\n")
    file.write("DIFFERENCE BETWEEN EARLY AND NON-EARLY GROUPS\n")
    file.write("=" * 70 + "\n\n")

    for row in difference_results:

        file.write(
            f"{row['variable']}\n"
        )

        file.write(
            f"  Non-early mean : "
            f"{row['non_early_mean']:.2f}\n"
        )

        file.write(
            f"  Early mean     : "
            f"{row['early_mean']:.2f}\n"
        )

        file.write(
            f"  Mean difference: "
            f"{row['mean_difference']:.2f}\n"
        )

        if row["mean_percent_difference"] is not None:

            file.write(
                f"  Mean difference (%): "
                f"{row['mean_percent_difference']:.2f}%\n"
            )

        file.write(
            f"  Non-early median : "
            f"{row['non_early_median']:.2f}\n"
        )

        file.write(
            f"  Early median     : "
            f"{row['early_median']:.2f}\n"
        )

        file.write(
            f"  Median difference: "
            f"{row['median_difference']:.2f}\n\n"
        )

    # Figure list
    file.write("=" * 70 + "\n")
    file.write("FIGURES CREATED\n")
    file.write("=" * 70 + "\n\n")

    for variable, path in plot_files.items():

        file.write(
            f"{variable}: {path}\n"
        )

    # Interpretation framework
    file.write("\n")
    file.write("=" * 70 + "\n")
    file.write("INTERPRETATION FRAMEWORK\n")
    file.write("=" * 70 + "\n\n")

    file.write(
        "1. Compare means and medians rather than relying only "
        "on means because several clinical activity variables "
        "are skewed.\n\n"
    )

    file.write(
        "2. A higher value in the early-readmission group indicates "
        "a higher observed level of that variable among encounters "
        "with early readmission.\n\n"
    )

    file.write(
        "3. These comparisons describe associations in the dataset "
        "and should not be interpreted as causal effects.\n\n"
    )

print("\n" + "=" * 70)
print("STAGE 6E COMPLETE")
print("=" * 70)

print(f"\nResults saved to:")
print(f"  {OUTPUT_FILE}")

print("\nFigures saved to:")
for path in plot_files.values():
    print(f"  {path}")