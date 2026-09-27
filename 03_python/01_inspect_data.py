import pandas as pd
from pathlib import Path

# File locations
raw_file = Path("01_data/01_raw/accepted_2007_to_2018Q4.csv.gz")

print("Inspecting LendingClub dataset...")
print(f"File: {raw_file}")

# Read first chunk to inspect structure
first_chunk = pd.read_csv(
    raw_file,
    compression="gzip",
    nrows=100_000,
    low_memory=False
)

print("\n--- COLUMNS ---")
print(first_chunk.columns.tolist())

print("\n--- SAMPLE ROWS ---")
print(first_chunk.head())

print("\n--- DATA TYPES ---")
print(first_chunk.dtypes)

# Full dataset inspection using chunks
chunk_size = 100_000
total_rows = 0
missing_counts = None
loan_status_counts = {}

for chunk in pd.read_csv(
    raw_file,
    compression="gzip",
    chunksize=chunk_size,
    low_memory=False
):
    total_rows += len(chunk)

    current_missing = chunk.isna().sum()

    if missing_counts is None:
        missing_counts = current_missing
    else:
        missing_counts = missing_counts.add(current_missing, fill_value=0)

    if "loan_status" in chunk.columns:
        status_counts = chunk["loan_status"].value_counts(dropna=False)

        for status, count in status_counts.items():
            loan_status_counts[status] = (
                loan_status_counts.get(status, 0) + count
            )

print("\n--- DATASET SIZE ---")
print(f"Total rows: {total_rows}")
print(f"Total columns: {len(first_chunk.columns)}")

print("\n--- TOP MISSING VALUES ---")
print(
    missing_counts
    .sort_values(ascending=False)
    .head(20)
)

print("\n--- LOAN STATUS COUNTS ---")
for status, count in sorted(
    loan_status_counts.items(),
    key=lambda x: x[1],
    reverse=True
):
    print(f"{status}: {count}")

print("\nInspection completed successfully.")