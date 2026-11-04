import pandas as pd

filename = "eirp_variable_100rep_allreg.csv"

df = pd.read_csv(filename)

# Create the region name based on the frequency
regions = {
    868.30: "EU868",
    433.75: "EU433",
    921.4: "AS915",
    473.3: "CN470"
}

df["region"] = df["freqMHz"].map(regions)

# Calculate the average collision rate (%) for each region and SF
result = (
    df.groupby(["sf", "region"])["collided_rate"]
      .mean()
      .unstack()
      .round(2)
)

print(result)

# Save the result
result.to_csv("average_collision_rate_by_region_by_sf.csv")