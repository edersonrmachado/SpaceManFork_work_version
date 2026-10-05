import pandas as pd
import matplotlib.pyplot as plt


filename="../../data/eirp868_12_30_gt0.csv"  



import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# 1. CARREGAR O ARQUIVO
# ============================================================



df = pd.read_csv(filename)


# ============================================================
# 2. GARANTIR QUE AS COLUNAS NUMÉRICAS ESTÃO COMO NÚMEROS
# ============================================================

df["sf"] = pd.to_numeric(df["sf"], errors="coerce")
df["eirp_dbm"] = pd.to_numeric(df["eirp_dbm"], errors="coerce")
df["final_pdr"] = pd.to_numeric(df["final_pdr"], errors="coerce")




# ============================================================
# 4. CALCULAR A MÉDIA DO PDR
#
# Para cada combinação:
#     EIRP + SF
#
# serão usadas TODAS as linhas existentes no arquivo.
# ============================================================

media = (
    df.groupby( ["eirp_dbm", "sf"], as_index=False)["final_pdr"].mean()
    

)

# ============================================================
# 5. ORDENAR OS DADOS
#
# Primeiro por SF e depois por EIRP.
# Isso garante que a linha seja desenhada corretamente.
# ============================================================

media = media.sort_values(
    ["sf", "eirp_dbm"]
)


# ============================================================
# 6. MOSTRAR NA TELA OS VALORES MÉDIOS CALCULADOS
# ============================================================

print("\nMédias de PDR por EIRP e SF:\n")

print(media.to_string(index=False))


# ============================================================
# 7. CRIAR O GRÁFICO
# ============================================================

plt.figure(figsize=(10, 6))


# ------------------------------------------------------------
# Cada SF será uma linha diferente
# ------------------------------------------------------------

for sf, dados_sf in media.groupby("sf"):

    # Garantir ordem crescente de EIRP
    dados_sf = dados_sf.sort_values("eirp_dbm")

    plt.plot(
        dados_sf["eirp_dbm"],       # eixo X
        dados_sf["final_pdr"],      # eixo Y

        marker="o",                 # mostra os pontos
        linestyle="-",              # LINHA CONTÍNUA
        linewidth=2,

        label=f"SF {int(sf)}"
    )


# ============================================================
# 8. CONFIGURAÇÕES DO GRÁFICO
# ============================================================

plt.xlabel("EIRP (dBm)")
plt.ylabel("PDR médio")

plt.title(
    "PDR médio em função do EIRP para cada SF"
)

plt.grid(
    True,
    alpha=0.3
)

plt.legend(
    title="Spreading Factor"
)

plt.tight_layout()


# ============================================================
# 9. MOSTRAR O GRÁFICO
# ============================================================

plt.show()