import pandas as pd
import matplotlib.pyplot as plt

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

metrics = {
    "collided_rate": "Collided",
    "non_visibility_rate": "Non-visible",
    "link_margin_failed_rate": "Link failed",
    "doppler_failed_rate": "Doppler failed",
    "final_pdr": "Final PDR"
}

fig, ax = plt.subplots(figsize=(11, 6))

for metric, label in metrics.items():

    ax.plot(
        df["sf"],
        df[metric],
        marker="o",
        linewidth=2,
        markersize=6,
        label=label
    )

ax.set_xlabel("Spreading Factor")
ax.set_ylabel("Percentage (%)")

ax.set_title(
    "Simulation Metrics versus Spreading Factor"
)

ax.set_xticks(df["sf"])

ax.set_ylim(0, 100)

ax.grid(
    True,
    axis="y",
    alpha=0.3
)

ax.legend()

plt.tight_layout()
plt.show()