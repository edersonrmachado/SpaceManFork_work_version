import pandas as pd

# 1. Carrega o CSV em um DataFrame
df = pd.read_csv("eu868_eirp_variable_initial_same.csv")

# Defina a quantidade de linhas que deseja remover para cada SF
x = 15  # Exemplo: apagar 2 linhas onde sf = 10
y = 25  # Exemplo: apagar 3 linhas onde sf = 11
z = 23  # Exemplo: apagar 5 linhas onde sf = 12

# 2. Seleciona os índices das primeiras N linhas de cada SF 
# (Use .head(n) para as primeiras, ou .sample(n) se quiser aleatórias)
indices_sf10 = df[df['sf'] == 10].head(x).index
indices_sf11 = df[df['sf'] == 11].head(y).index
indices_sf12 = df[df['sf'] == 12].head(z).index

# Junta todos os índices que devem ser apagados
indices_para_apagar = indices_sf10.union(indices_sf11).union(indices_sf12)

# 3. Remove as linhas do DataFrame
df_filtrado = df.drop(indices_para_apagar)

# (Opcional) Salva o resultado em um novo arquivo CSV
df_filtrado.to_csv('arquivo_atualizado.csv', index=False)

print(f"Total de linhas restantes: {len(df_filtrado)}")