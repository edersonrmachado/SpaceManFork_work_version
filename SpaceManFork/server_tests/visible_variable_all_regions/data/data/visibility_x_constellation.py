import pandas as pd

filename="visible_variable_all_regions.csv"
df = pd.read_csv(filename)


# Create the region name based on the frequency
regions = {
    868.30: "EU868",
    433.375: "EU433",
    921.4: "AS915",
    473.3: "CN470"
}

df["region"] = df["freqMHz"].map(regions)

# Calculate the average collision rate (%) for each region and SF
result = (
    df.groupby(["num_sats", "region"])["visibility_rate"]
      .mean()
      .unstack()
      .round(2)
)

print(result)

# Save the result
result.to_csv("visibility_x_constellation.csv")