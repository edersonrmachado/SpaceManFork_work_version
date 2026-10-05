import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

filename = "../../data/eu868_initial.csv"

df = pd.read_csv(filename)

df = df.map(
    lambda x: str(x).replace("**", "")
    if isinstance(x, str) else x
)

columns = [
    "sf",
    "collided_rate",
    "non_visibility_rate",
    "link_margin_failed_rate",
    "doppler_failed_rate",
    "final_pdr"
]

for col in columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.sort_values("sf")

metrics = [
    "collided_rate",
    "non_visibility_rate",
    "link_margin_failed_rate",
    "doppler_failed_rate",
    "final_pdr"
]

labels = [
    "Collided",
    "Non-visible",
    "Link failed",
    "Doppler failed",
    "Final PDR"
]

x = np.arange(len(df["sf"]))

width = 0.15

fig, ax = plt.subplots(figsize=(13, 7))

for i, (metric, label) in enumerate(zip(metrics, labels)):

    offset = (i - 2) * width

    ax.bar(
        x + offset,
        df[metric],
        width,
        label=label
    )

ax.set_xlabel("Spreading Factor")
ax.set_ylabel("Percentage (%)")
ax.set_title("Simulation Metrics by Spreading Factor")

ax.set_xticks(x)
ax.set_xticklabels(
    [f"SF {int(sf)}" for sf in df["sf"]]
)

ax.set_ylim(0, 100)

ax.grid(
    True,
    axis="y",
    alpha=0.3
)

ax.legend()

plt.tight_layout()
plt.show()