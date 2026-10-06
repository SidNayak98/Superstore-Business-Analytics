from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = (
    PROJECT_ROOT
    / "output"
    / "business_analysis"
    / "product_performance_quadrant.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "output" / "visualizations"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_PATH)

sales_median = df["Sales"].median()
profit_median = df["Profit"].median()

plt.figure(figsize=(11, 8))

plt.scatter(
    df["Sales"],
    df["Profit"],
    alpha=0.55,
    s=35
)

plt.axvline(
    sales_median,
    linestyle="--",
    linewidth=1
)

plt.axhline(
    profit_median,
    linestyle="--",
    linewidth=1
)

plt.xlabel("Sales ($)")
plt.ylabel("Profit ($)")
plt.title("Product Sales vs. Profitability")

plt.grid(alpha=0.2)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "02_sales_profit_portfolio.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

print("Saved: 02_sales_profit_portfolio.png")
print(f"Sales median: ${sales_median:,.2f}")
print(f"Profit median: ${profit_median:,.2f}")