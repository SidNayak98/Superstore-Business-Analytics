from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = (
    PROJECT_ROOT
    / "output"
    / "business_analysis"
    / "discount_analysis.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "output" / "visualizations"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_PATH)

# Normalize discount-band labels
# Convert en dashes to regular hyphens so they match discount_order
df["Discount Band"] = (
    df["Discount Band"]
    .astype(str)
    .str.replace("–", "-", regex=False)
    .str.strip()
)

# Preserve the intended discount-band ordering
discount_order = [
    "0%",
    "1-10%",
    "11-20%",
    "21-30%",
    "31-40%",
    "40%+"
]

df["Discount Band"] = pd.Categorical(
    df["Discount Band"],
    categories=discount_order,
    ordered=True
)

# Remove missing / unrecognized discount bands
df = df.dropna(subset=["Discount Band"])

# Sort according to the categorical order
df = df.sort_values("Discount Band")

# Convert profit margin from decimal to percentage points
# Example: 0.298 -> 29.8%
df["Profit Margin"] = df["Profit Margin"] * 100

# Print values being plotted for verification
print("\nDiscount bands being plotted:")
print(df[["Discount Band", "Profit Margin"]].to_string(index=False))

plt.figure(figsize=(10, 6))

plt.plot(
    df["Discount Band"].astype(str),
    df["Profit Margin"],
    marker="o",
    linewidth=2
)

plt.title("Observed Profit Margin by Discount Band")
plt.xlabel("Discount Band")
plt.ylabel("Profit Margin (%)")

# Allow negative profit margins
plt.ylim(-80, 35)

# Explicitly define all six x-axis positions
plt.xticks(
    range(len(discount_order)),
    discount_order
)

# Keep the entire line visible from 0% through 40%+
plt.xlim(-0.25, len(discount_order) - 0.75)

plt.grid(axis="y", alpha=0.3)

plt.figtext(
    0.5,
    0.01,
    "Observed association; not evidence of causation.",
    ha="center",
    fontsize=9
)

plt.tight_layout(rect=[0, 0.04, 1, 1])

plt.savefig(
    OUTPUT_DIR / "06_discount_profit_margin.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nSaved: 06_discount_profit_margin.png")