"""
Patient Readmission Analysis
Stage 20: Create Portfolio Visualizations

Creates key visualizations for the final analysis dataset.
"""

import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# 1. File paths
# ============================================================

INPUT_FILE = "data/processed/patient_readmission_analysis.csv"
OUTPUT_DIR = "results/figures"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# 2. Load data
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("=" * 70)
print("PATIENT READMISSION VISUALIZATION")
print("=" * 70)

print(f"Rows: {len(df):,}")
print(f"Columns: {df.shape[1]}")


# ============================================================
# 3. Overall readmission distribution
# ============================================================

readmission_counts = (
    df["early_readmission"]
    .value_counts()
    .sort_index()
)

readmission_labels = ["No Early Readmission", "Early Readmission"]

plt.figure(figsize=(8, 6))

ax = sns.barplot(
    x=readmission_labels,
    y=readmission_counts.values
)

plt.title("Early Readmission Distribution")
plt.xlabel("Readmission Status")
plt.ylabel("Number of Encounters")

for container in ax.containers:
    ax.bar_label(container, fmt="%d")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "01_early_readmission_distribution.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 4. Readmission rate by age group
# ============================================================

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

age_analysis = (
    df.groupby("age", observed=True)["early_readmission"]
    .agg(["mean", "count"])
    .reset_index()
)

age_analysis["readmission_rate"] = age_analysis["mean"] * 100

age_analysis["age"] = pd.Categorical(
    age_analysis["age"],
    categories=age_order,
    ordered=True
)

age_analysis = age_analysis.sort_values("age")

plt.figure(figsize=(10, 6))

ax = sns.barplot(
    data=age_analysis,
    x="age",
    y="readmission_rate"
)

plt.title("Early Readmission Rate by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Early Readmission Rate (%)")
plt.xticks(rotation=45)

for container in ax.containers:
    ax.bar_label(
        container,
        fmt="%.1f%%",
        padding=3
    )

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "02_readmission_by_age.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 5. Readmission rate by prior inpatient utilization
# ============================================================

inpatient_order = ["0", "1", "2", "3+"]

inpatient_analysis = (
    df.groupby("inpatient_visits_group", observed=True)
    ["early_readmission"]
    .agg(["mean", "count"])
    .reset_index()
)

inpatient_analysis["readmission_rate"] = (
    inpatient_analysis["mean"] * 100
)

inpatient_analysis["inpatient_visits_group"] = pd.Categorical(
    inpatient_analysis["inpatient_visits_group"],
    categories=inpatient_order,
    ordered=True
)

inpatient_analysis = inpatient_analysis.sort_values(
    "inpatient_visits_group"
)

plt.figure(figsize=(8, 6))

ax = sns.barplot(
    data=inpatient_analysis,
    x="inpatient_visits_group",
    y="readmission_rate"
)

plt.title("Early Readmission Rate by Prior Inpatient Visits")
plt.xlabel("Prior Inpatient Visits")
plt.ylabel("Early Readmission Rate (%)")

for container in ax.containers:
    ax.bar_label(
        container,
        fmt="%.1f%%",
        padding=3
    )

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "03_readmission_by_inpatient_visits.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 6. Readmission rate by prior emergency utilization
# ============================================================

emergency_order = ["0", "1", "2", "3+"]

emergency_analysis = (
    df.groupby("emergency_visits_group", observed=True)
    ["early_readmission"]
    .agg(["mean", "count"])
    .reset_index()
)

emergency_analysis["readmission_rate"] = (
    emergency_analysis["mean"] * 100
)

emergency_analysis["emergency_visits_group"] = pd.Categorical(
    emergency_analysis["emergency_visits_group"],
    categories=emergency_order,
    ordered=True
)

emergency_analysis = emergency_analysis.sort_values(
    "emergency_visits_group"
)

plt.figure(figsize=(8, 6))

ax = sns.barplot(
    data=emergency_analysis,
    x="emergency_visits_group",
    y="readmission_rate"
)

plt.title("Early Readmission Rate by Prior Emergency Visits")
plt.xlabel("Prior Emergency Visits")
plt.ylabel("Early Readmission Rate (%)")

for container in ax.containers:
    ax.bar_label(
        container,
        fmt="%.1f%%",
        padding=3
    )

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "04_readmission_by_emergency_visits.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 7. Readmission rate by diabetes medication use
# ============================================================

medication_analysis = (
    df.groupby("diabetesMed", observed=True)
    ["early_readmission"]
    .agg(["mean", "count"])
    .reset_index()
)

medication_analysis["readmission_rate"] = (
    medication_analysis["mean"] * 100
)

plt.figure(figsize=(8, 6))

ax = sns.barplot(
    data=medication_analysis,
    x="diabetesMed",
    y="readmission_rate"
)

plt.title("Early Readmission Rate by Diabetes Medication Use")
plt.xlabel("Diabetes Medication")
plt.ylabel("Early Readmission Rate (%)")

for container in ax.containers:
    ax.bar_label(
        container,
        fmt="%.1f%%",
        padding=3
    )

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "05_readmission_by_diabetes_medication.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 8. Readmission rate by primary diagnosis
# ============================================================

diagnosis_analysis = (
    df.groupby("primary_diagnosis_category", observed=True)
    ["early_readmission"]
    .agg(["mean", "count"])
    .reset_index()
)

diagnosis_analysis["readmission_rate"] = (
    diagnosis_analysis["mean"] * 100
)

# Keep categories with at least 1,000 encounters
diagnosis_analysis = diagnosis_analysis[
    diagnosis_analysis["count"] >= 1000
]

diagnosis_analysis = diagnosis_analysis.sort_values(
    "readmission_rate",
    ascending=True
)

plt.figure(figsize=(10, 8))

ax = sns.barplot(
    data=diagnosis_analysis,
    x="readmission_rate",
    y="primary_diagnosis_category"
)

plt.title(
    "Early Readmission Rate by Primary Diagnosis Category"
)

plt.xlabel("Early Readmission Rate (%)")
plt.ylabel("Primary Diagnosis Category")

for container in ax.containers:
    ax.bar_label(
        container,
        fmt="%.1f%%",
        padding=3
    )

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "06_readmission_by_primary_diagnosis.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 9. Readmission rate by discharge disposition
# ============================================================

discharge_analysis = (
    df.groupby("discharge_disposition", observed=True)
    ["early_readmission"]
    .agg(["mean", "count"])
    .reset_index()
)

discharge_analysis["readmission_rate"] = (
    discharge_analysis["mean"] * 100
)

# Keep categories with at least 1,000 encounters
discharge_analysis = discharge_analysis[
    discharge_analysis["count"] >= 1000
]

discharge_analysis = discharge_analysis.sort_values(
    "readmission_rate",
    ascending=True
)

plt.figure(figsize=(11, 8))

ax = sns.barplot(
    data=discharge_analysis,
    x="readmission_rate",
    y="discharge_disposition"
)

plt.title(
    "Early Readmission Rate by Discharge Disposition"
)

plt.xlabel("Early Readmission Rate (%)")
plt.ylabel("Discharge Disposition")

for container in ax.containers:
    ax.bar_label(
        container,
        fmt="%.1f%%",
        padding=3
    )

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "07_readmission_by_discharge_disposition.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 10. Combined utilization comparison
# ============================================================

utilization_data = pd.concat(
    [
        inpatient_analysis.assign(
            utilization_type="Inpatient"
        ).rename(
            columns={
                "inpatient_visits_group": "utilization_group"
            }
        ),

        emergency_analysis.assign(
            utilization_type="Emergency"
        ).rename(
            columns={
                "emergency_visits_group": "utilization_group"
            }
        )
    ],
    ignore_index=True
)

plt.figure(figsize=(10, 6))

sns.barplot(
    data=utilization_data,
    x="utilization_group",
    y="readmission_rate",
    hue="utilization_type"
)

plt.title("Early Readmission Rate by Prior Healthcare Utilization")
plt.xlabel("Prior Visits")
plt.ylabel("Early Readmission Rate (%)")
plt.legend(title="Utilization Type")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "08_utilization_comparison.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 11. Final output summary
# ============================================================

print("\nVisualization generation completed.")
print(f"Figures saved to: {OUTPUT_DIR}")

print("\nGenerated files:")

for filename in sorted(os.listdir(OUTPUT_DIR)):
    if filename.endswith(".png"):
        print(f"  - {filename}")

print("\n" + "=" * 70)