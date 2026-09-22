# ============================================================
# Patient Readmission Analysis
# Stage 5C: Decode Administrative ID Variables
# ============================================================

import pandas as pd


# ------------------------------------------------------------
# 1. File paths
# ------------------------------------------------------------

DATA_PATH = "data/processed/diabetic_data_cleaned.csv"
MAPPING_PATH = "data/raw/IDS_mapping.csv"
OUTPUT_PATH = "data/processed/diabetic_data_decoded.csv"


# ------------------------------------------------------------
# 2. Load dataset
# ------------------------------------------------------------

df = pd.read_csv(DATA_PATH)

print("=" * 70)
print("STAGE 5C: DECODE ADMINISTRATIVE ID VARIABLES")
print("=" * 70)

print(f"\nDataset before decoding: {df.shape}")


# ------------------------------------------------------------
# 3. Load mapping file
# ------------------------------------------------------------

# keep_default_na=False is important because the mapping file
# contains the literal text "NULL".
mapping_raw = pd.read_csv(
    MAPPING_PATH,
    header=None,
    dtype=str,
    keep_default_na=False
)

print(f"Mapping file shape: {mapping_raw.shape}")


# ------------------------------------------------------------
# 4. Identify mapping sections
# ------------------------------------------------------------

section_starts = []

for i in range(len(mapping_raw)):

    first_value = str(mapping_raw.iloc[i, 0]).strip()

    if first_value in [
        "admission_type_id",
        "discharge_disposition_id",
        "admission_source_id"
    ]:
        section_starts.append(i)


print(f"Mapping section starts: {section_starts}")


# ------------------------------------------------------------
# 5. Extract a mapping section
# ------------------------------------------------------------

def extract_mapping(start_row, end_row, id_column, description_column):

    section = mapping_raw.iloc[
        start_row:end_row
    ].copy()

    # First row contains the section header
    section.columns = section.iloc[0]

    # Remove header row
    section = section.iloc[1:].copy()

    # Keep only the required columns
    section = section[
        [id_column, description_column]
    ].copy()

    section.columns = [
        id_column,
        description_column
    ]

    # Remove completely empty rows
    section = section[
        section[id_column].astype(str).str.strip() != ""
    ].copy()

    # Preserve literal NULL values
    section[description_column] = (
        section[description_column]
        .astype(str)
        .str.strip()
    )

    # Explicitly convert empty descriptions to NULL
    section.loc[
        section[description_column] == "",
        description_column
    ] = "NULL"

    # Explicitly protect the literal NULL value
    section[description_column] = (
        section[description_column]
        .replace({
            "nan": "NULL",
            "NaN": "NULL",
            "None": "NULL"
        })
    )

    # Convert ID to integer
    section[id_column] = pd.to_numeric(
        section[id_column],
        errors="coerce"
    )

    section = section.dropna(
        subset=[id_column]
    )

    section[id_column] = section[id_column].astype(int)

    return section


# ------------------------------------------------------------
# 6. Extract all three mappings
# ------------------------------------------------------------

admission_type_mapping = extract_mapping(
    section_starts[0],
    section_starts[1],
    "admission_type_id",
    "description"
)

discharge_mapping = extract_mapping(
    section_starts[1],
    section_starts[2],
    "discharge_disposition_id",
    "description"
)

admission_source_mapping = extract_mapping(
    section_starts[2],
    len(mapping_raw),
    "admission_source_id",
    "description"
)


# ------------------------------------------------------------
# 7. Display mappings
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("ADMISSION TYPE MAPPING")
print("=" * 70)

print(
    admission_type_mapping.to_string(index=False)
)


print("\n" + "=" * 70)
print("DISCHARGE DISPOSITION MAPPING")
print("=" * 70)

print(
    discharge_mapping.to_string(index=False)
)


print("\n" + "=" * 70)
print("ADMISSION SOURCE MAPPING")
print("=" * 70)

print(
    admission_source_mapping.to_string(index=False)
)


# ------------------------------------------------------------
# 8. Merge admission type
# ------------------------------------------------------------

df = df.merge(
    admission_type_mapping,
    on="admission_type_id",
    how="left"
)

df = df.rename(
    columns={
        "description": "admission_type"
    }
)


# ------------------------------------------------------------
# 9. Merge discharge disposition
# ------------------------------------------------------------

df = df.merge(
    discharge_mapping,
    on="discharge_disposition_id",
    how="left"
)

df = df.rename(
    columns={
        "description": "discharge_disposition"
    }
)


# ------------------------------------------------------------
# 10. Merge admission source
# ------------------------------------------------------------

df = df.merge(
    admission_source_mapping,
    on="admission_source_id",
    how="left"
)

df = df.rename(
    columns={
        "description": "admission_source"
    }
)


# ------------------------------------------------------------
# 11. Final protection against NaN
# ------------------------------------------------------------

decoded_columns = [
    "admission_type",
    "discharge_disposition",
    "admission_source"
]

for column in decoded_columns:

    df[column] = (
        df[column]
        .astype("string")
        .fillna("NULL")
        .astype(str)
    )


# ------------------------------------------------------------
# 12. Check for unmapped IDs
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("UNMAPPED ID CHECK")
print("=" * 70)

for id_column, decoded_column in [
    ("admission_type_id", "admission_type"),
    ("discharge_disposition_id", "discharge_disposition"),
    ("admission_source_id", "admission_source")
]:

    unmapped = (
        df[decoded_column]
        .isna()
        .sum()
    )

    print(
        f"{id_column}: "
        f"{unmapped} unmapped values"
    )


# ------------------------------------------------------------
# 13. Verify NULL categories
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("NULL CATEGORY CHECK")
print("=" * 70)

for column in decoded_columns:

    null_count = (
        df[column] == "NULL"
    ).sum()

    print(
        f"{column}: "
        f"{null_count:,} literal NULL values"
    )


# ------------------------------------------------------------
# 14. Display decoded value counts
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("DECODED VALUE COUNTS")
print("=" * 70)


for column in decoded_columns:

    print("\n" + "-" * 70)
    print(column)
    print("-" * 70)

    print(
        df[column]
        .value_counts(dropna=False)
        .to_string()
    )


# ------------------------------------------------------------
# 15. Verify row count
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("ROW COUNT VERIFICATION")
print("=" * 70)

print(
    f"Rows before decoding: 101,766"
)

print(
    f"Rows after decoding:  {len(df):,}"
)

if len(df) == 101766:
    print("Row count preserved: PASS")
else:
    print("Row count preserved: REVIEW")


# ------------------------------------------------------------
# 16. Verify duplicate rows
# ------------------------------------------------------------

duplicate_rows = df.duplicated().sum()

print(
    f"\nDuplicate complete rows: "
    f"{duplicate_rows:,}"
)

if duplicate_rows == 0:
    print("Duplicate check: PASS")
else:
    print("Duplicate check: REVIEW")


# ------------------------------------------------------------
# 17. Verify encounter IDs
# ------------------------------------------------------------

unique_encounters = df["encounter_id"].nunique()

print(
    f"\nUnique encounter IDs: "
    f"{unique_encounters:,}"
)

if unique_encounters == len(df):
    print("Encounter uniqueness: PASS")
else:
    print("Encounter uniqueness: REVIEW")


# ------------------------------------------------------------
# 18. Final NaN check
# ------------------------------------------------------------

total_nan = df.isna().sum().sum()

print(
    f"\nTotal NaN values in dataset: "
    f"{total_nan:,}"
)


# ------------------------------------------------------------
# 19. Save decoded dataset
# ------------------------------------------------------------

df.to_csv(
    OUTPUT_PATH,
    index=False
)

print(
    f"\nDecoded dataset saved to:\n"
    f"{OUTPUT_PATH}"
)

print("\n" + "=" * 70)
print("STAGE 5C COMPLETE")
print("=" * 70)