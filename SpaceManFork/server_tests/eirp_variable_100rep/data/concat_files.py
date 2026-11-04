import pandas as pd

output_file="eirp_variable_100rep_allreg.csv"
file1="eu868_rep100_variableEIRP.csv"
file2="eu433_rep100_variableEIRP.csv"
file3="au915_rep100_variableEIRP.csv"
file4="cn470_rep100_variableEIRP.csv"
df_1 = pd.read_csv(file1)
df_2 = pd.read_csv(file2)
df_3 = pd.read_csv(file3)
df_4 = pd.read_csv(file4)

df = pd.concat([df_1, df_2, df_3, df_4], ignore_index=True)

df.to_csv(output_file, index=False)