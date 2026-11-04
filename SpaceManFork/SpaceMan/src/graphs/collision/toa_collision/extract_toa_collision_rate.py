import pandas as pd

filename = "../eirp_variable_poisson_all_regions.csv"

df = pd.read_csv(filename)

regions = {
    868.30: "EU868",
    433.375: "EU433",
    921.4: "AS915",
    473.3: "CN470"
}

df["region"] = df["freqMHz"].map(regions)

# Calcula a média do collided_rate e do pkt_toa para cada SF e região
result = (
    df.groupby(["sf", "region"])[["collided_rate", "pkt_toa"]]
      .mean()
      .round(2)
)

print(result)

result.to_csv("average_collision_rate_and_toa_by_region_by_sf.csv")