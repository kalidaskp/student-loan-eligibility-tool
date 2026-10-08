DROP TABLE IF EXISTS student_applications;

CREATE TABLE student_applications (
    application_id VARCHAR(20) PRIMARY KEY,
    student_age INTEGER,
    nationality VARCHAR(50),
    visa_type VARCHAR(50),
    visa_end_date DATE,
    university VARCHAR(100),
    program_level VARCHAR(30),
    enrollment_status VARCHAR(30),
    program_end_date DATE,
    annual_tuition NUMERIC(12, 2),
    annual_living_cost NUMERIC(12, 2),
    savings NUMERIC(12, 2),
    monthly_part_time_income NUMERIC(12, 2),
    family_support_annual NUMERIC(12, 2),
    existing_debt NUMERIC(12, 2),
    requested_loan_amount NUMERIC(12, 2),
    loan_duration_months INTEGER,
    guarantor_exists VARCHAR(10),
    guarantor_french_resident VARCHAR(10),
    guarantor_annual_income NUMERIC(12, 2),
    application_date DATE,
    decision VARCHAR(30),
    hard_failure_count INTEGER,
    condition_count INTEGER,
    eligibility_reasons TEXT
);