from pathlib import Path

import pandas as pd

# Scenario B: short-term student micro-loan policy
BANK_MAX_LOAN = 4_000
BANK_MAX_DURATION_MONTHS = 18
MIN_GUARANTOR_INCOME = 25_000
MIN_SAVINGS_MONTHS = 3

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "student_applications_micro_loan.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "student_applications_micro_loan_scored.csv"
)


def evaluate_application(row):
    hard_failures = []
    conditions = []

    application_date = pd.to_datetime(row["application_date"])
    visa_end_date = pd.to_datetime(row["visa_end_date"])

    loan_end_date = application_date + pd.DateOffset(
        months=int(row["loan_duration_months"])
    )

    # Hard product-eligibility rules
    if row["student_age"] < 18:
        hard_failures.append("Applicant is under 18.")

    if row["enrollment_status"] != "Enrolled":
        hard_failures.append(
            "Applicant is not enrolled in a recognised institution."
        )

    if row["requested_loan_amount"] > BANK_MAX_LOAN:
        hard_failures.append(
            f"Requested loan exceeds the micro-loan maximum of €{BANK_MAX_LOAN:,}."
        )

    if row["loan_duration_months"] > BANK_MAX_DURATION_MONTHS:
        hard_failures.append(
            "Loan duration exceeds the micro-loan maximum of "
            f"{BANK_MAX_DURATION_MONTHS} months."
        )

    # Manual-review / conditional rules
    if visa_end_date < loan_end_date:
        conditions.append(
            "Visa expires before the loan end date; residence renewal or "
            "post-study-work evidence is required."
        )

    if row["guarantor_exists"] != "Yes":
        conditions.append(
            "No guarantor provided; manual affordability review is required."
        )

    if row["guarantor_exists"] == "Yes":
        if row["guarantor_french_resident"] != "Yes":
            conditions.append(
                "Guarantor is not a French resident; enhanced verification is required."
            )

        if row["guarantor_annual_income"] < MIN_GUARANTOR_INCOME:
            conditions.append(
                f"Guarantor income is below €{MIN_GUARANTOR_INCOME:,} per year."
            )

    monthly_living_cost = row["annual_living_cost"] / 12
    required_savings = monthly_living_cost * MIN_SAVINGS_MONTHS

    if row["savings"] < required_savings:
        conditions.append(
            "Savings cover less than three months of living costs."
        )

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

    if row["requested_loan_amount"] > total_available_funds * 1.5:
        conditions.append(
            "Requested loan is more than 150% of documented available funds."
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
        reasons = ["All micro-loan eligibility rules passed."]

    return pd.Series(
        {
            "product_type": "Short-term student micro-loan",
            "max_product_loan_amount": BANK_MAX_LOAN,
            "max_product_duration_months": BANK_MAX_DURATION_MONTHS,
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

    print("Short-term micro-loan eligibility checking completed.")
    print("\nDecision summary:")
    print(scored_df["decision"].value_counts())

    print("\nDecision percentages:")
    print(
        (scored_df["decision"].value_counts(normalize=True) * 100)
        .round(1)
        .astype(str)
        + "%"
    )

    print(f"\nSaved scored dataset to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()