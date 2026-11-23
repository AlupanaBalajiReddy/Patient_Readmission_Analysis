"""
Stage 6F: Early Readmission by Admission & Discharge Characteristics

Purpose:
    Examine how early readmission rates vary across:
    - Admission type
    - Discharge disposition
    - Admission source

Important:
    These are descriptive encounter-level associations.
    They do not establish causality.

Input:
    data/processed/diabetic_data_decoded.csv

Outputs:
    results/analysis_results/readmission_by_admission_discharge.txt

Figures:
    results/figures/early_readmission_by_admission_type.png
    results/figures/early_readmission_by_discharge_disposition.png
    results/figures/early_readmission_by_admission_source.png
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
    "readmission_by_admission_discharge.txt"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FIGURE_DIR, exist_ok=True)


# ============================================================
# 2. Load dataset
# ============================================================

df = pd.read_csv(
    INPUT_FILE,
    keep_default_na=False
)

print("=" * 70)
print("STAGE 6F: READMISSION BY ADMISSION & DISCHARGE CHARACTERISTICS")
print("=" * 70)

print(f"\nDataset shape: {df.shape}")


# ============================================================
# 3. Variables
# ============================================================

administrative_variables = [
    "admission_type",
    "discharge_disposition",
    "admission_source"
]

print("\nAdministrative variables:")
for variable in administrative_variables:
    print(f"- {variable}")


# ============================================================
# 4. Validate columns
# ============================================================

required_columns = administrative_variables + [
    "early_readmission"
]

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
# 5. Overall early-readmission rate
# ============================================================

overall_rate = df["early_readmission"].mean() * 100

print("\n" + "=" * 70)
print("OVERALL EARLY READMISSION")
print("=" * 70)

print(
    f"\nOverall early-readmission rate: "
    f"{overall_rate:.2f}%"
)


# ============================================================
# 6. Analyze each administrative variable
# ============================================================

all_results = {}

for variable in administrative_variables:

    print("\n" + "=" * 70)
    print(f"READMISSION BY {variable.upper()}")
    print("=" * 70)

    summary = (
        df.groupby(variable, dropna=False)
        .agg(
            encounters=("early_readmission", "size"),
            early_readmissions=("early_readmission", "sum"),
            early_readmission_rate=("early_readmission", "mean")
        )
        .reset_index()
    )

    summary["early_readmission_rate"] *= 100

    summary["difference_from_overall_pp"] = (
        summary["early_readmission_rate"]
        - overall_rate
    )

    summary = summary.sort_values(
        "early_readmission_rate",
        ascending=False
    )

    all_results[variable] = summary

    print("\nCategory summary:")

    print(
        summary.to_string(
            index=False,
            formatters={
                "early_readmission_rate": "{:.2f}".format,
                "difference_from_overall_pp": "{:.2f}".format
            }
        )
    )


# ============================================================
# 7. Identify small categories
# ============================================================

print("\n" + "=" * 70)
print("SMALL CATEGORY CHECK")
print("=" * 70)

for variable, summary in all_results.items():

    small_categories = summary[
        summary["encounters"] < 100
    ]

    print(f"\n{variable}:")

    if small_categories.empty:
        print("  No categories with fewer than 100 encounters.")

    else:
        print(
            small_categories.to_string(
                index=False,
                formatters={
                    "early_readmission_rate": "{:.2f}".format,
                    "difference_from_overall_pp": "{:.2f}".format
                }
            )
        )


# ============================================================
# 8. Create figures
# ============================================================

print("\n" + "=" * 70)
print("CREATING FIGURES")
print("=" * 70)


figure_names = {
    "admission_type":
        "early_readmission_by_admission_type.png",

    "discharge_disposition":
        "early_readmission_by_discharge_disposition.png",

    "admission_source":
        "early_readmission_by_admission_source.png"
}


plot_titles = {
    "admission_type":
        "Early Readmission Rate by Admission Type",

    "discharge_disposition":
        "Early Readmission Rate by Discharge Disposition",

    "admission_source":
        "Early Readmission Rate by Admission Source"
}


axis_labels = {
    "admission_type":
        "Admission Type",

    "discharge_disposition":
        "Discharge Disposition",

    "admission_source":
        "Admission Source"
}


for variable in administrative_variables:

    summary = all_results[variable].copy()

    # Sort categories by rate for visualization
    summary = summary.sort_values(
        "early_readmission_rate",
        ascending=True
    )

    plt.figure(figsize=(10, 7))

    sns.barplot(
        data=summary,
        x="early_readmission_rate",
        y=variable
    )

    plt.axvline(
        overall_rate,
        linestyle="--",
        linewidth=1.5,
        label=f"Overall rate = {overall_rate:.2f}%"
    )

    plt.title(plot_titles[variable])

    plt.xlabel("Early Readmission Rate (%)")
    plt.ylabel(axis_labels[variable])

    plt.legend()

    plt.tight_layout()

    figure_path = os.path.join(
        FIGURE_DIR,
        figure_names[variable]
    )

    plt.savefig(
        figure_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Saved: {figure_path}")


# ============================================================
# 9. Save results
# ============================================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "STAGE 6F: READMISSION BY ADMISSION & "
        "DISCHARGE CHARACTERISTICS\n"
    )

    file.write("=" * 70 + "\n\n")

    file.write(
        f"Dataset shape: {df.shape}\n"
    )

    file.write(
        f"Overall early-readmission rate: "
        f"{overall_rate:.2f}%\n\n"
    )

    file.write(
        "Important interpretation note:\n"
        "These are descriptive encounter-level associations. "
        "They do not establish causality.\n\n"
    )

    # --------------------------------------------------------
    # Category results
    # --------------------------------------------------------

    for variable, summary in all_results.items():

        file.write("\n")
        file.write("=" * 70 + "\n")
        file.write(
            f"READMISSION BY {variable.upper()}\n"
        )
        file.write("=" * 70 + "\n\n")

        file.write(
            summary.to_string(
                index=False,
                formatters={
                    "early_readmission_rate": "{:.2f}".format,
                    "difference_from_overall_pp": "{:.2f}".format
                }
            )
        )

        file.write("\n\n")

        # Small categories
        small_categories = summary[
            summary["encounters"] < 100
        ]

        file.write(
            "Categories with fewer than 100 encounters:\n"
        )

        if small_categories.empty:

            file.write(
                "  None\n"
            )

        else:

            file.write(
                small_categories.to_string(
                    index=False,
                    formatters={
                        "early_readmission_rate": "{:.2f}".format,
                        "difference_from_overall_pp": "{:.2f}".format
                    }
                )
            )

            file.write("\n")

    # --------------------------------------------------------
    # Figures
    # --------------------------------------------------------

    file.write("\n")
    file.write("=" * 70 + "\n")
    file.write("FIGURES CREATED\n")
    file.write("=" * 70 + "\n\n")

    for figure_name in figure_names.values():

        file.write(
            f"results/figures/{figure_name}\n"
        )

    # --------------------------------------------------------
    # Interpretation framework
    # --------------------------------------------------------

    file.write("\n")
    file.write("=" * 70 + "\n")
    file.write("INTERPRETATION FRAMEWORK\n")
    file.write("=" * 70 + "\n\n")

    file.write(
        "1. Compare each category's early-readmission rate "
        "with the overall dataset rate.\n\n"
    )

    file.write(
        "2. Categories with very small encounter counts should "
        "not be interpreted strongly because their observed rates "
        "can be unstable.\n\n"
    )

    file.write(
        "3. Administrative categories describe characteristics "
        "of the hospital encounter and its admission/discharge "
        "pathway.\n\n"
    )

    file.write(
        "4. Differences in readmission rates are descriptive "
        "associations and should not be interpreted as causal "
        "effects.\n\n"
    )


# ============================================================
# 10. Completion message
# ============================================================

print("\n" + "=" * 70)
print("STAGE 6F COMPLETE")
print("=" * 70)

print("\nResults saved to:")
print(f"  {OUTPUT_FILE}")

print("\nFigures saved to:")

for figure_name in figure_names.values():
    print(
        f"  {os.path.join(FIGURE_DIR, figure_name)}"
    )