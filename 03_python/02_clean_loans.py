import pandas as pd
from pathlib import Path

# File paths
RAW_FILE = Path("01_data/01_raw/accepted_2007_to_2018Q4.csv.gz")
OUTPUT_FILE = Path("01_data/02_processed/loans_cleaned.csv")

print("Loading required LendingClub columns...")

# Columns required for our analysis
required_columns = [
    "id",
    "issue_d",
    "loan_amnt",
    "funded_amnt",
    "term",
    "int_rate",
    "installment",
    "grade",
    "sub_grade",
    "emp_length",
    "home_ownership",
    "annual_inc",
    "verification_status",
    "dti",
    "delinq_2yrs",
    "fico_range_low",
    "fico_range_high",
    "open_acc",
    "pub_rec",
    "revol_bal",
    "revol_util",
    "total_acc",
    "loan_status",
    "last_pymnt_d",
    "total_pymnt",
    "recoveries"
]

# Read only required columns
df = pd.read_csv(
    RAW_FILE,
    compression="gzip",
    usecols=required_columns,
    low_memory=False
)

print(f"Original rows loaded: {len(df):,}")

# Remove duplicate loan IDs
df = df.drop_duplicates(subset="id")

# Convert dates
df["issue_d"] = pd.to_datetime(
    df["issue_d"],
    format="%b-%Y",
    errors="coerce"
)

df["last_pymnt_d"] = pd.to_datetime(
    df["last_pymnt_d"],
    format="%b-%Y",
    errors="coerce"
)

# Clean percentage fields
df["int_rate"] = (
    df["int_rate"]
    .astype(str)
    .str.replace("%", "", regex=False)
    .astype(float)
)

df["revol_util"] = (
    df["revol_util"]
    .astype(str)
    .str.replace("%", "", regex=False)
)

df["revol_util"] = pd.to_numeric(
    df["revol_util"],
    errors="coerce"
)

# Clean term
df["term"] = (
    df["term"]
    .astype(str)
    .str.extract(r"(\d+)")[0]
)

df["term"] = pd.to_numeric(
    df["term"],
    errors="coerce"
)

# Clean employment length
df["emp_length"] = (
    df["emp_length"]
    .astype(str)
    .str.replace("< 1 year", "0", regex=False)
    .str.replace("10+ years", "10", regex=False)
    .str.replace(" years", "", regex=False)
    .str.replace(" year", "", regex=False)
)

df["emp_length"] = pd.to_numeric(
    df["emp_length"],
    errors="coerce"
)

# Average FICO score
df["fico_avg"] = (
    df["fico_range_low"] +
    df["fico_range_high"]
) / 2

# Create loan outcome groups
df["risk_outcome"] = "Other"

df.loc[
    df["loan_status"] == "Fully Paid",
    "risk_outcome"
] = "Good"

df.loc[
    df["loan_status"].isin(["Charged Off", "Default"]),
    "risk_outcome"
] = "Bad"

df.loc[
    df["loan_status"].isin([
        "Late (16-30 days)",
        "Late (31-120 days)",
        "In Grace Period"
    ]),
    "risk_outcome"
] = "At Risk"

df.loc[
    df["loan_status"] == "Current",
    "risk_outcome"
] = "Current"

# Bad outcome flag
df["bad_loan_flag"] = (
    df["risk_outcome"] == "Bad"
).astype(int)

# At-risk flag
df["at_risk_flag"] = (
    df["risk_outcome"] == "At Risk"
).astype(int)

# Create vintage fields
df["issue_year"] = df["issue_d"].dt.year
df["issue_month"] = df["issue_d"].dt.month
df["issue_quarter"] = df["issue_d"].dt.to_period("Q").astype(str)

# Sort data
df = df.sort_values("issue_d")

# Create output folder if needed
OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

# Save cleaned dataset
df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n--- CLEANING SUMMARY ---")
print(f"Final rows: {len(df):,}")
print(f"Final columns: {len(df.columns)}")

print("\n--- RISK OUTCOME ---")
print(df["risk_outcome"].value_counts(dropna=False))

print("\n--- BAD LOAN RATE ---")
print(
    f"{df['bad_loan_flag'].mean() * 100:.2f}%"
)

print("\n--- MISSING VALUES ---")
print(
    df.isna()
      .sum()
      .sort_values(ascending=False)
      .head(15)
)

print("\nCleaned dataset saved successfully:")
print(OUTPUT_FILE)