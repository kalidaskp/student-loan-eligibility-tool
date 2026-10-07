from pathlib import Path

import pandas as pd

BANK_MAX_LOAN = 20_000
BANK_MAX_DURATION_MONTHS = 120
MIN_GUARANTOR_INCOME = 25_000
MIN_SAVINGS_MONTHS = 3

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "raw" / "student_applications_raw.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "student_applications_scored.csv"


def evaluate_application(row):
    hard_failures = []
    conditions = []

    application_date = pd.to_datetime(row["application_date"])
    visa_end_date = pd.to_datetime(row["visa_end_date"])
    loan_end_date = application_date + pd.DateOffset(
        months=int(row["loan_duration_months"])
    )

    # Hard eligibility rules
    if row["student_age"] < 18:
        hard_failures.append("Applicant is under 18.")

    if row["enrollment_status"] != "Enrolled":
        hard_failures.append("Applicant is not enrolled in a recognised institution.")

    if row["requested_loan_amount"] > BANK_MAX_LOAN:
        hard_failures.append(
            f"Requested loan exceeds the bank maximum of €{BANK_MAX_LOAN:,}."
        )

    if row["loan_duration_months"] > BANK_MAX_DURATION_MONTHS:
        hard_failures.append(
            f"Loan duration exceeds the bank maximum of {BANK_MAX_DURATION_MONTHS} months."
        )

    if visa_end_date < loan_end_date:
        hard_failures.append("Visa expires before the loan is scheduled to end.")

    if row["guarantor_exists"] != "Yes":
        hard_failures.append("No guarantor has been provided.")

    if row["guarantor_french_resident"] != "Yes":
        hard_failures.append("Guarantor is not a French resident.")

    if row["guarantor_annual_income"] < MIN_GUARANTOR_INCOME:
        hard_failures.append(
            f"Guarantor income is below €{MIN_GUARANTOR_INCOME:,} per year."
        )

    # Financial checks for conditional eligibility
    monthly_living_cost = row["annual_living_cost"] / 12
    required_savings = monthly_living_cost * MIN_SAVINGS_MONTHS

    if row["savings"] < required_savings:
        conditions.append("Savings cover less than three months of living costs.")

    annual_part_time_income = row["monthly_part_time_income"] * 12
    total_available_funds = (
        row["savings"]
        + annual_part_time_income
        + row["family_support_annual"]
    )
    annual_study_cost = row["annual_tuition"] + row["annual_living_cost"]

    if total_available_funds < annual_study_cost:
        conditions.append(
            "Available funds do not cover annual tuition and living costs."
        )

    if row["existing_debt"] > 5_000:
        conditions.append("Existing debt is above €5,000.")

    if row["requested_loan_amount"] > total_available_funds:
        conditions.append(
            "Requested loan is higher than the applicant's documented available funds."
        )

    # Final decision
    if hard_failures:
        decision = "Not eligible"
        reasons = hard_failures + conditions
    elif conditions:
        decision = "Conditional"
        reasons = conditions
    else:
        decision = "Eligible"
        reasons = ["All eligibility rules passed."]

    return pd.Series(
        {
            "decision": decision,
            "hard_failure_count": len(hard_failures),
            "condition_count": len(conditions),
            "eligibility_reasons": " | ".join(reasons),
        }
    )


def main():
    df = pd.read_csv(INPUT_PATH)

    results = df.apply(evaluate_application, axis=1)
    scored_df = pd.concat([df, results], axis=1)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    scored_df.to_csv(OUTPUT_PATH, index=False)

    print("Eligibility checking completed.")
    print("\nDecision summary:")
    print(scored_df["decision"].value_counts())

    print("\nSample results:")
    print(
        scored_df[
            [
                "application_id",
                "requested_loan_amount",
                "decision",
                "hard_failure_count",
                "condition_count",
                "eligibility_reasons",
            ]
        ].head(10)
    )

    print(f"\nSaved scored dataset to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()