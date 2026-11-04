import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import linregress

# Set global font configuration
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'

# Load the previously generated file
filename = "average_collision_rate_and_toa_by_region_by_sf.csv"
df = pd.read_csv(filename)

# Aesthetic and axis limit configurations
fig_facecolor = "#FFFFFF"
dpi_set = 700
fig_width = 3.5
fig_height = 2.8

fontsize_xticks = 9
fontsize_xy_labels = 10
fontsize_legend = 7

lw_plots = 0.8
markersize_plots = 1.0
alpha_plots = 0.8

lw_grid = 0.8
fontsize_labels = 7

lw_legend=0.5
alpha_grid = 0.45
#leg_right = 0.91
#leg_hight = 0.04
lw_grid = 0.78
frame_leg_alpha=0.9
space_handle_leg=1.2
space_handle_pad_leg =0.5

# Options for Y-axis limits (modify here as needed)
ylim_inf = 0
ylim_sup = 7

colors = {
    "EU433": "#4682B4",
    "EU868": "#E69F00",
    "AS915": "#d62728",
    "CN470": "#2ca02c"
}

# Output file names for the EU868 region
fig_name_pdf = "collision_rate_vs_toa_eu868.pdf"
fig_name_eps = "collision_rate_vs_toa_eu868.eps"
fig_name_svg = "collision_rate_vs_toa_eu868.svg"

# Create figure using the exact same structure
fig, ax = plt.subplots(
    figsize=(fig_width, fig_height),
    dpi=dpi_set,
    facecolor=fig_facecolor
)

df_eu868 = df[df["region"] == "EU868"].dropna(
    subset=["pkt_toa", "collided_rate", "sf"]
)

if not df_eu868.empty:
  x_868 = df_eu868["pkt_toa"]
  y_868 = df_eu868["collided_rate"]

  slope_868, intercept_868, r_value_868, _, _ = linregress(x_868, y_868)
  r_squared_868 = r_value_868**2

  eu868_color = colors.get("EU868", "#E69F00")

  # Scatter plot
  ax.scatter(
      x_868,
      y_868,
      color=eu868_color,
      s=(markersize_plots ** 2) * 10,
      alpha=alpha_plots,
      label="EU868",
  )
  
  # Linear fit line (multiplicação corrigida)
  x_line_868 = np.linspace(x_868.min(), x_868.max(), 100)
  ax.plot(
      x_line_868,
      slope_868 * x_line_868 + intercept_868,
      color=eu868_color,
      linewidth=lw_plots,
      linestyle="--",
      label=f"Fit (R² = {r_squared_868:.4f})",
  )

  # Add SFxx labels with manual adjustments to avoid overlap
  for _, row in df_eu868.iterrows():
    sf_val = int(row['sf'])
    
    # Default position settings (above the point)
    xytext_val = (0, 6)
    ha_val = "center"
    
    # Specific adjustments to avoid conflicts if points are close
    if sf_val == 8:
      xytext_val = (10, -12) # Placed below and shifted to the side
    elif sf_val == 10:
      xytext_val = (0, 11)   # Specific adjustment if needed
      
    ax.annotate(
        f"SF{sf_val}",
        (row["pkt_toa"], row["collided_rate"]),
        textcoords="offset points",
        xytext=xytext_val,
        ha=ha_val,
        fontsize=fontsize_labels,
    )

ax.set_xlabel("Packet Time on Air (s)", fontsize=fontsize_xy_labels)
ax.set_ylabel("Collision Rate (%)", fontsize=fontsize_xy_labels)

# Apply configurable Y-axis limits
ax.set_ylim(ylim_inf, ylim_sup)

# Customizing ticks to include 3.0 explicitly alongside automatic ticks
current_xticks = ax.get_xticks()
new_xticks = sorted(list(set(list(current_xticks) + [3.0])))
ax.set_xticks(new_xticks)

ax.tick_params(axis="both", labelsize=fontsize_xticks)
#ax.legend(fontsize=fontsize_legend, framealpha=frame_leg_alpha)
ax.legend(
    linewidth=lw_legend,
    fontsize=fontsize_legend,
    title_fontsize=fontsize_legend,
    loc="upper left",
    #bbox_to_anchor=(leg_right,leg_hight,),  
    framealpha=frame_leg_alpha,
    handlelength=space_handle_leg,
    handletextpad = space_handle_pad_leg  # Reduce distance between symbols and text
)

ax.grid(
    True,
    linestyle=":",
    alpha=alpha_grid,
    linewidth=lw_grid
)

# Adjust layout consistently
plt.tight_layout()
plt.subplots_adjust(top=0.72)

# Save the figure in the requested formats
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

plt.show()