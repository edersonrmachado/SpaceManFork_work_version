import pandas as pd

filename="cn470_visibility_variable_sf12.csv"
filename="visible_variable_all_regions.csv"
df = pd.read_csv(filename)
# Conta as ocorrências para cada valor de num_sats
sats_5   = (df['num_sats'] == 5).sum()
sats_25  = (df['num_sats'] == 25).sum()
sats_50  = (df['num_sats'] == 50).sum()
sats_75  = (df['num_sats'] == 75).sum()
sats_100 = (df['num_sats'] == 100).sum()
sats_125 = (df['num_sats'] == 125).sum()
sats_150 = (df['num_sats'] == 150).sum()

# Exibe os prints para cada um
print(f"num of 5 sats: {sats_5}")
print(f"num of 25 sats: {sats_25}")
print(f"num of 50 sats: {sats_50}")
print(f"num of 75 sats: {sats_75}")
print(f"num of 100 sats: {sats_100}")
print(f"num of 125 sats: {sats_125}")
print(f"num of 150 sats: {sats_150}")