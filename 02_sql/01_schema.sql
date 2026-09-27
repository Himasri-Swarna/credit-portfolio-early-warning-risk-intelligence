-- =========================================================
-- Credit Portfolio Early-Warning & Risk Intelligence
-- Database Schema
-- =========================================================

CREATE DATABASE IF NOT EXISTS credit_risk_intelligence;

USE credit_risk_intelligence;

-- =========================================================
-- 1. Drop Existing Tables
-- =========================================================

DROP TABLE IF EXISTS fact_loans;
DROP TABLE IF EXISTS dim_borrower_segment;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS test_dim_date;

-- =========================================================
-- 2. Date Dimension
-- =========================================================

CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    date_value DATE,
    year_num INT,
    month_num INT,
    month_name VARCHAR(20),
    quarter_name VARCHAR(5),
    year_month_label VARCHAR(7)
);

-- =========================================================
-- 3. Borrower / Risk Segment Dimension
-- =========================================================

CREATE TABLE dim_borrower_segment (
    segment_id INT PRIMARY KEY,
    risk_segment VARCHAR(50),
    fico_band VARCHAR(20),
    dti_band VARCHAR(20),
    income_band VARCHAR(30)
);

-- =========================================================
-- 4. Main Loan Fact Table
-- =========================================================

CREATE TABLE fact_loans (

    id VARCHAR(50) PRIMARY KEY,

    -- Date / Time Attributes
    issue_d DATE,
    issue_year INT,
    issue_month INT,
    issue_quarter VARCHAR(10),

    date_key INT,
    segment_id INT,

    -- Loan Amounts
    loan_amnt DECIMAL(15,2),
    funded_amnt DECIMAL(15,2),
    exposure_amount DECIMAL(15,2),

    -- Loan Terms / Pricing
    term INT,
    int_rate DECIMAL(8,4),
    installment DECIMAL(15,2),
    annual_installment DECIMAL(15,2),

    -- Loan Grade
    grade VARCHAR(5),
    sub_grade VARCHAR(10),

    -- Employment / Income
    emp_length DECIMAL(5,2),
    home_ownership VARCHAR(30),
    annual_inc DECIMAL(18,2),

    income_band VARCHAR(30),
    verification_status VARCHAR(30),

    -- Debt / Credit Profile
    dti DECIMAL(10,4),
    dti_band VARCHAR(20),

    delinq_2yrs INT,

    fico_range_low INT,
    fico_range_high INT,
    fico_avg DECIMAL(8,2),
    fico_band VARCHAR(20),

    open_acc INT,
    pub_rec INT,
    revol_bal DECIMAL(15,2),
    revol_util DECIMAL(8,4),
    total_acc INT,

    -- Loan Outcome
    loan_status VARCHAR(50),
    risk_outcome VARCHAR(30),
    risk_segment VARCHAR(50),

    -- Risk Flags
    bad_loan_flag TINYINT,
    at_risk_flag TINYINT,
    adverse_outcome_flag TINYINT,

    -- Payment / Recovery
    last_pymnt_d DATE,
    total_pymnt DECIMAL(18,2),
    recoveries DECIMAL(18,2),

    recovery_rate DECIMAL(10,6),
    net_loss_proxy DECIMAL(18,2),

    -- Borrower Leverage
    loan_to_income_ratio DECIMAL(12,6),

    -- =====================================================
    -- Relationships
    -- =====================================================

    FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key),

    FOREIGN KEY (segment_id)
        REFERENCES dim_borrower_segment(segment_id)
);