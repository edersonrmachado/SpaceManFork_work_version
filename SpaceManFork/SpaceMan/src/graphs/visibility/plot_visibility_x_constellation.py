import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'
# input file
filename="visible_variable_all_regions.csv"

# outputs
fig_name_pdf="visibility.pdf" 
fig_name_eps="visibility.eps"
fig_name_svg="visibility.svg"

df = pd.read_csv(filename)

# create the region name based on the frequency
regions = {
    868.30: "EU868",
    433.375: "EU433",
    921.4: "AS915",
    473.3: "CN470"
}
df["region"] = df["freqMHz"].map(regions)

# calculate the average visibility rate  for each region and number of satellite
result = (
    df.groupby(["num_sats", "region"])["visibility_rate"]
      .mean()
      .unstack()
      .round(2)
)

print(result)

# save the result
result.to_csv("visibility_x_constellation.csv")

# read the results 
df_result = pd.read_csv("visibility_x_constellation.csv", index_col="num_sats")

# figure config 
fig_name = "visibility.pdf"
fig_facecolor = "#FFFFFF"
dpi_set = 700
fig_width = 3.5
fig_height = 2.2
fontsize_xticks = 9
fontsize_xy_labels = 10
fontsize_legend = 7.5
lw_plots=0.9
markersize_plots=3
alpha_plots=0.7
lw_legend=0.5
ylim_min=0
ylim_max=120
alpha_grid=0.45
leg_right=0.975
leg_hight=-0.0
lw_grid=0.8
frame_leg_alpha=0.9
color_eu433="#4682B4" 
color_eu868="#E69F00"
color_as915="#d62728"
color_cn470="#2ca02c"


fig, ax = plt.subplots( figsize=(fig_width, fig_height), dpi=dpi_set, facecolor=fig_facecolor)

# plots
ax.plot(
    df_result.index,
    df_result["EU433"],
    marker="o",
    linewidth=lw_plots,
    markersize=markersize_plots,
    color=color_eu433,
    alpha=alpha_plots,
    label="EU433",
)
ax.plot(
    df_result.index,
    df_result["EU868"],
    marker="s",
    linewidth=lw_plots,
    markersize=markersize_plots,
    color=color_eu868,
    alpha=alpha_plots,
    label="EU868",
)
ax.plot(
    df_result.index,
    df_result["AS915"],
    marker="d",
    linewidth=lw_plots,
    markersize=markersize_plots,
    color=color_as915,
    alpha=alpha_plots,
    label="AS915",
)
ax.plot(
    df_result.index,
    df_result["CN470"],
    marker="^",
    linewidth=lw_plots,
    markersize=markersize_plots,
    color=color_cn470,
    alpha=alpha_plots,
    label="CN470",
)
# axis labels
ax.set_xlabel("Number of satellites", fontsize=fontsize_xy_labels)
ax.set_ylabel("Visibility rate (%)", fontsize=fontsize_xy_labels)

# ticks
ax.set_xticks(df_result.index)
ax.set_yticks(range(0, 101, 20))  
ax.set_ylim([ylim_min,ylim_max])
ax.tick_params(axis="both", labelsize=fontsize_xticks)

# legend
ax.legend(
    title="Region",
    linewidth=lw_legend,
    fontsize=fontsize_legend,
    title_fontsize=fontsize_legend,
    loc="lower right",
    bbox_to_anchor=(leg_right,leg_hight,),  
    framealpha=frame_leg_alpha,
)
ax.grid(True, linestyle="--", alpha=alpha_grid, linewidth=lw_grid)

# save fig
plt.tight_layout()

plt.savefig(
    fig_name_pdf, dpi=dpi_set, bbox_inches="tight", facecolor=fig_facecolor
)
plt.savefig(
    fig_name_eps, dpi=dpi_set, bbox_inches="tight", facecolor=fig_facecolor
)
plt.savefig(
    fig_name_svg, dpi=dpi_set, bbox_inches="tight", facecolor=fig_facecolor
)


#plt.show()