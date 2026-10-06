from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = (
    PROJECT_ROOT
    / "output"
    / "business_analysis"
    / "rfm_analysis.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "output" / "visualizations"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_PATH)

segment_counts = (
    df["Customer Segment"]
    .value_counts()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))

# Use a different colour palette from the Profit by Category chart
colors = plt.cm.tab10(range(len(segment_counts)))

plt.bar(
    segment_counts.index,
    segment_counts.values,
    color=colors
)

plt.title("Customer Distribution by RFM Segment")
plt.xlabel("RFM Segment")
plt.ylabel("Number of Customers")

plt.xticks(rotation=25)
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "05_rfm_segment_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Saved: 05_rfm_segment_distribution.png")