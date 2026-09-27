import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# =========================================================
# Credit Portfolio Early-Warning & Risk Intelligence
# Python EDA
# =========================================================

INPUT_FILE = Path(
    "01_data/02_processed/fact_loans.csv"
)

SEGMENT_FILE = Path(
    "01_data/02_processed/segment_risk_summary.csv"
)

CHART_DIR = Path(
    "07_outputs/charts"
)

SUMMARY_DIR = Path(
    "07_outputs/summary_tables"
)

CHART_DIR.mkdir(parents=True, exist_ok=True)
SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

CHUNK_SIZE = 100_000

print("=" * 60)
print("CREDIT PORTFOLIO PYTHON EDA")
print("=" * 60)


# =========================================================
# 1. MONTHLY RISK ANALYSIS
# =========================================================

print("\n1. Building monthly risk summary...")

monthly_parts = []

USE_COLS = [
    "issue_year",
    "issue_month",
    "exposure_amount",
    "adverse_outcome_flag"
]

for chunk in pd.read_csv(
    INPUT_FILE,
    usecols=USE_COLS,
    chunksize=CHUNK_SIZE,
    low_memory=False
):

    chunk = chunk.dropna(
        subset=["issue_year", "issue_month"]
    )

    grouped = (
        chunk
        .groupby(
            ["issue_year", "issue_month"],
            as_index=False
        )
        .agg(
            loan_count=("adverse_outcome_flag", "size"),
            exposure=("exposure_amount", "sum"),
            adverse_loans=("adverse_outcome_flag", "sum")
        )
    )

    monthly_parts.append(grouped)


monthly = pd.concat(
    monthly_parts,
    ignore_index=True
)

monthly = (
    monthly
    .groupby(
        ["issue_year", "issue_month"],
        as_index=False
    )
    .agg(
        loan_count=("loan_count", "sum"),
        exposure=("exposure", "sum"),
        adverse_loans=("adverse_loans", "sum")
    )
)

monthly["adverse_rate_pct"] = (
    100 *
    monthly["adverse_loans"] /
    monthly["loan_count"]
)

monthly["year_month"] = (
    monthly["issue_year"].astype(int).astype(str)
    + "-"
    + monthly["issue_month"].astype(int)
    .astype(str)
    .str.zfill(2)
)

monthly = monthly.sort_values(
    ["issue_year", "issue_month"]
)

monthly.to_csv(
    SUMMARY_DIR / "monthly_risk_summary.csv",
    index=False
)

print(
    f"Monthly summary created: {len(monthly)} rows"
)


# =========================================================
# 2. GRADE-LEVEL RISK
# =========================================================

print("\n2. Building grade-level risk summary...")

grade_parts = []

USE_COLS = [
    "grade",
    "exposure_amount",
    "loan_amnt",
    "bad_loan_flag",
    "adverse_outcome_flag"
]

for chunk in pd.read_csv(
    INPUT_FILE,
    usecols=USE_COLS,
    chunksize=CHUNK_SIZE,
    low_memory=False
):

    chunk = chunk.dropna(subset=["grade"])

    grouped = (
        chunk
        .groupby("grade", as_index=False)
        .agg(
            loan_count=("grade", "size"),
            exposure=("exposure_amount", "sum"),
            avg_loan_amount=("loan_amnt", "mean"),
            bad_loans=("bad_loan_flag", "sum"),
            adverse_loans=("adverse_outcome_flag", "sum")
        )
    )

    grade_parts.append(grouped)


grade = pd.concat(
    grade_parts,
    ignore_index=True
)

grade = (
    grade
    .groupby("grade", as_index=False)
    .agg(
        loan_count=("loan_count", "sum"),
        exposure=("exposure", "sum"),
        avg_loan_amount=("avg_loan_amount", "mean"),
        bad_loans=("bad_loans", "sum"),
        adverse_loans=("adverse_loans", "sum")
    )
)

grade["bad_rate_pct"] = (
    100 *
    grade["bad_loans"] /
    grade["loan_count"]
)

grade["adverse_rate_pct"] = (
    100 *
    grade["adverse_loans"] /
    grade["loan_count"]
)

grade = grade.sort_values("grade")

grade.to_csv(
    SUMMARY_DIR / "grade_risk_summary.csv",
    index=False
)

print("Grade summary created.")


# =========================================================
# 3. LOAN TERM RISK
# =========================================================

print("\n3. Building loan-term summary...")

term_parts = []

USE_COLS = [
    "term",
    "exposure_amount",
    "int_rate",
    "bad_loan_flag",
    "adverse_outcome_flag"
]

for chunk in pd.read_csv(
    INPUT_FILE,
    usecols=USE_COLS,
    chunksize=CHUNK_SIZE,
    low_memory=False
):

    chunk = chunk.dropna(subset=["term"])

    grouped = (
        chunk
        .groupby("term", as_index=False)
        .agg(
            loan_count=("term", "size"),
            exposure=("exposure_amount", "sum"),
            avg_interest_rate=("int_rate", "mean"),
            bad_loans=("bad_loan_flag", "sum"),
            adverse_loans=("adverse_outcome_flag", "sum")
        )
    )

    term_parts.append(grouped)


term = pd.concat(
    term_parts,
    ignore_index=True
)

term = (
    term
    .groupby("term", as_index=False)
    .agg(
        loan_count=("loan_count", "sum"),
        exposure=("exposure", "sum"),
        avg_interest_rate=("avg_interest_rate", "mean"),
        bad_loans=("bad_loans", "sum"),
        adverse_loans=("adverse_loans", "sum")
    )
)

term["bad_rate_pct"] = (
    100 *
    term["bad_loans"] /
    term["loan_count"]
)

term["adverse_rate_pct"] = (
    100 *
    term["adverse_loans"] /
    term["loan_count"]
)

term.to_csv(
    SUMMARY_DIR / "term_risk_summary.csv",
    index=False
)

print("Term summary created.")


# =========================================================
# 4. LOAD INDEPENDENT BORROWER SEGMENT SUMMARY
# =========================================================

print("\n4. Loading borrower segment summary...")

segments = pd.read_csv(
    SEGMENT_FILE
)

segments = segments.sort_values(
    ["adverse_outcome_rate_pct", "exposure"],
    ascending=[False, False]
)

segments.head(20).to_csv(
    SUMMARY_DIR / "top_20_risk_segments.csv",
    index=False
)

print(
    f"Segment summary loaded: {len(segments)} segments"
)


# =========================================================
# 5. CHART 1 — MONTHLY ADVERSE OUTCOME RATE
# =========================================================

print("\n5. Creating monthly risk chart...")

plt.figure(figsize=(12, 6))

plt.plot(
    monthly["year_month"],
    monthly["adverse_rate_pct"]
)

plt.title(
    "Monthly Adverse Outcome Rate"
)

plt.xlabel("Origination Month")
plt.ylabel("Adverse Outcome Rate (%)")

plt.xticks(
    monthly["year_month"][::12],
    rotation=45
)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "01_monthly_adverse_rate.png",
    dpi=150
)

plt.close()


# =========================================================
# 6. CHART 2 — RISK BY GRADE
# =========================================================

print("Creating grade risk chart...")

plt.figure(figsize=(10, 6))

plt.bar(
    grade["grade"],
    grade["adverse_rate_pct"]
)

plt.title(
    "Adverse Outcome Rate by Loan Grade"
)

plt.xlabel("Loan Grade")
plt.ylabel("Adverse Outcome Rate (%)")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "02_grade_adverse_rate.png",
    dpi=150
)

plt.close()


# =========================================================
# 7. CHART 3 — LOAN TERM RISK
# =========================================================

print("Creating term risk chart...")

plt.figure(figsize=(8, 6))

plt.bar(
    term["term"].astype(str),
    term["adverse_rate_pct"]
)

plt.title(
    "Adverse Outcome Rate by Loan Term"
)

plt.xlabel("Loan Term (Months)")
plt.ylabel("Adverse Outcome Rate (%)")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "03_term_adverse_rate.png",
    dpi=150
)

plt.close()


# =========================================================
# 8. CHART 4 — TOP RISK SEGMENTS
# =========================================================

print("Creating top risk segment chart...")

top_segments = (
    segments
    .head(10)
    .sort_values("adverse_outcome_rate_pct")
)

labels = (
    top_segments["fico_band"].astype(str)
    + " | "
    + top_segments["dti_band"].astype(str)
    + " | "
    + top_segments["income_band"].astype(str)
)

plt.figure(figsize=(12, 7))

plt.barh(
    labels,
    top_segments["adverse_outcome_rate_pct"]
)

plt.title(
    "Top 10 Borrower Segments by Adverse Outcome Rate"
)

plt.xlabel("Adverse Outcome Rate (%)")
plt.ylabel("Borrower Segment")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "04_top_risk_segments.png",
    dpi=150
)

plt.close()


# =========================================================
# 9. CHART 5 — PORTFOLIO EXPOSURE BY GRADE
# =========================================================

print("Creating exposure concentration chart...")

plt.figure(figsize=(10, 6))

plt.bar(
    grade["grade"],
    grade["exposure"] / 1_000_000_000
)

plt.title(
    "Portfolio Exposure by Loan Grade"
)

plt.xlabel("Loan Grade")
plt.ylabel("Exposure (Billions)")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "05_grade_exposure.png",
    dpi=150
)

plt.close()


# =========================================================
# 10. FINAL SUMMARY
# =========================================================

print("\n" + "=" * 60)
print("PYTHON EDA COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nSummary files:")
print(SUMMARY_DIR)

print("\nCharts:")
print(CHART_DIR)

print("\nCreated charts:")

for file in sorted(CHART_DIR.glob("*.png")):
    print(" -", file.name)

print("\nEDA stage completed.")