import pandas as pd
from pathlib import Path


# CONFIGURATION

DATA_PATH = Path("data/Superstore_sales_dataset.csv")
OUTPUT_DIR = Path("output/audit")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# LOAD DATA

print("=" * 70)
print("SUPERSTORE SALES DATA AUDIT")
print("=" * 70)

print("\nLoading dataset...")

df = pd.read_csv(DATA_PATH)

print(f"Dataset loaded successfully: {DATA_PATH}")


# BASIC DATASET INFORMATION

print("\n" + "=" * 70)
print("1. DATASET OVERVIEW")
print("=" * 70)

print(f"\nNumber of records: {len(df):,}")
print(f"Number of columns: {len(df.columns):,}")

print("\nColumns:")
for i, column in enumerate(df.columns, start=1):
    print(f"  {i:2}. {column}")


# DATA TYPES

print("\n" + "=" * 70)
print("2. DATA TYPES")
print("=" * 70)

print(df.dtypes)


# DATE CONVERSION

print("\n" + "=" * 70)
print("3. DATE INFORMATION")
print("=" * 70)

# Convert date columns to datetime
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    errors="coerce"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    errors="coerce"
)

print(
    f"\nOrder date range: "
    f"{df['Order Date'].min().date()} "
    f"→ "
    f"{df['Order Date'].max().date()}"
)

print(
    f"Ship date range: "
    f"{df['Ship Date'].min().date()} "
    f"→ "
    f"{df['Ship Date'].max().date()}"
)


# UNIQUE ENTITY COUNTS

print("\n" + "=" * 70)
print("4. UNIQUE ENTITIES")
print("=" * 70)

unique_entities = {
    "Customers": df["Customer ID"].nunique(),
    "Orders": df["Order ID"].nunique(),
    "Products": df["Product ID"].nunique(),
    "Cities": df["City"].nunique(),
    "States": df["State"].nunique(),
    "Regions": df["Region"].nunique(),
    "Categories": df["Category"].nunique(),
    "Sub-Categories": df["Sub-Category"].nunique(),
    "Segments": df["Segment"].nunique(),
    "Ship Modes": df["Ship Mode"].nunique(),
}

for entity, count in unique_entities.items():
    print(f"{entity:20}: {count:,}")


# CATEGORICAL VALUES

print("\n" + "=" * 70)
print("5. CATEGORICAL VALUES")
print("=" * 70)

categorical_columns = [
    "Category",
    "Sub-Category",
    "Region",
    "Segment",
    "Ship Mode"
]

for column in categorical_columns:

    print(f"\n--- {column} ---")

    values = sorted(
        df[column]
        .dropna()
        .unique()
        .tolist()
    )

    for value in values:
        print(f"  {value}")


# CATEGORY DISTRIBUTIONS

print("\n" + "=" * 70)
print("6. CATEGORY DISTRIBUTIONS")
print("=" * 70)

for column in categorical_columns:

    print(f"\n--- {column} ---")

    counts = df[column].value_counts()

    print(counts)


# MISSING VALUES

print("\n" + "=" * 70)
print("7. MISSING VALUES")
print("=" * 70)

missing = pd.DataFrame({
    "column": df.columns,
    "missing_count": df.isnull().sum().values,
})

missing["missing_percentage"] = (
    missing["missing_count"] / len(df) * 100
)

missing_nonzero = missing[
    missing["missing_count"] > 0
].copy()

if missing_nonzero.empty:
    print("\nNo missing values detected.")
else:
    print("\nColumns containing missing values:")
    print(
        missing_nonzero.to_string(index=False)
    )


# DUPLICATE RECORDS

print("\n" + "=" * 70)
print("8. DUPLICATE RECORDS")
print("=" * 70)

duplicate_count = df.duplicated().sum()

print(f"\nDuplicate rows: {duplicate_count:,}")

if duplicate_count == 0:
    print("No exact duplicate rows detected.")
else:
    print("Duplicate rows were detected.")


# DUPLICATE ORDER IDS

print("\n" + "=" * 70)
print("9. ORDER STRUCTURE")
print("=" * 70)

order_counts = df["Order ID"].value_counts()

print(
    f"\nAverage records per order: "
    f"{len(df) / df['Order ID'].nunique():.2f}"
)

print(
    f"Orders containing multiple records: "
    f"{(order_counts > 1).sum():,}"
)

print(
    f"Largest number of records for one order: "
    f"{order_counts.max():,}"
)


# CUSTOMER STRUCTURE

print("\n" + "=" * 70)
print("10. CUSTOMER STRUCTURE")
print("=" * 70)

customer_order_counts = (
    df.groupby("Customer ID")["Order ID"]
      .nunique()
)

print(
    f"\nAverage orders per customer: "
    f"{customer_order_counts.mean():.2f}"
)

print(
    f"Customers with multiple orders: "
    f"{(customer_order_counts > 1).sum():,}"
)

print(
    f"Maximum orders from one customer: "
    f"{customer_order_counts.max():,}"
)


# NUMERIC COLUMN SUMMARY

print("\n" + "=" * 70)
print("11. NUMERIC VARIABLES")
print("=" * 70)

numeric_columns = df.select_dtypes(
    include="number"
).columns.tolist()

print("\nNumeric columns:")

for column in numeric_columns:
    print(f"  {column}")

print("\nDescriptive statistics:")

print(
    df[numeric_columns]
    .describe()
    .transpose()
    .to_string()
)


# NEGATIVE VALUES

print("\n" + "=" * 70)
print("12. NEGATIVE VALUES")
print("=" * 70)

for column in numeric_columns:

    negative_count = (
        df[column] < 0
    ).sum()

    if negative_count > 0:

        print(
            f"{column:15}: "
            f"{negative_count:,} negative values"
        )


# ZERO VALUES

print("\n" + "=" * 70)
print("13. ZERO VALUES")
print("=" * 70)

for column in numeric_columns:

    zero_count = (
        df[column] == 0
    ).sum()

    if zero_count > 0:

        print(
            f"{column:15}: "
            f"{zero_count:,} zero values"
        )


# DATE VALIDATION

print("\n" + "=" * 70)
print("14. DATE VALIDATION")
print("=" * 70)

invalid_order_dates = df["Order Date"].isna().sum()
invalid_ship_dates = df["Ship Date"].isna().sum()

print(
    f"\nInvalid/missing Order Dates: "
    f"{invalid_order_dates:,}"
)

print(
    f"Invalid/missing Ship Dates: "
    f"{invalid_ship_dates:,}"
)

ship_before_order = (
    df["Ship Date"] < df["Order Date"]
).sum()

print(
    f"Ship dates before order dates: "
    f"{ship_before_order:,}"
)


# SHIPPING DURATION

print("\n" + "=" * 70)
print("15. SHIPPING DURATION")
print("=" * 70)

df["Shipping Duration"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

print(
    f"\nAverage shipping duration: "
    f"{df['Shipping Duration'].mean():.2f} days"
)

print(
    f"Minimum shipping duration: "
    f"{df['Shipping Duration'].min()} days"
)

print(
    f"Maximum shipping duration: "
    f"{df['Shipping Duration'].max()} days"
)


# DATASET SUMMARY

print("\n" + "=" * 70)
print("16. AUDIT SUMMARY")
print("=" * 70)

audit_summary = pd.DataFrame([
    ["Records", len(df)],
    ["Columns", len(df.columns)],
    ["Unique Customers", df["Customer ID"].nunique()],
    ["Unique Orders", df["Order ID"].nunique()],
    ["Unique Products", df["Product ID"].nunique()],
    ["Unique Cities", df["City"].nunique()],
    ["Unique States", df["State"].nunique()],
    ["Unique Regions", df["Region"].nunique()],
    ["Categories", df["Category"].nunique()],
    ["Sub-Categories", df["Sub-Category"].nunique()],
    ["Segments", df["Segment"].nunique()],
    ["Ship Modes", df["Ship Mode"].nunique()],
    ["Duplicate Rows", duplicate_count],
    ["Missing Cells", df.isnull().sum().sum()],
    ["Invalid Order Dates", invalid_order_dates],
    ["Invalid Ship Dates", invalid_ship_dates],
    ["Ship Before Order", ship_before_order],
])

audit_summary.columns = [
    "Metric",
    "Value"
]

print(
    audit_summary.to_string(index=False)
)


# DATA DICTIONARY

print("\n" + "=" * 70)
print("17. DATA DICTIONARY")
print("=" * 70)

data_dictionary = pd.DataFrame({
    "column": df.columns,
    "data_type": df.dtypes.astype(str).values,
    "missing_values": df.isnull().sum().values,
    "missing_percentage": (
        df.isnull().sum().values / len(df) * 100
    ),
    "unique_values": df.nunique().values
})

print(
    data_dictionary.to_string(index=False)
)


# SAVE AUDIT OUTPUTS

print("\n" + "=" * 70)
print("18. SAVING AUDIT OUTPUTS")
print("=" * 70)

audit_summary.to_csv(
    OUTPUT_DIR / "audit_summary.csv",
    index=False
)

missing.to_csv(
    OUTPUT_DIR / "missing_values.csv",
    index=False
)

data_dictionary.to_csv(
    OUTPUT_DIR / "data_dictionary.csv",
    index=False
)

# Save categorical distributions
for column in categorical_columns:

    counts = (
        df[column]
        .value_counts()
        .rename_axis(column)
        .reset_index(name="count")
    )

    safe_name = (
        column
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )

    counts.to_csv(
        OUTPUT_DIR / f"{safe_name}_distribution.csv",
        index=False
    )


# FINAL MESSAGE

print("\nAudit complete.")

print(
    f"\nAudit files saved to: "
    f"{OUTPUT_DIR}"
)

print("\nGenerated files:")

for file in sorted(OUTPUT_DIR.iterdir()):
    print(f"  - {file.name}")

print("\n" + "=" * 70)