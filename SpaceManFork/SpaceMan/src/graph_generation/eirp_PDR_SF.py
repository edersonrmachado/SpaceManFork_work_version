import pandas as pd
import matplotlib.pyplot as plt


# Arquivo CSV de entrada
csv_file = "../../data/eu868_second_eirp16_30_gt0.csv"


# Ler CSV
df = pd.read_csv(csv_file)


# Corrigir nomes caso existam colunas com **
df.columns = df.columns.str.replace("**", "", regex=False)


# Garantir que os campos são numéricos
df["sf"] = pd.to_numeric(df["sf"])
df["eirp_dbm"] = pd.to_numeric(df["eirp_dbm"])
df["final_pdr"] = pd.to_numeric(df["final_pdr"])


# Ordenar
df = df.sort_values(["sf", "eirp_dbm"])


# Criar gráfico
plt.figure(figsize=(10, 6))


# Uma curva para cada SF
for sf, group in df.groupby("sf"):

    plt.plot(
        group["eirp_dbm"],
        group["final_pdr"],  
        marker="o",
        linewidth=2,
        label=f"SF{int(sf)}"
    )


# Configuração do gráfico
plt.xlabel("EIRP (dBm)")
plt.ylabel("PDR (%)")

plt.title("LoRaWAN - PDR x EIRP")

plt.grid(True)

plt.ylim(0, 100)

plt.legend(title="Spreading Factor")

plt.tight_layout()


# Salvar imagem
plt.savefig(
    "eirp_vs_pdr.png",
    dpi=300,
    bbox_inches="tight"
)


plt.show()