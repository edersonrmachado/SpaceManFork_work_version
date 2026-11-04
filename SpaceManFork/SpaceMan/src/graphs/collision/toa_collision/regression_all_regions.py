import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import linregress

# Carregar o arquivo gerado anteriormente
filename = "average_collision_rate_and_toa_by_region_by_sf.csv"
df = pd.read_csv(filename)

# Obter a lista de regiões únicas
regions = df["region"].unique()

plt.figure(figsize=(10, 6))

for region in regions:
  df_region = df[df["region"] == region].dropna(
      subset=["pkt_toa", "collided_rate"]
  )

  if len(df_region) < 2:
    continue

  x = df_region["pkt_toa"]
  y = df_region["collided_rate"]

  # Realizar a regressão linear (y = ax + b) para cada região
  slope, intercept, r_value, p_value, std_err = linregress(x, y)
  r_squared = r_value**2

  print(f"=== Região: {region} ===")
  print(f"Equação da reta: y = {slope:.4f}x + {intercept:.4f}")
  print(f"Coeficiente de determinação (R^2): {r_squared:.4f}")
  print(f"Intercepto (b): {intercept:.4f}")

  if r_squared > 0.98 and abs(intercept) < (0.05 * np.mean(y)):
    print(
        f"Resultado ({region}): As grandezas são diretamente proporcionais.\n"
    )
  else:
    print(
        f"Resultado ({region}): NÃO atendem estritamente aos critérios.\n"
    )

  # Plotar dispersão e linha de tendência para a região
  plt.scatter(x, y, label=f"{region} (Dados)")
  x_line = np.linspace(x.min(), x.max(), 100)
  plt.plot(
      x_line,
      slope * x_line + intercept,
      linestyle="--",
      label=f"{region} (Fit: y={slope:.2f}x+{intercept:.2f})",
  )

plt.xlabel("Packet Time on Air (pkt_toa)")
plt.ylabel("Collision Rate (%)")
plt.title("Análise de Proporcionalidade por Região")
plt.legend()
plt.grid(True, linestyle=":", alpha=0.6)
plt.show()