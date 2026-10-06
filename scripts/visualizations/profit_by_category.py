from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = (
    PROJECT_ROOT
    / "output"
    / "business_analysis"
    / "profit_by_category.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "output" / "visualizations"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_PATH)

df = df.sort_values("Profit", ascending=False)

plt.figure(figsize=(9, 6))

# Give each product category its own colour
colors = plt.cm.Set2(range(len(df)))

plt.bar(
    df["Category"],
    df["Profit"],
    color=colors
)

plt.title("Profit by Product Category")
plt.xlabel("Category")
plt.ylabel("Profit ($)")
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "03_profit_by_category.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Saved: 03_profit_by_category.png")