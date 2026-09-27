import pandas as pd
from pathlib import Path

BASE = Path("01_data/02_processed")

FACT_FILE = BASE / "fact_loans.csv"
DATE_FILE = BASE / "dim_date.csv"
SEGMENT_FILE = BASE / "dim_borrower_segment.csv"
OUTPUT_FILE = BASE / "fact_loans.csv"

print("Loading tables...")

fact = pd.read_csv(FACT_FILE)
dim_date = pd.read_csv(DATE_FILE)
dim_segment = pd.read_csv(SEGMENT_FILE)

# --------------------------------------------------
# 1. Prepare dates
# --------------------------------------------------

fact["issue_d"] = pd.to_datetime(
    fact["issue_d"],
    errors="coerce"
)

dim_date["date"] = pd.to_datetime(
    dim_date["date"],
    errors="coerce"
)

# --------------------------------------------------
# 2. Add date_key to fact table
# --------------------------------------------------

fact["date_key"] = (
    fact["issue_d"].dt.year * 10000
    + fact["issue_d"].dt.month * 100
    + fact["issue_d"].dt.day
)

# --------------------------------------------------
# 3. Create segment key
# --------------------------------------------------

segment_columns = [
    "risk_segment",
    "fico_band",
    "dti_band",
    "income_band"
]

fact = fact.merge(
    dim_segment[
        segment_columns + ["segment_id"]
    ],
    on=segment_columns,
    how="left"
)

# --------------------------------------------------
# 4. Validation
# --------------------------------------------------

print("\n--- LINK VALIDATION ---")

print(f"Fact rows: {len(fact):,}")

print(
    f"Missing date keys: "
    f"{fact['date_key'].isna().sum():,}"
)

print(
    f"Missing segment IDs: "
    f"{fact['segment_id'].isna().sum():,}"
)

print(
    f"Unique date keys: "
    f"{fact['date_key'].nunique():,}"
)

print(
    f"Unique segment IDs: "
    f"{fact['segment_id'].nunique():,}"
)

# --------------------------------------------------
# 5. Save updated fact table
# --------------------------------------------------

fact.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nFact table successfully linked to dimensions.")
print(OUTPUT_FILE)