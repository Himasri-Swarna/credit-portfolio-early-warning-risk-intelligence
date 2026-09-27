import pandas as pd
from pathlib import Path

# =========================================================
# Credit Portfolio Early-Warning & Risk Intelligence
# Build Independent Borrower Segment Risk Summary
# =========================================================

INPUT_FILE = Path(
    "01_data/02_processed/fact_loans.csv"
)

OUTPUT_FILE = Path(
    "01_data/02_processed/segment_risk_summary.csv"
)

CHUNK_SIZE = 100_000

# IMPORTANT:
# Do NOT use risk_segment here because risk_segment
# was created partly from loan outcomes.
#
# We use borrower characteristics that are independent
# of the outcome:
#   - FICO band
#   - DTI band
#   - Income band

USE_COLS = [
    "fico_band",
    "dti_band",
    "income_band",
    "loan_amnt",
    "exposure_amount",
    "adverse_outcome_flag"
]

print("Starting independent borrower segment aggregation...")

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

    # Remove rows without usable segment characteristics
    chunk = chunk.dropna(
        subset=[
            "fico_band",
            "dti_band",
            "income_band"
        ]
    )

    # Aggregate within each chunk
    grouped = (
        chunk
        .groupby(
            [
                "fico_band",
                "dti_band",
                "income_band"
            ],
            as_index=False
        )
        .agg(
            loan_count=("loan_amnt", "size"),
            exposure=("exposure_amount", "sum"),
            total_loan_amount=("loan_amnt", "sum"),
            adverse_loans=("adverse_outcome_flag", "sum")
        )
    )

    partial_results.append(grouped)


print("\nCombining chunk results...")

combined = pd.concat(
    partial_results,
    ignore_index=True
)

# Combine results from all chunks
summary = (
    combined
    .groupby(
        [
            "fico_band",
            "dti_band",
            "income_band"
        ],
        as_index=False
    )
    .agg(
        loan_count=("loan_count", "sum"),
        exposure=("exposure", "sum"),
        total_loan_amount=("total_loan_amount", "sum"),
        adverse_loans=("adverse_loans", "sum")
    )
)

# Average loan amount
summary["avg_loan_amount"] = (
    summary["total_loan_amount"]
    / summary["loan_count"]
)

# Adverse outcome rate
summary["adverse_outcome_rate_pct"] = (
    100
    * summary["adverse_loans"]
    / summary["loan_count"]
)

# Round metrics
summary["exposure"] = summary["exposure"].round(2)

summary["total_loan_amount"] = (
    summary["total_loan_amount"].round(2)
)

summary["avg_loan_amount"] = (
    summary["avg_loan_amount"].round(2)
)

summary["adverse_outcome_rate_pct"] = (
    summary["adverse_outcome_rate_pct"].round(2)
)

# Keep sufficiently large segments
summary = summary[
    summary["loan_count"] >= 100
].copy()

# Sort by adverse rate first,
# exposure second
summary = summary.sort_values(
    by=[
        "adverse_outcome_rate_pct",
        "exposure"
    ],
    ascending=[
        False,
        False
    ]
)

# Save
summary.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n========================================")
print("Independent segment summary created")
print("========================================")

print(f"Rows: {len(summary):,}")

print(f"Output: {OUTPUT_FILE}")

print("\nTop 10 independent borrower segments:")

print(
    summary.head(10).to_string(
        index=False
    )
)