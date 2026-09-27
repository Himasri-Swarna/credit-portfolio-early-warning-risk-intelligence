import pandas as pd
from pathlib import Path

# =========================================================
# Credit Portfolio Early-Warning & Risk Intelligence
# Build Portfolio-Level Executive Summary
# =========================================================

INPUT_FILE = Path(
    "01_data/02_processed/fact_loans.csv"
)

OUTPUT_FILE = Path(
    "07_outputs/summary_tables/portfolio_summary.csv"
)

CHUNK_SIZE = 100_000

USE_COLS = [
    "loan_amnt",
    "funded_amnt",
    "exposure_amount",
    "int_rate",
    "dti",
    "fico_avg",
    "bad_loan_flag",
    "adverse_outcome_flag",
    "recoveries",
    "recovery_rate",
    "risk_segment"
]

print("Starting portfolio-level aggregation...")

partial_results = []

for chunk_number, chunk in enumerate(
    pd.read_csv(
        INPUT_FILE,
        usecols=USE_COLS,
        chunksize=CHUNK_SIZE,
        low_memory=False
    ),
    start=1
):

    print(f"Processing chunk {chunk_number}...")

    grouped = pd.DataFrame({
        "loan_count": [len(chunk)],
        "total_loan_amount": [chunk["loan_amnt"].sum()],
        "funded_amount": [chunk["funded_amnt"].sum()],
        "exposure": [chunk["exposure_amount"].sum()],
        "total_recoveries": [chunk["recoveries"].sum()],
        "bad_loans": [chunk["bad_loan_flag"].sum()],
        "adverse_loans": [chunk["adverse_outcome_flag"].sum()]
    })

    partial_results.append(grouped)


print("\nCombining chunk results...")

combined = pd.concat(
    partial_results,
    ignore_index=True
)

# =========================================================
# Combine totals
# =========================================================

total_loan_count = combined["loan_count"].sum()
total_loan_amount = combined["total_loan_amount"].sum()
total_funded_amount = combined["funded_amount"].sum()
total_exposure = combined["exposure"].sum()
total_recoveries = combined["total_recoveries"].sum()
total_bad_loans = combined["bad_loans"].sum()
total_adverse_loans = combined["adverse_loans"].sum()

# =========================================================
# Calculate portfolio KPIs
# =========================================================

summary = pd.DataFrame({
    "metric": [
        "Total Loans",
        "Total Loan Amount",
        "Total Funded Amount",
        "Total Exposure",
        "Total Recoveries",
        "Bad Loans",
        "Adverse Outcome Loans",
        "Bad Loan Rate %",
        "Adverse Outcome Rate %",
        "Portfolio Recovery %",
    ],

    "value": [
        total_loan_count,
        total_loan_amount,
        total_funded_amount,
        total_exposure,
        total_recoveries,
        total_bad_loans,
        total_adverse_loans,

        100 * total_bad_loans / total_loan_count,

        100 * total_adverse_loans / total_loan_count,

        100 * total_recoveries / total_exposure
        if total_exposure != 0 else 0
    ]
})

# =========================================================
# Round values
# =========================================================

summary["value"] = summary["value"].round(2)

# =========================================================
# Save result
# =========================================================

summary.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n========================================")
print("PORTFOLIO SUMMARY CREATED SUCCESSFULLY")
print("========================================")

print(f"Output: {OUTPUT_FILE}")

print("\nPortfolio KPIs:")
print(summary.to_string(index=False))