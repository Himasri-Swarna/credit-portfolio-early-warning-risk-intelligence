import pandas as pd
from pathlib import Path

# File paths
INPUT_FILE = Path("01_data/02_processed/fact_loans.csv")
OUTPUT_DIR = Path("01_data/02_processed")

print("Loading fact loans...")

df = pd.read_csv(INPUT_FILE)

# =========================================================
# 1. DATE DIMENSION
# =========================================================

print("\nCreating dim_date...")

df["issue_d"] = pd.to_datetime(
    df["issue_d"],
    errors="coerce"
)

# Get unique loan issue dates
dates = (
    df["issue_d"]
    .dropna()
    .drop_duplicates()
    .sort_values()
)

dim_date = pd.DataFrame({
    "date": dates
})

dim_date["date_key"] = (
    dim_date["date"].dt.year * 10000
    + dim_date["date"].dt.month * 100
    + dim_date["date"].dt.day
)

dim_date["year"] = dim_date["date"].dt.year
dim_date["month"] = dim_date["date"].dt.month
dim_date["month_name"] = dim_date["date"].dt.month_name()
dim_date["quarter"] = "Q" + dim_date["date"].dt.quarter.astype(str)
dim_date["year_month"] = (
    dim_date["date"].dt.to_period("M").astype(str)
)

dim_date = dim_date[
    [
        "date_key",
        "date",
        "year",
        "month",
        "month_name",
        "quarter",
        "year_month"
    ]
]

# Save date dimension
dim_date.to_csv(
    OUTPUT_DIR / "dim_date.csv",
    index=False
)

print(f"dim_date rows: {len(dim_date):,}")


# =========================================================
# 2. BORROWER / RISK SEGMENT DIMENSION
# =========================================================

print("\nCreating dim_borrower_segment...")

segment_columns = [
    "risk_segment",
    "fico_band",
    "dti_band",
    "income_band"
]

dim_borrower_segment = (
    df[segment_columns]
    .drop_duplicates()
    .reset_index(drop=True)
)

# Create surrogate segment ID
dim_borrower_segment.insert(
    0,
    "segment_id",
    range(
        1,
        len(dim_borrower_segment) + 1
    )
)

# Save dimension
dim_borrower_segment.to_csv(
    OUTPUT_DIR / "dim_borrower_segment.csv",
    index=False
)

print(
    f"dim_borrower_segment rows: "
    f"{len(dim_borrower_segment):,}"
)


# =========================================================
# 3. VALIDATION
# =========================================================

print("\n--- DIMENSION VALIDATION ---")

print("\nDate dimension:")
print(dim_date.head())

print("\nBorrower segment dimension:")
print(dim_borrower_segment.head())

print("\nUnique risk segments:")
print(
    dim_borrower_segment["risk_segment"]
    .value_counts(dropna=False)
)

print("\nDimension tables created successfully.")