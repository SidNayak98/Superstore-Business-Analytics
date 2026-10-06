import pandas as pd
from pathlib import Path


# CONFIGURATION

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "Superstore_sales_dataset.csv"

OUTPUT_DIR = PROJECT_ROOT / "output" / "cleaning"
CLEANED_DATA_PATH = PROJECT_ROOT / "data" / "Superstore_sales_cleaned.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# LOAD DATA

print("=" * 70)
print("SUPERSTORE SALES DATA CLEANING")
print("=" * 70)

print("\nLoading dataset...")

df = pd.read_csv(DATA_PATH)

print(f"Dataset loaded successfully: {DATA_PATH}")
print(f"Original records: {len(df):,}")
print(f"Original columns: {len(df.columns):,}")


# RECORD INITIAL STATE

original_record_count = len(df)
original_column_count = len(df.columns)


# STANDARDIZE COLUMN NAMES

print("\n" + "=" * 70)
print("1. COLUMN NAME STANDARDIZATION")
print("=" * 70)

# Remove leading/trailing whitespace from column names
df.columns = df.columns.str.strip()

print("\nColumn names standardized.")

print("\nColumns:")
for column in df.columns:
    print(f"  {column}")


# STANDARDIZE TEXT FIELDS

print("\n" + "=" * 70)
print("2. TEXT STANDARDIZATION")
print("=" * 70)

text_columns = df.select_dtypes(
    include=["object"]
).columns.tolist()

for column in text_columns:

    # Remove leading/trailing whitespace
    df[column] = df[column].str.strip()

print(
    f"\nStandardized {len(text_columns)} text columns."
)


# STANDARDIZE DATE COLUMNS

print("\n" + "=" * 70)
print("3. DATE STANDARDIZATION")
print("=" * 70)

date_columns = [
    "Order Date",
    "Ship Date"
]

for column in date_columns:

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce",
        format="mixed"
    )

    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"],
        errors="coerce",
        format="mixed"
    )

    print(
        f"{column}: converted to datetime"
    )


# STANDARDIZE NUMERIC COLUMNS

print("\n" + "=" * 70)
print("4. NUMERIC STANDARDIZATION")
print("=" * 70)

numeric_columns = [
    "Row ID",
    "Postal Code",
    "Sales",
    "Quantity",
    "Discount",
    "Profit"
]

for column in numeric_columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    print(
        f"{column}: converted to numeric"
    )


# REMOVE EXACT DUPLICATES

print("\n" + "=" * 70)
print("5. DUPLICATE REMOVAL")
print("=" * 70)

duplicate_count = df.duplicated().sum()

print(
    f"\nDuplicate rows detected: "
    f"{duplicate_count:,}"
)

if duplicate_count > 0:

    df = df.drop_duplicates()

    print(
        f"Removed {duplicate_count:,} "
        f"exact duplicate rows."
    )

else:

    print("No exact duplicate rows to remove.")


# REQUIRED FIELD VALIDATION

print("\n" + "=" * 70)
print("6. REQUIRED FIELD VALIDATION")
print("=" * 70)

required_columns = [
    "Row ID",
    "Order ID",
    "Order Date",
    "Ship Date",
    "Ship Mode",
    "Customer ID",
    "Customer Name",
    "Segment",
    "Country",
    "City",
    "State",
    "Postal Code",
    "Region",
    "Product ID",
    "Category",
    "Sub-Category",
    "Product Name",
    "Sales",
    "Quantity",
    "Discount",
    "Profit"
]

missing_required_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_required_columns:

    print("\nERROR:")
    print("The following required columns are missing:")

    for column in missing_required_columns:
        print(f"  - {column}")

    raise ValueError(
        "Dataset does not contain all required columns."
    )

else:

    print(
        f"\nAll {len(required_columns)} "
        f"required columns are present."
    )


# MISSING VALUE CHECK

print("\n" + "=" * 70)
print("7. MISSING VALUE CHECK")
print("=" * 70)

missing_values = (
    df.isnull()
      .sum()
)

missing_nonzero = (
    missing_values[
        missing_values > 0
    ]
)

if missing_nonzero.empty:

    print("\nNo missing values detected.")

else:

    print("\nMissing values detected:")

    for column, count in missing_nonzero.items():

        percentage = (
            count / len(df) * 100
        )

        print(
            f"  {column}: "
            f"{count:,} "
            f"({percentage:.2f}%)"
        )


# INVALID DATE CHECK

print("\n" + "=" * 70)
print("8. DATE VALIDATION")
print("=" * 70)

invalid_order_dates = (
    df["Order Date"].isna().sum()
)

invalid_ship_dates = (
    df["Ship Date"].isna().sum()
)

print(
    f"\nInvalid Order Dates: "
    f"{invalid_order_dates:,}"
)

print(
    f"Invalid Ship Dates: "
    f"{invalid_ship_dates:,}"
)

# Check whether shipping occurred before ordering
ship_before_order = (
    df["Ship Date"] < df["Order Date"]
).sum()

print(
    f"Ship dates before order dates: "
    f"{ship_before_order:,}"
)


# HANDLE INVALID DATES

print("\n" + "=" * 70)
print("9. INVALID DATE HANDLING")
print("=" * 70)

invalid_date_rows = (
    df["Order Date"].isna()
    | df["Ship Date"].isna()
    | (df["Ship Date"] < df["Order Date"])
)

invalid_date_count = invalid_date_rows.sum()

if invalid_date_count > 0:

    print(
        f"\nInvalid date records detected: "
        f"{invalid_date_count:,}"
    )

    # Save records where Ship Date occurs before Order Date
    invalid_shipping_dates = df[
        df["Ship Date"] < df["Order Date"]
    ].copy()

    invalid_shipping_dates["Shipping Duration"] = (
        invalid_shipping_dates["Ship Date"]
        - invalid_shipping_dates["Order Date"]
    ).dt.days

    invalid_shipping_dates.to_csv(
        OUTPUT_DIR / "invalid_shipping_dates.csv",
        index=False
    )

    print(
        f"Saved {len(invalid_shipping_dates):,} records "
        "with negative shipping durations for inspection."
    )

    # Remove invalid date records from cleaned dataset
    df = df[~invalid_date_rows].copy()

    print(
        f"Removed {invalid_date_count:,} invalid date records."
    )

else:

    print("\nNo invalid date relationships found.")


# NUMERIC VALUE VALIDATION

print("\n" + "=" * 70)
print("10. NUMERIC VALUE VALIDATION")
print("=" * 70)


# Quantity should not be zero or negative
invalid_quantity = (
    df["Quantity"] <= 0
).sum()

print(
    f"\nNon-positive quantities: "
    f"{invalid_quantity:,}"
)


# Sales should not be negative
invalid_sales = (
    df["Sales"] < 0
).sum()

print(
    f"Negative sales values: "
    f"{invalid_sales:,}"
)


# Discount should normally be between 0 and 1
invalid_discount = (
    (df["Discount"] < 0)
    | (df["Discount"] > 1)
).sum()

print(
    f"Invalid discount values: "
    f"{invalid_discount:,}"
)


# HANDLE INVALID NUMERIC VALUES

print("\n" + "=" * 70)
print("11. INVALID NUMERIC VALUE HANDLING")
print("=" * 70)

invalid_numeric_rows = (
    (df["Quantity"] <= 0)
    | (df["Sales"] < 0)
    | (df["Discount"] < 0)
    | (df["Discount"] > 1)
)

invalid_numeric_count = (
    invalid_numeric_rows.sum()
)

if invalid_numeric_count > 0:

    print(
        f"\nRemoving {invalid_numeric_count:,} "
        f"rows with invalid numeric values."
    )

    df = df.loc[
        ~invalid_numeric_rows
    ].copy()

else:

    print(
        "\nNo invalid numeric values found."
    )


# PROFIT VALIDATION

print("\n" + "=" * 70)
print("12. PROFIT VALIDATION")
print("=" * 70)

negative_profit_count = (
    df["Profit"] < 0
).sum()

print(
    f"\nNegative profit records: "
    f"{negative_profit_count:,}"
)

print(
    "\nNegative profit values are preserved."
)

print(
    "They represent potentially unprofitable "
    "business transactions rather than invalid data."
)


# CREATE SHIPPING DURATION

print("\n" + "=" * 70)
print("13. FEATURE ENGINEERING")
print("=" * 70)

df["Shipping Duration"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

print(
    "Created: Shipping Duration"
)


# CREATE PROFIT MARGIN

df["Profit Margin"] = df["Profit"].div(
    df["Sales"].replace(0, pd.NA)
)

print(
    "Created: Profit Margin"
)


# CREATE TIME FEATURES

df["Order Year"] = (
    df["Order Date"].dt.year
)

df["Order Quarter"] = (
    "Q"
    + df["Order Date"]
        .dt.quarter
        .astype(str)
)

df["Order Month"] = (
    df["Order Date"].dt.month
)

df["Order Month Name"] = (
    df["Order Date"]
        .dt.month_name()
)

print(
    "Created: Order Year"
)

print(
    "Created: Order Quarter"
)

print(
    "Created: Order Month"
)

print(
    "Created: Order Month Name"
)


# CUSTOMER-LEVEL FEATURES

print("\n" + "=" * 70)
print("14. CUSTOMER FEATURES")
print("=" * 70)

customer_summary = (
    df.groupby("Customer ID")
      .agg(
          Customer_Sales=("Sales", "sum"),
          Customer_Profit=("Profit", "sum"),
          Customer_Orders=("Order ID", "nunique"),
          Customer_Quantity=("Quantity", "sum"),
          Last_Order_Date=("Order Date", "max")
      )
      .reset_index()
)

print(
    f"\nCustomer summary created for "
    f"{len(customer_summary):,} customers."
)

print(
    "\nCustomer-level features are kept in a "
    "separate table rather than duplicating them "
    "across every transaction."
)


# FINAL VALIDATION

print("\n" + "=" * 70)
print("15. FINAL VALIDATION")
print("=" * 70)

final_duplicate_count = (
    df.duplicated().sum()
)

final_missing_count = (
    df.isnull().sum().sum()
)

final_invalid_shipping = (
    df["Shipping Duration"] < 0
).sum()

final_invalid_margin = (
    df["Profit Margin"].isna()
).sum()

print(
    f"\nRemaining duplicate rows: "
    f"{final_duplicate_count:,}"
)

print(
    f"Remaining missing cells: "
    f"{final_missing_count:,}"
)

print(
    f"Invalid shipping durations: "
    f"{final_invalid_shipping:,}"
)

print(
    f"Undefined profit margins: "
    f"{final_invalid_margin:,}"
)


# CLEANING SUMMARY

print("\n" + "=" * 70)
print("16. CLEANING SUMMARY")
print("=" * 70)

final_record_count = len(df)

rows_removed = (
    original_record_count
    - final_record_count
)

cleaning_summary = pd.DataFrame([
    [
        "Original Records",
        original_record_count
    ],
    [
        "Final Records",
        final_record_count
    ],
    [
        "Rows Removed",
        rows_removed
    ],
    [
        "Duplicate Rows Removed",
        duplicate_count
    ],
    [
        "Invalid Date Rows Removed",
        invalid_date_count
    ],
    [
        "Invalid Numeric Rows Removed",
        invalid_numeric_count
    ],
    [
        "Final Duplicate Rows",
        final_duplicate_count
    ],
    [
        "Final Missing Cells",
        final_missing_count
    ],
    [
        "Final Invalid Shipping Durations",
        final_invalid_shipping
    ],
    [
        "Negative Profit Records",
        negative_profit_count
    ]
])

cleaning_summary.columns = [
    "Metric",
    "Value"
]

print(
    cleaning_summary.to_string(
        index=False
    )
)


# SAVE CLEANED DATASET

print("\n" + "=" * 70)
print("17. SAVING CLEANED DATA")
print("=" * 70)

df.to_csv(
    CLEANED_DATA_PATH,
    index=False
)

print(
    f"\nCleaned dataset saved to:"
)

print(
    f"{CLEANED_DATA_PATH}"
)


# SAVE CUSTOMER SUMMARY

CUSTOMER_SUMMARY_PATH = (
    OUTPUT_DIR / "customer_summary.csv"
)

customer_summary.to_csv(
    CUSTOMER_SUMMARY_PATH,
    index=False
)

print(
    f"\nCustomer summary saved to:"
)

print(
    f"{CUSTOMER_SUMMARY_PATH}"
)


# SAVE CLEANING REPORT

CLEANING_REPORT_PATH = (
    OUTPUT_DIR / "cleaning_summary.csv"
)

cleaning_summary.to_csv(
    CLEANING_REPORT_PATH,
    index=False
)

print(
    f"\nCleaning summary saved to:"
)

print(
    f"{CLEANING_REPORT_PATH}"
)


# FINAL MESSAGE

print("\n" + "=" * 70)
print("DATA CLEANING COMPLETE")
print("=" * 70)

print(
    f"\nOriginal records: "
    f"{original_record_count:,}"
)

print(
    f"Final records: "
    f"{final_record_count:,}"
)

print(
    f"Rows removed: "
    f"{rows_removed:,}"
)

print(
    "\nThe cleaned dataset is ready "
    "for business analysis."
)

print("\nGenerated files:")

print(
    f"  - {CLEANED_DATA_PATH}"
)

print(
    f"  - {CUSTOMER_SUMMARY_PATH}"
)

print(
    f"  - {CLEANING_REPORT_PATH}"
)