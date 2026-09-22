"""
Stage 7B: Practical Significance Analysis

Purpose:
    Quantify the practical magnitude of differences in early
    readmission rates across important variables.

This stage complements statistical significance testing.

Main outputs:
    - Group sizes
    - Early readmission rates
    - Absolute percentage-point differences
    - Relative differences
    - Utilization-category readmission rates

Important:
    These are descriptive associations, not causal effects.
"""

import os

import numpy as np
import pandas as pd


# ============================================================
# 1. Paths
# ============================================================

INPUT_FILE = (
    "data/processed/"
    "diabetic_data_decoded.csv"
)

OUTPUT_DIR = (
    "results/analysis_results"
)

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "practical_significance.txt"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# 2. Load dataset
# ============================================================

df = pd.read_csv(
    INPUT_FILE,
    keep_default_na=False
)

print("=" * 70)
print("STAGE 7B: PRACTICAL SIGNIFICANCE ANALYSIS")
print("=" * 70)

print(
    f"\nDataset shape: {df.shape}"
)


# ============================================================
# 3. Basic target information
# ============================================================

overall_rate = (
    df["early_readmission"].mean()
    * 100
)

total_encounters = len(df)

early_readmissions = (
    df["early_readmission"].sum()
)

print("\n" + "=" * 70)
print("OVERALL READMISSION")
print("=" * 70)

print(
    f"\nTotal encounters: "
    f"{total_encounters:,}"
)

print(
    f"Early readmissions: "
    f"{early_readmissions:,}"
)

print(
    f"Overall early-readmission rate: "
    f"{overall_rate:.2f}%"
)


# ============================================================
# 4. Helper function
# ============================================================

def calculate_group_rates(
    data,
    variable,
    sort_categories=False
):
    """
    Calculate:
        - encounter count
        - early readmission count
        - early readmission rate
        - difference from overall rate
        - relative difference from overall rate
    """

    summary = (
        data
        .groupby(
            variable,
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
            )
        )
        .reset_index()
    )

    summary["early_readmission_rate"] = (
        summary["early_readmissions"]
        / summary["encounters"]
        * 100
    )

    summary["difference_from_overall_pp"] = (
        summary["early_readmission_rate"]
        - overall_rate
    )

    summary["relative_difference_percent"] = (
        (
            summary["early_readmission_rate"]
            - overall_rate
        )
        / overall_rate
        * 100
    )

    if sort_categories:
        summary = summary.sort_values(
            variable
        )

    return summary


# ============================================================
# 5. Utilization categories
# ============================================================

print("\n" + "=" * 70)
print("UTILIZATION ANALYSIS")
print("=" * 70)


# ------------------------------------------------------------
# Outpatient
# ------------------------------------------------------------

df["outpatient_category"] = pd.cut(
    df["number_outpatient"],
    bins=[
        -np.inf,
        0,
        1,
        2,
        np.inf
    ],
    labels=[
        "0",
        "1",
        "2",
        "3+"
    ],
    right=True
)


# ------------------------------------------------------------
# Emergency
# ------------------------------------------------------------

df["emergency_category"] = pd.cut(
    df["number_emergency"],
    bins=[
        -np.inf,
        0,
        1,
        2,
        np.inf
    ],
    labels=[
        "0",
        "1",
        "2",
        "3+"
    ],
    right=True
)


# ------------------------------------------------------------
# Inpatient
# ------------------------------------------------------------

df["inpatient_category"] = pd.cut(
    df["number_inpatient"],
    bins=[
        -np.inf,
        0,
        1,
        2,
        np.inf
    ],
    labels=[
        "0",
        "1",
        "2",
        "3+"
    ],
    right=True
)


utilization_variables = {
    "Outpatient visits": "outpatient_category",
    "Emergency visits": "emergency_category",
    "Inpatient visits": "inpatient_category"
}


utilization_results = {}


for name, variable in utilization_variables.items():

    summary = calculate_group_rates(
        df,
        variable,
        sort_categories=True
    )

    utilization_results[name] = summary

    print(
        f"\n{name}:"
    )

    print(
        summary.to_string(
            index=False
        )
    )


# ============================================================
# 6. Categorical variables
# ============================================================

print("\n" + "=" * 70)
print("KEY CATEGORICAL VARIABLES")
print("=" * 70)


categorical_variables = {
    "Diabetes medication": "diabetesMed",
    "Medication change": "change",
    "Insulin": "insulin",
    "Age": "age",
    "Discharge disposition": "discharge_disposition"
}


categorical_results = {}


for name, variable in categorical_variables.items():

    summary = calculate_group_rates(
        df,
        variable
    )

    categorical_results[name] = summary

    print(
        f"\n{name}:"
    )

    print(
        summary.to_string(
            index=False
        )
    )


# ============================================================
# 7. Calculate strongest practical differences
# ============================================================

print("\n" + "=" * 70)
print("PRACTICAL DIFFERENCE SUMMARY")
print("=" * 70)


def practical_difference(
    summary,
    variable,
    minimum_encounters=100
):
    """
    Identify the highest and lowest observed rates
    among sufficiently large groups.
    """

    filtered = summary[
        summary["encounters"]
        >= minimum_encounters
    ].copy()

    if filtered.empty:
        return None

    highest = filtered.loc[
        filtered["early_readmission_rate"].idxmax()
    ]

    lowest = filtered.loc[
        filtered["early_readmission_rate"].idxmin()
    ]

    absolute_difference = (
        highest["early_readmission_rate"]
        - lowest["early_readmission_rate"]
    )

    return {
        "highest_category":
            highest[variable],

        "highest_rate":
            highest["early_readmission_rate"],

        "highest_n":
            highest["encounters"],

        "lowest_category":
            lowest[variable],

        "lowest_rate":
            lowest["early_readmission_rate"],

        "lowest_n":
            lowest["encounters"],

        "absolute_difference_pp":
            absolute_difference
    }


practical_summaries = {}


for name, summary in utilization_results.items():

    variable = (
        utilization_variables[name]
    )

    result = practical_difference(
        summary,
        variable,
        minimum_encounters=100
    )

    practical_summaries[name] = result


for name, summary in categorical_results.items():

    variable = (
        categorical_variables[name]
    )

    result = practical_difference(
        summary,
        variable,
        minimum_encounters=100
    )

    practical_summaries[name] = result


for name, result in practical_summaries.items():

    if result is None:
        continue

    print(
        f"\n{name}:"
    )

    print(
        f"  Highest observed rate: "
        f"{result['highest_category']} "
        f"({result['highest_rate']:.2f}%, "
        f"n={result['highest_n']:,})"
    )

    print(
        f"  Lowest observed rate: "
        f"{result['lowest_category']} "
        f"({result['lowest_rate']:.2f}%, "
        f"n={result['lowest_n']:,})"
    )

    print(
        f"  Absolute difference: "
        f"{result['absolute_difference_pp']:.2f} "
        f"percentage points"
    )


# ============================================================
# 8. Specific key comparisons
# ============================================================

print("\n" + "=" * 70)
print("KEY COMPARISONS")
print("=" * 70)


key_comparisons = []


# ------------------------------------------------------------
# Inpatient: 0 vs 3+
# ------------------------------------------------------------

inpatient_summary = (
    utilization_results["Inpatient visits"]
)

inpatient_0 = inpatient_summary[
    inpatient_summary["inpatient_category"]
    == "0"
]

inpatient_3plus = inpatient_summary[
    inpatient_summary["inpatient_category"]
    == "3+"
]


if (
    not inpatient_0.empty
    and not inpatient_3plus.empty
):

    rate_0 = (
        inpatient_0.iloc[0]
        ["early_readmission_rate"]
    )

    rate_3plus = (
        inpatient_3plus.iloc[0]
        ["early_readmission_rate"]
    )

    difference = (
        rate_3plus - rate_0
    )

    relative_difference = (
        difference / rate_0 * 100
    )

    key_comparisons.append({
        "comparison":
            "Inpatient visits: 0 vs 3+",

        "lower_group_rate":
            rate_0,

        "higher_group_rate":
            rate_3plus,

        "absolute_difference_pp":
            difference,

        "relative_difference_percent":
            relative_difference
    })

    print(
        f"\nInpatient visits:"
    )

    print(
        f"  0 visits: "
        f"{rate_0:.2f}%"
    )

    print(
        f"  3+ visits: "
        f"{rate_3plus:.2f}%"
    )

    print(
        f"  Difference: "
        f"{difference:.2f} percentage points"
    )

    print(
        f"  Relative difference: "
        f"{relative_difference:.1f}%"
    )


# ------------------------------------------------------------
# Emergency: 0 vs 3+
# ------------------------------------------------------------

emergency_summary = (
    utilization_results["Emergency visits"]
)

emergency_0 = emergency_summary[
    emergency_summary["emergency_category"]
    == "0"
]

emergency_3plus = emergency_summary[
    emergency_summary["emergency_category"]
    == "3+"
]


if (
    not emergency_0.empty
    and not emergency_3plus.empty
):

    rate_0 = (
        emergency_0.iloc[0]
        ["early_readmission_rate"]
    )

    rate_3plus = (
        emergency_3plus.iloc[0]
        ["early_readmission_rate"]
    )

    difference = (
        rate_3plus - rate_0
    )

    relative_difference = (
        difference / rate_0 * 100
    )

    key_comparisons.append({
        "comparison":
            "Emergency visits: 0 vs 3+",

        "lower_group_rate":
            rate_0,

        "higher_group_rate":
            rate_3plus,

        "absolute_difference_pp":
            difference,

        "relative_difference_percent":
            relative_difference
    })

    print(
        f"\nEmergency visits:"
    )

    print(
        f"  0 visits: "
        f"{rate_0:.2f}%"
    )

    print(
        f"  3+ visits: "
        f"{rate_3plus:.2f}%"
    )

    print(
        f"  Difference: "
        f"{difference:.2f} percentage points"
    )

    print(
        f"  Relative difference: "
        f"{relative_difference:.1f}%"
    )


# ------------------------------------------------------------
# Outpatient: 0 vs 1+
# ------------------------------------------------------------

outpatient_summary = (
    utilization_results["Outpatient visits"]
)

outpatient_0 = outpatient_summary[
    outpatient_summary["outpatient_category"]
    == "0"
]

outpatient_nonzero = (
    df["number_outpatient"] > 0
)

outpatient_nonzero_rate = (
    df.loc[
        outpatient_nonzero,
        "early_readmission"
    ].mean()
    * 100
)

outpatient_zero_rate = (
    df.loc[
        ~outpatient_nonzero,
        "early_readmission"
    ].mean()
    * 100
)

difference = (
    outpatient_nonzero_rate
    - outpatient_zero_rate
)

relative_difference = (
    difference
    / outpatient_zero_rate
    * 100
)

key_comparisons.append({
    "comparison":
        "Outpatient visits: 0 vs 1+",

    "lower_group_rate":
        outpatient_zero_rate,

    "higher_group_rate":
        outpatient_nonzero_rate,

    "absolute_difference_pp":
        difference,

    "relative_difference_percent":
        relative_difference
})


print(
    f"\nOutpatient visits:"
)

print(
    f"  0 visits: "
    f"{outpatient_zero_rate:.2f}%"
)

print(
    f"  1+ visits: "
    f"{outpatient_nonzero_rate:.2f}%"
)

print(
    f"  Difference: "
    f"{difference:.2f} percentage points"
)

print(
    f"  Relative difference: "
    f"{relative_difference:.1f}%"
)


# ============================================================
# 9. Save results
# ============================================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "STAGE 7B: PRACTICAL SIGNIFICANCE ANALYSIS\n"
    )

    file.write("=" * 70 + "\n\n")

    file.write(
        f"Dataset shape: {df.shape}\n"
    )

    file.write(
        f"Total encounters: "
        f"{total_encounters:,}\n"
    )

    file.write(
        f"Early readmissions: "
        f"{early_readmissions:,}\n"
    )

    file.write(
        f"Overall early-readmission rate: "
        f"{overall_rate:.2f}%\n\n"
    )

    file.write(
        "Purpose:\n"
        "Quantify the practical magnitude of observed "
        "differences in early-readmission rates.\n\n"
    )

    file.write(
        "Important interpretation note:\n"
        "These results describe associations between "
        "encounter characteristics and early readmission. "
        "They do not establish causality.\n\n"
    )

    # --------------------------------------------------------
    # Utilization
    # --------------------------------------------------------

    file.write("=" * 70 + "\n")
    file.write(
        "UTILIZATION VARIABLES\n"
    )
    file.write("=" * 70 + "\n\n")

    for name, summary in utilization_results.items():

        file.write(
            f"{name}\n"
        )

        file.write(
            "-" * 50 + "\n"
        )

        file.write(
            summary.to_string(
                index=False
            )
        )

        file.write("\n\n")

    # --------------------------------------------------------
    # Categorical
    # --------------------------------------------------------

    file.write("=" * 70 + "\n")
    file.write(
        "KEY CATEGORICAL VARIABLES\n"
    )
    file.write("=" * 70 + "\n\n")

    for name, summary in categorical_results.items():

        file.write(
            f"{name}\n"
        )

        file.write(
            "-" * 50 + "\n"
        )

        file.write(
            summary.to_string(
                index=False
            )
        )

        file.write("\n\n")

    # --------------------------------------------------------
    # Practical differences
    # --------------------------------------------------------

    file.write("=" * 70 + "\n")
    file.write(
        "PRACTICAL DIFFERENCE SUMMARY\n"
    )
    file.write("=" * 70 + "\n\n")

    for name, result in practical_summaries.items():

        if result is None:
            continue

        file.write(
            f"{name}\n"
        )

        file.write(
            f"  Highest observed category: "
            f"{result['highest_category']}\n"
        )

        file.write(
            f"  Highest observed rate: "
            f"{result['highest_rate']:.2f}% "
            f"(n={result['highest_n']:,})\n"
        )

        file.write(
            f"  Lowest observed category: "
            f"{result['lowest_category']}\n"
        )

        file.write(
            f"  Lowest observed rate: "
            f"{result['lowest_rate']:.2f}% "
            f"(n={result['lowest_n']:,})\n"
        )

        file.write(
            f"  Absolute difference: "
            f"{result['absolute_difference_pp']:.2f} "
            f"percentage points\n\n"
        )

    # --------------------------------------------------------
    # Key comparisons
    # --------------------------------------------------------

    file.write("=" * 70 + "\n")
    file.write(
        "KEY COMPARISONS\n"
    )
    file.write("=" * 70 + "\n\n")

    for comparison in key_comparisons:

        file.write(
            f"{comparison['comparison']}\n"
        )

        file.write(
            f"  Lower group rate: "
            f"{comparison['lower_group_rate']:.2f}%\n"
        )

        file.write(
            f"  Higher group rate: "
            f"{comparison['higher_group_rate']:.2f}%\n"
        )

        file.write(
            f"  Absolute difference: "
            f"{comparison['absolute_difference_pp']:.2f} "
            f"percentage points\n"
        )

        file.write(
            f"  Relative difference: "
            f"{comparison['relative_difference_percent']:.1f}%\n\n"
        )

    # --------------------------------------------------------
    # Final interpretation
    # --------------------------------------------------------

    file.write("=" * 70 + "\n")
    file.write(
        "INTERPRETATION GUIDANCE\n"
    )
    file.write("=" * 70 + "\n\n")

    file.write(
        "Absolute percentage-point difference:\n"
        "Difference between two observed early-readmission "
        "rates.\n\n"
    )

    file.write(
        "Relative difference:\n"
        "Percentage increase or decrease relative to the "
        "reference group's observed rate.\n\n"
    )

    file.write(
        "Practical significance:\n"
        "A statistically significant association may still "
        "have a small practical difference. Therefore, "
        "readmission rates and effect sizes should be "
        "considered together with p-values.\n\n"
    )

    file.write(
        "Caution:\n"
        "These are encounter-level descriptive associations. "
        "They should not be interpreted as causal effects "
        "or individual patient risk estimates.\n"
    )


# ============================================================
# 10. Completion
# ============================================================

print("\n" + "=" * 70)
print("STAGE 7B COMPLETE")
print("=" * 70)

print(
    "\nResults saved to:"
)

print(
    f"  {OUTPUT_FILE}"
)