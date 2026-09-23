import random
import urllib.request


OUTPUT_FILE = "../data/starlink_100.tle"

N = 100
SEED = 12345

URL = (
    "https://huggingface.co/datasets/"
    "juliensimon/starlink-tle-latest/"
    "resolve/main/data/starlink.tle"
)


# =========================
# DOWNLOAD TLE FILE
# =========================

print("Downloading Starlink TLEs...")

with urllib.request.urlopen(URL) as response:
    content = response.read().decode("utf-8")


# =========================
# PARSE TLE
# =========================

lines = [
    line.strip()
    for line in content.splitlines()
    if line.strip()
]


satellites = []

i = 0

while i + 2 < len(lines):

    name = lines[i]
    line1 = lines[i + 1]
    line2 = lines[i + 2]

    # Check that this is a valid TLE triplet
    if line1.startswith("1 ") and line2.startswith("2 "):
        satellites.append(
            (
                name,
                line1,
                line2
            )
        )

        i += 3

    else:
        i += 1


# =========================
# SELECT 100
# =========================

random.seed(SEED)

selected = random.sample(
    satellites,
    N
)


# =========================
# SAVE
# =========================

with open(OUTPUT_FILE, "w") as f:

    for name, line1, line2 in selected:

        f.write(f"{name}\n")
        f.write(f"{line1}\n")
        f.write(f"{line2}\n")


# =========================
# OUTPUT
# =========================

print(f"Total TLEs available: {len(satellites)}")
print(f"Starlinks selected: {N}")
print(f"Seed: {SEED}")
print(f"TLE file saved: {OUTPUT_FILE}")