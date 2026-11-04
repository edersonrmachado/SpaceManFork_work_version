import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator

# Set global font configuration
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'

# Input file
filename = "eirp_variable_poisson_all_regions.csv"

# Outputs
fig_name_pdf = "pdr_vs_eirp_subplots.pdf" 
fig_name_eps = "pdr_vs_eirp_subplots.eps"
fig_name_svg = "pdr_vs_eirp_subplots.svg"

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

# Figure config for multi-panel
fig_facecolor = "#FFFFFF"
dpi_set = 700
fig_width = 7.0   
fig_height = 2.2
fontsize_xticks = 8
fontsize_xy_labels = 9
fontsize_legend = 5
alpha_plots = 0.8
lw_legend = 0.5
ylim_min = -20
ylim_max = 100
alpha_grid = 0.2
lw_grid = 0.8
frame_leg_alpha = 0.9

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

unique_sfs = sorted(df_agg["sf"].unique())
fig, axes = plt.subplots(1, len(unique_sfs), figsize=(fig_width, fig_height), dpi=dpi_set, facecolor=fig_facecolor, sharey=True)

regions_list = list(markers.keys())
bar_width = 0.8
num_regions = len(regions_list)

for idx, sf_val in enumerate(unique_sfs):
    ax = axes[idx] if len(unique_sfs) > 1 else axes
    sf_data = df_agg[df_agg["sf"] == sf_val]
    
    for i, region in enumerate(regions_list):
        data = sf_data[sf_data["region"] == region].sort_values("eirp_dbm")
        if data.empty:
            continue

        # Grouped bar offsets
        offset = (i - num_regions / 2 + 0.5) * bar_width
        x_pos = data["eirp_dbm"] + offset

        ax.bar(
            x_pos,
            data["mean_pdr"],
            width=bar_width,
            color=colors[region],
            alpha=alpha_plots,
            label=region if idx == 0 else "",
            zorder=3
        )

    ax.set_title(f"SF {int(sf_val)}", fontsize=fontsize_xy_labels)
    ax.set_xlabel("EIRP (dBm)", fontsize=fontsize_xy_labels)
    if idx == 0:
        ax.set_ylabel("Mean PDR (%)", fontsize=fontsize_xy_labels)
    
    ax.set_xticks([0, 15, 30])
    ax.set_xticklabels(["0", "15", "30"])
    ax.set_yticks(range(0, 101, 20))  
    ax.set_ylim([ylim_min, ylim_max])
    ax.tick_params(axis="both", labelsize=fontsize_xticks)
    ax.grid(True, which="major", linestyle="--", alpha=alpha_grid, linewidth=lw_grid)

    if idx == 0:
        ax.legend(
            title="Region",
            linewidth=lw_legend,
            fontsize=fontsize_legend,
            title_fontsize=fontsize_legend,
            loc="lower right",
            framealpha=frame_leg_alpha,
        )

# Save figure in multiple formats
plt.tight_layout()

plt.savefig(fig_name_pdf, dpi=dpi_set, bbox_inches="tight", facecolor=fig_facecolor)
plt.savefig(fig_name_eps, dpi=dpi_set, bbox_inches="tight", facecolor=fig_facecolor)
plt.savefig(fig_name_svg, dpi=dpi_set, bbox_inches="tight", facecolor=fig_facecolor)

# plt.show()