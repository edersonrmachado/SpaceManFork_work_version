import pandas as pd
import matplotlib.pyplot as plt

filename = "average_collision_rate_by_region_by_sf.csv"

df = pd.read_csv(filename)

# Set SF as the index
df = df.set_index("sf")

# Create the grouped bar chart
ax = df.plot(
    kind="bar",
    figsize=(10, 6),
    width=0.8
)

# Labels and title
ax.set_xlabel("Spreading Factor (SF)")
ax.set_ylabel("Collision Rate (%)")
ax.set_title("Collision Rate by Region and Spreading Factor")

# Show legend
ax.legend(title="Region")

# Add grid
ax.grid(axis="y", linestyle="--", alpha=0.5)

# Adjust layout
plt.tight_layout()


###################################



###################################

df = pd.read_csv(filename)

# Set SF as the index
df = df.set_index("sf")

# Find the maximum collision rate
max_collision_rate = df.max().max()

# Set the upper limit to 10% above the maximum value
y_max = max_collision_rate * 1.10

# Create the figure
plt.figure(figsize=(10, 6))

# Plot each region with a different color, line style and marker
plt.plot(
    df.index,
    df["EU433"],
    label="EU433",
    linestyle="-",
    marker="o",
    linewidth=2,
    markersize=6,
    zorder=4
)

plt.plot(
    df.index,
    df["EU868"],
    label="EU868",
    linestyle="--",
    marker="s",
    linewidth=2,
    markersize=6,
    zorder=3
)


plt.plot(
    df.index,
    df["CN470"],
    label="CN470",
    linestyle="-",
    marker="^",
    linewidth=2,
    markersize=6,
    zorder=5
)

plt.plot(
    df.index,
    df["AS915"],
    label="AS915",
    linestyle="-",
    marker="D",
    linewidth=2,
    markersize=7,
    zorder=2
)


# Set Y-axis limits
plt.ylim(0, y_max)

# Labels
plt.xlabel("Spreading Factor (SF)")
plt.ylabel("Collision Rate (%)")

# Title
plt.title("Collision Rate vs. Spreading Factor")

# Legend
plt.legend(title="Region")

# Grid
plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.5
)

# Grid
plt.grid(
    axis="x",
    linestyle="--",
    alpha=0.5
)

# Adjust layout
plt.tight_layout()

# Save figure
plt.savefig(
    "collision_rate_vs_sf.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()