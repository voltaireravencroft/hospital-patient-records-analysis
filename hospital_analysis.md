# Hospital Patient Records Analysis

SQL analysis of patient admission patterns, length of stay, costs, and insurance coverage for Massachusetts General Hospital (2011-2022).

## Overview

Analysis of synthetic healthcare data (~1,000 patients, 28,000 encounters, 48,000 procedures) to identify operational inefficiencies and cost patterns in hospital admissions.

## Business Questions

1. How many patients have been admitted or readmitted over time?
2. How long are patients staying in the hospital, on average?
3. How much is the average cost per visit?
4. How many procedures are covered by insurance?

## Key Findings

### 1. Admission and Readmission Patterns

**Critical Finding: 55-79% readmission rates (2011-2019)**

- 2011-2019: Extremely high readmission rates (55-79%)
- 2019 peak: 79.1% readmission rate (106 readmissions out of 134 total admissions)
- 2020-2021: Dramatic drop to ~35% readmission rate
- Suggests either major intervention implemented or COVID-19 impact on elective procedures

### 2. Length of Stay Analysis

**96.8% of inpatient stays are exactly 1 day**

- Average length of stay: 1.54 days
- 1,099 out of 1,135 admissions (96.8%) were single-day stays
- Only 36 stays (3.2%) exceeded 1 day
- Longest stay: 344 days (likely long-term care patient)
- **Data Quality Flag**: This distribution is unusual for "inpatient" classification

### 3. Cost Analysis

**Average visit cost: $3,639.68**

**Cost by encounter type:**
- Inpatient: $7,761.35 average (highest)
- Urgent care: $6,369.16
- Emergency: $4,629.65
- Wellness: $4,260.71
- Ambulatory: $2,894.11
- Outpatient: $2,237.30 (lowest)

**Patient financial burden:**
- Average insurance coverage: $1,114.97 (30.6% of total)
- Average patient responsibility: $2,524.72 (69.4% out-of-pocket)

### 4. Insurance Coverage

**Only 52% of procedures have insurance coverage**

- Total procedures: 47,701
- Procedures with coverage: 24,791 (52.0%)
- Procedures without coverage: 22,910 (48.0%)

**Coverage by provider:**
- Medicare: 19,492 procedures (78% of covered procedures)
- Medicaid: 2,837 procedures ($19,473 avg coverage)
- Blue Cross Blue Shield: 1,220 procedures
- Private insurers (UnitedHealthcare, Aetna, Cigna): Minimal coverage

**Insight**: This is likely a public hospital serving primarily Medicare/Medicaid patients.

## Tools & Technologies

- **Database**: MySQL 9.6 (Docker container)
- **Query Language**: SQL
- **Data Loading**: Python (mysql-connector-python, csv)
- **Analysis**: Complex JOINs, aggregations, window functions
- **Visualization Data**: Exported to CSV for dashboard creation

## SQL Techniques Demonstrated

- Multi-table JOINs (procedures → encounters → payers)
- Date functions (YEAR(), DATEDIFF())
- Aggregate functions (COUNT, AVG, MIN, MAX)
- Conditional aggregation (CASE WHEN)
- Subqueries
- GROUP BY with complex expressions
- Percentage calculations

## Files

- `hospital_analysis_queries.sql` - All analytical queries
- `load_hospital_data.py` - Data loading script
- `export_results.py` - Results export script
- `analysis_results/` - Query results in CSV format

## Data Source

**Source**: Maven Analytics - Hospital Patient Records  
**License**: Public Domain  
**Dataset**: Synthetic data for Massachusetts General Hospital (2011-2022)  
**Records**: 973 patients, 27,891 encounters, 47,701 procedures

## Recommendations

Based on analysis findings:

1. **Investigate readmission causes** - 55-79% rates are 3-4x national average
2. **Clarify "inpatient" definition** - 96.8% single-day stays suggest classification issues
3. **Review insurance contracting** - Only 52% procedure coverage is concerningly low
4. **Patient financial counseling** - 69% out-of-pocket burden may impact care access

## Author

**Michael Galvan**  
Transitioning from Operations Management to Data Analytics  
[GitHub](https://github.com/voltaireravencroft) | [LinkedIn](www.linkedin.com/in/michael-a-galvan)