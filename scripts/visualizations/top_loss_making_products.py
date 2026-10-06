from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = (
    PROJECT_ROOT
    / "output"
    / "business_analysis"
    / "loss_making_products.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "output" / "visualizations"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_PATH)

df = df.sort_values("Profit", ascending=True).head(10)
df = df.sort_values("Profit", ascending=True)

# Shorten extremely long product names for readability
df["Short Name"] = df["Product Name"].str.slice(0, 55)

plt.figure(figsize=(11, 7))

plt.barh(
    df["Short Name"],
    df["Profit"]
)

plt.title("Top 10 Loss-Making Products")
plt.xlabel("Profit ($)")
plt.ylabel("Product")

plt.grid(axis="x", alpha=0.3)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "04_top_loss_making_products.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

print("Saved: 04_top_loss_making_products.png")