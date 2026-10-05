import pandas as pd
import matplotlib.pyplot as plt

filename = "../../data/eu868_initial.csv"

# Ler CSV
df = pd.read_csv(filename)

# Remover "**" caso exista
df = df.map(
    lambda x: str(x).replace("**", "")
    if isinstance(x, str) else x
)

# Converter colunas numéricas
df["sf"] = pd.to_numeric(df["sf"], errors="coerce")
df["bw"] = pd.to_numeric(df["bw"], errors="coerce")
df["ldro"] = pd.to_numeric(df["ldro"], errors="coerce")
df["tx_power_dbm"] = pd.to_numeric(
    df["tx_power_dbm"],
    errors="coerce"
)
df["bytes_per_joule"] = pd.to_numeric(
    df["bytes_per_joule"],
    errors="coerce"
)

# Remover linhas sem bytes/joule
df = df.dropna(subset=["bytes_per_joule"])

# Ordenar pelas configurações
df = df.sort_values(
    ["sf", "bw", "ldro", "tx_power_dbm"]
)

# Criar nome para cada configuração
df["config"] = (
    "SF " + df["sf"].astype(int).astype(str)
    + "\nBW " + df["bw"].astype(int).astype(str)
    + "\nLDRO " + df["ldro"].astype(int).astype(str)
    + "\nP " + df["tx_power_dbm"].astype(str) + " dBm"
)

# Criar gráfico
fig, ax = plt.subplots(figsize=(14, 7))

bars = ax.bar(
    df["config"],
    df["bytes_per_joule"]
)

ax.set_xlabel("Configuration")
ax.set_ylabel("Bytes per Joule (bytes/J)")
ax.set_title("Energy Efficiency by Configuration")

ax.grid(
    True,
    axis="y",
    alpha=0.3
)

# Colocar valor em cima de cada barra
for bar, value in zip(
    bars,
    df["bytes_per_joule"]
):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{value:.2f}",
        ha="center",
        va="bottom",
        fontsize=9
    )

ax.set_ylim(0,500)
plt.xticks(rotation=45, ha="right")

plt.tight_layout()
plt.show()