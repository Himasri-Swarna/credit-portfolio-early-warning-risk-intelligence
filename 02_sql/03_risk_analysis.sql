-- =========================================================
-- CREDIT PORTFOLIO EARLY-WARNING & RISK INTELLIGENCE
-- Risk Analysis SQL
-- Database: credit_risk_intelligence
-- =========================================================


-- =========================================================
-- 1. PORTFOLIO OVERVIEW
-- =========================================================

USE credit_risk_intelligence;

SELECT
    COUNT(*) AS total_loans,
    SUM(funded_amnt) AS total_funded_amount,
    SUM(exposure_amount) AS total_exposure,
    AVG(loan_amnt) AS avg_loan_amount,
    AVG(int_rate) AS avg_interest_rate,
    AVG(dti) AS avg_dti,
    AVG(fico_avg) AS avg_fico,
    ROUND(
        100.0 * SUM(bad_loan_flag) / COUNT(*),
        2
    ) AS bad_loan_rate_pct,
    ROUND(
        100.0 * SUM(adverse_outcome_flag) / COUNT(*),
        2
    ) AS adverse_outcome_rate_pct
FROM fact_loans;


-- =========================================================
-- 2. LOAN STATUS DISTRIBUTION
-- =========================================================

USE credit_risk_intelligence;

SELECT
    loan_status,
    COUNT(*) AS loan_count,
    SUM(exposure_amount) AS exposure,
    ROUND(
        100.0 * COUNT(*) /
        (SELECT COUNT(*) FROM fact_loans),
        2
    ) AS portfolio_share_pct
FROM fact_loans
GROUP BY loan_status
ORDER BY loan_count DESC;


-- =========================================================
-- 3. RISK BY LOAN GRADE
-- =========================================================

USE credit_risk_intelligence;

SELECT
    grade,
    COUNT(*) AS loan_count,
    SUM(exposure_amount) AS exposure,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_amount,
    ROUND(AVG(int_rate), 2) AS avg_interest_rate,
    ROUND(
        100.0 * SUM(bad_loan_flag) / COUNT(*),
        2
    ) AS bad_loan_rate_pct,
    ROUND(
        100.0 * SUM(adverse_outcome_flag) / COUNT(*),
        2
    ) AS adverse_outcome_rate_pct
FROM fact_loans
GROUP BY grade
ORDER BY adverse_outcome_rate_pct DESC;


-- =========================================================
-- 4. RISK BY FICO BAND
-- =========================================================

USE credit_risk_intelligence;

SELECT
    fico_band,
    COUNT(*) AS loan_count,
    SUM(exposure_amount) AS exposure,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_amount,
    ROUND(
        100.0 * SUM(bad_loan_flag) / COUNT(*),
        2
    ) AS bad_loan_rate_pct,
    ROUND(
        100.0 * SUM(adverse_outcome_flag) / COUNT(*),
        2
    ) AS adverse_outcome_rate_pct
FROM fact_loans
GROUP BY fico_band
ORDER BY adverse_outcome_rate_pct DESC;


-- =========================================================
-- 5. RISK BY DTI BAND
-- =========================================================

USE credit_risk_intelligence;

SELECT
    dti_band,
    COUNT(*) AS loan_count,
    SUM(exposure_amount) AS exposure,
    ROUND(AVG(dti), 2) AS avg_dti,
    ROUND(
        100.0 * SUM(bad_loan_flag) / COUNT(*),
        2
    ) AS bad_loan_rate_pct,
    ROUND(
        100.0 * SUM(adverse_outcome_flag) / COUNT(*),
        2
    ) AS adverse_outcome_rate_pct
FROM fact_loans
GROUP BY dti_band
ORDER BY adverse_outcome_rate_pct DESC;


-- =========================================================
-- 6. RISK BY INCOME BAND
-- =========================================================

USE credit_risk_intelligence;

SELECT
    income_band,
    COUNT(*) AS loan_count,
    SUM(exposure_amount) AS exposure,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_amount,
    ROUND(
        100.0 * SUM(bad_loan_flag) / COUNT(*),
        2
    ) AS bad_loan_rate_pct,
    ROUND(
        100.0 * SUM(adverse_outcome_flag) / COUNT(*),
        2
    ) AS adverse_outcome_rate_pct
FROM fact_loans
GROUP BY income_band
ORDER BY adverse_outcome_rate_pct DESC;


-- =========================================================
-- 7. ORIGINATION VINTAGE ANALYSIS
-- =========================================================

USE credit_risk_intelligence;

SELECT
    issue_year,
    COUNT(*) AS loan_count,
    SUM(exposure_amount) AS exposure,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_amount,
    ROUND(
        100.0 * SUM(bad_loan_flag) / COUNT(*),
        2
    ) AS bad_loan_rate_pct,
    ROUND(
        100.0 * SUM(adverse_outcome_flag) / COUNT(*),
        2
    ) AS adverse_outcome_rate_pct
FROM fact_loans
WHERE issue_year IS NOT NULL
GROUP BY issue_year
ORDER BY issue_year;


-- =========================================================
-- 8. YEAR-OVER-YEAR VINTAGE CHANGE
-- Uses LAG()
-- =========================================================

USE credit_risk_intelligence;

WITH yearly_risk AS
(
    SELECT
        issue_year,
        COUNT(*) AS loan_count,
        ROUND(
            100.0 * SUM(adverse_outcome_flag) / COUNT(*),
            2
        ) AS adverse_rate_pct
    FROM fact_loans
    WHERE issue_year IS NOT NULL
    GROUP BY issue_year
)

SELECT
    issue_year,
    loan_count,
    adverse_rate_pct,
    LAG(adverse_rate_pct) OVER (
        ORDER BY issue_year
    ) AS previous_year_rate,
    ROUND(
        adverse_rate_pct -
        LAG(adverse_rate_pct) OVER (
            ORDER BY issue_year
        ),
        2
    ) AS year_over_year_change_pp
FROM yearly_risk
ORDER BY issue_year;


-- =========================================================
-- 9. TOP RISK SEGMENTS
-- IMPORTANT:
-- Run this query INDIVIDUALLY.
-- =========================================================

USE credit_risk_intelligence;

SELECT
    d.segment_id,
    d.risk_segment,
    d.fico_band,
    d.dti_band,
    d.income_band,
    s.loan_count,
    s.exposure,
    s.avg_loan_amount,
    s.adverse_outcome_rate_pct
FROM dim_borrower_segment d

INNER JOIN
(
    SELECT
        segment_id,
        COUNT(*) AS loan_count,
        SUM(exposure_amount) AS exposure,
        ROUND(AVG(loan_amnt), 2) AS avg_loan_amount,
        ROUND(
            100.0 * SUM(adverse_outcome_flag) / COUNT(*),
            2
        ) AS adverse_outcome_rate_pct
    FROM fact_loans
    WHERE segment_id IS NOT NULL
    GROUP BY segment_id
    HAVING COUNT(*) >= 100
) s
    ON d.segment_id = s.segment_id

ORDER BY
    s.adverse_outcome_rate_pct DESC,
    s.exposure DESC

LIMIT 20;


-- =========================================================
-- 10. RANK INDEPENDENT BORROWER SEGMENTS
-- Uses RANK()
-- =========================================================

USE credit_risk_intelligence;

WITH borrower_segments AS
(
    SELECT
        fico_band,
        dti_band,
        income_band,
        COUNT(*) AS loan_count,
        SUM(exposure_amount) AS exposure,

        ROUND(
            100.0 * SUM(adverse_outcome_flag) / COUNT(*),
            2
        ) AS adverse_rate_pct

    FROM fact_loans

    WHERE fico_band IS NOT NULL
      AND dti_band IS NOT NULL
      AND income_band IS NOT NULL

    GROUP BY
        fico_band,
        dti_band,
        income_band

    HAVING COUNT(*) >= 100
)

SELECT
    RANK() OVER (
        ORDER BY adverse_rate_pct DESC
    ) AS risk_rank,

    fico_band,
    dti_band,
    income_band,
    loan_count,
    exposure,
    adverse_rate_pct

FROM borrower_segments

ORDER BY
    risk_rank,
    exposure DESC

LIMIT 20;


-- =========================================================
-- 11. TOP BORROWER SEGMENT WITHIN EACH LOAN GRADE
-- Uses ROW_NUMBER()
-- =========================================================

USE credit_risk_intelligence;

WITH grade_segments AS
(
    SELECT
        grade,
        fico_band,
        dti_band,
        income_band,

        COUNT(*) AS loan_count,

        SUM(exposure_amount) AS exposure,

        ROUND(
            100.0 * SUM(adverse_outcome_flag) / COUNT(*),
            2
        ) AS adverse_rate_pct

    FROM fact_loans

    WHERE grade IS NOT NULL
      AND fico_band IS NOT NULL
      AND dti_band IS NOT NULL
      AND income_band IS NOT NULL

    GROUP BY
        grade,
        fico_band,
        dti_band,
        income_band

    HAVING COUNT(*) >= 100
),

ranked_segments AS
(
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY grade
            ORDER BY
                adverse_rate_pct DESC,
                exposure DESC
        ) AS segment_rank

    FROM grade_segments
)

SELECT
    grade,
    segment_rank,
    fico_band,
    dti_band,
    income_band,
    loan_count,
    exposure,
    adverse_rate_pct

FROM ranked_segments

WHERE segment_rank = 1

ORDER BY grade;


-- =========================================================
-- 12. MONTHLY ADVERSE OUTCOME RATE
-- 3-MONTH ROLLING ADVERSE OUTCOME RATE
-- Uses window functions
-- =========================================================

USE credit_risk_intelligence;

WITH monthly_risk AS
(
    SELECT
        issue_year,
        issue_month,

        COUNT(*) AS loan_count,

        SUM(exposure_amount) AS exposure,

        SUM(adverse_outcome_flag) AS adverse_loans

    FROM fact_loans

    WHERE issue_year IS NOT NULL
      AND issue_month IS NOT NULL

    GROUP BY
        issue_year,
        issue_month
)

SELECT
    issue_year,
    issue_month,
    loan_count,
    exposure,

    ROUND(
        100.0 * adverse_loans / loan_count,
        2
    ) AS monthly_adverse_rate_pct,

    ROUND(
        100.0 *
        SUM(adverse_loans) OVER
        (
            ORDER BY issue_year, issue_month
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        )
        /
        SUM(loan_count) OVER
        (
            ORDER BY issue_year, issue_month
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS rolling_3_month_adverse_rate_pct

FROM monthly_risk

ORDER BY
    issue_year,
    issue_month;


-- =========================================================
-- 13. CUMULATIVE PORTFOLIO EXPOSURE
-- Uses SUM() OVER()
-- =========================================================

USE credit_risk_intelligence;

WITH monthly_exposure AS
(
    SELECT
        issue_year,
        issue_month,
        SUM(exposure_amount) AS monthly_exposure

    FROM fact_loans

    WHERE issue_year IS NOT NULL
      AND issue_month IS NOT NULL

    GROUP BY
        issue_year,
        issue_month
)

SELECT
    issue_year,
    issue_month,
    monthly_exposure,

    SUM(monthly_exposure) OVER
    (
        ORDER BY issue_year, issue_month
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_exposure

FROM monthly_exposure

ORDER BY
    issue_year,
    issue_month;


-- =========================================================
-- 14. INTEREST RATE VS RISK OUTCOME
-- =========================================================

USE credit_risk_intelligence;

SELECT
    grade,

    ROUND(AVG(int_rate), 2) AS avg_interest_rate,

    ROUND(AVG(loan_amnt), 2) AS avg_loan_amount,

    COUNT(*) AS loan_count,

    ROUND(
        100.0 * SUM(bad_loan_flag) / COUNT(*),
        2
    ) AS bad_loan_rate_pct,

    ROUND(
        100.0 * SUM(adverse_outcome_flag) / COUNT(*),
        2
    ) AS adverse_outcome_rate_pct

FROM fact_loans

WHERE grade IS NOT NULL
  AND int_rate IS NOT NULL

GROUP BY grade

ORDER BY
    avg_interest_rate DESC;


-- =========================================================
-- 15. RECOVERY PERFORMANCE
-- =========================================================

USE credit_risk_intelligence;

SELECT
    grade,

    COUNT(*) AS loan_count,

    SUM(exposure_amount) AS exposure,

    SUM(recoveries) AS total_recoveries,

    ROUND(
        AVG(recovery_rate) * 100,
        2
    ) AS avg_recovery_rate_pct,

    ROUND(
        SUM(recoveries) /
        NULLIF(SUM(exposure_amount), 0) * 100,
        2
    ) AS portfolio_recovery_pct

FROM fact_loans

WHERE bad_loan_flag = 1
  AND grade IS NOT NULL

GROUP BY grade

ORDER BY
    avg_recovery_rate_pct DESC;


-- =========================================================
-- 16. RISK BY LOAN TERM
-- =========================================================

USE credit_risk_intelligence;

SELECT
    term,

    COUNT(*) AS loan_count,

    SUM(exposure_amount) AS exposure,

    ROUND(
        AVG(int_rate),
        2
    ) AS avg_interest_rate,

    ROUND(
        AVG(loan_amnt),
        2
    ) AS avg_loan_amount,

    ROUND(
        100.0 * SUM(bad_loan_flag) / COUNT(*),
        2
    ) AS bad_loan_rate_pct,

    ROUND(
        100.0 * SUM(adverse_outcome_flag) / COUNT(*),
        2
    ) AS adverse_outcome_rate_pct

FROM fact_loans

WHERE term IS NOT NULL

GROUP BY term

ORDER BY
    adverse_outcome_rate_pct DESC;


-- =========================================================
-- 17. PORTFOLIO CONCENTRATION BY GRADE
-- Uses subquery
-- =========================================================

USE credit_risk_intelligence;

SELECT
    grade,

    COUNT(*) AS loan_count,

    SUM(exposure_amount) AS exposure,

    ROUND(
        100.0 * SUM(exposure_amount) /
        (
            SELECT SUM(exposure_amount)
            FROM fact_loans
        ),
        2
    ) AS exposure_share_pct,

    ROUND(
        100.0 * SUM(adverse_outcome_flag) / COUNT(*),
        2
    ) AS adverse_outcome_rate_pct

FROM fact_loans

GROUP BY grade

ORDER BY
    exposure_share_pct DESC;


-- =========================================================
-- 18. RECENT VINTAGE VS HISTORICAL BASELINE
-- Uses CTE + subquery
-- =========================================================

USE credit_risk_intelligence;

WITH yearly_risk AS
(
    SELECT
        issue_year,
        COUNT(*) AS loan_count,
        SUM(exposure_amount) AS exposure,

        ROUND(
            100.0 * SUM(adverse_outcome_flag) / COUNT(*),
            2
        ) AS adverse_rate_pct

    FROM fact_loans

    WHERE issue_year IS NOT NULL

    GROUP BY issue_year
),

baseline AS
(
    SELECT
        AVG(adverse_rate_pct) AS historical_avg_rate

    FROM yearly_risk

    WHERE issue_year < (
        SELECT MAX(issue_year)
        FROM yearly_risk
    )
)

SELECT
    y.issue_year,
    y.loan_count,
    y.exposure,
    y.adverse_rate_pct,

    ROUND(
        b.historical_avg_rate,
        2
    ) AS historical_avg_rate,

    ROUND(
        y.adverse_rate_pct -
        b.historical_avg_rate,
        2
    ) AS difference_from_historical_avg_pp

FROM yearly_risk y

CROSS JOIN baseline b

WHERE y.issue_year = (
    SELECT MAX(issue_year)
    FROM yearly_risk
)

ORDER BY y.issue_year;