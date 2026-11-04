import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata


filename ="eirp_variable_poisson_all_regions.csv"
# Load simulation dataset
df = pd.read_csv(filename)

# Map frequency to frequency region
regions = {
    868.30: "EU868",
    433.375: "EU433",
    921.4: "AS915",
    473.3: "CN470"
}
df["region"] = df["freqMHz"].map(regions)

# Fallback: fill unmapped regions using frequency value if needed
df["region"] = df["region"].fillna(df["freqMHz"].astype(str) + " MHz")

# Compute realization index per group
df['realization'] = df.groupby(['region', 'sf']).cumcount()

# Color mapping by Region
region_colors = {
    "EU868": "#1f77b4",   # Blue
    "EU433": "#2ca02c",   # Green
    "AS915": "#ff7f0e",   # Orange
    "CN470": "#d62728"    # Red
}

# Line styles by Spreading Factor (SF)
sf_line_styles = {
    12: '-',    # Solid line
    11: '--',   # Dashed line
    10: ':-',   # Dotted line
    9: '-.',    # Dash-dot line
    8: ':'      # Dense dotted line
}

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Iterate over Region and SF combinations
for (region_name, sf_val), group in df.groupby(['region', 'sf']):
    if len(group) < 3:
        continue  # Skip groups with insufficient points for surface grid interpolation
    
    color = region_colors.get(region_name, 'gray')
    linestyle = sf_line_styles.get(sf_val, '-')

    # Extract 3D coordinates
    x = group['eirp_dbm'].values
    y = group['realization'].values
    z = group['final_pdr'].values

    # Create grid mesh for 3D surface interpolation
    xi = np.linspace(x.min(), x.max(), 15)
    yi = np.linspace(y.min(), y.max(), 15)
    X, Y = np.meshgrid(xi, yi)

    # Interpolate Z values (PDR) over mesh grid
    Z = griddata((x, y), z, (X, Y), method='nearest')

    # Plot 3D surface wireframe with region color and SF line style
    ax.plot_wireframe(
        X, Y, Z,
        color=color,
        linestyle=linestyle,
        linewidth=1.2,
        alpha=0.75,
        label=f'{region_name} - SF{sf_val}'
    )

# Set labels and title
ax.set_xlabel('EIRP (dBm)')
ax.set_ylabel('Realization Index (0..N)')
ax.set_zlabel('Final PDR (%)')
ax.set_title('3D Surface Plot: PDR by Region (Color) and Spreading Factor (Line Style)')

# Display legend
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')

plt.tight_layout()
plt.show()