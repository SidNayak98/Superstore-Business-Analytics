# Superstore Sales Analysis

A business analytics portfolio project exploring sales performance,
profitability, customer purchasing behavior, discount patterns,
geographic performance, and shipping activity using a Superstore retail
transactions dataset.

The project demonstrates a workflow from raw data auditing and cleaning
through business analysis, findings extraction, and visualization. The
emphasis is on interpreting results in a business context.

## Project Objectives

-   Evaluate sales performance across time, products, categories, and
    regions.
-   Compare profitability across categories, products, and geographic
    markets.
-   Identify products with negative total profit and products whose
    sales and profit performance differ.
-   Segment customers using Recency, Frequency, and Monetary (RFM)
    measures.
-   Examine how observed profitability varies across discount bands.
-   Explore geographic sales performance and shipping duration.
-   Translate descriptive findings into areas for business
    investigation.

## Workflow at a Glance

Run the scripts in this order:

1.  `scripts/01_data_audit.py`
2.  `scripts/02_data_cleaning.py`
3.  `scripts/03_business_analysis.py`
4.  `scripts/extract_findings.py`
5.  The required scripts in `scripts/visualizations/`

The first three scripts audit, clean, and analyze the data. The findings
extraction script consolidates notable results. Visualization scripts
turn selected analysis outputs into charts for the report.

> Run each stage after its inputs have been created. The exact filenames
> and output locations are defined in the scripts. If the repository
> layout changes, update paths and this README accordingly.

## Script Order and Outputs

### 1. Data audit --- `scripts/data_audit.py`

**Purpose:** Inspect the raw dataset before changing it and document its
initial condition.

The audit checks the dataset structure, column types, missing values,
duplicates, categorical distributions, date validity, order and customer
structure, numeric fields, and shipping durations. It also creates a
data dictionary and audit summary.

**Outputs:** `output/audit/`

-   `audit_summary.csv` --- summary of key audit checks.
-   `missing_values.csv` --- missing-value counts.
-   `data_dictionary.csv` --- column names, data types, and related
    metadata.
-   Category distribution CSV files --- summaries of selected
    categorical fields.

**Why first:** Auditing helps identify quality concerns before cleaning
decisions are made.

### 2. Data cleaning and feature engineering --- `scripts/data_cleaning.py`

**Purpose:** Standardize and validate the data, create analysis-ready
fields, and save the cleaned dataset.

The cleaning process standardizes column names and text, converts date
and numeric fields, checks duplicates and invalid values, and creates
derived fields such as shipping duration, profit margin, and
order-period attributes. It also produces a customer-level summary.

Records where the ship date precedes the order date are excluded because
they imply a negative shipping duration. These records are retained
separately for review. Negative profit is preserved because it can
represent a meaningful business outcome rather than a data error.

**Outputs:**

-   `data/Superstore_sales_cleaned.csv` --- cleaned dataset used by
    subsequent analysis scripts.
-   `output/cleaning/cleaning_summary.csv` --- summary of cleaning
    actions and final data checks.
-   `output/cleaning/invalid_shipping_dates.csv` --- records excluded
    because the ship date precedes the order date.
-   `output/cleaning/customer_summary.csv` --- customer-level summary.

**Current run summary:** The workflow started with 9,994 records and
retained 8,286 records for analysis. It excluded 1,708 records with
invalid shipping-date relationships, removed no exact duplicate rows,
and preserved records with negative profit.

**Why second:** Subsequent analysis should use one consistent,
documented dataset rather than repeatedly cleaning the raw file.

### 3. Business analysis --- `scripts/business_analysis.py`

**Purpose:** Calculate business metrics and create tables used to
interpret results and build charts.

The script analyzes five areas:

| Analysis Area | Examples of Outputs |
|---|---|
| Sales performance | Sales over time, by category, sub-category, product, and region |
| Profitability | Profit by category and region, loss-making products, and product performance quadrants |
| Customer analytics | Customer segment performance, customer value, and RFM analysis |
| Discount analysis | Sales and profit measures by discount band |
| Geographic and shipping analysis | State and city performance, shipping-mode analysis, and shipping-duration analysis |

**Outputs:** `output/business_analysis/`

-   `sales_over_time.csv`
-   `sales_by_category.csv`
-   `sales_by_subcategory.csv`
-   `sales_by_product.csv`
-   `sales_by_region.csv`
-   `profit_by_category.csv`
-   `loss_making_products.csv`
-   `profit_by_region.csv`
-   `product_performance_quadrant.csv`
-   `customer_segments.csv`
-   `customer_value.csv`
-   `rfm_analysis.csv`
-   `discount_analysis.csv`
-   `state_analysis.csv`
-   `city_analysis.csv`
-   `shipping_mode_analysis.csv`
-   `shipping_duration_analysis.csv`

**Why third:** The script operates on the cleaned dataset and produces
structured analysis tables for the report and visualizations.

### 4. Findings extraction --- `scripts/extract_findings.py`

**Purpose:** Consolidate notable results from the analysis outputs into
a concise summary for report writing.

This stage is intended to highlight results such as high- and
low-performing categories or regions, loss-making products, RFM
observations, discount-band profitability, and shipping-duration
extremes.

**Outputs:** Findings summary files, according to the current script
configuration. Check the script for the exact output filenames and
directory.

**Why fourth:** Extracting findings after the analysis helps keep the
report tied to calculated results rather than values manually copied
from multiple tables.

### 5. Visualizations --- `scripts/visualizations/`

**Purpose:** Generate charts from the business-analysis outputs for
inclusion in the final report.

The visualization scripts cover:

1.  Monthly Sales Trend
2.  Sales vs. Profit Product Portfolio
3.  Profit by Category
4.  Top Loss-Making Products
5.  RFM Segment Distribution
6.  Observed Profit Margin by Discount Band
7.  Top States by Sales
8.  Shipping Duration by Ship Mode

**Outputs:** Chart image files are saved to the output locations
configured by the individual visualization scripts. Consult each script
for exact filenames and destinations.

**Why last:** Generating charts from completed analysis tables helps
keep the report and visualizations consistent.

## Repository Structure

``` text
retail-business-analytics/
├── README.md
├── requirements.txt
├── data/
│   ├── Superstore_sales_dataset.csv
│   └── Superstore_sales_cleaned.csv
├── scripts/
│   ├── 01_data_audit.py
│   ├── 02_data_cleaning.py
│   ├── 03_business_analysis.py
│   ├── extract_findings.py
│   └── visualizations/
│       └── [visualization scripts]
├── output/
│   ├── audit/
│   │   ├── audit_summary.csv
│   │   ├── missing_values.csv
│   │   ├── data_dictionary.csv
│   │   └── [category distribution files]
│   ├── cleaning/
│   │   ├── cleaning_summary.csv
│   │   ├── invalid_shipping_dates.csv
│   │   └── customer_summary.csv
│   ├── business_analysis/
│   │   ├── sales_over_time.csv
│   │   ├── state_analysis.csv
│   │   ├── discount_analysis.csv
│   │   └── [other analysis CSV files]
│   ├── findings/
│   │   └── [findings summary files, if configured]
│   └── visualizations/
│       └── [generated chart images, if configured]
├── notebooks/
│   └── [optional analysis notebooks]
├── dashboard/
│   ├── app.py
│   └── pages/
├── images/
│   └── [documentation images, if any]
└── report/
    └── Final_Report.pdf
```

This is an explanatory tree, not a guarantee that every file or
directory is currently present. Some are created only after scripts run.
The output paths in the scripts are authoritative; update this tree if
the actual project differs.

## Key Results from the Current Analysis

The current run analyzed 8,286 records representing 4,119 orders and 791
customers.

| Metric                            | Result          |
|-----------------------------------|----------------:|
| Total sales                       | $1,939,399.61   |
| Total profit                      | $249,505.81     |
| Overall profit margin             | 12.87%          |
| Total quantity sold               | 31,289          |
| Average order value               | $470.84         |
| Products with negative total profit | 318           |

These figures describe the current cleaned dataset and may change if the
source data or cleaning rules are updated.

## Methodological Notes

-   **Invalid shipping dates:** Records where the ship date precedes the
    order date are excluded from the cleaned analysis dataset and
    retained separately for audit.
-   **Negative profit:** Negative-profit records are preserved because
    they can represent real business outcomes.
-   **Discount analysis:** Differences in profitability across discount
    bands are descriptive associations, not proof that discounts caused
    the observed outcomes.
-   **RFM segmentation:** RFM groups summarize historical purchasing
    behavior. They do not independently establish customer churn,
    lifetime value, or marketing effectiveness.
-   **Product portfolio quadrants:** Star, Winner, Volume, and Weak
    classifications use median sales and profit thresholds. They are
    relative comparisons within this dataset, not universal performance
    standards.
-   **Shipping duration:** The unusually high observed average for
    Standard Class should be validated against underlying records and
    potential outliers before operational conclusions are drawn.
-   **Cost and ROI limitations:** The dataset does not provide all
    detailed product costs, marketing expenditure, or customer
    acquisition costs needed to calculate full contribution margin or
    marketing ROI.

## Requirements and Running the Project

Install the packages listed in `requirements.txt` in Python
environment.

Run the scripts from the repository root so project-relative paths
resolve as expected:

``` bash
python scripts/01_data_audit.py
python scripts/02_data_cleaning.py
python scripts/03_business_analysis.py
python scripts/extract_findings.py
```

Then run the required visualization scripts in
`scripts/visualizations/`. Check each script for its filename and
execution command.

## Dataset Source

The CSV used for this project was obtained from the following GitHub
repository:

-   [Superstore Sales Analysis
    dataset](https://github.com/yajasarora/Superstore-Sales-Analysis-with-Tableau/blob/master/Superstore%20sales%20dataset.csv)

This identifies the repository from which the CSV was obtained; it
should not be assumed to be the dataset's original creator unless that
provenance is independently verified.

## Intended Use

This is an independent portfolio project demonstrating data auditing,
cleaning, descriptive business analysis, customer segmentation,
visualization, and communication of business findings. The results are
exploratory and intended to identify areas for further investigation,
not to establish causal relationships or prescribe business actions
without additional evidence.
