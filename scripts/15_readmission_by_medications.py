"""
Stage 6G: Early Readmission by Diabetes Medication & Treatment Patterns

Purpose:
    Examine how early readmission rates vary across diabetes
    medication and treatment-related variables.

Variables analyzed:
    - diabetesMed
    - change
    - insulin
    - selected oral diabetes medications

Important:
    These are descriptive encounter-level associations.
    They do not establish causality.

Input:
    data/processed/diabetic_data_decoded.csv

Outputs:
    results/analysis_results/readmission_by_medications.txt

Figures:
    results/figures/early_readmission_by_diabetesMed.png
    results/figures/early_readmission_by_change.png
    results/figures/early_readmission_by_insulin.png
    results/figures/early_readmission_by_medications.png
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
    "readmission_by_medications.txt"
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
print("STAGE 6G: READMISSION BY DIABETES MEDICATION & TREATMENT")
print("=" * 70)

print(f"\nDataset shape: {df.shape}")


# ============================================================
# 3. Define medication variables
# ============================================================

treatment_variables = [
    "diabetesMed",
    "change",
    "insulin",
    "metformin",
    "glipizide",
    "glyburide",
    "pioglitazone",
    "rosiglitazone",
    "repaglinide",
    "nateglinide",
    "chlorpropamide",
    "glimepiride",
    "acetohexamide",
    "tolbutamide",
    "acarbose",
    "miglitol",
    "troglitazone",
    "tolazamide",
    "glyburide-metformin",
    "glipizide-metformin",
    "glimepiride-pioglitazone",
    "metformin-rosiglitazone",
    "metformin-pioglitazone"
]

print("\nTreatment variables to analyze:")

for variable in treatment_variables:
    print(f"- {variable}")


# ============================================================
# 4. Validate columns
# ============================================================

required_columns = treatment_variables + [
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

overall_rate = (
    df["early_readmission"].mean() * 100
)

print("\n" + "=" * 70)
print("OVERALL EARLY READMISSION")
print("=" * 70)

print(
    f"\nOverall early-readmission rate: "
    f"{overall_rate:.2f}%"
)


# ============================================================
# 6. Analyze treatment variables
# ============================================================

all_results = {}

for variable in treatment_variables:

    print("\n" + "=" * 70)
    print(
        f"READMISSION BY {variable.upper()}"
    )
    print("=" * 70)

    summary = (
        df.groupby(
            variable,
            dropna=False
        )
        .agg(
            encounters=("early_readmission", "size"),
            early_readmissions=("early_readmission", "sum"),
            early_readmission_rate=(
                "early_readmission",
                "mean"
            )
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
                "early_readmission_rate":
                    "{:.2f}".format,
                "difference_from_overall_pp":
                    "{:.2f}".format
            }
        )
    )


# ============================================================
# 7. Identify small categories
# ============================================================

print("\n" + "=" * 70)
print("SMALL CATEGORY CHECK")
print("=" * 70)

small_category_results = {}

for variable, summary in all_results.items():

    small_categories = summary[
        summary["encounters"] < 100
    ].copy()

    small_category_results[variable] = (
        small_categories
    )

    print(f"\n{variable}:")

    if small_categories.empty:

        print(
            "  No categories with fewer than "
            "100 encounters."
        )

    else:

        print(
            small_categories.to_string(
                index=False,
                formatters={
                    "early_readmission_rate":
                        "{:.2f}".format,
                    "difference_from_overall_pp":
                        "{:.2f}".format
                }
            )
        )


# ============================================================
# 8. Create focused figures
# ============================================================

print("\n" + "=" * 70)
print("CREATING FIGURES")
print("=" * 70)


# ------------------------------------------------------------
# Figure 1: diabetesMed
# ------------------------------------------------------------

focused_variables = [
    "diabetesMed",
    "change",
    "insulin"
]

focused_figure_names = {
    "diabetesMed":
        "early_readmission_by_diabetesMed.png",

    "change":
        "early_readmission_by_change.png",

    "insulin":
        "early_readmission_by_insulin.png"
}

focused_titles = {
    "diabetesMed":
        "Early Readmission Rate by Diabetes Medication Use",

    "change":
        "Early Readmission Rate by Medication Change",

    "insulin":
        "Early Readmission Rate by Insulin Treatment"
}

for variable in focused_variables:

    summary = all_results[variable].copy()

    summary = summary.sort_values(
        "early_readmission_rate",
        ascending=True
    )

    plt.figure(figsize=(8, 5))

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

    plt.title(
        focused_titles[variable]
    )

    plt.xlabel(
        "Early Readmission Rate (%)"
    )

    plt.ylabel(variable)

    plt.legend()

    plt.tight_layout()

    figure_path = os.path.join(
        FIGURE_DIR,
        focused_figure_names[variable]
    )

    plt.savefig(
        figure_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Saved: {figure_path}")


# ============================================================
# 9. Create medication comparison figure
# ============================================================

print("\nCreating medication comparison figure...")


# Select commonly observed oral medications.
oral_medications = [
    "metformin",
    "glipizide",
    "glyburide",
    "pioglitazone",
    "rosiglitazone"
]

medication_comparison = []

for medication in oral_medications:

    summary = all_results[medication]

    for _, row in summary.iterrows():

        category = row[medication]

        medication_comparison.append({
            "medication": medication,
            "category": category,
            "encounters": row["encounters"],
            "early_readmissions":
                row["early_readmissions"],
            "early_readmission_rate":
                row["early_readmission_rate"]
        })


medication_comparison_df = pd.DataFrame(
    medication_comparison
)


plt.figure(figsize=(11, 7))

sns.barplot(
    data=medication_comparison_df,
    x="early_readmission_rate",
    y="medication",
    hue="category"
)

plt.axvline(
    overall_rate,
    linestyle="--",
    linewidth=1.5,
    label=f"Overall rate = {overall_rate:.2f}%"
)

plt.title(
    "Early Readmission Rate Across Selected Diabetes Medications"
)

plt.xlabel(
    "Early Readmission Rate (%)"
)

plt.ylabel("Medication")

plt.legend(
    title="Treatment Status",
    bbox_to_anchor=(1.02, 1),
    loc="upper left"
)

plt.tight_layout()

medication_figure_path = os.path.join(
    FIGURE_DIR,
    "early_readmission_by_medications.png"
)

plt.savefig(
    medication_figure_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    f"Saved: {medication_figure_path}"
)


# ============================================================
# 10. Save results
# ============================================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "STAGE 6G: READMISSION BY DIABETES "
        "MEDICATION & TREATMENT PATTERNS\n"
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
        "These are descriptive encounter-level "
        "associations. They do not establish causality.\n\n"
    )

    # --------------------------------------------------------
    # All treatment variables
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
                    "early_readmission_rate":
                        "{:.2f}".format,
                    "difference_from_overall_pp":
                        "{:.2f}".format
                }
            )
        )

        file.write("\n\n")

        # Small categories
        file.write(
            "Categories with fewer than 100 encounters:\n"
        )

        small_categories = (
            small_category_results[variable]
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
                        "early_readmission_rate":
                            "{:.2f}".format,
                        "difference_from_overall_pp":
                            "{:.2f}".format
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

    for figure_name in focused_figure_names.values():

        file.write(
            f"results/figures/{figure_name}\n"
        )

    file.write(
        "results/figures/"
        "early_readmission_by_medications.png\n"
    )

    # --------------------------------------------------------
    # Interpretation framework
    # --------------------------------------------------------

    file.write("\n")
    file.write("=" * 70 + "\n")
    file.write("INTERPRETATION FRAMEWORK\n")
    file.write("=" * 70 + "\n\n")

    file.write(
        "1. Compare each treatment category's "
        "early-readmission rate with the overall rate.\n\n"
    )

    file.write(
        "2. Medication categories with very small "
        "encounter counts should not be interpreted strongly.\n\n"
    )

    file.write(
        "3. Medication status describes treatment "
        "patterns recorded during the encounter.\n\n"
    )

    file.write(
        "4. Differences in readmission rates are "
        "descriptive associations and should not be "
        "interpreted as causal effects.\n\n"
    )


# ============================================================
# 11. Completion message
# ============================================================

print("\n" + "=" * 70)
print("STAGE 6G COMPLETE")
print("=" * 70)

print("\nResults saved to:")
print(f"  {OUTPUT_FILE}")

print("\nFigures saved to:")

for figure_name in focused_figure_names.values():
    print(
        f"  {os.path.join(FIGURE_DIR, figure_name)}"
    )

print(
    f"  {medication_figure_path}"
)