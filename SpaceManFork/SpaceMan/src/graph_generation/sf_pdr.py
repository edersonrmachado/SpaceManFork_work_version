import sys

import matplotlib.pyplot as plt
import pandas as pd

csv_file = "../../data/eu868_t1.csv"

df = pd.read_csv(csv_file)
df = df.sort_values("sf")

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(df["sf"], df["final_pdr"], marker="o", linewidth=2)

# valor em cima de cada ponto
for sf, pdr in zip(df["sf"], df["final_pdr"]):
    ax.annotate(f"{pdr:.2f}", (sf, pdr), textcoords="offset points",
                xytext=(0, 8), ha="center", fontsize=9)

ax.set_xlabel("Spreading Factor (SF)")
ax.set_ylabel("PDR (%)")
ax.set_title("PDR por Spreading Factor")
ax.set_xticks(sorted(df["sf"].unique()))
ax.set_ylim(bottom=0)
ax.grid(True, linestyle="--", alpha=0.5)

fig.tight_layout()
fig.savefig("sf_pdr.png", dpi=200)
plt.show()