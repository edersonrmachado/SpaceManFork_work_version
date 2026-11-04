import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Concatenate CSV files.")
parser.add_argument("files", nargs="+", help="Input CSV files")
parser.add_argument(
    "-o", "--output",
    default="output.csv",
    help="Output CSV filename (default: output.csv)"
)

args = parser.parse_args()

# Read input files
dfs = [pd.read_csv(file) for file in args.files]

# Define individual DataFrames
df1 = dfs[0]
df2 = dfs[1] if len(dfs) > 1 else None
df3 = dfs[2] if len(dfs) > 2 else None
df4 = dfs[3] if len(dfs) > 3 else None

# Concatenate all DataFrames
df = pd.concat(dfs, ignore_index=True)

# Save the output file
df.to_csv(args.output, index=False)

print(f"Files successfully concatenated into: {args.output}")