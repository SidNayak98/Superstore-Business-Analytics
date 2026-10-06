from pathlib import Path
import pandas as pd


# CONFIGURATION

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ANALYSIS_DIR = PROJECT_ROOT / "output" / "business_analysis"
OUTPUT_DIR = PROJECT_ROOT / "output" / "findings"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# HELPERS

def load_csv(filename):
    """Load an analysis CSV from the business analysis output folder."""
    path = ANALYSIS_DIR / filename

    if not path.exists():
        print(f"WARNING: Missing file: {filename}")
        return None

    return pd.read_csv(path)


def money(value):
    return f"${value:,.2f}"


def pct(value):
    return f"{value:.2f}%"


def print_section(title):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def print_finding(label, value):
    print(f"{label:<35} {value}")


# REPORT 1 — SALES PERFORMANCE

def analyze_sales():

    print_section("REPORT 1 — SALES PERFORMANCE")

    category = load_csv("sales_by_category.csv")
    subcategory = load_csv("sales_by_subcategory.csv")
    product = load_csv("sales_by_product.csv")
    region = load_csv("sales_by_region.csv")
    time = load_csv("sales_over_time.csv")

    findings = []

    # --------------------------------------------------------
    # Category
    # --------------------------------------------------------

    if category is not None:

        category = category.sort_values("Sales", ascending=False)

        top = category.iloc[0]
        bottom = category.iloc[-1]

        findings.append(
            f"Highest-sales category: {top['Category']} "
            f"({money(top['Sales'])})"
        )

        findings.append(
            f"Lowest-sales category: {bottom['Category']} "
            f"({money(bottom['Sales'])})"
        )

        print_finding(
            "Highest-sales category:",
            f"{top['Category']} — {money(top['Sales'])}"
        )

        print_finding(
            "Lowest-sales category:",
            f"{bottom['Category']} — {money(bottom['Sales'])}"
        )

    # --------------------------------------------------------
    # Sub-category
    # --------------------------------------------------------

    if subcategory is not None:

        subcategory = subcategory.sort_values("Sales", ascending=False)

        top = subcategory.iloc[0]
        bottom = subcategory.iloc[-1]

        findings.append(
            f"Highest-sales sub-category: {top['Sub-Category']} "
            f"({money(top['Sales'])})"
        )

        findings.append(
            f"Lowest-sales sub-category: {bottom['Sub-Category']} "
            f"({money(bottom['Sales'])})"
        )

        print_finding(
            "Highest-sales sub-category:",
            f"{top['Sub-Category']} — {money(top['Sales'])}"
        )

        print_finding(
            "Lowest-sales sub-category:",
            f"{bottom['Sub-Category']} — {money(bottom['Sales'])}"
        )

    # --------------------------------------------------------
    # Products
    # --------------------------------------------------------

    if product is not None:

        product = product.sort_values("Sales", ascending=False)

        print()
        print("Top 10 Products by Sales")
        print("-" * 40)

        for _, row in product.head(10).iterrows():
            print(
                f"{row['Product Name']}: "
                f"{money(row['Sales'])}"
            )

        # Candidate finding: highest-sales product
        top_product = product.iloc[0]

        finding = (
            f"Highest-sales product: "
            f"{top_product['Product Name']} "
            f"({money(top_product['Sales'])})"
        )

        findings.append(finding)

        print_finding(
            "Candidate finding:",
            finding
        )

        print()
        print("Bottom 10 Products by Sales")
        print("-" * 40)

        for _, row in product.tail(10).sort_values(
            "Sales"
        ).iterrows():
            print(
                f"{row['Product Name']}: "
                f"{money(row['Sales'])}"
            )

        # Candidate finding: lowest-sales product
        bottom_product = product.iloc[-1]

        finding = (
            f"Lowest-sales product: "
            f"{bottom_product['Product Name']} "
            f"({money(bottom_product['Sales'])})"
        )

        findings.append(finding)

        print_finding(
            "Candidate finding:",
            finding
        )

    # --------------------------------------------------------
    # Region
    # --------------------------------------------------------

    if region is not None:

        region = region.sort_values("Sales", ascending=False)

        print()
        print("Sales by Region")
        print("-" * 40)

        for _, row in region.iterrows():
            print(
                f"{row['Region']}: "
                f"{money(row['Sales'])}"
            )

        # Candidate findings
        top_region = region.iloc[0]
        bottom_region = region.iloc[-1]

        finding = (
            f"Highest-sales region: "
            f"{top_region['Region']} "
            f"({money(top_region['Sales'])})"
        )

        findings.append(finding)

        print_finding(
            "Candidate finding:",
            finding
        )

        finding = (
            f"Lowest-sales region: "
            f"{bottom_region['Region']} "
            f"({money(bottom_region['Sales'])})"
        )

        findings.append(finding)

        print_finding(
            "Candidate finding:",
            finding
        )

    # --------------------------------------------------------
    # Time
    # --------------------------------------------------------

    if time is not None:

        time["Order Date"] = pd.to_datetime(
            time["Order Date"]
        )

        time = time.sort_values("Order Date")

        highest_month = time.loc[
            time["Sales"].idxmax()
        ]

        lowest_month = time.loc[
            time["Sales"].idxmin()
        ]

        print()
        print("Sales Over Time")
        print("-" * 40)

        print_finding(
            "Highest-sales month:",
            f"{highest_month['Order Date'].strftime('%Y-%m')} — "
            f"{money(highest_month['Sales'])}"
        )

        print_finding(
            "Lowest-sales month:",
            f"{lowest_month['Order Date'].strftime('%Y-%m')} — "
            f"{money(lowest_month['Sales'])}"
        )

        # Candidate findings
        finding = (
            f"Highest-sales month: "
            f"{highest_month['Order Date'].strftime('%Y-%m')} "
            f"({money(highest_month['Sales'])})"
        )

        findings.append(finding)

        finding = (
            f"Lowest-sales month: "
            f"{lowest_month['Order Date'].strftime('%Y-%m')} "
            f"({money(lowest_month['Sales'])})"
        )

        findings.append(finding)

    return findings


# REPORT 2 — PROFITABILITY

def analyze_profitability():

    print_section("REPORT 2 — PROFITABILITY")

    category = load_csv("profit_by_category.csv")
    losses = load_csv("loss_making_products.csv")
    region = load_csv("profit_by_region.csv")
    quadrant = load_csv("product_performance_quadrant.csv")

    findings = []

    # --------------------------------------------------------
    # Category
    # --------------------------------------------------------

    if category is not None:

        category = category.sort_values(
            "Profit",
            ascending=False
        )

        top = category.iloc[0]
        bottom = category.iloc[-1]

        findings.append(
            f"Most profitable category: {top['Category']} "
            f"({money(top['Profit'])})"
        )

        findings.append(
            f"Least profitable category: {bottom['Category']} "
            f"({money(bottom['Profit'])})"
        )

        print_finding(
            "Most profitable category:",
            f"{top['Category']} — {money(top['Profit'])}"
        )

        print_finding(
            "Least profitable category:",
            f"{bottom['Category']} — {money(bottom['Profit'])}"
        )

    # --------------------------------------------------------
    # Loss-making products
    # --------------------------------------------------------

    if losses is not None:

        losses = losses.sort_values(
            "Profit"
        )

        print()
        print("Loss-Making Products")
        print("-" * 40)

        print_finding(
            "Number of loss-making products:",
            f"{len(losses):,}"
        )

        # Candidate finding
        finding = (
            f"Number of loss-making products: "
            f"{len(losses):,}"
        )

        findings.append(finding)

        print()
        print("Largest Product Losses")

        for _, row in losses.head(10).iterrows():
            print(
                f"{row['Product Name']}: "
                f"{money(row['Profit'])}"
            )

        # Candidate finding: largest loss
        if not losses.empty:

            largest_loss = losses.iloc[0]

            finding = (
                f"Largest product loss: "
                f"{largest_loss['Product Name']} "
                f"({money(largest_loss['Profit'])})"
            )

            findings.append(finding)

            print_finding(
                "Candidate finding:",
                finding
            )

    # --------------------------------------------------------
    # Region
    # --------------------------------------------------------

    if region is not None:

        region = region.sort_values(
            "Profit",
            ascending=False
        )

        print()
        print("Profit by Region")
        print("-" * 40)

        for _, row in region.iterrows():
            print(
                f"{row['Region']}: "
                f"{money(row['Profit'])}"
            )

        # Candidate findings
        top_region = region.iloc[0]
        bottom_region = region.iloc[-1]

        finding = (
            f"Highest-profit region: "
            f"{top_region['Region']} "
            f"({money(top_region['Profit'])})"
        )

        findings.append(finding)

        finding = (
            f"Lowest-profit region: "
            f"{bottom_region['Region']} "
            f"({money(bottom_region['Profit'])})"
        )

        findings.append(finding)

    # --------------------------------------------------------
    # Product quadrants
    # --------------------------------------------------------

    if quadrant is not None:

        print()
        print("Product Performance Quadrants")
        print("-" * 40)

        counts = quadrant[
            "Performance Quadrant"
        ].value_counts()

        for quadrant_name, count in counts.items():

            print(
                f"{quadrant_name}: {count:,} products"
            )

            # Candidate finding
            findings.append(
                f"{quadrant_name} products: "
                f"{count:,}"
            )

    return findings


# REPORT 3 — CUSTOMER ANALYTICS

def analyze_customers():

    print_section("REPORT 3 — CUSTOMER ANALYTICS")

    segments = load_csv("customer_segments.csv")
    customer_value = load_csv("customer_value.csv")
    rfm = load_csv("rfm_analysis.csv")

    findings = []

    # --------------------------------------------------------
    # Customer segments
    # --------------------------------------------------------

    if segments is not None:

        print("Customer Segment Performance")
        print("-" * 40)

        for _, row in segments.iterrows():

            print(
                f"{row['Segment']}: "
                f"Sales={money(row['Sales'])}, "
                f"Profit={money(row['Profit'])}"
            )

        top = segments.loc[
            segments["Sales"].idxmax()
        ]

        findings.append(
            f"Highest-sales customer segment: "
            f"{top['Segment']}"
        )

    # --------------------------------------------------------
    # Customer value
    # --------------------------------------------------------

    if customer_value is not None:

        customer_value = customer_value.sort_values(
            "Sales",
            ascending=False
        )

        print()
        print("Top 10 Customers by Sales")
        print("-" * 40)

        for _, row in customer_value.head(10).iterrows():

            print(
                f"{row['Customer Name']}: "
                f"{money(row['Sales'])}"
            )

        # Candidate finding
        top_customer = customer_value.iloc[0]

        finding = (
            f"Highest-sales customer: "
            f"{top_customer['Customer Name']} "
            f"({money(top_customer['Sales'])})"
        )

        findings.append(finding)

        print_finding(
            "Candidate finding:",
            finding
        )

    # --------------------------------------------------------
    # RFM
    # --------------------------------------------------------

    if rfm is not None:

        print()
        print("RFM Segment Distribution")
        print("-" * 40)

        if "RFM Segment" in rfm.columns:

            distribution = (
                rfm["RFM Segment"]
                .value_counts()
            )

            for segment, count in distribution.items():

                print(
                    f"{segment}: {count:,} customers"
                )

            # Candidate finding: largest RFM group
            top_rfm_segment = distribution.idxmax()
            top_rfm_count = distribution.max()

            finding = (
                f"Largest RFM customer group: "
                f"{top_rfm_segment} "
                f"({top_rfm_count:,} customers)"
            )

            findings.append(finding)

            print_finding(
                "Candidate finding:",
                finding
            )

    return findings


# REPORT 4 — DISCOUNT ANALYSIS

def analyze_discounts():

    print_section("REPORT 4 — DISCOUNT ANALYSIS")

    discount = load_csv("discount_analysis.csv")

    findings = []

    if discount is None:
        return findings

    print("Discount Bands")
    print("-" * 40)

    for _, row in discount.iterrows():

        print(
            f"{row['Discount Band']}: "
            f"Sales={money(row['Total_Sales'])}, "
            f"Profit={money(row['Total_Profit'])}, "
            f"Margin={pct(row['Profit Margin'])}"
        )

    # Highest and lowest observed margin

    highest_margin = discount.loc[
        discount["Profit Margin"].idxmax()
    ]

    lowest_margin = discount.loc[
        discount["Profit Margin"].idxmin()
    ]

    print()
    print_finding(
        "Highest observed margin:",
        f"{highest_margin['Discount Band']} — "
        f"{pct(highest_margin['Profit Margin'])}"
    )

    print_finding(
        "Lowest observed margin:",
        f"{lowest_margin['Discount Band']} — "
        f"{pct(lowest_margin['Profit Margin'])}"
    )

    findings.append(
        f"Highest observed profit margin: "
        f"{highest_margin['Discount Band']} "
        f"({pct(highest_margin['Profit Margin'])})"
    )

    findings.append(
        f"Lowest observed profit margin: "
        f"{lowest_margin['Discount Band']} "
        f"({pct(lowest_margin['Profit Margin'])})"
    )

    findings.append(
        "Discount analysis should be interpreted as an "
        "association between discount level and observed profitability, "
        "not as evidence of causation."
    )

    return findings


# REPORT 5 — GEOGRAPHIC & SHIPPING

def analyze_geography_shipping():

    print_section("REPORT 5 — GEOGRAPHIC & SHIPPING ANALYSIS")

    states = load_csv("state_analysis.csv")
    cities = load_csv("city_analysis.csv")
    shipping = load_csv("shipping_mode_analysis.csv")
    duration = load_csv("shipping_duration_analysis.csv")

    findings = []

    # --------------------------------------------------------
    # States
    # --------------------------------------------------------

        # Candidate findings
    top_state = states.iloc[0]
    bottom_state = states.iloc[-1]

    findings.append(
        f"Highest-sales state: "
        f"{top_state['State']} "
        f"({money(top_state['Sales'])})"
    )

    findings.append(
        f"Lowest-sales state: "
        f"{bottom_state['State']} "
        f"({money(bottom_state['Sales'])})"
    )
# --------------------------------------------------------
# Cities
# --------------------------------------------------------

    # Candidate findings
    top_city = cities.iloc[0]
    bottom_city = cities.iloc[-1]

    findings.append(
        f"Highest-sales city: "
        f"{top_city['City']} "
        f"({money(top_city['Sales'])})"
    )

    findings.append(
        f"Lowest-sales city: "
        f"{bottom_city['City']} "
        f"({money(bottom_city['Sales'])})"
    )

# --------------------------------------------------------
# Shipping mode
# --------------------------------------------------------

    # Candidate findings
    fastest_mode = shipping.loc[
        shipping["Average_Shipping_Duration"].idxmin()
    ]

    slowest_mode = shipping.loc[
        shipping["Average_Shipping_Duration"].idxmax()
    ]

    findings.append(
        f"Fastest shipping mode by average duration: "
        f"{fastest_mode['Ship Mode']} "
        f"({fastest_mode['Average_Shipping_Duration']:.2f} days)"
    )

    findings.append(
        f"Slowest shipping mode by average duration: "
        f"{slowest_mode['Ship Mode']} "
        f"({slowest_mode['Average_Shipping_Duration']:.2f} days)"
    )

    return findings


# SAVE FINDINGS

def save_findings(all_findings):

    path = OUTPUT_DIR / "candidate_findings.txt"

    with open(path, "w", encoding="utf-8") as file:

        file.write(
            "SUPERSTORE BUSINESS ANALYTICS\n"
            "CANDIDATE BUSINESS FINDINGS\n"
        )

        file.write("=" * 70 + "\n\n")

        for report, findings in all_findings.items():

            file.write(f"{report}\n")
            file.write("-" * 70 + "\n")

            for finding in findings:
                file.write(f"- {finding}\n")

            file.write("\n")

    print()
    print("=" * 70)
    print(f"Candidate findings saved to: {path}")
    print("=" * 70)


# MAIN

def main():

    all_findings = {}

    all_findings["REPORT 1 — SALES PERFORMANCE"] = analyze_sales()

    all_findings["REPORT 2 — PROFITABILITY"] = analyze_profitability()

    all_findings["REPORT 3 — CUSTOMER ANALYTICS"] = analyze_customers()

    all_findings["REPORT 4 — DISCOUNT ANALYSIS"] = analyze_discounts()

    all_findings[
        "REPORT 5 — GEOGRAPHIC & SHIPPING ANALYSIS"
    ] = analyze_geography_shipping()

    save_findings(all_findings)


if __name__ == "__main__":
    main()