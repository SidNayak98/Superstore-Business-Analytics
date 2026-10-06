from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = (
    PROJECT_ROOT
    / "output"
    / "business_analysis"
    / "state_analysis.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "output" / "visualizations"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_PATH)

df = (
    df.sort_values("Sales", ascending=False)
    .head(10)
    .sort_values("Sales", ascending=True)
)

plt.figure(figsize=(10, 7))

plt.barh(
    df["State"],
    df["Sales"]
)

plt.title("Top 10 States by Sales")
plt.xlabel("Sales ($)")
plt.ylabel("State")

plt.grid(axis="x", alpha=0.3)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "07_top_states_by_sales.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

print("Saved: 07_top_states_by_sales.png")