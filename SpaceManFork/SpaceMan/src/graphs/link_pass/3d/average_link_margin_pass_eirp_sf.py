import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator
from matplotlib.lines import Line2D

# Set global font configuration
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'

# Input file
filename = "../eirp_variable_poisson_all_regions.csv"

# Output files for figures
fig_name_pdf = "link_pass_rate_vs_eirp.pdf"
fig_name_eps = "link_pass_rate_vs_eirp.eps"
fig_name_svg = "link_pass_rate_vs_eirp.svg"
csv_output = "average_link_margin_pass_rate_by_region_sf_eirp.csv"

# Load dataset
df = pd.read_csv(filename)

# Create region name based on frequency
regions = {
    868.30: "EU868",
    433.375:"EU433",
    921.4: "AS915",
    473.3: "CN470"
}

df["region"] = df["freqMHz"].map(regions)

# Calculate and save the aggregated matrix/CSV
result = (
    df.groupby(["sf", "eirp_dbm", "region"])["link_margin_pass_rate"]
      .mean()
      .unstack()
      .round(2)
)

print("Table:")
print(result)

# Save file
result.to_csv(csv_output)
