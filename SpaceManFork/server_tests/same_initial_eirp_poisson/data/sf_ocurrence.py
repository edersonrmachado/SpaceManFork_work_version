import pandas as pd


filename="eirp_variable_initial_same_all_regs.csv"
filename="cn470_eirp_variable_initial_same.csv"
#filename="arquivo_atualizado.csv"
df = pd.read_csv(filename)
# Conta as ocorrências para cada valor de num_sats
sf7   = (df['sf'] == 7).sum()
sf8   = (df['sf'] == 8).sum()
sf9   = (df['sf'] == 9).sum()
sf10   = (df['sf'] == 10).sum()
sf11   = (df['sf'] == 11).sum()
sf12  = (df['sf'] == 12).sum()

# Exibe os prints para cada um


print(f"num of sf 7: {sf7}")
print(f"num of sf 8:{sf8}")
print(f"num of sf 9:{sf9}")
print(f"num of sf 10:{sf10}")
print(f"num of sf 11:{sf11}")
print(f"num of sf 12:{sf12}")




# 2. Filtra os SFs 10, 11 e 12, agrupa por SF e EIRP, e conta as ocorrências
resultado = df[df['sf'].isin([7,8,9,10, 11, 12])].groupby(['sf', 'eirp_dbm']).size().reset_index(name='occurrences')

# 3. Ordena para ficar organizado e exibe
print(resultado.sort_values(by='sf'))    



