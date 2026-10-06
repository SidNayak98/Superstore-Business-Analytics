import pandas as pd
from pathlib import Path



# CONFIGURATION


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "Superstore_sales_cleaned.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "output"
    / "business_analysis"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)



# LOAD DATA


print("\n" + "=" * 70)
print("LOADING CLEANED DATA")
print("=" * 70)

df = pd.read_csv(DATA_PATH)

# Restore date columns
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

print(f"\nRecords loaded: {len(df):,}")
print(f"Columns loaded: {len(df.columns)}")



# HELPER FUNCTIONS


def save_analysis(dataframe, filename):
    """Save an analysis table to the business analysis output folder."""

    path = OUTPUT_DIR / filename
    dataframe.to_csv(path, index=False)

    print(f"Saved: {path}")



# REPORT 1 — SALES PERFORMANCE


print("\n" + "=" * 70)
print("REPORT 1 — SALES PERFORMANCE")
print("=" * 70)



# 1.1 SALES KPIs


total_sales = df["Sales"].sum()

total_orders = df["Order ID"].nunique()

total_quantity = df["Quantity"].sum()

average_order_value = (
    total_sales / total_orders
    if total_orders > 0
    else 0
)

print("\nSales KPIs")
print("-" * 40)

print(f"Total Sales:       ${total_sales:,.2f}")
print(f"Total Orders:      {total_orders:,}")
print(f"Total Quantity:    {total_quantity:,}")
print(f"Average Order Value: ${average_order_value:,.2f}")



# 1.2 SALES OVER TIME


sales_by_month = (
    df.groupby(
        df["Order Date"].dt.to_period("M")
    )
    .agg(
        Sales=("Sales", "sum"),
        Orders=("Order ID", "nunique"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
)

sales_by_month["Order Date"] = (
    sales_by_month["Order Date"]
    .astype(str)
)

sales_by_month["Sales Growth"] = (
    sales_by_month["Sales"]
    .pct_change() * 100
)

save_analysis(
    sales_by_month,
    "sales_over_time.csv"
)



# 1.3 SALES BY CATEGORY


sales_by_category = (
    df.groupby("Category")
    .agg(
        Sales=("Sales", "sum"),
        Orders=("Order ID", "nunique"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
    .sort_values("Sales", ascending=False)
)

save_analysis(
    sales_by_category,
    "sales_by_category.csv"
)



# 1.4 SALES BY SUB-CATEGORY


sales_by_subcategory = (
    df.groupby("Sub-Category")
    .agg(
        Sales=("Sales", "sum"),
        Orders=("Order ID", "nunique"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
    .sort_values("Sales", ascending=False)
)

save_analysis(
    sales_by_subcategory,
    "sales_by_subcategory.csv"
)



# 1.5 SALES BY PRODUCT


sales_by_product = (
    df.groupby(
        ["Product ID", "Product Name"]
    )
    .agg(
        Sales=("Sales", "sum"),
        Orders=("Order ID", "nunique"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
    .sort_values("Sales", ascending=False)
)

save_analysis(
    sales_by_product,
    "sales_by_product.csv"
)



# 1.6 SALES BY REGION


sales_by_region = (
    df.groupby("Region")
    .agg(
        Sales=("Sales", "sum"),
        Orders=("Order ID", "nunique"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
    .sort_values("Sales", ascending=False)
)

save_analysis(
    sales_by_region,
    "sales_by_region.csv"
)



# REPORT 2 — PROFITABILITY


print("\n" + "=" * 70)
print("REPORT 2 — PROFITABILITY")
print("=" * 70)



# 2.1 PROFIT KPIs


total_profit = df["Profit"].sum()

profit_margin = (
    total_profit / total_sales
    if total_sales != 0
    else 0
)

profit_per_order = (
    total_profit / total_orders
    if total_orders > 0
    else 0
)

profit_per_unit = (
    total_profit / total_quantity
    if total_quantity > 0
    else 0
)

print("\nProfitability KPIs")
print("-" * 40)

print(f"Total Profit:       ${total_profit:,.2f}")
print(f"Profit Margin:      {profit_margin:.2%}")
print(f"Profit per Order:   ${profit_per_order:,.2f}")
print(f"Profit per Unit:    ${profit_per_unit:,.2f}")



# 2.2 PROFIT BY CATEGORY


profit_by_category = (
    df.groupby("Category")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum"),
        Orders=("Order ID", "nunique")
    )
    .reset_index()
)

profit_by_category["Profit Margin"] = (
    profit_by_category["Profit"]
    / profit_by_category["Sales"]
)

profit_by_category = profit_by_category.sort_values(
    "Profit",
    ascending=False
)

save_analysis(
    profit_by_category,
    "profit_by_category.csv"
)



# 2.3 LOSS-MAKING PRODUCTS


profit_by_product = (
    df.groupby(
        ["Product ID", "Product Name"]
    )
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum"),
        Orders=("Order ID", "nunique")
    )
    .reset_index()
)

profit_by_product["Profit Margin"] = (
    profit_by_product["Profit"]
    / profit_by_product["Sales"]
)

loss_making_products = (
    profit_by_product[
        profit_by_product["Profit"] < 0
    ]
    .sort_values("Profit")
)

save_analysis(
    loss_making_products,
    "loss_making_products.csv"
)



# 2.4 PROFIT BY REGION


profit_by_region = (
    df.groupby("Region")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum"),
        Orders=("Order ID", "nunique")
    )
    .reset_index()
)

profit_by_region["Profit Margin"] = (
    profit_by_region["Profit"]
    / profit_by_region["Sales"]
)

profit_by_region = profit_by_region.sort_values(
    "Profit",
    ascending=False
)

save_analysis(
    profit_by_region,
    "profit_by_region.csv"
)



# 2.5 HIGH SALES / HIGH PROFIT ANALYSIS


product_performance = profit_by_product.copy()

sales_median = product_performance["Sales"].median()
profit_median = product_performance["Profit"].median()


def classify_product(row):

    high_sales = row["Sales"] >= sales_median
    high_profit = row["Profit"] >= profit_median

    if high_sales and high_profit:
        return "Star"

    if not high_sales and high_profit:
        return "Winner"

    if high_sales and not high_profit:
        return "Volume"

    return "Weak"


product_performance["Performance Quadrant"] = (
    product_performance.apply(
        classify_product,
        axis=1
    )
)

save_analysis(
    product_performance,
    "product_performance_quadrant.csv"
)



# REPORT 3 — CUSTOMER ANALYTICS


print("\n" + "=" * 70)
print("REPORT 3 — CUSTOMER ANALYTICS")
print("=" * 70)



# 3.1 CUSTOMER SEGMENT PERFORMANCE


segment_analysis = (
    df.groupby("Segment")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"),
        Quantity=("Quantity", "sum"),
        Customers=("Customer ID", "nunique")
    )
    .reset_index()
)

segment_analysis["Profit Margin"] = (
    segment_analysis["Profit"]
    / segment_analysis["Sales"]
)

save_analysis(
    segment_analysis,
    "customer_segments.csv"
)



# 3.2 CUSTOMER VALUE


customer_analysis = (
    df.groupby(
        ["Customer ID", "Customer Name"]
    )
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"),
        Quantity=("Quantity", "sum"),
        Last_Order_Date=("Order Date", "max")
    )
    .reset_index()
)

customer_analysis["Profit Margin"] = (
    customer_analysis["Profit"]
    / customer_analysis["Sales"]
)

customer_analysis = customer_analysis.sort_values(
    "Sales",
    ascending=False
)

save_analysis(
    customer_analysis,
    "customer_value.csv"
)



# 3.3 RFM ANALYSIS


analysis_date = df["Order Date"].max()

rfm = (
    df.groupby("Customer ID")
    .agg(
        Recency=(
            "Order Date",
            lambda x: (analysis_date - x.max()).days
        ),
        Frequency=("Order ID", "nunique"),
        Monetary=("Sales", "sum")
    )
    .reset_index()
)


# RFM scores
rfm["R_Score"] = pd.qcut(
    rfm["Recency"],
    5,
    labels=[5, 4, 3, 2, 1],
    duplicates="drop"
)

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
)

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
)

rfm["RFM Score"] = (
    rfm["R_Score"].astype(str)
    + rfm["F_Score"].astype(str)
    + rfm["M_Score"].astype(str)
)


def classify_rfm(row):

    r = int(row["R_Score"])
    f = int(row["F_Score"])
    m = int(row["M_Score"])

    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"

    if f >= 4 and m >= 3:
        return "Loyal"

    if r >= 4 and f <= 3:
        return "Potential Loyalists"

    if r <= 2 and m >= 4:
        return "At Risk"

    return "Low Value"


rfm["Customer Segment"] = rfm.apply(
    classify_rfm,
    axis=1
)

save_analysis(
    rfm,
    "rfm_analysis.csv"
)



# REPORT 4 — DISCOUNT ANALYSIS


print("\n" + "=" * 70)
print("REPORT 4 — DISCOUNT ANALYSIS")
print("=" * 70)



# 4.1 DISCOUNT BANDS


discount_bins = [
    -0.001,
    0.00,
    0.10,
    0.20,
    0.30,
    0.40,
    float("inf")
]

discount_labels = [
    "0%",
    "1–10%",
    "11–20%",
    "21–30%",
    "31–40%",
    "40%+"
]

df["Discount Band"] = pd.cut(
    df["Discount"],
    bins=discount_bins,
    labels=discount_labels,
    include_lowest=True
)



# 4.2 DISCOUNT ANALYSIS


discount_analysis = (
    df.groupby(
        "Discount Band",
        observed=True
    )
    .agg(
        Average_Sales=("Sales", "mean"),
        Average_Profit=("Profit", "mean"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Records=("Order ID", "count")
    )
    .reset_index()
)

discount_analysis["Profit Margin"] = (
    discount_analysis["Total_Profit"]
    / discount_analysis["Total_Sales"]
)

save_analysis(
    discount_analysis,
    "discount/discount_analysis.csv"
)



# REPORT 5 — GEOGRAPHIC & SHIPPING ANALYSIS


print("\n" + "=" * 70)
print("REPORT 5 — GEOGRAPHIC & SHIPPING ANALYSIS")
print("=" * 70)



# 5.1 STATE ANALYSIS


state_analysis = (
    df.groupby("State")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
)

state_analysis["Profit Margin"] = (
    state_analysis["Profit"]
    / state_analysis["Sales"]
)

state_analysis = state_analysis.sort_values(
    "Profit",
    ascending=False
)

save_analysis(
    state_analysis,
    "state_analysis.csv"
)



# 5.2 CITY ANALYSIS


city_analysis = (
    df.groupby(
        ["State", "City"]
    )
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
)

city_analysis["Profit Margin"] = (
    city_analysis["Profit"]
    / city_analysis["Sales"]
)

city_analysis = city_analysis.sort_values(
    "Profit",
    ascending=False
)

save_analysis(
    city_analysis,
    "city_analysis.csv"
)



# 5.3 SHIPPING MODE


shipping_mode_analysis = (
    df.groupby("Ship Mode")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"),
        Average_Shipping_Duration=(
            "Shipping Duration",
            "mean"
        )
    )
    .reset_index()
)

shipping_mode_analysis["Profit Margin"] = (
    shipping_mode_analysis["Profit"]
    / shipping_mode_analysis["Sales"]
)

save_analysis(
    shipping_mode_analysis,
    "shipping_mode_analysis.csv"
)



# 5.4 SHIPPING DURATION


shipping_duration_analysis = (
    df.groupby("Shipping Duration")
    .agg(
        Orders=("Order ID", "nunique"),
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

shipping_duration_analysis["Profit Margin"] = (
    shipping_duration_analysis["Profit"]
    / shipping_duration_analysis["Sales"]
)

save_analysis(
    shipping_duration_analysis,
    "shipping_duration_analysis.csv"
)



# FINAL SUMMARY


print("\n" + "=" * 70)
print("BUSINESS ANALYSIS COMPLETE")
print("=" * 70)

print(f"\nRecords analyzed: {len(df):,}")
print(f"Total Sales: ${total_sales:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Total Quantity: {total_quantity:,}")

print(f"\nAnalysis files saved to:")
print(OUTPUT_DIR)