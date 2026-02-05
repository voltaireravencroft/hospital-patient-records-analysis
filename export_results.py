import mysql.connector
import csv

# Database connection
conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='root',
    password='password123',
    database='hospital_db'
)
cursor = conn.cursor()

# Output directory
output_dir = r'C:\Users\User\Downloads\Hospital+Patient+Records\analysis_results'

# Create output directory if it doesn't exist
import os
os.makedirs(output_dir, exist_ok=True)

# Query definitions with output filenames
queries = {
    'admissions_by_year.csv': """
        SELECT 
            YEAR(START) as year,
            COUNT(*) as total_admissions,
            COUNT(DISTINCT PATIENT) as unique_patients,
            COUNT(*) - COUNT(DISTINCT PATIENT) as readmissions,
            ROUND(100.0 * (COUNT(*) - COUNT(DISTINCT PATIENT)) / COUNT(*), 1) as readmission_rate_pct
        FROM encounters
        WHERE ENCOUNTERCLASS = 'inpatient'
        GROUP BY YEAR(START)
        ORDER BY year
    """,
    
    'length_of_stay_distribution.csv': """
        SELECT 
            CASE 
                WHEN DATEDIFF(STOP, START) = 1 THEN '1 day'
                WHEN DATEDIFF(STOP, START) BETWEEN 2 AND 3 THEN '2-3 days'
                WHEN DATEDIFF(STOP, START) BETWEEN 4 AND 7 THEN '4-7 days'
                WHEN DATEDIFF(STOP, START) BETWEEN 8 AND 14 THEN '8-14 days'
                WHEN DATEDIFF(STOP, START) BETWEEN 15 AND 30 THEN '15-30 days'
                ELSE '30+ days'
            END as length_of_stay_range,
            COUNT(*) as num_stays,
            ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM encounters WHERE ENCOUNTERCLASS = 'inpatient'), 1) as percentage
        FROM encounters
        WHERE ENCOUNTERCLASS = 'inpatient'
        GROUP BY length_of_stay_range
        ORDER BY MIN(DATEDIFF(STOP, START))
    """,
    
    'costs_by_encounter_type.csv': """
        SELECT 
            ENCOUNTERCLASS,
            COUNT(*) as num_encounters,
            ROUND(AVG(TOTAL_CLAIM_COST), 2) as avg_cost,
            ROUND(MIN(TOTAL_CLAIM_COST), 2) as min_cost,
            ROUND(MAX(TOTAL_CLAIM_COST), 2) as max_cost
        FROM encounters
        GROUP BY ENCOUNTERCLASS
        ORDER BY avg_cost DESC
    """,
    
    'insurance_coverage_by_provider.csv': """
        SELECT 
            payers.NAME as insurance_company,
            COUNT(p.CODE) as procedures_covered,
            ROUND(AVG(e.PAYER_COVERAGE), 2) as avg_coverage_amount
        FROM procedures p
        JOIN encounters e ON p.ENCOUNTER = e.Id
        JOIN payers ON e.PAYER = payers.Id
        WHERE e.PAYER_COVERAGE > 0
        GROUP BY payers.NAME
        ORDER BY procedures_covered DESC
    """
}

# Execute queries and save to CSV
for filename, query in queries.items():
    print(f"Executing query for {filename}...")
    cursor.execute(query)
    
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(results)
    
    print(f"  ✓ Saved {len(results)} rows to {filename}")

cursor.close()
conn.close()

print("\nAll results exported successfully!")
print(f"Files saved to: {output_dir}")