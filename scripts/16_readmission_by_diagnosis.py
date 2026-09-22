"""
Stage 6H: Early Readmission by Diagnosis Categories

Purpose:
    Group ICD-9 diagnosis codes into broader clinical categories
    and compare early-readmission rates across those categories.

Diagnosis fields:
    - diag_1: Primary diagnosis
    - diag_2: Secondary diagnosis
    - diag_3: Tertiary diagnosis

Important:
    ICD-9 codes are categorical codes, not continuous numerical
    measurements. They are therefore grouped into broader
    diagnosis categories before analysis.

Important interpretation note:
    These are descriptive encounter-level associations.
    They do not establish causality.

Input:
    data/processed/diabetic_data_decoded.csv

Outputs:
    results/analysis_results/readmission_by_diagnosis.txt

Figures:
    results/figures/early_readmission_by_primary_diagnosis_category.png
    results/figures/early_readmission_by_secondary_diagnosis_category.png
    results/figures/early_readmission_by_tertiary_diagnosis_category.png
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
    "readmission_by_diagnosis.txt"
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
print("STAGE 6H: READMISSION BY DIAGNOSIS CATEGORIES")
print("=" * 70)

print(f"\nDataset shape: {df.shape}")


# ============================================================
# 3. Diagnosis columns
# ============================================================

diagnosis_columns = [
    "diag_1",
    "diag_2",
    "diag_3"
]

required_columns = diagnosis_columns + [
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

print("\nDiagnosis columns:")
for column in diagnosis_columns:
    print(f"- {column}")


# ============================================================
# 4. Overall early-readmission rate
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
# 5. ICD-9 category function
# ============================================================

def classify_icd9(code):
    """
    Convert an ICD-9 diagnosis code into a broad category.

    Categories are based on ICD-9 numerical ranges.

    Returns:
        Broad diagnosis category.
    """

    if code == "" or code == "?" or code == "Unknown":
        return "Unknown"

    code = str(code).strip()

    # V-codes and E-codes
    if code.startswith("V"):
        return "Supplementary / External Factors"

    if code.startswith("E"):
        return "Injury / External Causes"

    # Attempt numerical conversion
    try:
        value = float(code)
    except ValueError:
        return "Other / Unclassified"

    # --------------------------------------------------------
    # ICD-9 broad categories
    # --------------------------------------------------------

    if 1 <= value <= 139:
        return "Infectious / Parasitic"

    elif 140 <= value <= 239:
        return "Neoplasms"

    elif 240 <= value <= 279:
        return "Endocrine / Metabolic"

    elif 280 <= value <= 289:
        return "Blood / Blood-forming Organs"

    elif 290 <= value <= 319:
        return "Mental Disorders"

    elif 320 <= value <= 359:
        return "Nervous System"

    elif 360 <= value <= 389:
        return "Sense Organs"

    elif 390 <= value <= 459:
        return "Circulatory"

    elif 460 <= value <= 519:
        return "Respiratory"

    elif 520 <= value <= 579:
        return "Digestive"

    elif 580 <= value <= 629:
        return "Genitourinary"

    elif 630 <= value <= 679:
        return "Pregnancy / Childbirth"

    elif 680 <= value <= 709:
        return "Skin / Subcutaneous Tissue"

    elif 710 <= value <= 739:
        return "Musculoskeletal"

    elif 740 <= value <= 759:
        return "Congenital Conditions"

    elif 760 <= value <= 779:
        return "Perinatal Conditions"

    elif 780 <= value <= 799:
        return "Symptoms / Signs / Abnormal Findings"

    elif 800 <= value <= 999:
        return "Injury / Poisoning"

    else:
        return "Other / Unclassified"


# ============================================================
# 6. Create diagnosis categories
# ============================================================

for column in diagnosis_columns:

    category_column = f"{column}_category"

    df[category_column] = df[column].apply(
        classify_icd9
    )


print("\n" + "=" * 70)
print("DIAGNOSIS CATEGORY COUNTS")
print("=" * 70)

for column in diagnosis_columns:

    category_column = f"{column}_category"

    print(
        f"\n{column}:"
    )

    print(
        df[category_column]
        .value_counts()
        .to_string()
    )


# ============================================================
# 7. Analyze each diagnosis position
# ============================================================

all_results = {}

for column in diagnosis_columns:

    category_column = f"{column}_category"

    print("\n" + "=" * 70)

    if column == "diag_1":
        title = "PRIMARY DIAGNOSIS"

    elif column == "diag_2":
        title = "SECONDARY DIAGNOSIS"

    else:
        title = "TERTIARY DIAGNOSIS"

    print(
        f"READMISSION BY {title} CATEGORY"
    )

    print("=" * 70)

    summary = (
        df.groupby(
            category_column,
            dropna=False
        )
        .agg(
            encounters=(
                "early_readmission",
                "size"
            ),
            early_readmissions=(
                "early_readmission",
                "sum"
            ),
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

    all_results[column] = summary

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
# 8. Small category check
# ============================================================

print("\n" + "=" * 70)
print("SMALL CATEGORY CHECK")
print("=" * 70)

small_category_results = {}

for column, summary in all_results.items():

    category_column = f"{column}_category"

    small_categories = summary[
        summary["encounters"] < 100
    ].copy()

    small_category_results[column] = (
        small_categories
    )

    print(f"\n{column}:")

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
# 9. Create figures
# ============================================================

print("\n" + "=" * 70)
print("CREATING FIGURES")
print("=" * 70)


figure_names = {
    "diag_1":
        "early_readmission_by_primary_diagnosis_category.png",

    "diag_2":
        "early_readmission_by_secondary_diagnosis_category.png",

    "diag_3":
        "early_readmission_by_tertiary_diagnosis_category.png"
}


figure_titles = {
    "diag_1":
        "Early Readmission Rate by Primary Diagnosis Category",

    "diag_2":
        "Early Readmission Rate by Secondary Diagnosis Category",

    "diag_3":
        "Early Readmission Rate by Tertiary Diagnosis Category"
}


for column in diagnosis_columns:

    category_column = f"{column}_category"

    summary = all_results[column].copy()

    # Sort from lowest to highest rate
    summary = summary.sort_values(
        "early_readmission_rate",
        ascending=True
    )

    plt.figure(figsize=(11, 8))

    sns.barplot(
        data=summary,
        x="early_readmission_rate",
        y=category_column
    )

    plt.axvline(
        overall_rate,
        linestyle="--",
        linewidth=1.5,
        label=f"Overall rate = {overall_rate:.2f}%"
    )

    plt.title(
        figure_titles[column]
    )

    plt.xlabel(
        "Early Readmission Rate (%)"
    )

    plt.ylabel(
        "Diagnosis Category"
    )

    plt.legend()

    plt.tight_layout()

    figure_path = os.path.join(
        FIGURE_DIR,
        figure_names[column]
    )

    plt.savefig(
        figure_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"Saved: {figure_path}"
    )


# ============================================================
# 10. Identify major diagnosis categories
# ============================================================

print("\n" + "=" * 70)
print("MAJOR DIAGNOSIS CATEGORIES")
print("=" * 70)

major_category_results = {}

for column, summary in all_results.items():

    major_categories = summary[
        summary["encounters"] >= 1000
    ].copy()

    major_category_results[column] = (
        major_categories
    )

    print(f"\n{column}:")

    if major_categories.empty:

        print(
            "  No categories with at least "
            "1,000 encounters."
        )

    else:

        print(
            major_categories.to_string(
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
# 11. Save results
# ============================================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "STAGE 6H: READMISSION BY DIAGNOSIS CATEGORIES\n"
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
        "ICD-9 diagnosis codes are categorical codes, "
        "not continuous numerical measurements. They were "
        "grouped into broad ICD-9 categories for analysis.\n\n"
    )

    file.write(
        "These are descriptive encounter-level associations. "
        "They do not establish causality.\n\n"
    )

    # --------------------------------------------------------
    # Category counts
    # --------------------------------------------------------

    file.write("=" * 70 + "\n")
    file.write("DIAGNOSIS CATEGORY COUNTS\n")
    file.write("=" * 70 + "\n\n")

    for column in diagnosis_columns:

        category_column = f"{column}_category"

        file.write(
            f"{column}:\n"
        )

        counts = (
            df[category_column]
            .value_counts()
        )

        file.write(
            counts.to_string()
        )

        file.write("\n\n")

    # --------------------------------------------------------
    # Readmission rates
    # --------------------------------------------------------

    for column, summary in all_results.items():

        category_column = f"{column}_category"

        file.write("\n")
        file.write("=" * 70 + "\n")

        if column == "diag_1":
            title = "PRIMARY DIAGNOSIS"

        elif column == "diag_2":
            title = "SECONDARY DIAGNOSIS"

        else:
            title = "TERTIARY DIAGNOSIS"

        file.write(
            f"READMISSION BY {title} CATEGORY\n"
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
            small_category_results[column]
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

        # Major categories
        file.write("\n")
        file.write(
            "Major categories with at least "
            "1,000 encounters:\n"
        )

        major_categories = (
            major_category_results[column]
        )

        if major_categories.empty:

            file.write(
                "  None\n"
            )

        else:

            file.write(
                major_categories.to_string(
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
        "1. Diagnosis codes were analyzed as categorical "
        "ICD-9 codes rather than numerical measurements.\n\n"
    )

    file.write(
        "2. Broad ICD-9 categories were used to reduce the "
        "number of individual diagnosis codes and improve "
        "interpretability.\n\n"
    )

    file.write(
        "3. Categories with very small encounter counts "
        "should not be interpreted strongly.\n\n"
    )

    file.write(
        "4. Major categories with at least 1,000 encounters "
        "provide a more stable descriptive comparison.\n\n"
    )

    file.write(
        "5. Differences in readmission rates are descriptive "
        "associations and should not be interpreted as "
        "causal effects.\n\n"
    )


# ============================================================
# 12. Completion message
# ============================================================

print("\n" + "=" * 70)
print("STAGE 6H COMPLETE")
print("=" * 70)

print("\nResults saved to:")
print(f"  {OUTPUT_FILE}")

print("\nFigures saved to:")

for figure_name in figure_names.values():

    print(
        f"  {os.path.join(FIGURE_DIR, figure_name)}"
    )