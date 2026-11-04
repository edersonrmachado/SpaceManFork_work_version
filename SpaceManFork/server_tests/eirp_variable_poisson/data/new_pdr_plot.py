import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator

# Set global font configuration
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'

# Input file
filename = "eirp_variable_poisson_all_regions.csv"

# Outputs
fig_name_pdf = "pdr_vs_eirp.pdf" 
fig_name_eps = "pdr_vs_eirp.eps"
fig_name_svg = "pdr_vs_eirp.svg"

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

# Aggregate data: calculate mean final_pdr grouped by region, eirp_dbm, and sf
df_agg = (
    df.groupby(["region", "eirp_dbm", "sf"])["final_pdr"]
      .mean()
      .reset_index()
      .rename(columns={"final_pdr": "mean_pdr"})
)

# Figure config
fig_facecolor = "#FFFFFF"
dpi_set = 700
fig_width = 3.5
fig_height = 2.2
fontsize_xticks = 9
fontsize_xy_labels = 10
fontsize_sflabels = 6
fontsize_legend = 6
lw_plots = 0.7
markersize_plots =  1.5
alpha_plots = 0.8
lw_legend = 0.5
ylim_min = -20
ylim_max = 100
alpha_grid = 0.2
lw_grid = 0.8
frame_leg_alpha = 0.9

# Region styles
markers = {
    "EU433": "o",
    "EU868": "s",
    "CN470": "^",
    "AS915": "D"
}

colors = {
    "EU433": "#4682B4", 
    "EU868": "#E69F00",
    "AS915": "#d62728",
    "CN470": "#2ca02c"
}

fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=dpi_set, facecolor=fig_facecolor)

# Plot each region using the aggregated data
for region in markers:
    data = df_agg[df_agg["region"] == region].sort_values("eirp_dbm")
    
    if data.empty:
        continue

    ax.plot(
        data["eirp_dbm"],
        data["mean_pdr"],
        marker=markers[region],
        markersize=markersize_plots,
        linewidth=lw_plots,
        color=colors[region],
        alpha=alpha_plots,
        label=region,
        zorder=3
    )

    # Annotate each unique SF exactly once
    sf_groups = data.groupby("sf").first().reset_index()
    
    for _, row in sf_groups.iterrows():
        sf_val = int(row['sf'])
        
        # Define offset: below (-10) for EU868, above (6) for others
        y_offset = -10 if region == "EU868" else 6
        
        ax.annotate(
            f"{sf_val}",
            (row["eirp_dbm"], row["mean_pdr"]),
            xytext=(0, y_offset),
            textcoords="offset points",
            ha="center",
            fontsize=fontsize_sflabels,
            color=colors[region]
        )

# Axis labels
ax.set_xlabel("EIRP (dBm)", fontsize=fontsize_xy_labels)
ax.set_ylabel("Mean PDR (%)", fontsize=fontsize_xy_labels)

# Ticks and limits
#ax.set_xticks([4, 8, 12, 16, 22, 26, 30])
ax.xaxis.set_minor_locator(MultipleLocator(1))
ax.set_yticks(range(0, 101, 20))  
ax.set_ylim([ylim_min, ylim_max])
ax.tick_params(axis="both", labelsize=fontsize_xticks)

# Legend
ax.legend(
    title="Region",
    linewidth=lw_legend,
    fontsize=fontsize_legend,
    title_fontsize=fontsize_legend,
    loc="upper left",
    framealpha=frame_leg_alpha,
)
ax.grid(True, which="major", linestyle="--", alpha=alpha_grid, linewidth=lw_grid)
ax.grid(True, which="minor", linestyle=":", alpha=0.1, linewidth=0.5)

# Save figure in multiple formats
plt.tight_layout()

plt.savefig(fig_name_pdf, dpi=dpi_set, bbox_inches="tight", facecolor=fig_facecolor)
plt.savefig(fig_name_eps, dpi=dpi_set, bbox_inches="tight", facecolor=fig_facecolor)
plt.savefig(fig_name_svg, dpi=dpi_set, bbox_inches="tight", facecolor=fig_facecolor)

# plt.show()