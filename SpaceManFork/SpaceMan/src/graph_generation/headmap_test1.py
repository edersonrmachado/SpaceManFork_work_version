import pandas as pd
import matplotlib.pyplot as plt

filename = "../../data/eu868_initial.csv"

df = pd.read_csv(filename)

# Remove **
df = df.map(
    lambda x: str(x).replace("**", "")
    if isinstance(x, str) else x
)

metrics = [
    "collided_rate",
    "non_visibility_rate",
    "link_margin_failed_rate",
    "doppler_failed_rate",
    "final_pdr"
]

for col in ["sf"] + metrics:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Criar matriz SF x métricas
heatmap_data = df.set_index("sf")[metrics]

# Renomear para ficar mais bonito
heatmap_data.columns = [
    "Collided",
    "Non-visible",
    "Link failed",
    "Doppler failed",
    "Final PDR"
]

fig, ax = plt.subplots(figsize=(10, 6))

im = ax.imshow(
    heatmap_data,
    cmap="viridis",
    aspect="auto"
)

# Eixo X
ax.set_xticks(range(len(heatmap_data.columns)))
ax.set_xticklabels(heatmap_data.columns)

# Eixo Y
ax.set_yticks(range(len(heatmap_data.index)))
ax.set_yticklabels(
    [f"SF {int(sf)}" for sf in heatmap_data.index]
)

# Mostrar os valores dentro das células
for i in range(len(heatmap_data)):
    for j in range(len(heatmap_data.columns)):
        ax.text(
            j,
            i,
            f"{heatmap_data.iloc[i, j]:.2f}",
            ha="center",
            va="center"
        )

ax.set_title("Simulation Results by SF")

fig.colorbar(
    im,
    ax=ax,
    label="Percentage (%)"
)

plt.tight_layout()
plt.show()