import pandas as pd
import matplotlib.pyplot as plt

# Font sizes
fontsize_xylabels = 12
fontsize_xyticks = 10
fontsize_sflabels = 9
fontsize_legend = 10
fontsize_legend_title = 10

# Load data
filename = "average_final_pdr_by_region_sf_eirp.csv"
df = pd.read_csv(filename)

df = df.melt(
    id_vars=["sf", "eirp_dbm"],
    var_name="region",
    value_name="mean_pdr"
)

df = df.dropna(subset=["mean_pdr"])

# Colors by region
colors = {
    "EU433": "blue",
    "EU868": "orange",
    "CN470": "green",
    "AS915": "red"
}

# Bar plot
plt.figure(figsize=(12, 6))

regions = list(colors.keys())
bar_width = 0.2
group_spacing = 1.5  # Increase to add more space between region groups

# Plot bars for each region
for i, region in enumerate(regions):

    data = df[df["region"] == region].sort_values("sf")

    if data.empty:
        continue

    # Center bars within each region group
    n_bars = len(data)
    offsets = [
        (j - (n_bars - 1) / 2) * bar_width
        for j in range(n_bars)
    ]

    for (_, row), offset in zip(data.iterrows(), offsets):

        bar_x = i * group_spacing + offset

        plt.bar(
            bar_x,
            row["mean_pdr"],
            width=bar_width * 0.9,
            color=colors[region],
            zorder=3
        )

        # SF labels
        plt.annotate(
            f"SF{int(row['sf'])}",
            (bar_x, row["mean_pdr"]),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            fontsize=fontsize_sflabels,
            color=colors[region]
        )

# X-axis ticks
plt.xticks(
    [i * group_spacing for i in range(len(regions))],
    regions,
    fontsize=fontsize_xyticks
)

# Axis labels
plt.xlabel("Region", fontsize=fontsize_xylabels)
plt.ylabel("Mean PDR (%)", fontsize=fontsize_xylabels)

# Grid
plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.5,
    zorder=0
)

# Y-axis limits
plt.ylim(0, 100)

# Legend
# Each region has its own color, so create a legend manually
from matplotlib.patches import Patch

legend_handles = [
    Patch(facecolor=colors[region], label=region)
    for region in regions
]

plt.legend(
    handles=legend_handles,
    title="Region",
    fontsize=fontsize_legend,
    title_fontsize=fontsize_legend_title,
    loc="upper left"
)

plt.tight_layout()

# Save figure
plt.savefig(
    "mean_pdr_bar_plot.png",
    dpi=300,
    bbox_inches="tight"
)

# Display plot
plt.show()