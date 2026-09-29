import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# uso: python plot_sf_pdr.py [arquivo.csv]
csv_file = "../../data/eu868_t1.csv"

df = pd.read_csv(csv_file).sort_values("sf")

total = df["total_pkt"]

# percentuais em relação ao total de pacotes (2 casas decimais)
df["collided_pct"] = (df["collided"] * 100 / total).round(2)
df["non_visible_pct"] = (df["non_visible"] * 100 / total).round(2)
df["doppler_error_pct"] = (df["doppler_error"] * 100 / total).round(2)

# ATENÇÃO: o CSV não tem coluna com a contagem de falhas por link margin.
# Aqui assumo que é o que sobra: total - colisões - não visíveis - doppler - sucesso.
link_failed = (df["total_pkt"] - df["collided"] - df["non_visible"]
               - df["doppler_error"] - df["succes_rec_tx"])
df["link_failed_pct"] = (link_failed * 100 / total).round(2)

# PDR = transmissões recebidas com sucesso * 100 / total
df["pdr"] = (df["succes_rec_tx"] * 100 / total).round(2)

categories = ["collided_pct", "non_visible_pct", "link_failed_pct",
              "doppler_error_pct", "pdr"]
labels = ["Collided", "Non visible", "Link failed", "Doppler error", "Success"]
colors = ["tab:red", "tab:orange", "tab:purple", "tab:brown", "tab:green"]

# tabela no terminal e em CSV
print(df[["sf"] + categories].to_string(index=False))
df[["sf"] + categories].to_csv("sf_percentages.csv", index=False)

# ---------- Gráfico 1: SF x PDR ----------
fig1, ax1 = plt.subplots(figsize=(7, 4.5))
ax1.plot(df["sf"], df["pdr"], marker="o", linewidth=2)
for sf, pdr in zip(df["sf"], df["pdr"]):
    ax1.annotate(f"{pdr:.2f}", (sf, pdr), textcoords="offset points",
                 xytext=(0, 8), ha="center", fontsize=9)
ax1.set_xlabel("Spreading Factor (SF)")
ax1.set_ylabel("PDR (%)")
ax1.set_title("PDR por Spreading Factor")
ax1.set_xticks(sorted(df["sf"].unique()))
ax1.set_ylim(bottom=0)
ax1.grid(True, linestyle="--", alpha=0.5)
fig1.tight_layout()
fig1.savefig("sf_pdr.png", dpi=200)

# ---------- Gráfico 2: 3D (x = SF, y = categoria, z = %) ----------
n = len(df)
fig2 = plt.figure(figsize=(11, 7))
ax2 = fig2.add_subplot(111, projection="3d")

for j, (col, color) in enumerate(zip(categories, colors)):
    ax2.bar3d(np.arange(n), np.full(n, j), np.zeros(n),  # x, y, z (base)
              0.6, 0.6, df[col].to_numpy(),              # largura x, largura y, altura z
              color=color, shade=True)

ax2.set_xticks(np.arange(n) + 0.3)
ax2.set_xticklabels(df["sf"].astype(int))
ax2.set_yticks(np.arange(len(labels)) + 0.3)
ax2.set_yticklabels(labels)
ax2.set_xlabel("Spreading Factor (SF)")
ax2.set_zlabel("% dos pacotes")
ax2.set_zlim(0, 100)
ax2.set_title("Distribuição dos pacotes por SF")
fig2.savefig("sf_losses_3d.png", dpi=200)

plt.show()