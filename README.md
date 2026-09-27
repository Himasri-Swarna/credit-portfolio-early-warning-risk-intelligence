\# Credit Portfolio Early-Warning \& Risk Intelligence Platform



\## 📌 Project Overview



The \*\*Credit Portfolio Early-Warning \& Risk Intelligence Platform\*\* is an end-to-end analytics project built to analyze:



\- Loan portfolio risk

\- Borrower characteristics

\- Portfolio concentration

\- Recovery performance

\- Observed adverse outcomes



The project uses the public \*\*LendingClub accepted-loans dataset (2007–2018 Q4)\*\* and combines \*\*Python, SQL, and Power BI\*\* to create a portfolio-level risk intelligence workflow.



> \*\*Important:\*\* This is a public LendingClub portfolio analysis. It is not an internal Indian bank portfolio. Macroeconomic/RBI context was considered as a future enhancement but is \*\*not integrated into the current dashboard\*\*.



\---



\## 🎯 Business Problem



Lenders need to understand where credit risk is concentrated and identify borrower or portfolio segments associated with higher observed adverse outcomes.



This project addresses questions such as:



\- How large is the analyzed loan portfolio?

\- What is the observed adverse outcome rate?

\- How do outcomes vary across loan grades?

\- How do FICO score, DTI, income, and interest rate relate to observed outcomes?

\- How has portfolio risk changed across loan vintages and over time?

\- Where is portfolio exposure concentrated?

\- Which borrower segments show higher observed adverse outcome rates?

\- How can portfolio data support early-warning and risk investigation?



\---



\## 🎯 Objectives



\- Clean and transform a large loan-level dataset.

\- Build reusable analytical tables for portfolio risk analysis.

\- Perform exploratory data analysis using Python.

\- Perform advanced portfolio analysis using SQL.

\- Develop borrower-risk and portfolio-concentration views.

\- Build a five-page Power BI risk intelligence dashboard.

\- Highlight observed patterns that can support credit-risk investigation.



\---



\## 📊 Dataset



\- \*\*Primary dataset:\*\* LendingClub Accepted Loans

\- \*\*Period:\*\* 2007–2018 Q4

\- \*\*Source:\*\* Public LendingClub loan dataset

\- \*\*Records after cleaning:\*\* Approximately \*\*2.26 million loan records\*\*



The dataset contains:



\- Borrower information

\- Loan information

\- Credit-risk information

\- Repayment information

\- Recovery information

\- Loan-outcome information



\### Important Limitation



The dataset represents LendingClub's historical portfolio and should not be presented as a current or Indian banking portfolio.



The analysis is descriptive and analytical. It does not constitute a:



\- Credit approval model

\- Investment recommendation

\- Production underwriting system



\---



\## 🔍 Key Portfolio Metrics



The current Power BI dashboard reports approximately:



| Metric | Value |

|---|---:|

| \*\*Total Loans\*\* | 2.26M |

| \*\*Total Exposure\*\* | 34.00B |

| \*\*Adverse Outcome Rate\*\* | 13.40% |

| \*\*Bad Loan Rate\*\* | 11.88% |

| \*\*Portfolio Recovery Rate\*\* | 0.96% |

| \*\*Average Interest Rate\*\* | \~13.09 |

| \*\*Average DTI\*\* | 18.82 |



> \*\*Metric note:\*\* Currency units are retained in the dataset's original units. They are not converted to INR.



\---



\## 🔍 Risk Definitions



The project uses an analytical outcome framework created during preprocessing.



\### Bad Loan



Loans classified into adverse final-status categories such as charged-off or default-related outcomes are represented through the `bad\_loan\_flag`.



\### Adverse Outcome



The `adverse\_outcome\_flag` provides a broader analytical indicator used to examine loans requiring risk attention.



\### Risk Segment



The `risk\_segment` field is a derived descriptive classification based on borrower/risk characteristics and observed outcome information.



Because this classification partly uses outcome-derived information, it should \*\*not\*\* be treated as an independent predictive feature or causal model input.



\---



\## 🧹 Data Preparation



Python preprocessing performs tasks including:



\- Date parsing and standardization

\- Interest-rate cleaning

\- Revolving-utilization cleaning

\- Loan-term normalization

\- Employment-length cleaning

\- FICO average calculation

\- Risk-outcome classification

\- Bad-loan and adverse-outcome flags

\- Exposure calculation

\- Annual installment calculation

\- Loan-to-income ratio

\- DTI bands

\- FICO bands

\- Income bands

\- Recovery-rate calculation

\- Net-loss proxy

\- Issue year/month/quarter derivation



\### Data Leakage Control



During borrower-segment analysis, an initial segmentation approach was identified as outcome-derived.



The final independent segment analysis uses:



\- \*\*FICO band\*\*

\- \*\*DTI band\*\*

\- \*\*Income band\*\*



This prevents the segment-level adverse-rate analysis from simply reproducing the outcome definition.



\---



\## 🐍 Python \& EDA



The Python workflow includes:



\### Data Inspection



\- Dataset structure

\- Data types

\- Missing values

\- Basic quality checks



\### Data Cleaning



\- Standardized important fields

\- Created analytical features

\- Generated the cleaned/fact datasets



\### Exploratory Analysis



The EDA covers:



\- Monthly adverse outcome trends

\- Loan-grade risk

\- Loan-term risk

\- FICO risk

\- DTI risk

\- Income risk

\- Interest-rate risk

\- Portfolio exposure

\- Borrower-segment risk



Generated outputs include charts and summary CSV tables used to support the dashboard.



\---



\## 🗄️ SQL Analysis



The MySQL database is:



```text

credit\_risk\_intelligence



\### Main Tables



\- `fact\_loans`

\- `dim\_date`

\- `dim\_borrower\_segment`



\### SQL Analysis Covers



1\. \*\*Portfolio overview\*\*

2\. \*\*Loan-status distribution\*\*

3\. \*\*Risk by loan grade\*\*

4\. \*\*FICO-band analysis\*\*

5\. \*\*DTI-band analysis\*\*

6\. \*\*Income-band analysis\*\*

7\. \*\*Vintage analysis\*\*

8\. \*\*Year-over-year vintage analysis\*\*

9\. \*\*Independent borrower-segment analysis\*\*

10\. \*\*Segment ranking\*\*

11\. \*\*Segment analysis within grade\*\*

12\. \*\*Monthly adverse-rate trends\*\*

13\. \*\*Cumulative portfolio exposure\*\*

14\. \*\*Interest rate vs. risk by grade\*\*

15\. \*\*Recovery performance\*\*

16\. \*\*Loan-term risk\*\*

17\. \*\*Portfolio concentration by grade\*\*

18\. \*\*Recent-vintage vs. historical baseline analysis\*\*



\## 📈 Power BI Dashboard



The final dashboard contains \*\*5 analytical pages\*\*.



\### Dashboard Screenshots



\#### 1. Credit Portfolio Executive Overview



!\[Credit Portfolio Executive Overview](assets/screenshots/01\_executive-overview.png)



\### 1. Credit Portfolio Executive Overview



\*\*Tab:\*\* `Executive Overview`



Provides a high-level portfolio view with:



\- Total loans

\- Total exposure

\- Adverse outcome rate

\- Bad loan rate

\- Portfolio recovery rate

\- Average interest rate

\- Average DTI

\- Monthly adverse outcome trend

\- Adverse outcome rate by grade

\- Portfolio exposure by grade

\- Portfolio risk snapshot



\---



\#### 2. Vintage \& Trend Risk Intelligence



!\[Vintage \& Trend Risk Intelligence](assets/screenshots/02\_vintage-trend-risk.png)



\### 2. Vintage \& Trend Risk Intelligence



\*\*Tab:\*\* `Vintage \& Trend Risk`



Analyzes portfolio behavior across issue vintages and time.



Includes:



\- Adverse outcome rate by vintage year

\- Loan volume by vintage year

\- Portfolio exposure by vintage year

\- 3-month rolling adverse outcome rate

\- Monthly adverse outcome trend

\- Vintage risk vs. historical baseline

\- Vintage risk summary



Vintage comparisons should be interpreted carefully because newer loan vintages may not have fully matured. Observed differences do not necessarily imply that newer vintages are inherently safer or riskier.



\---



\#### 3. Borrower Risk Intelligence



!\[Borrower Risk Intelligence](assets/screenshots/03\_borrower-risk.png)



\### 3. Borrower Risk Intelligence



\*\*Tab:\*\* `Borrower Risk`



Examines borrower characteristics associated with observed outcomes.



Includes:



\- Adverse outcome rate by FICO band

\- Adverse outcome rate by DTI band

\- Adverse outcome rate by income band

\- FICO vs. DTI risk profile

\- Adverse outcome rate by interest rate

\- Borrower risk segment summary



The interest-rate visual uses the underlying loan-level rate and can be relatively dense because interest rate is a continuous variable.



\---



\#### 4. Portfolio Concentration \& Exposure Intelligence



!\[Portfolio Concentration \& Exposure Intelligence](assets/screenshots/04\_portfolio-concentration.png)



\### 4. Portfolio Concentration \& Exposure Intelligence



\*\*Tab:\*\* `Portfolio Concentration`



Examines where portfolio exposure and loan volume are concentrated.



Includes:



\- Portfolio exposure by loan grade

\- Loan volume by loan grade

\- Portfolio exposure by loan term

\- Loan volume by loan term

\- Exposure and adverse outcome rate by grade

\- Portfolio exposure concentration by grade

\- Grade-level portfolio summary



Observed exposure concentration is descriptive and does not by itself indicate that a grade is inherently more or less risky.



\---



\#### 5. Credit Risk Investigation \& Early Warning



!\[Credit Risk Investigation \& Early Warning](assets/screenshots/05\_risk-investigation.png)



\### 5. Credit Risk Investigation \& Early Warning



\*\*Tab:\*\* `Risk Investigation`



Provides an investigation-oriented view of borrower and portfolio risk.



Includes:



\- Adverse outcome rate by FICO band

\- Adverse outcome rate by DTI band

\- Adverse outcome rate by income band

\- FICO vs. DTI risk profile

\- Adverse outcome rate by interest rate

\- Portfolio exposure by loan grade

\- Monthly adverse outcome trend

\- Portfolio risk snapshot



This page is intended to support \*\*risk investigation and early-warning analysis\*\*, not automated credit decisions.



\## 🔎 Key Observed Findings



The analysis shows several descriptive patterns:



\- The analyzed portfolio contains approximately \*\*2.26 million loans\*\*.

\- Total analyzed exposure is approximately \*\*34.00B\*\* in the dataset's original currency units.

\- The overall observed adverse outcome rate is approximately \*\*13.40%\*\*.

\- The observed bad-loan rate is approximately \*\*11.88%\*\*.

\- Loan outcomes vary across FICO, DTI, income, grade, term, and interest-rate groups.

\- Portfolio exposure is concentrated primarily in loan grades \*\*C and B\*\*.

\- The 36-month term represents substantially more loans than the 60-month term in the analyzed dataset.

\- More recent vintages show lower observed adverse rates in the available data, but this comparison is affected by \*\*loan seasoning/maturity\*\*, particularly for the latest vintage.



\### Example Vintage Observation



For the 2018 vintage, the observed adverse rate is approximately \*\*4.16%\*\*, compared with a historical pre-2018 average of approximately \*\*13.92%\*\* in the SQL analysis.



This should not be interpreted as evidence that 2018 loans were inherently safer because newer loans have had less time to reach adverse outcomes.



\---



\## 📁 Project Architecture



```text

Credit Portfolio Early-Warning \& Risk Intelligence Platform/

│

├── 01\_data/

│   ├── 01\_raw/

│   │   └── accepted\_2007\_to\_2018Q4.csv.gz

│   │

│   └── 02\_processed/

│       ├── loans\_cleaned.csv

│       ├── fact\_loans.csv

│       ├── dim\_date.csv

│       ├── dim\_borrower\_segment.csv

│       └── segment\_risk\_summary.csv

│

├── 02\_sql/

│   ├── 01\_schema.sql

│   ├── 02\_data\_loading.sql

│   ├── 03\_risk\_analysis.sql

│   └── 04\_advanced\_analysis.sql

│

├── 03\_python/

│   ├── notebooks/

│   ├── 01\_inspect\_data.py

│   ├── 02\_clean\_loans.py

│   ├── 03\_build\_fact\_loans.py

│   ├── 04\_build\_dimensions.py

│   ├── 05\_link\_dimensions.py

│   └── 06\_build\_segment\_summary.py

│

├── 04\_eda/

│   ├── 01\_eda.py

│   ├── 02\_borrower\_risk\_analysis.py

│   └── 03\_build\_portfolio\_summary.py

│

├── 05\_powerbi/

│

├── 06\_docs/

│

├── 07\_outputs/

│   ├── charts/

│   └── summary\_tables/

│

├── assets/

│   └── screenshots/

│

├── README.md

└── requirements.txt



\## 🛠️ Technology Stack



\### Programming \& Analytics



\- Python

\- Pandas

\- NumPy



\### Database \& SQL



\- MySQL

\- SQL

\- Window Functions

\- CTEs

\- Aggregations

\- Ranking Analysis



\### Business Intelligence



\- Microsoft Power BI

\- DAX

\- Power Query

\- Interactive Dashboards



\### Development Tools



\- Git

\- GitHub

\- Jupyter Notebook

\- VS Code



\---



\## ⚠️ Limitations



\- \*\*Public dataset limitation:\*\* The analysis is based on LendingClub data and is not representative of a specific Indian bank.

\- \*\*Historical data:\*\* The dataset covers loans issued through 2018 Q4 and is not a current credit portfolio.

\- \*\*Vintage/seasoning bias:\*\* Newer loans have had less time to mature.

\- \*\*Outcome-derived fields:\*\* Some derived risk labels use observed outcomes and should not be treated as independent predictive variables.

\- \*\*No causal inference:\*\* Observed relationships do not establish causation.

\- \*\*No production credit model:\*\* This project is an analytics and risk-intelligence platform, not a production underwriting engine.

\- \*\*No RBI integration:\*\* Macroeconomic/RBI indicators were considered as a future enhancement but are not currently integrated.

\- \*\*Recovery metric:\*\* Recovery analysis is based on the available dataset fields and should not be interpreted as a complete accounting loss calculation.

\- \*\*Contribution/profit concepts:\*\* The project does not claim true accounting profit or loss where required cost components are unavailable.



\## 🚀 Future Enhancements



Potential next versions could include:



\- RBI macroeconomic indicators

\- Unemployment and inflation context

\- Time-aware early-warning indicators

\- More robust borrower segmentation

\- Survival/seasoning analysis

\- Predictive probability-of-default modeling

\- Model monitoring

\- Automated Power BI refresh

\- Portfolio stress testing

\- Scenario analysis

\- Alerting for deteriorating risk segments

\- Interactive drill-through borrower investigations



\---



\## 💡 Project Outcome



This project demonstrates an end-to-end analytics workflow:



\*\*Raw Data → Data Cleaning → Feature Engineering → EDA → SQL Risk Analysis → Power BI Dashboard → Risk Intelligence\*\*



It demonstrates practical skills in:



\- Large-scale data handling

\- Data cleaning

\- SQL analytics

\- Risk analytics

\- Business intelligence

\- DAX

\- Data visualization

\- Portfolio analysis

\- Analytical storytelling

\- Data-quality and leakage awareness



\---



\## ⚠️ Disclaimer



This project is intended for \*\*educational and portfolio demonstration purposes\*\*.



The findings are descriptive analyses of historical public data and should not be used as financial, investment, lending, or credit-approval advice.

