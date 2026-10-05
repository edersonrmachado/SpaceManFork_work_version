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

sfs = sorted(df["sf"].unique())

# Colormap
cmap = plt.get_cmap("viridis")
colors = cmap(
    np.linspace(0, 1, len(sfs))
)

# Pequeno deslocamento vertical para não sobrepor os pontos
offsets = np.linspace(
    -0.25,
    0.25,
    len(sfs)
)

fig, ax = plt.subplots(figsize=(11, 7))

for sf, color, offset in zip(
    sfs,
    colors,
    offsets
):

    row = df[df["sf"] == sf].iloc[0]

    values = [
        row[metric]
        for metric in metrics
    ]

    y = np.arange(len(metrics)) + offset

    ax.scatter(
        values,
        y,
        s=70,
        color=color,
        label=f"SF {int(sf)}"
    )

ax.set_yticks(
    np.arange(len(metrics))
)

ax.set_yticklabels(labels)

ax.set_xlabel("Percentage (%)")
ax.set_ylabel("Metric")

ax.set_title(
    "Simulation Metrics by Spreading Factor"
)

ax.grid(
    True,
    axis="x",
    alpha=0.3
)

ax.legend(
    title="Spreading Factor",
    ncol=2
)

ax.invert_yaxis()

ax.set_xlim(-2, 100)
plt.tight_layout()
plt.show()