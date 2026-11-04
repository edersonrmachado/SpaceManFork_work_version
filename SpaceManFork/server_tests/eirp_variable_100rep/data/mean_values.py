import pandas as pd

filename="au915_rep100_variableEIRP.csv"

df = pd.read_csv(filename)


result = []

for column in df.columns:
    values = df[column].dropna().unique()

    if len(values) == 1:
        result.append({
            "parameter": column,
            "value": values[0],
            "type": "fixed"
        })
    else:
        result.append({
            "parameter": column,
            "value": df[column].mean(),
            "type": "mean"
        })

result = pd.DataFrame(result)

# Mostrar sempre 2 casas decimais
result["value"] = result["value"].map(lambda x: f"{x:.2f}")

print(result.to_string(index=False))