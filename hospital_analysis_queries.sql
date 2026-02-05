-- Hospital Patient Records Analysis
-- Massachusetts General Hospital Data (2011-2022)
-- Analyst: Michael Galvan

-- ============================================
-- QUESTION 1: Admissions and Readmissions Over Time
-- ============================================

-- Admissions by year with readmission rates
SELECT 
    YEAR(START) as year,
    COUNT(*) as total_admissions,
    COUNT(DISTINCT PATIENT) as unique_patients,
    COUNT(*) - COUNT(DISTINCT PATIENT) as readmissions,
    ROUND(100.0 * (COUNT(*) - COUNT(DISTINCT PATIENT)) / COUNT(*), 1) as readmission_rate_pct
FROM encounters
WHERE ENCOUNTERCLASS = 'inpatient'
GROUP BY YEAR(START)
ORDER BY year;

-- ============================================
-- QUESTION 2: Length of Stay Analysis
-- ============================================

-- Overall length of stay statistics
SELECT 
    AVG(DATEDIFF(STOP, START)) as avg_length_of_stay_days,
    MIN(DATEDIFF(STOP, START)) as min_stay_days,
    MAX(DATEDIFF(STOP, START)) as max_stay_days,
    COUNT(*) as total_inpatient_stays
FROM encounters
WHERE ENCOUNTERCLASS = 'inpatient';

-- Length of stay distribution
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
ORDER BY MIN(DATEDIFF(STOP, START));

-- ============================================
-- QUESTION 3: Cost Analysis
-- ============================================

-- Overall cost statistics across all encounters
SELECT 
    ROUND(AVG(BASE_ENCOUNTER_COST), 2) as avg_base_cost,
    ROUND(AVG(TOTAL_CLAIM_COST), 2) as avg_total_claim,
    ROUND(AVG(PAYER_COVERAGE), 2) as avg_insurance_coverage,
    ROUND(AVG(TOTAL_CLAIM_COST - PAYER_COVERAGE), 2) as avg_patient_responsibility,
    COUNT(*) as total_encounters
FROM encounters;

-- Cost breakdown by encounter type
SELECT 
    ENCOUNTERCLASS,
    COUNT(*) as num_encounters,
    ROUND(AVG(TOTAL_CLAIM_COST), 2) as avg_cost,
    ROUND(MIN(TOTAL_CLAIM_COST), 2) as min_cost,
    ROUND(MAX(TOTAL_CLAIM_COST), 2) as max_cost
FROM encounters
GROUP BY ENCOUNTERCLASS
ORDER BY avg_cost DESC;

-- ============================================
-- QUESTION 4: Insurance Coverage Analysis
-- ============================================

-- Procedure coverage statistics
SELECT 
    COUNT(*) as total_procedures,
    COUNT(CASE WHEN e.PAYER_COVERAGE > 0 THEN 1 END) as procedures_with_coverage,
    COUNT(CASE WHEN e.PAYER_COVERAGE = 0 THEN 1 END) as procedures_no_coverage,
    ROUND(100.0 * COUNT(CASE WHEN e.PAYER_COVERAGE > 0 THEN 1 END) / COUNT(*), 1) as pct_with_coverage
FROM procedures p
JOIN encounters e ON p.ENCOUNTER = e.Id;

-- Coverage by insurance provider
SELECT 
    payers.NAME as insurance_company,
    COUNT(p.CODE) as procedures_covered,
    ROUND(AVG(e.PAYER_COVERAGE), 2) as avg_coverage_amount
FROM procedures p
JOIN encounters e ON p.ENCOUNTER = e.Id
JOIN payers ON e.PAYER = payers.Id
WHERE e.PAYER_COVERAGE > 0
GROUP BY payers.NAME
ORDER BY procedures_covered DESC;