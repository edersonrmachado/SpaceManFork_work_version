import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator
from matplotlib.lines import Line2D

# Set global font configuration
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'

# Input file
filename = "../eirp_variable_poisson_all_regions.csv"

# Output files for figures
fig_name_pdf = "link_pass_vs_eirp.pdf"
fig_name_eps = "link_pass_vs_eirp.eps"
fig_name_svg = "link_pass_vs_eirp.svg"
csv_output = "average_link_margin_pass_rate_by_region_sf_eirp.csv"

# Load dataset
df = pd.read_csv(filename)

# Create region name based on frequency
regions = {
    868.30: "EU868",
    433.375:"EU433",
    921.4: "AS915",
    473.3: "CN470"
}

df["region"] = df["freqMHz"].map(regions)

# Calculate and save the aggregated matrix/CSV
result = (
    df.groupby(["sf", "eirp_dbm", "region"])["link_margin_pass_rate"]
      .mean()
      .unstack()
      .round(2)
)

print("Table:")
print(result)

# Save file
result.to_csv(csv_output)

# Aggregate data for plotting
df_agg = (
    df.groupby(["region", "eirp_dbm", "sf"])["link_margin_pass_rate"]
      .mean()
      .reset_index()
      .rename(columns={"link_margin_pass_rate": "mean_pass_rate"})
)

# Figure configuration
fig_facecolor = "#FFFFFF"
dpi_set = 700
fig_width = 3.5
fig_height = 2.8

fontsize_xticks = 9
fontsize_xy_labels = 10
fontsize_legend = 7

lw_plots = 0.7
markersize_plots = 3.0
alpha_plots = 0.8

ylim_min = -10
ylim_max = 110

alpha_grid = 0.4
lw_grid = 0.8
frame_leg_alpha = 0.0

space_handle_leg = 1
space_handle_pad_leg = 0.3

# Colors for each region
colors = {
    "EU433": "#4682B4",
    "EU868": "#E69F00",
    "AS915": "#d62728",
    "CN470": "#2ca02c"
}

# Markers for each SF
sf_markers = {
    7: "o",
    8: "s",
    9: "P",
    10: "D",
    11: "x",
    12: "^"
}

# Create figure
fig, ax = plt.subplots(
    figsize=(fig_width, fig_height),
    dpi=dpi_set,
    facecolor=fig_facecolor
)

# Plot each region
for region in colors:

    region_data = df_agg[
        df_agg["region"] == region
    ].sort_values(["eirp_dbm", "sf"])

    if region_data.empty:
        continue
        
    # Connect all SF points belonging to the same region
    ax.plot(
        region_data["eirp_dbm"],
        region_data["mean_pass_rate"],
        linestyle="-",
        linewidth=lw_plots,
        color=colors[region],
        alpha=alpha_plots,
        zorder=2
    )

    # Plot individual markers according to SF
    for sf_val, group in region_data.groupby("sf"):

        ax.scatter(
            group["eirp_dbm"],
            group["mean_pass_rate"],
            marker=sf_markers.get(int(sf_val), "o"),
            s=markersize_plots**2,
            color=colors[region],
            alpha=alpha_plots,
            zorder=3
        )

# Axis labels
ax.set_xlabel("EIRP (dBm)", fontsize=fontsize_xy_labels)
ax.set_ylabel("Mean Link Margin Pass Rate (%)", fontsize=fontsize_xy_labels)

# Ticks and limits
ax.xaxis.set_minor_locator(MultipleLocator(1))
ax.set_yticks(range(0, 101, 20))
ax.set_ylim([ylim_min, ylim_max])

ax.tick_params(
    axis="both",
    labelsize=fontsize_xticks
)

# Grid
ax.grid(
    True,
    which="major",
    linestyle="--",
    alpha=alpha_grid,
    linewidth=lw_grid
)

ax.grid(
    True,
    which="minor",
    linestyle=":",
    alpha=0.1,
    linewidth=0.5
)

# ==========================================
# SINGLE LEGEND: REGIONS + SPREADING FACTORS
# ==========================================

# Region handles
region_handles = [
    Line2D(
        [0], [0],
        color=colors[region],
        linewidth=lw_plots,
        linestyle="-",
        label=region
    )
    for region in colors
]

# SF handles
sf_handles = [
    Line2D(
        [0], [0],
        color="black",
        marker=sf_markers[sf],
        linestyle="None",
        markersize=markersize_plots-0.2,
        label=f"SF{sf}"
    )
    for sf in sf_markers
]

# Combine handles
all_handles = region_handles + sf_handles

ax.legend(
    handles=all_handles,
    title="Region / Spreading Factor",
    fontsize=fontsize_legend,
    title_fontsize=fontsize_legend,
    loc="upper left",
    ncol=3,
    framealpha=frame_leg_alpha,
    handlelength=space_handle_leg,
    handletextpad=space_handle_pad_leg,
    columnspacing=0.8,
    labelspacing=0.5
)

# Adjust layout
plt.tight_layout()
plt.subplots_adjust(top=0.72)

# Save figure in multiple formats
plt.savefig(
    fig_name_pdf,
    dpi=dpi_set,
    bbox_inches="tight",
    facecolor=fig_facecolor
)

plt.savefig(
    fig_name_eps,
    dpi=dpi_set,
    bbox_inches="tight",
    facecolor=fig_facecolor
)

plt.savefig(
    fig_name_svg,
    dpi=dpi_set,
    bbox_inches="tight",
    facecolor=fig_facecolor
)

# plt.show()