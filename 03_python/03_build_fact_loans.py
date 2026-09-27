import pandas as pd
from pathlib import Path

INPUT_FILE = Path("01_data/02_processed/loans_cleaned.csv")
OUTPUT_FILE = Path("01_data/02_processed/fact_loans.csv")

print("Loading cleaned loan data...")

df = pd.read_csv(INPUT_FILE)

# --------------------------------------------------
# 1. Loan exposure
# --------------------------------------------------

df["exposure_amount"] = df["funded_amnt"]

# --------------------------------------------------
# 2. Average monthly installment burden
# --------------------------------------------------

df["annual_installment"] = df["installment"] * 12

# --------------------------------------------------
# 3. Income-to-loan relationship
# --------------------------------------------------

df["loan_to_income_ratio"] = (
    df["loan_amnt"] / df["annual_inc"].replace(0, pd.NA)
)

# --------------------------------------------------
# 4. Risk segmentation
# --------------------------------------------------

def assign_risk_segment(row):

    if row["risk_outcome"] == "Bad":
        return "High Risk"

    if row["risk_outcome"] == "At Risk":
        return "Elevated Risk"

    if pd.notna(row["fico_avg"]) and row["fico_avg"] < 670:
        return "Higher Risk"

    if pd.notna(row["dti"]) and row["dti"] > 25:
        return "Higher Risk"

    if row["risk_outcome"] == "Good":
        return "Lower Risk"

    if row["risk_outcome"] == "Current":
        return "Current"

    return "Other"


df["risk_segment"] = df.apply(
    assign_risk_segment,
    axis=1
)

# --------------------------------------------------
# 5. DTI bands
# --------------------------------------------------

df["dti_band"] = pd.cut(
    df["dti"],
    bins=[-float("inf"), 10, 20, 30, 40, float("inf")],
    labels=[
        "<=10",
        "10-20",
        "20-30",
        "30-40",
        "40+"
    ]
)

# --------------------------------------------------
# 6. FICO bands
# --------------------------------------------------

df["fico_band"] = pd.cut(
    df["fico_avg"],
    bins=[
        -float("inf"),
        579,
        669,
        739,
        799,
        float("inf")
    ],
    labels=[
        "<580",
        "580-669",
        "670-739",
        "740-799",
        "800+"
    ]
)

# --------------------------------------------------
# 7. Income bands
# --------------------------------------------------

df["income_band"] = pd.cut(
    df["annual_inc"],
    bins=[
        -float("inf"),
        30000,
        60000,
        100000,
        150000,
        float("inf")
    ],
    labels=[
        "<30K",
        "30K-60K",
        "60K-100K",
        "100K-150K",
        "150K+"
    ]
)

# --------------------------------------------------
# 8. Recovery metrics
# --------------------------------------------------

df["recovery_rate"] = (
    df["recoveries"] /
    df["funded_amnt"].replace(0, pd.NA)
)

# Recovery rate should not exceed 100%
df["recovery_rate"] = df["recovery_rate"].clip(
    lower=0,
    upper=1
)

# --------------------------------------------------
# 9. Net loss proxy for bad loans
# --------------------------------------------------

df["net_loss_proxy"] = (
    df["funded_amnt"] - df["recoveries"]
)

# Only interpret this as a simple analytical proxy,
# not an accounting loss.
df.loc[
    df["bad_loan_flag"] == 0,
    "net_loss_proxy"
] = 0

# --------------------------------------------------
# 10. Loan outcome category
# --------------------------------------------------

df["adverse_outcome_flag"] = (
    df["risk_outcome"].isin(
        ["Bad", "At Risk"]
    )
).astype(int)

# --------------------------------------------------
# 11. Select useful analytical columns
# --------------------------------------------------

fact_columns = [
    "id",
    "issue_d",
    "issue_year",
    "issue_month",
    "issue_quarter",
    "loan_amnt",
    "funded_amnt",
    "exposure_amount",
    "term",
    "int_rate",
    "installment",
    "annual_installment",
    "grade",
    "sub_grade",
    "emp_length",
    "home_ownership",
    "annual_inc",
    "income_band",
    "verification_status",
    "dti",
    "dti_band",
    "delinq_2yrs",
    "fico_range_low",
    "fico_range_high",
    "fico_avg",
    "fico_band",
    "open_acc",
    "pub_rec",
    "revol_bal",
    "revol_util",
    "total_acc",
    "loan_status",
    "risk_outcome",
    "risk_segment",
    "bad_loan_flag",
    "at_risk_flag",
    "adverse_outcome_flag",
    "last_pymnt_d",
    "total_pymnt",
    "recoveries",
    "recovery_rate",
    "net_loss_proxy",
    "loan_to_income_ratio"
]

df = df[fact_columns]

# --------------------------------------------------
# 12. Save analytical fact table
# --------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

# --------------------------------------------------
# 13. Validation
# --------------------------------------------------

print("\n--- FACT TABLE SUMMARY ---")

print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")

print("\n--- RISK SEGMENTS ---")
print(
    df["risk_segment"]
    .value_counts(dropna=False)
)

print("\n--- ADVERSE OUTCOME RATE ---")
print(
    f"{df['adverse_outcome_flag'].mean() * 100:.2f}%"
)

print("\n--- EXPOSURE ---")
print(
    f"${df['exposure_amount'].sum():,.2f}"
)

print("\n--- FACT TABLE MISSING VALUES ---")
print(
    df.isna()
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

print("\nFact table saved successfully:")
print(OUTPUT_FILE)