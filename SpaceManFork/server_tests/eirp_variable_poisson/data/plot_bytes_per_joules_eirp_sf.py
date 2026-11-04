import pandas as pd
import matplotlib.pyplot as plt

# Font sizes
fontsize_xylabels = 12
fontsize_xyticks = 10
fontsize_sflabels = 9
fontsize_legend = 10
fontsize_legend_title = 10

# Load data
filename = "average_bytes_per_joule_by_region_sf_eirp.csv"

df = pd.read_csv(filename)

df = df.melt(
    id_vars=["sf", "eirp_dbm"],
    var_name="region",
    value_name="bytes_per_joule"
)

df = df.dropna(subset=["bytes_per_joule"])

# Plot
plt.figure(figsize=(10, 6))

markers = {
    "EU433": "o",
    "EU868": "s",
    "CN470": "^",
    "AS915": "D"
}

colors = {
    "EU433": "blue",
    "EU868": "orange",
    "CN470": "green",
    "AS915": "red"
}

for region in markers:

    data = df[df["region"] == region].sort_values("eirp_dbm")

    plt.plot(
        data["eirp_dbm"],
        data["bytes_per_joule"],
        marker=markers[region],
        markersize=4,
        linewidth=1.5,
        color=colors[region],
        label=region,
        zorder=3
    )

    # SF labels
    for _, row in data.iterrows():

        offset_x = 0
        offset_y = 6

        if region == "EU433" and int(row["sf"]) in [7, 8, 9, 10]:
            offset_y = -12

        elif region == "EU868" and int(row["sf"]) == 9:
            offset_y = -12

        elif region == "CN470":
            offset_y = -12

            if int(row["sf"]) in [11, 12]:
                offset_x = 12

        elif region == "AS915":
            if int(row["sf"]) in [10, 12]:
                offset_x = 12

        plt.annotate(
            f"SF{int(row['sf'])}",
            (row["eirp_dbm"], row["bytes_per_joule"]),
            xytext=(offset_x, offset_y),
            textcoords="offset points",
            ha="center",
            fontsize=fontsize_sflabels,
            color=colors[region]
        )

# Axis ticks
eirp_ticks = sorted(df["eirp_dbm"].unique())

plt.xticks(
    eirp_ticks,
    fontsize=fontsize_xyticks
)

plt.yticks(
    fontsize=fontsize_xyticks
)

# Axis labels
plt.xlabel(
    "EIRP (dBm)",
    fontsize=fontsize_xylabels
)

plt.ylabel(
    "Mean Bytes per Joule",
    fontsize=fontsize_xylabels
)

# Grid
plt.grid(
    axis="x",
    linestyle="--",
    alpha=0.5
)

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.5
)

# Legend
plt.legend(
    title="Region",
    fontsize=fontsize_legend,
    title_fontsize=fontsize_legend_title,
    loc="upper left"
)

plt.tight_layout()

plt.savefig(
    "mean_bytes_per_joule_vs_eirp.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()