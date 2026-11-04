import matplotlib.pyplot as plt
import pandas as pd

# 1. Carrega os dados salvos no CSV
df_result = pd.read_csv("visibility_x_constellation.csv", index_col="num_sats")


# fig names
fig_1='visibility.pdf'

# plots - customized style
fig_facecolor='#FFFFFF'
dpi_set=600
fig_width=3.5 
fig_height=2.2 
fontsize_xticks=10 
fontsize_labels=11
fontsize_text=9 
fontsize_text2=11
dop_shift_color='black'
dop_rate_color='darkgreen'

# text 
fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=dpi_set, facecolor=fig_facecolor)

# 2. Plota diretamente como gráfico de barras agrupadas usando o Pandas
# O Pandas já cria as barras lado a lado para cada 'num_sats' e cada 'region'
ax = df_result.plot(kind="bar", figsize=(10, 6), width=0.8, edgecolor="black")

# 3. Personalização dos títulos, eixos e grade
plt.title(
    "Visibilidade Média de Satélites por Região (Gráfico de Barras)",
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("Número de Satélites (num_sats)", fontsize=12)
plt.ylabel("Visibilidade Média (%)", fontsize=12)

# Ajusta a rotação do eixo X para os números ficarem retos
plt.xticks(rotation=0)
plt.yticks(range(0, 101, 10))  # Eixo Y de 0% a 100%

# Adiciona legenda e grade de apoio apenas no eixo Y
plt.legend(title="Região", fontsize=10, loc="lower right")
plt.grid(axis="y", linestyle="--", alpha=0.6)

# 4. Exibe o gráfico
plt.tight_layout()
plt.show()