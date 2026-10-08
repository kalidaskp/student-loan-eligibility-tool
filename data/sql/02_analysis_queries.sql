-- 1. Overall decision breakdown
SELECT
    decision,
    COUNT(*) AS application_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS percentage_of_total
FROM student_applications
GROUP BY decision
ORDER BY application_count DESC;


-- 2. Average loan request and average savings by decision
SELECT
    decision,
    COUNT(*) AS application_count,
    ROUND(AVG(requested_loan_amount), 2) AS avg_requested_loan,
    ROUND(AVG(savings), 2) AS avg_savings,
    ROUND(AVG(existing_debt), 2) AS avg_existing_debt
FROM student_applications
GROUP BY decision
ORDER BY avg_requested_loan DESC;


-- 3. Decision outcomes by program level
SELECT
    program_level,
    decision,
    COUNT(*) AS application_count
FROM student_applications
GROUP BY program_level, decision
ORDER BY program_level, decision;


-- 4. Decision outcomes by university
SELECT
    university,
    decision,
    COUNT(*) AS application_count
FROM student_applications
GROUP BY university, decision
ORDER BY university, application_count DESC;


-- 5. Most common screening outcomes/reasons
SELECT
    decision,
    eligibility_reasons,
    COUNT(*) AS application_count
FROM student_applications
GROUP BY decision, eligibility_reasons
ORDER BY application_count DESC
LIMIT 15;
