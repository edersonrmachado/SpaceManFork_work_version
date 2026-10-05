import pandas as pd
import matplotlib.pyplot as plt

filename = "../../data/eu868_initial.csv"

df = pd.read_csv(filename)

# Remover "**"
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

titles = [
    "Collision Rate",
    "Non-visibility Rate",
    "Link Margin Failure Rate",
    "Doppler Failure Rate",
    "Final PDR"
]

fig, axes = plt.subplots(
    3,
    2,
    figsize=(12, 12)
)

axes = axes.flatten()

for ax, metric, title in zip(axes, metrics, titles):

    ax.plot(
        df["sf"],
        df[metric],
        marker="o",
        linewidth=2,
        markersize=6
    )

    ax.set_title(title)
    ax.set_xlabel("Spreading Factor")
    ax.set_ylabel("Percentage (%)")

    ax.grid(
        True,
        axis="y",
        alpha=0.3
    )

# Remover o sexto subplot vazio
axes[-1].remove()

plt.suptitle(
    "Simulation Metrics by Spreading Factor",
    fontsize=15
)

plt.tight_layout()
plt.show()