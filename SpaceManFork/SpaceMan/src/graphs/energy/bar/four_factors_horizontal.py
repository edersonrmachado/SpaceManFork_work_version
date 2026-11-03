import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.lines import Line2D

# Set global font configuration
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'

# Input and output files
filename = "../eirp_variable_poisson_all_regions.csv"
fig_name_pdf = "metrics_max_eirp_vs_sf.pdf"
fig_name_eps = "metrics_max_eirp_vs_sf.eps"
fig_name_svg = "metrics_max_eirp_vs_sf.svg"

# Load dataset
df = pd.read_csv(filename)

# Create region name based on frequency
regions = {
    868.30: "EU868",
    433.375: "EU433",
    921.4: "AS915",
    473.3: "CN470"
}

df["region"] = df["freqMHz"].map(regions)

# Define maximum EIRP values for each region
max_eirp_dict = {
    "EU433": 12,
    "EU868": 16,
    "AS915": 30,
    "CN470": 19
}

# Filter dataframe for max EIRP per region
filtered_subsets = []
for region_name, eirp_val in max_eirp_dict.items():
    subset = df[(df["region"] == region_name) & (df["eirp_dbm"] == eirp_val)]
    filtered_subsets.append(subset)

filtered_df = pd.concat(filtered_subsets)

# Metrics to analyze and plot
metrics = [
    "collided_rate", 
    "non_visibility_rate", 
    "link_margin_failed_rate", 
    "doppler_failed_rate", 
    "final_pdr"
]

metric_display_names = [
    "Collided", 
    "Non-Visible", 
    "Link Fail", 
    "Doppler Fail", 
    "Final PDR"
]

# Aggregate data: mean for each metric grouped by region (averaged across SFs)
df_agg = (
    filtered_df.groupby("region")[metrics]
    .mean()
    .reset_index()
)

print("Aggregated metrics at Max EIRP per region:")
print(df_agg)

# Figure configuration (1x4 single-row grid)
fig_facecolor = "#FFFFFF"
dpi_set = 700
fig_width = 14.0   # Expanded width for 4 horizontal subplots
fig_height = 3.5    # Height for a single row

fontsize_xticks = 9.5
fontsize_yticks = 10
fontsize_xy_labels = 11
fontsize_legend = 9
fontsize_values = 9
bar_width = 0.55
alpha_grid = 0.3
y_lim_inf = 0
y_lim_sup = 110  # Range adjusted to accommodate value labels on top

bar_metrics_color = "midnightblue"
bar_colors = [bar_metrics_color, bar_metrics_color, bar_metrics_color, bar_metrics_color, "#2ca02c"]

# Create 1x4 subplots (single row, 4 columns)
fig, axes = plt.subplots(1, 4, figsize=(fig_width, fig_height), dpi=dpi_set, facecolor=fig_facecolor, sharey=True)

# Define grid layout order: EU433 -> EU868 -> AS915 -> CN470
subplot_grid = [
    ("EU433", axes[0]),
    ("EU868", axes[1]),
    ("AS915", axes[2]),
    ("CN470", axes[3])
]

for region_name, ax in subplot_grid:
    region_data = df_agg[df_agg["region"] == region_name]
    
    if region_data.empty:
        continue

    # Extract mean values for the metrics
    values = region_data[metrics].values.flatten()
    x = np.arange(len(metrics))

    # Plot bars
    bars = ax.bar(
        x,
        values,
        width=bar_width,
        color=bar_colors,
        alpha=1,
        edgecolor="#333333",
        linewidth=0.5,
        zorder=4
    )

    # Add value labels on top of each bar (1 decimal place)
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height:.1f}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),  # 3 points vertical offset
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=fontsize_values,
            color="#222222",
            rotation=0
        )

    # Subplot styling
    ax.set_xticks(x)
    ax.set_xticklabels(metric_display_names, fontsize=fontsize_xticks, rotation=30, ha="right")
    ax.tick_params(axis="y", labelsize=fontsize_yticks)
    ax.set_ylim(y_lim_inf, y_lim_sup)
    
    ax.grid(True, linestyle="--", alpha=alpha_grid, linewidth=0.8)

    # Small legend in the upper left corner with Region and EIRP
    legend_text = f"{region_name} (EIRP: {max_eirp_dict[region_name]} dBm)"
    dummy_handle = Line2D([0], [0], color="none")
    ax.legend(
        [dummy_handle], 
        [legend_text], 
        loc="upper left", 
        fontsize=fontsize_legend, 
        handlelength=0, 
        handletextpad=0, 
        framealpha=0.0
    )

# Common axis label for Y axis
fig.text(0.01, 0.55, "Percentage (%)", va="center", rotation="vertical", fontsize=fontsize_xy_labels)

# Adjust layout for 1x4 horizontal arrangement
plt.tight_layout()
plt.subplots_adjust(top=0.92, bottom=0.25, left=0.04, right=0.98, wspace=0.15)

# Save figure in multiple formats
plt.savefig(fig_name_pdf, dpi=dpi_set, bbox_inches="tight", facecolor=fig_facecolor)
plt.savefig(fig_name_eps, dpi=dpi_set, bbox_inches="tight", facecolor=fig_facecolor)
plt.savefig(fig_name_svg, dpi=dpi_set, bbox_inches="tight", facecolor=fig_facecolor)

# plt.show()