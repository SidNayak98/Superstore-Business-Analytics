from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = (
    PROJECT_ROOT
    / "output"
    / "business_analysis"
    / "shipping_mode_analysis.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "output" / "visualizations"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_PATH)

df = df.sort_values(
    "Average_Shipping_Duration",
    ascending=False
)

plt.figure(figsize=(10, 6))

plt.bar(
    df["Ship Mode"],
    df["Average_Shipping_Duration"]
)

plt.title("Average Shipping Duration by Ship Mode")
plt.xlabel("Ship Mode")
plt.ylabel("Average Shipping Duration (days)")

plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "08_shipping_duration_by_mode.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

print("Saved: 08_shipping_duration_by_mode.png")