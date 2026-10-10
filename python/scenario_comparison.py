from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED = PROJECT_ROOT / "data" / "processed"

SCENARIO_A_PATH = PROCESSED / "student_applications_original_scored.csv"
SCENARIO_B_PATH = PROCESSED / "student_applications_micro_loan_scored.csv"
COMBINED_PATH = PROCESSED / "student_applications_combined.csv"
SUMMARY_PATH = PROCESSED / "scenario_comparison_summary.csv"


def summarize_scenario(df, scenario_name):
    summary = (
        df["decision"]
        .value_counts()
        .rename_axis("decision")
        .reset_index(name="application_count")
    )
    summary["scenario"] = scenario_name
    summary["percentage"] = (
        summary["application_count"] / len(df) * 100
    ).round(1)
    return summary[["scenario", "decision", "application_count", "percentage"]]


def main():
    scenario_a = pd.read_csv(SCENARIO_A_PATH)
    scenario_b = pd.read_csv(SCENARIO_B_PATH)

    print("Same columns and order:", scenario_a.columns.equals(scenario_b.columns))
    print("Only in Scenario A:", sorted(set(scenario_a.columns) - set(scenario_b.columns)))
    print("Only in Scenario B:", sorted(set(scenario_b.columns) - set(scenario_a.columns)))

    common_columns = [
        column for column in scenario_a.columns
        if column in scenario_b.columns
    ]

    scenario_a_common = scenario_a[common_columns].copy()
    scenario_b_common = scenario_b[common_columns].copy()

    scenario_a_common["scenario"] = "standard_student_loan"
    scenario_b_common["scenario"] = "short_term_micro_loan"

    combined = pd.concat(
        [scenario_a_common, scenario_b_common],
        ignore_index=True,
    )

    summary = pd.concat(
        [
            summarize_scenario(scenario_a, "standard_student_loan"),
            summarize_scenario(scenario_b, "short_term_micro_loan"),
        ],
        ignore_index=True,
    )

    COMBINED_PATH.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(COMBINED_PATH, index=False)
    summary.to_csv(SUMMARY_PATH, index=False)

    print("\nDecision comparison:")
    print(summary.to_string(index=False))

    print(f"\nCombined data saved to: {COMBINED_PATH}")
    print(f"Summary saved to: {SUMMARY_PATH}")


if __name__ == "__main__":
    main()