import pandas as pd
import matplotlib.pyplot as plt

filename = "../../data/eu868_initial.csv"

df = pd.read_csv(filename)

df = df.map(
    lambda x: str(x).replace("**", "")
    if isinstance(x, str) else x
)

columns = [
    "sf",
    "collided_rate",
    "non_visibility_rate",
    "link_margin_failed_rate",
    "doppler_failed_rate",
    "final_pdr"
]

for col in columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.sort_values("sf")

fig, ax = plt.subplots(figsize=(10, 6))

ax.barh(
    [f"SF {int(sf)}" for sf in df["sf"]],
    df["final_pdr"]
)

ax.set_xlabel("Final PDR")
ax.set_ylabel("Spreading Factor")

ax.set_title(
    "Final PDR by Spreading Factor"
)

ax.grid(
    True,
    axis="x",
    alpha=0.3
)

plt.tight_layout()
plt.show()