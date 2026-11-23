"""
Stage 7B: Practical Significance Analysis

Purpose:
    Quantify the practical magnitude of observed differences in
    early-readmission rates.

Important:
    These results describe encounter-level associations.
    They do not establish causality or individual patient risk.
"""

import os
import pandas as pd


# ============================================================
# 1. PATHS
# ============================================================

INPUT_FILE = "data/processed/diabetic_data_decoded.csv"

OUTPUT_DIR = "results/analysis_results"
OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "practical_significance.txt"
)


# ============================================================
# 2. LOAD DATA
# ============================================================

df = pd.read_csv(
    INPUT_FILE,
    keep_default_na=False
)

print("=" * 70)
print("STAGE 7B: PRACTICAL SIGNIFICANCE ANALYSIS")
print("=" * 70)

print(f"\nDataset shape: {df.shape}")

total_encounters = len(df)
early_readmissions = df["early_readmission"].sum()

overall_rate = (
    early_readmissions / total_encounters
) * 100

print(f"Total encounters: {total_encounters:,}")
print(f"Early readmissions: {early_readmissions:,}")
print(f"Overall early-readmission rate: {overall_rate:.2f}%")


# ============================================================
# 3. OUTPUT STORAGE
# ============================================================

os.makedirs(OUTPUT_DIR, exist_ok=True)

output_lines = []

output_lines.append(
    "STAGE 7B: PRACTICAL SIGNIFICANCE ANALYSIS"
)

output_lines.append("=" * 70)

output_lines.append(
    f"\nDataset shape: {df.shape}"
)

output_lines.append(
    f"Total encounters: {total_encounters:,}"
)

output_lines.append(
    f"Early readmissions: {early_readmissions:,}"
)

output_lines.append(
    f"Overall early-readmission rate: {overall_rate:.2f}%"
)

output_lines.append("")

output_lines.append("Purpose:")
output_lines.append(
    "Quantify the practical magnitude of observed "
    "differences in early-readmission rates."
)

output_lines.append("")

output_lines.append("Important interpretation note:")
output_lines.append(
    "These results describe associations between encounter "
    "characteristics and early readmission. They do not "
    "establish causality."
)

output_lines.append("")


# ============================================================
# 4. HELPER FUNCTION
# ============================================================

def calculate_group_rates(dataframe, variable):
    """
    Calculate encounter count, early-readmission count,
    early-readmission rate, difference from overall rate,
    and relative difference.
    """

    grouped = (
        dataframe
        .groupby(variable, dropna=False, observed=False)
        .agg(
            encounters=("early_readmission", "size"),
            early_readmissions=("early_readmission", "sum")
        )
        .reset_index()
    )

    grouped["early_readmission_rate"] = (
        grouped["early_readmissions"]
        / grouped["encounters"]
        * 100
    )

    grouped["difference_from_overall_pp"] = (
        grouped["early_readmission_rate"]
        - overall_rate
    )

    grouped["relative_difference_percent"] = (
        grouped["difference_from_overall_pp"]
        / overall_rate
        * 100
    )

    return grouped


def add_dataframe_to_output(dataframe):
    """
    Add a formatted dataframe to the text output.
    """

    output_lines.append(
        dataframe.to_string(index=False)
    )

    output_lines.append("")


# ============================================================
# 5. CREATE UTILIZATION CATEGORIES
# ============================================================

df["outpatient_category"] = pd.cut(
    df["number_outpatient"],
    bins=[-1, 0, 1, 2, float("inf")],
    labels=["0", "1", "2", "3+"]
)

df["emergency_category"] = pd.cut(
    df["number_emergency"],
    bins=[-1, 0, 1, 2, float("inf")],
    labels=["0", "1", "2", "3+"]
)

df["inpatient_category"] = pd.cut(
    df["number_inpatient"],
    bins=[-1, 0, 1, 2, float("inf")],
    labels=["0", "1", "2", "3+"]
)


# ============================================================
# 6. UTILIZATION VARIABLES
# ============================================================

output_lines.append("=" * 70)
output_lines.append("UTILIZATION VARIABLES")
output_lines.append("=" * 70)

# ------------------------------------------------------------
# Outpatient
# ------------------------------------------------------------

output_lines.append("\nOutpatient visits")
output_lines.append("-" * 50)

outpatient_results = calculate_group_rates(
    df,
    "outpatient_category"
)

add_dataframe_to_output(outpatient_results)


# ------------------------------------------------------------
# Emergency
# ------------------------------------------------------------

output_lines.append("Emergency visits")
output_lines.append("-" * 50)

emergency_results = calculate_group_rates(
    df,
    "emergency_category"
)

add_dataframe_to_output(emergency_results)


# ------------------------------------------------------------
# Inpatient
# ------------------------------------------------------------

output_lines.append("Inpatient visits")
output_lines.append("-" * 50)

inpatient_results = calculate_group_rates(
    df,
    "inpatient_category"
)

add_dataframe_to_output(inpatient_results)


# ============================================================
# 7. KEY CATEGORICAL VARIABLES
# ============================================================

output_lines.append("=" * 70)
output_lines.append("KEY CATEGORICAL VARIABLES")
output_lines.append("=" * 70)


categorical_variables = {
    "Diabetes medication": "diabetesMed",
    "Medication change": "change",
    "Insulin": "insulin",
    "Age": "age",
    "Discharge disposition": "discharge_disposition"
}


categorical_results = {}

for display_name, variable in categorical_variables.items():

    output_lines.append(f"\n{display_name}")
    output_lines.append("-" * 50)

    result = calculate_group_rates(
        df,
        variable
    )

    categorical_results[variable] = result

    add_dataframe_to_output(result)


# ============================================================
# 8. PRACTICAL DIFFERENCE SUMMARY
# ============================================================

output_lines.append("=" * 70)
output_lines.append("PRACTICAL DIFFERENCE SUMMARY")
output_lines.append("=" * 70)


def practical_difference(
    dataframe,
    variable,
    minimum_n=100
):
    """
    Calculate the difference between the highest and lowest
    observed rates among categories with at least minimum_n
    encounters.
    """

    valid = dataframe[
        dataframe["encounters"] >= minimum_n
    ].copy()

    if valid.empty:
        return None

    highest = valid.loc[
        valid["early_readmission_rate"].idxmax()
    ]

    lowest = valid.loc[
        valid["early_readmission_rate"].idxmin()
    ]

    difference = (
        highest["early_readmission_rate"]
        - lowest["early_readmission_rate"]
    )

    return {
        "highest_category": highest[variable],
        "highest_rate": highest["early_readmission_rate"],
        "highest_n": highest["encounters"],
        "lowest_category": lowest[variable],
        "lowest_rate": lowest["early_readmission_rate"],
        "lowest_n": lowest["encounters"],
        "difference": difference
    }


# ------------------------------------------------------------
# Outpatient
# ------------------------------------------------------------

summary = practical_difference(
    outpatient_results,
    "outpatient_category"
)

output_lines.append("\nOutpatient visits")

if summary:
    output_lines.append(
        f"  Highest observed category: "
        f"{summary['highest_category']}"
    )

    output_lines.append(
        f"  Highest observed rate: "
        f"{summary['highest_rate']:.2f}% "
        f"(n={summary['highest_n']:,})"
    )

    output_lines.append(
        f"  Lowest observed category: "
        f"{summary['lowest_category']}"
    )

    output_lines.append(
        f"  Lowest observed rate: "
        f"{summary['lowest_rate']:.2f}% "
        f"(n={summary['lowest_n']:,})"
    )

    output_lines.append(
        f"  Absolute difference: "
        f"{summary['difference']:.2f} percentage points"
    )


# ------------------------------------------------------------
# Emergency
# ------------------------------------------------------------

summary = practical_difference(
    emergency_results,
    "emergency_category"
)

output_lines.append("\nEmergency visits")

if summary:
    output_lines.append(
        f"  Highest observed category: "
        f"{summary['highest_category']}"
    )

    output_lines.append(
        f"  Highest observed rate: "
        f"{summary['highest_rate']:.2f}% "
        f"(n={summary['highest_n']:,})"
    )

    output_lines.append(
        f"  Lowest observed category: "
        f"{summary['lowest_category']}"
    )

    output_lines.append(
        f"  Lowest observed rate: "
        f"{summary['lowest_rate']:.2f}% "
        f"(n={summary['lowest_n']:,})"
    )

    output_lines.append(
        f"  Absolute difference: "
        f"{summary['difference']:.2f} percentage points"
    )


# ------------------------------------------------------------
# Inpatient
# ------------------------------------------------------------

summary = practical_difference(
    inpatient_results,
    "inpatient_category"
)

output_lines.append("\nInpatient visits")

if summary:
    output_lines.append(
        f"  Highest observed category: "
        f"{summary['highest_category']}"
    )

    output_lines.append(
        f"  Highest observed rate: "
        f"{summary['highest_rate']:.2f}% "
        f"(n={summary['highest_n']:,})"
    )

    output_lines.append(
        f"  Lowest observed category: "
        f"{summary['lowest_category']}"
    )

    output_lines.append(
        f"  Lowest observed rate: "
        f"{summary['lowest_rate']:.2f}% "
        f"(n={summary['lowest_n']:,})"
    )

    output_lines.append(
        f"  Absolute difference: "
        f"{summary['difference']:.2f} percentage points"
    )


# ------------------------------------------------------------
# Diabetes medication
# ------------------------------------------------------------

summary = practical_difference(
    categorical_results["diabetesMed"],
    "diabetesMed"
)

output_lines.append("\nDiabetes medication")

if summary:
    output_lines.append(
        f"  Highest observed category: "
        f"{summary['highest_category']}"
    )

    output_lines.append(
        f"  Highest observed rate: "
        f"{summary['highest_rate']:.2f}% "
        f"(n={summary['highest_n']:,})"
    )

    output_lines.append(
        f"  Lowest observed category: "
        f"{summary['lowest_category']}"
    )

    output_lines.append(
        f"  Lowest observed rate: "
        f"{summary['lowest_rate']:.2f}% "
        f"(n={summary['lowest_n']:,})"
    )

    output_lines.append(
        f"  Absolute difference: "
        f"{summary['difference']:.2f} percentage points"
    )


# ------------------------------------------------------------
# Medication change
# ------------------------------------------------------------

summary = practical_difference(
    categorical_results["change"],
    "change"
)

output_lines.append("\nMedication change")

if summary:
    output_lines.append(
        f"  Highest observed category: "
        f"{summary['highest_category']}"
    )

    output_lines.append(
        f"  Highest observed rate: "
        f"{summary['highest_rate']:.2f}% "
        f"(n={summary['highest_n']:,})"
    )

    output_lines.append(
        f"  Lowest observed category: "
        f"{summary['lowest_category']}"
    )

    output_lines.append(
        f"  Lowest observed rate: "
        f"{summary['lowest_rate']:.2f}% "
        f"(n={summary['lowest_n']:,})"
    )

    output_lines.append(
        f"  Absolute difference: "
        f"{summary['difference']:.2f} percentage points"
    )


# ------------------------------------------------------------
# Insulin
# ------------------------------------------------------------

summary = practical_difference(
    categorical_results["insulin"],
    "insulin"
)

output_lines.append("\nInsulin")

if summary:
    output_lines.append(
        f"  Highest observed category: "
        f"{summary['highest_category']}"
    )

    output_lines.append(
        f"  Highest observed rate: "
        f"{summary['highest_rate']:.2f}% "
        f"(n={summary['highest_n']:,})"
    )

    output_lines.append(
        f"  Lowest observed category: "
        f"{summary['lowest_category']}"
    )

    output_lines.append(
        f"  Lowest observed rate: "
        f"{summary['lowest_rate']:.2f}% "
        f"(n={summary['lowest_n']:,})"
    )

    output_lines.append(
        f"  Absolute difference: "
        f"{summary['difference']:.2f} percentage points"
    )


# ------------------------------------------------------------
# Age
# ------------------------------------------------------------

summary = practical_difference(
    categorical_results["age"],
    "age"
)

output_lines.append("\nAge")

if summary:
    output_lines.append(
        f"  Highest observed category: "
        f"{summary['highest_category']}"
    )

    output_lines.append(
        f"  Highest observed rate: "
        f"{summary['highest_rate']:.2f}% "
        f"(n={summary['highest_n']:,})"
    )

    output_lines.append(
        f"  Lowest observed category: "
        f"{summary['lowest_category']}"
    )

    output_lines.append(
        f"  Lowest observed rate: "
        f"{summary['lowest_rate']:.2f}% "
        f"(n={summary['lowest_n']:,})"
    )

    output_lines.append(
        f"  Absolute difference: "
        f"{summary['difference']:.2f} percentage points"
    )


# ------------------------------------------------------------
# Discharge disposition
# ------------------------------------------------------------

summary = practical_difference(
    categorical_results["discharge_disposition"],
    "discharge_disposition"
)

output_lines.append("\nDischarge disposition")

if summary:
    output_lines.append(
        f"  Highest observed category: "
        f"{summary['highest_category']}"
    )

    output_lines.append(
        f"  Highest observed rate: "
        f"{summary['highest_rate']:.2f}% "
        f"(n={summary['highest_n']:,})"
    )

    output_lines.append(
        f"  Lowest observed category: "
        f"{summary['lowest_category']}"
    )

    output_lines.append(
        f"  Lowest observed rate: "
        f"{summary['lowest_rate']:.2f}% "
        f"(n={summary['lowest_n']:,})"
    )

    output_lines.append(
        f"  Absolute difference: "
        f"{summary['difference']:.2f} percentage points"
    )


# ============================================================
# 9. KEY COMPARISONS
# ============================================================

output_lines.append("")
output_lines.append("=" * 70)
output_lines.append("KEY COMPARISONS")
output_lines.append("=" * 70)


def get_rate(dataframe, variable, category):
    row = dataframe[
        dataframe[variable].astype(str)
        == str(category)
    ]

    if row.empty:
        return None

    return (
        row.iloc[0]["early_readmission_rate"]
    )


def add_key_comparison(
    title,
    dataframe,
    variable,
    lower_category,
    higher_category
):

    lower_rate = get_rate(
        dataframe,
        variable,
        lower_category
    )

    higher_rate = get_rate(
        dataframe,
        variable,
        higher_category
    )

    if lower_rate is None or higher_rate is None:
        return

    absolute_difference = (
        higher_rate - lower_rate
    )

    relative_difference = (
        absolute_difference
        / lower_rate
        * 100
    )

    output_lines.append(f"\n{title}")

    output_lines.append(
        f"  Lower group rate: "
        f"{lower_rate:.2f}%"
    )

    output_lines.append(
        f"  Higher group rate: "
        f"{higher_rate:.2f}%"
    )

    output_lines.append(
        f"  Absolute difference: "
        f"{absolute_difference:.2f} percentage points"
    )

    output_lines.append(
        f"  Relative difference: "
        f"{relative_difference:.1f}%"
    )


add_key_comparison(
    "Inpatient visits: 0 vs 3+",
    inpatient_results,
    "inpatient_category",
    "0",
    "3+"
)

add_key_comparison(
    "Emergency visits: 0 vs 3+",
    emergency_results,
    "emergency_category",
    "0",
    "3+"
)

# Outpatient 0 vs 1+
outpatient_zero_rate = get_rate(
    outpatient_results,
    "outpatient_category",
    "0"
)

outpatient_nonzero = df[
    df["number_outpatient"] >= 1
]

outpatient_nonzero_rate = (
    outpatient_nonzero["early_readmission"].mean()
    * 100
)

if (
    outpatient_zero_rate is not None
    and outpatient_zero_rate > 0
):

    outpatient_difference = (
        outpatient_nonzero_rate
        - outpatient_zero_rate
    )

    outpatient_relative = (
        outpatient_difference
        / outpatient_zero_rate
        * 100
    )

    output_lines.append(
        "\nOutpatient visits: 0 vs 1+"
    )

    output_lines.append(
        f"  Lower group rate: "
        f"{outpatient_zero_rate:.2f}%"
    )

    output_lines.append(
        f"  Higher group rate: "
        f"{outpatient_nonzero_rate:.2f}%"
    )

    output_lines.append(
        f"  Absolute difference: "
        f"{outpatient_difference:.2f} percentage points"
    )

    output_lines.append(
        f"  Relative difference: "
        f"{outpatient_relative:.1f}%"
    )


# ============================================================
# 10. INTERPRETATION GUIDANCE
# ============================================================

output_lines.append("")
output_lines.append("=" * 70)
output_lines.append("INTERPRETATION GUIDANCE")
output_lines.append("=" * 70)

output_lines.append("")

output_lines.append(
    "Absolute percentage-point difference:"
)

output_lines.append(
    "Difference between two observed early-readmission rates."
)

output_lines.append("")

output_lines.append(
    "Relative difference:"
)

output_lines.append(
    "Percentage increase or decrease relative to "
    "the reference group's observed rate."
)

output_lines.append("")

output_lines.append(
    "Practical significance:"
)

output_lines.append(
    "A statistically significant association may still "
    "have a small practical difference. Therefore, "
    "readmission rates and effect sizes should be "
    "considered together with p-values."
)

output_lines.append("")

output_lines.append(
    "Caution:"
)

output_lines.append(
    "These are encounter-level descriptive associations. "
    "They should not be interpreted as causal effects "
    "or individual patient risk estimates."
)


# ============================================================
# 11. SAVE RESULTS
# ============================================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "\n".join(output_lines)
    )


# ============================================================
# 12. FINAL MESSAGE
# ============================================================

print("\nPractical significance analysis completed.")

print(
    f"Results saved to: {OUTPUT_FILE}"
)

print(
    f"Output lines: {len(output_lines)}"
)