import pandas as pd
import matplotlib.pyplot as plt

filename = "../../data/eu868_initial.csv"


df = pd.read_csv(filename)

# Se o arquivo contém "**" antes de alguns valores, remover
df = df.map(
    lambda x: str(x).replace("**", "")
    if isinstance(x, str) else x
)

# Converter as colunas relevantes para números
columns = [
    "sf",
    "collided_rate",
    "non_visibility_rate",
    "link_margin_failed_rate",
    "doppler_failed_rate",
    "final_pdr"
]

for col in columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")


# ============================================================
# 2. Definir as métricas do eixo X
# ============================================================

metrics = [
    "collided_rate",
    "non_visibility_rate",
    "link_margin_failed_rate",
    "doppler_failed_rate",
    "final_pdr"
]

x_labels = [
    "Collided",
    "Non-visible",
    "Link failed",
    "Doppler failed",
    "Final PDR"
]


# ============================================================
# 3. Criar o gráfico
# ============================================================

fig, ax = plt.subplots(figsize=(11, 6))

# SFs presentes no arquivo
sfs = sorted(df["sf"].unique())

# Colormap
cmap = plt.get_cmap("viridis")

# Uma cor diferente para cada SF
colors = cmap(
    [i / max(1, len(sfs) - 1) for i in range(len(sfs))]
)


# ============================================================
# 4. Uma linha para cada SF
# ============================================================

for sf, color in zip(sfs, colors):

    # Pegar a linha correspondente ao SF
    row = df[df["sf"] == sf].iloc[0]

    # Valores das cinco métricas
    values = [
        row["collided_rate"],
        row["non_visibility_rate"],
        row["link_margin_failed_rate"],
        row["doppler_failed_rate"],
        row["final_pdr"]
    ]

    ax.plot(
        x_labels,
        values,
        marker="o",
        linewidth=2,
        markersize=6,
        color=color,
        label=f"SF {int(sf)}"
    )


# ============================================================
# 5. Configuração visual
# ============================================================

ax.set_xlabel("Metric")
ax.set_ylabel("Percentage (%)")

ax.set_title(
    "Simulation Results by Spreading Factor"
)

# Como seus valores chegam aproximadamente a 65%
ax.set_ylim(0, 70)

ax.grid(
    True,
    axis="y",
    alpha=0.3
)

ax.legend(
    title="Spreading Factor",
    ncol=2
)

ax.set_ylim(0,100)
plt.tight_layout()

plt.show()