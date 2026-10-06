from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = PROJECT_ROOT / "output" / "business_analysis" / "sales_over_time.csv"
OUTPUT_DIR = PROJECT_ROOT / "output" / "visualizations"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_PATH)

df["Order Date"] = pd.to_datetime(df["Order Date"])
df = df.sort_values("Order Date")

plt.figure(figsize=(12, 6))
plt.plot(df["Order Date"], df["Sales"], linewidth=2)

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales ($)")
plt.xticks(rotation=45)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "01_monthly_sales_trend.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

print("Saved: 01_monthly_sales_trend.png")