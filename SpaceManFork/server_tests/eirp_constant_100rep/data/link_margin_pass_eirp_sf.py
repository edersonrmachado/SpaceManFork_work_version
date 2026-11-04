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

# Calculate the average link margin pass rate for each SF, EIRP and region
result = (
    df.groupby(["sf", "eirp_dbm", "region"])["link_margin_pass_rate"]
      .mean()
      .unstack()
      .round(2)
)

print(result)

# Save the result
result.to_csv("average_link_margin_pass_rate_by_region_sf_eirp.csv")