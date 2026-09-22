# ============================================================
# Patient Readmission Analysis
# Stage 6D: Readmission by Hospital Utilization
# ============================================================

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ------------------------------------------------------------
# 1. File paths
# ------------------------------------------------------------

DATA_PATH = "data/processed/diabetic_data_decoded.csv"

FIGURE_PATH_OUTPATIENT = (
    "results/figures/"
    "early_readmission_by_outpatient_visits.png"
)

FIGURE_PATH_EMERGENCY = (
    "results/figures/"
    "early_readmission_by_emergency_visits.png"
)

FIGURE_PATH_INPATIENT = (
    "results/figures/"
    "early_readmission_by_inpatient_visits.png"
)

RESULT_PATH = (
    "results/analysis_results/"
    "readmission_by_utilization.txt"
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
print("STAGE 6D: READMISSION BY HOSPITAL UTILIZATION")
print("=" * 70)

print(
    f"\nDataset shape: {df.shape}"
)


# ------------------------------------------------------------
# 4. Define utilization variables
# ------------------------------------------------------------

utilization_columns = [
    "number_outpatient",
    "number_emergency",
    "number_inpatient"
]


# ------------------------------------------------------------
# 5. Overall early readmission rate
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
# 6. DESCRIPTIVE STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("UTILIZATION DESCRIPTIVE STATISTICS")
print("=" * 70)


descriptive_summary = pd.DataFrame(
    index=utilization_columns,
    columns=[
        "mean",
        "median",
        "75th_percentile",
        "90th_percentile",
        "maximum",
        "zero_count",
        "zero_percentage"
    ]
)


for column in utilization_columns:

    descriptive_summary.loc[column, "mean"] = (
        df[column].mean()
    )

    descriptive_summary.loc[column, "median"] = (
        df[column].median()
    )

    descriptive_summary.loc[
        column,
        "75th_percentile"
    ] = (
        df[column].quantile(0.75)
    )

    descriptive_summary.loc[
        column,
        "90th_percentile"
    ] = (
        df[column].quantile(0.90)
    )

    descriptive_summary.loc[column, "maximum"] = (
        df[column].max()
    )

    zero_count = (
        df[column] == 0
    ).sum()

    descriptive_summary.loc[
        column,
        "zero_count"
    ] = zero_count

    descriptive_summary.loc[
        column,
        "zero_percentage"
    ] = (
        zero_count / len(df) * 100
    )


descriptive_summary = descriptive_summary.round(2)

print(
    descriptive_summary.to_string()
)


# ============================================================
# 7. Compare utilization by readmission status
# ============================================================

print("\n" + "=" * 70)
print("UTILIZATION BY EARLY READMISSION STATUS")
print("=" * 70)


grouped_summary = (
    df.groupby(
        "early_readmission",
        observed=False
    )[utilization_columns]
    .agg(
        [
            "count",
            "mean",
            "median",
            "min",
            "max"
        ]
    )
    .round(2)
)


print(
    grouped_summary.to_string()
)


# ============================================================
# 8. Calculate zero-utilization percentage by target
# ============================================================

print("\n" + "=" * 70)
print("ZERO UTILIZATION BY EARLY READMISSION STATUS")
print("=" * 70)


zero_utilization_summary = {}

for column in utilization_columns:

    summary = (
        df.groupby(
            "early_readmission",
            observed=False
        )[column]
        .apply(
            lambda x: (x == 0).mean() * 100
        )
        .round(2)
    )

    zero_utilization_summary[column] = summary


zero_utilization_df = pd.DataFrame(
    zero_utilization_summary
)

print(
    zero_utilization_df.to_string()
)


# ============================================================
# 9. Create utilization categories
# ============================================================

print("\n" + "=" * 70)
print("CREATING UTILIZATION CATEGORIES")
print("=" * 70)


# We group values so that the plots remain readable.
# 0 = no previous encounters
# 1 = exactly one
# 2 = exactly two
# 3+ = three or more

for column in utilization_columns:

    category_column = f"{column}_category"

    df[category_column] = pd.cut(
        df[column],
        bins=[-1, 0, 1, 2, float("inf")],
        labels=[
            "0",
            "1",
            "2",
            "3+"
        ]
    )

    print(
        f"{column} categories created: "
        f"{category_column}"
    )


# ============================================================
# 10. Calculate readmission rate by utilization category
# ============================================================

category_summaries = {}

for column in utilization_columns:

    category_column = f"{column}_category"

    summary = (
        df.groupby(
            category_column,
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

    summary["early_readmission_rate"] = (
        summary["early_readmissions"]
        / summary["total_encounters"]
        * 100
    ).round(2)

    category_summaries[column] = summary

    print("\n" + "-" * 70)
    print(
        f"{column.upper()} — EARLY READMISSION RATE"
    )
    print("-" * 70)

    print(
        summary.to_string()
    )


# ============================================================
# 11. Function to create utilization plot
# ============================================================

def create_utilization_plot(
    summary,
    category_column,
    title,
    x_label,
    output_path
):

    plot_df = (
        summary
        .reset_index()
    )

    plt.figure(
        figsize=(8, 5)
    )

    sns.barplot(
        data=plot_df,
        x=category_column,
        y="early_readmission_rate"
    )

    plt.title(title)

    plt.xlabel(x_label)

    plt.ylabel(
        "Early Readmission Rate (%)"
    )

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# ============================================================
# 12. Create outpatient utilization plot
# ============================================================

create_utilization_plot(
    category_summaries["number_outpatient"],
    "number_outpatient_category",
    "Early Readmission Rate by Previous Outpatient Visits",
    "Previous Outpatient Visits",
    FIGURE_PATH_OUTPATIENT
)


# ============================================================
# 13. Create emergency utilization plot
# ============================================================

create_utilization_plot(
    category_summaries["number_emergency"],
    "number_emergency_category",
    "Early Readmission Rate by Previous Emergency Visits",
    "Previous Emergency Visits",
    FIGURE_PATH_EMERGENCY
)


# ============================================================
# 14. Create inpatient utilization plot
# ============================================================

create_utilization_plot(
    category_summaries["number_inpatient"],
    "number_inpatient_category",
    "Early Readmission Rate by Previous Inpatient Visits",
    "Previous Inpatient Visits",
    FIGURE_PATH_INPATIENT
)


# ============================================================
# 15. Save analysis results
# ============================================================

with open(
    RESULT_PATH,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "STAGE 6D: READMISSION BY HOSPITAL UTILIZATION\n"
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
        "UTILIZATION DESCRIPTIVE STATISTICS\n"
    )

    file.write(
        "-" * 50 + "\n"
    )

    file.write(
        descriptive_summary.to_string()
    )

    file.write("\n\n")

    file.write(
        "UTILIZATION BY EARLY READMISSION STATUS\n"
    )

    file.write(
        "-" * 50 + "\n"
    )

    file.write(
        grouped_summary.to_string()
    )

    file.write("\n\n")

    file.write(
        "ZERO UTILIZATION BY EARLY READMISSION STATUS\n"
    )

    file.write(
        "-" * 50 + "\n"
    )

    file.write(
        zero_utilization_df.to_string()
    )

    file.write("\n\n")

    for column in utilization_columns:

        file.write(
            "\n"
            + "=" * 70
            + "\n"
        )

        file.write(
            f"{column.upper()} — EARLY READMISSION RATE\n"
        )

        file.write(
            "=" * 70
            + "\n"
        )

        file.write(
            category_summaries[column].to_string()
        )

        file.write("\n")


# ============================================================
# 16. Completion message
# ============================================================

print("\n" + "=" * 70)
print("OUTPUT FILES")
print("=" * 70)

print(
    f"\nOutpatient figure:\n"
    f"{FIGURE_PATH_OUTPATIENT}"
)

print(
    f"\nEmergency figure:\n"
    f"{FIGURE_PATH_EMERGENCY}"
)

print(
    f"\nInpatient figure:\n"
    f"{FIGURE_PATH_INPATIENT}"
)

print(
    f"\nAnalysis results:\n"
    f"{RESULT_PATH}"
)

print("\n" + "=" * 70)
print("STAGE 6D COMPLETE")
print("=" * 70)