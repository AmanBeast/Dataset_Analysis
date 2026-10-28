# 📊 Enterprise Data Analytics Portfolio & Case Studies

[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Tableau](https://img.shields.io/badge/Tableau-E97627?style=for-the-badge&logo=tableau&logoColor=white)](https://www.tableau.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)

A curated repository of production-grade **Data Analytics**, **Business Intelligence (BI)**, and **Predictive Modeling** case studies authored by **Aman Bisht**. Each project reflects the full analytical value chain: from raw messy data ingestion and ETL preprocessing to relational database modeling, advanced analytical querying, executive dashboarding, and interactive decision deployment.

🌐 **Live Portfolio Website:** [dataanalystresume.vercel.app](https://dataanalystresume.vercel.app/)  
📫 **Contact:** [amanbishtab99@gmail.com](mailto:amanbishtab99@gmail.com) | +91 7973478552 | [LinkedIn Profile](https://linkedin.com/in/aman-bisht)

---

## 🗂️ Flagship Project Directory

| # | Project Name | Domain | Primary Stack | Key Metrics & Highlights |
| :-: | :--- | :--- | :--- | :--- |
| **01** | [**Healthcare Operations & Revenue Intelligence**](./01_Healthcare_Clinical_Operations_Analysis) | Healthcare | Tableau, SQL, Relational Modeling | Modeled 5 relational tables; identified scheduling gaps to **cut clinic idle time by 22%** and **lift billing realization by 18%**. |
| **02** | [**Telecom Subscriber Churn & Retention Diagnostic**](./02_Telecom_Customer_Churn_Retention) | Telecom | Python, Pandas, Seaborn, EDA | Diagnosed 7,043 subscriber records; isolated a **3.5x higher churn velocity** in month-to-month contracts; designed retention playbook to protect **14% ARR**. |
| **03** | [**Omnichannel Retail Sales Analytics & SQL Benchmarking**](./03_Omnichannel_Retail_Sales_SQL_PowerBI) | Retail / Commerce | PostgreSQL, Window Functions, Power BI | Automated MoM growth benchmarking using CTEs and `LAG`/`LEAD`; isolated top **10% SKUs driving 45% margin**; **slashed reporting time by 60%**. |
| **04** | [**End-to-End Predictive Survival Pipeline & Web Simulator**](./04_Predictive_Passenger_Survival_Pipeline) | Decision Systems | Python, MySQL, Scikit-Learn, Streamlit | Full-lifecycle pipeline: feature binning, MySQL relational staging, Decision Tree training, and **interactive Streamlit cloud deployment** with live scorecards. |
| **05** | [**BFSI Banking Transactions & Wealth Segmentation**](./05_BFSI_Banking_Wealth_Segmentation) | Banking & Finance | PostgreSQL, Schema Design, SQL CASE | Normalized 3-tier banking schema; calculated client wealth tiers (Premium, Regular, Low Balance) and guarded against division-by-zero using `NULLIF`. |

---

## 🧹 Data Cleaning & Preprocessing Philosophy

Across all case studies, raw datasets were subjected to a rigorous data preparation and validation pipeline:

```mermaid
graph LR
    A[Raw Unstructured Logs] --> B[Data Auditing & Type Casting]
    B --> C[Null Imputation & Error Handling]
    C --> D[Outlier Detection & Feature Binning]
    D --> E[(Relational SQL Staging)]
    E --> F[BI Dashboards & ML Deployment]
```

1. **Missing Data Imputation & Null Safety:**
   - Applied domain-stratified median imputation (e.g. imputing age by passenger class and gender in Python).
   - Utilized `COALESCE` in PostgreSQL to eliminate orphaned null values in client contact registers.
   - Enforced `NULLIF(denominator, 0)` across all financial growth rate calculations to guarantee query stability.
2. **Feature Engineering & Categorical Binning:**
   - Converted continuous, noisy distributions into actionable managerial bins (e.g. Age Brackets, Fare Classes, Wealth Tiers, and Service Adoption Scores).
   - Re-coded sparse columns and eliminated high-null columns (e.g. dropping `Cabin` due to >77% missing data).
3. **Relational Integrity & Schema Normalization:**
   - Structured flat CSVs into 3rd Normal Form (3NF) relational tables with primary and foreign key constraints across MySQL and PostgreSQL.

---

## 🛠️ Core Technical Competencies

- **Database Systems & Querying:** PostgreSQL, MySQL, Star & Snowflake Schemas, Window Functions (`ROW_NUMBER`, `DENSE_RANK`, `LAG`, `LEAD`), CTEs, Subqueries, Stored Procedures, Views, Index Optimization.
- **Business Intelligence & Dashboards:** Power BI Desktop, DAX Measure Engineering, Power Query M-code, Tableau Desktop (LOD Expressions, Action Filters), Advanced Excel (Pivot Tables, XLOOKUP, Modeling).
- **Analytical Programming & Machine Learning:** Python (Pandas, NumPy, Matplotlib, Seaborn, Scikit-Learn), Statistical Hypothesis Testing, Exploratory Data Analysis (EDA), Feature Engineering.
- **Application & Dashboard Deployment:** Streamlit, React.js, Next.js, FastAPI, RESTful APIs, Git, GitHub, Vercel.

---

## 📂 Repository Tree

```text
Dataset_Analysis/
├── 01_Healthcare_Clinical_Operations_Analysis/
│   ├── assets/
│   │   ├── specialization_revenue_workload.png
│   │   └── payment_status_distribution.png
│   ├── data/
│   │   ├── appointments.csv
│   │   ├── billing.csv
│   │   ├── doctors.csv
│   │   ├── patients.csv
│   │   └── treatments.csv
│   ├── Book1.twb
│   └── README.md
│
├── 02_Telecom_Customer_Churn_Retention/
│   ├── assets/
│   │   ├── churn_by_contract.png
│   │   └── monthly_charges_churn_density.png
│   ├── data/
│   │   └── Telco-Customer-Churn.csv
│   └── README.md
│
├── 03_Omnichannel_Retail_Sales_SQL_PowerBI/
│   ├── assets/
│   │   └── regional_and_product_sales.png
│   ├── data/
│   │   └── sales_transactions_cleaned.csv
│   ├── sql/
│   │   ├── sales_window_functions_ctes.sql
│   │   └── awesome_chocolates.sql
│   └── README.md
│
├── 04_Predictive_Passenger_Survival_Pipeline/
│   ├── assets/
│   │   └── survival_class_gender.png
│   ├── data/
│   │   ├── titanic_raw.csv
│   │   └── titanic_cleaned.csv
│   ├── app.py
│   └── README.md
│
├── 05_BFSI_Banking_Wealth_Segmentation/
│   ├── assets/
│   │   └── wealth_tier_distribution.png
│   ├── data/
│   │   └── banking_accounts.csv
│   ├── sql/
│   │   └── banking_schema_wealth_segmentation.sql
│   └── README.md
│
└── README.md
```

---

## 👤 Author & Contact

**Aman Bisht**  
- **Email:** [amanbishtab99@gmail.com](mailto:amanbishtab99@gmail.com)  
- **Mobile:** +91 7973478552  
- **LinkedIn:** [linkedin.com/in/aman-bisht](https://linkedin.com/in/aman-bisht)  
- **GitHub:** [github.com/AmanBeast](https://github.com/AmanBeast)  
- **Portfolio Website:** [dataanalyst-resume.vercel.app](https://dataanalystresume.vercel.app)
