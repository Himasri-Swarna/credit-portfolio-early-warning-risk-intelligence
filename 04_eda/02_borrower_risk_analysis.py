import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# =========================================================
# Credit Portfolio Early-Warning & Risk Intelligence
# Borrower Risk Analysis
# =========================================================

INPUT_FILE = Path(
    "01_data/02_processed/fact_loans.csv"
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
print("BORROWER RISK ANALYSIS")
print("=" * 60)


# =========================================================
# 1. FICO BAND RISK
# =========================================================

print("\n1. Building FICO-band risk summary...")

fico_parts = []

USE_COLS = [
    "fico_band",
    "exposure_amount",
    "adverse_outcome_flag",
    "bad_loan_flag"
]

for chunk in pd.read_csv(
    INPUT_FILE,
    usecols=USE_COLS,
    chunksize=CHUNK_SIZE,
    low_memory=False
):

    chunk = chunk.dropna(subset=["fico_band"])

    grouped = (
        chunk
        .groupby("fico_band", as_index=False)
        .agg(
            loan_count=("fico_band", "size"),
            exposure=("exposure_amount", "sum"),
            adverse_loans=("adverse_outcome_flag", "sum"),
            bad_loans=("bad_loan_flag", "sum")
        )
    )

    fico_parts.append(grouped)


fico = pd.concat(
    fico_parts,
    ignore_index=True
)

fico = (
    fico
    .groupby("fico_band", as_index=False)
    .agg(
        loan_count=("loan_count", "sum"),
        exposure=("exposure", "sum"),
        adverse_loans=("adverse_loans", "sum"),
        bad_loans=("bad_loans", "sum")
    )
)

fico["adverse_rate_pct"] = (
    100 * fico["adverse_loans"] / fico["loan_count"]
)

fico["bad_rate_pct"] = (
    100 * fico["bad_loans"] / fico["loan_count"]
)

fico.to_csv(
    SUMMARY_DIR / "fico_risk_summary.csv",
    index=False
)

print("FICO summary created.")


# =========================================================
# 2. DTI BAND RISK
# =========================================================

print("\n2. Building DTI-band risk summary...")

dti_parts = []

USE_COLS = [
    "dti_band",
    "exposure_amount",
    "adverse_outcome_flag",
    "bad_loan_flag"
]

for chunk in pd.read_csv(
    INPUT_FILE,
    usecols=USE_COLS,
    chunksize=CHUNK_SIZE,
    low_memory=False
):

    chunk = chunk.dropna(subset=["dti_band"])

    grouped = (
        chunk
        .groupby("dti_band", as_index=False)
        .agg(
            loan_count=("dti_band", "size"),
            exposure=("exposure_amount", "sum"),
            adverse_loans=("adverse_outcome_flag", "sum"),
            bad_loans=("bad_loan_flag", "sum")
        )
    )

    dti_parts.append(grouped)


dti = pd.concat(
    dti_parts,
    ignore_index=True
)

dti = (
    dti
    .groupby("dti_band", as_index=False)
    .agg(
        loan_count=("loan_count", "sum"),
        exposure=("exposure", "sum"),
        adverse_loans=("adverse_loans", "sum"),
        bad_loans=("bad_loans", "sum")
    )
)

dti["adverse_rate_pct"] = (
    100 * dti["adverse_loans"] / dti["loan_count"]
)

dti["bad_rate_pct"] = (
    100 * dti["bad_loans"] / dti["loan_count"]
)

dti.to_csv(
    SUMMARY_DIR / "dti_risk_summary.csv",
    index=False
)

print("DTI summary created.")


# =========================================================
# 3. INCOME BAND RISK
# =========================================================

print("\n3. Building income-band risk summary...")

income_parts = []

USE_COLS = [
    "income_band",
    "exposure_amount",
    "adverse_outcome_flag",
    "bad_loan_flag"
]

for chunk in pd.read_csv(
    INPUT_FILE,
    usecols=USE_COLS,
    chunksize=CHUNK_SIZE,
    low_memory=False
):

    chunk = chunk.dropna(subset=["income_band"])

    grouped = (
        chunk
        .groupby("income_band", as_index=False)
        .agg(
            loan_count=("income_band", "size"),
            exposure=("exposure_amount", "sum"),
            adverse_loans=("adverse_outcome_flag", "sum"),
            bad_loans=("bad_loan_flag", "sum")
        )
    )

    income_parts.append(grouped)


income = pd.concat(
    income_parts,
    ignore_index=True
)

income = (
    income
    .groupby("income_band", as_index=False)
    .agg(
        loan_count=("loan_count", "sum"),
        exposure=("exposure", "sum"),
        adverse_loans=("adverse_loans", "sum"),
        bad_loans=("bad_loans", "sum")
    )
)

income["adverse_rate_pct"] = (
    100 * income["adverse_loans"] / income["loan_count"]
)

income["bad_rate_pct"] = (
    100 * income["bad_loans"] / income["loan_count"]
)

income.to_csv(
    SUMMARY_DIR / "income_risk_summary.csv",
    index=False
)

print("Income summary created.")


# =========================================================
# 4. INTEREST RATE BAND RISK
# =========================================================

print("\n4. Building interest-rate band summary...")

rate_parts = []

USE_COLS = [
    "int_rate",
    "exposure_amount",
    "adverse_outcome_flag",
    "bad_loan_flag"
]

for chunk in pd.read_csv(
    INPUT_FILE,
    usecols=USE_COLS,
    chunksize=CHUNK_SIZE,
    low_memory=False
):

    chunk = chunk.dropna(subset=["int_rate"])

    # Create interest-rate bands
    chunk["rate_band"] = pd.cut(
        chunk["int_rate"],
        bins=[
            0,
            8,
            12,
            16,
            20,
            25,
            100
        ],
        labels=[
            "<=8%",
            "8-12%",
            "12-16%",
            "16-20%",
            "20-25%",
            "25%+"
        ],
        include_lowest=True
    )

    grouped = (
        chunk
        .groupby("rate_band", observed=True)
        .agg(
            loan_count=("rate_band", "size"),
            exposure=("exposure_amount", "sum"),
            adverse_loans=("adverse_outcome_flag", "sum"),
            bad_loans=("bad_loan_flag", "sum")
        )
        .reset_index()
    )

    rate_parts.append(grouped)


rate = pd.concat(
    rate_parts,
    ignore_index=True
)

rate = (
    rate
    .groupby("rate_band", observed=True, as_index=False)
    .agg(
        loan_count=("loan_count", "sum"),
        exposure=("exposure", "sum"),
        adverse_loans=("adverse_loans", "sum"),
        bad_loans=("bad_loans", "sum")
    )
)

rate["adverse_rate_pct"] = (
    100 * rate["adverse_loans"] / rate["loan_count"]
)

rate["bad_rate_pct"] = (
    100 * rate["bad_loans"] / rate["loan_count"]
)

rate.to_csv(
    SUMMARY_DIR / "interest_rate_risk_summary.csv",
    index=False
)

print("Interest-rate summary created.")


# =========================================================
# 5. CHART — FICO RISK
# =========================================================

print("\n5. Creating FICO risk chart...")

fico_plot = fico.copy()

plt.figure(figsize=(10, 6))

plt.bar(
    fico_plot["fico_band"],
    fico_plot["adverse_rate_pct"]
)

plt.title(
    "Adverse Outcome Rate by FICO Band"
)

plt.xlabel("FICO Band")
plt.ylabel("Adverse Outcome Rate (%)")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "06_fico_adverse_rate.png",
    dpi=150
)

plt.close()


# =========================================================
# 6. CHART — DTI RISK
# =========================================================

print("Creating DTI risk chart...")

plt.figure(figsize=(10, 6))

plt.bar(
    dti["dti_band"],
    dti["adverse_rate_pct"]
)

plt.title(
    "Adverse Outcome Rate by DTI Band"
)

plt.xlabel("DTI Band")
plt.ylabel("Adverse Outcome Rate (%)")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "07_dti_adverse_rate.png",
    dpi=150
)

plt.close()


# =========================================================
# 7. CHART — INCOME RISK
# =========================================================

print("Creating income risk chart...")

plt.figure(figsize=(10, 6))

plt.bar(
    income["income_band"],
    income["adverse_rate_pct"]
)

plt.title(
    "Adverse Outcome Rate by Income Band"
)

plt.xlabel("Income Band")
plt.ylabel("Adverse Outcome Rate (%)")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "08_income_adverse_rate.png",
    dpi=150
)

plt.close()


# =========================================================
# 8. CHART — INTEREST RATE RISK
# =========================================================

print("Creating interest-rate risk chart...")

plt.figure(figsize=(10, 6))

plt.bar(
    rate["rate_band"].astype(str),
    rate["adverse_rate_pct"]
)

plt.title(
    "Adverse Outcome Rate by Interest-Rate Band"
)

plt.xlabel("Interest Rate Band")
plt.ylabel("Adverse Outcome Rate (%)")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "09_interest_rate_adverse_rate.png",
    dpi=150
)

plt.close()


# =========================================================
# 9. FINAL OUTPUT
# =========================================================

print("\n" + "=" * 60)
print("BORROWER RISK ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nCreated summary files:")

print(" - fico_risk_summary.csv")
print(" - dti_risk_summary.csv")
print(" - income_risk_summary.csv")
print(" - interest_rate_risk_summary.csv")

print("\nCreated charts:")

print(" - 06_fico_adverse_rate.png")
print(" - 07_dti_adverse_rate.png")
print(" - 08_income_adverse_rate.png")
print(" - 09_interest_rate_adverse_rate.png")

print("\nBorrower risk analysis completed.")