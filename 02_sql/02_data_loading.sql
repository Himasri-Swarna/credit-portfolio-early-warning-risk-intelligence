-- =========================================================
-- Credit Portfolio Early-Warning & Risk Intelligence
-- Data Loading
-- =========================================================

USE credit_risk_intelligence;

-- =========================================================
-- 1. Enable LOCAL INFILE
-- =========================================================

SET GLOBAL local_infile = 1;

-- =========================================================
-- 2. Load Date Dimension
-- =========================================================

LOAD DATA LOCAL INFILE
'C:/Users/himas/OneDrive/Final Projects/Credit Portfolio Early-Warning & Risk Intelligence Platform/01_data/02_processed/dim_date.csv'
INTO TABLE dim_date
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    date_key,
    date_value,
    year_num,
    month_num,
    month_name,
    quarter_name,
    year_month_label
);

-- =========================================================
-- 3. Load Borrower / Risk Segment Dimension
-- =========================================================

LOAD DATA LOCAL INFILE
'C:/Users/himas/OneDrive/Final Projects/Credit Portfolio Early-Warning & Risk Intelligence Platform/01_data/02_processed/dim_borrower_segment.csv'
INTO TABLE dim_borrower_segment
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    segment_id,
    risk_segment,
    fico_band,
    dti_band,
    income_band
);

-- =========================================================
-- 4. Load Main Loan Fact Table
-- Column order matches fact_loans.csv exactly
-- =========================================================

LOAD DATA LOCAL INFILE
'C:/Users/himas/OneDrive/Final Projects/Credit Portfolio Early-Warning & Risk Intelligence Platform/01_data/02_processed/fact_loans.csv'
INTO TABLE fact_loans
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    id,
    issue_d,
    issue_year,
    issue_month,
    issue_quarter,
    loan_amnt,
    funded_amnt,
    exposure_amount,
    term,
    int_rate,
    installment,
    annual_installment,
    grade,
    sub_grade,
    emp_length,
    home_ownership,
    annual_inc,
    income_band,
    verification_status,
    dti,
    dti_band,
    delinq_2yrs,
    fico_range_low,
    fico_range_high,
    fico_avg,
    fico_band,
    open_acc,
    pub_rec,
    revol_bal,
    revol_util,
    total_acc,
    loan_status,
    risk_outcome,
    risk_segment,
    bad_loan_flag,
    at_risk_flag,
    adverse_outcome_flag,
    last_pymnt_d,
    total_pymnt,
    recoveries,
    recovery_rate,
    net_loss_proxy,
    loan_to_income_ratio,
    date_key,
    segment_id
);

-- =========================================================
-- 5. Verify Loaded Row Counts
-- =========================================================

SELECT
    'dim_date' AS table_name,
    COUNT(*) AS row_count
FROM dim_date

UNION ALL

SELECT
    'dim_borrower_segment',
    COUNT(*)
FROM dim_borrower_segment

UNION ALL

SELECT
    'fact_loans',
    COUNT(*)
FROM fact_loans;