import random
from pathlib import Path

import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

N_APPLICATIONS = 150

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "student_applications_micro_loan.csv"
)

universities = [
    "Paris Dauphine",
    "Sorbonne University",
    "ESSEC",
    "HEC Paris",
    "Université Paris-Saclay",
    "Sciences Po",
]

nationalities = [
    "India",
    "China",
    "Brazil",
    "Nigeria",
    "Vietnam",
    "Turkey",
    "Morocco",
    "USA",
    "Germany",
    "Italy",
]

visa_types = [
    "Student visa",
    "Residence permit",
]

rows = []

for i in range(1, N_APPLICATIONS + 1):
    application_date = pd.Timestamp("2026-10-08")

    guarantor_exists = np.random.choice(["Yes", "No"], p=[0.7, 0.3])

    if guarantor_exists == "Yes":
        guarantor_french_resident = np.random.choice(
            ["Yes", "No"],
            p=[0.8, 0.2],
        )
        guarantor_annual_income = np.random.choice(
            [15000, 25000, 35000, 50000, 70000],
            p=[0.2, 0.25, 0.25, 0.2, 0.1],
        )
    else:
        guarantor_french_resident = "No"
        guarantor_annual_income = 0

    rows.append(
        {
            "application_id": f"MICRO{i:04d}",
            "student_age": np.random.randint(19, 32),
            "nationality": random.choice(nationalities),
            "visa_type": random.choice(visa_types),
            "visa_end_date": (
                application_date
                + pd.DateOffset(months=np.random.randint(3, 36))
            ).date(),
            "university": random.choice(universities),
            "program_level": random.choice(["Bachelor", "Master", "PhD"]),
            "enrollment_status": np.random.choice(
                ["Enrolled", "Not enrolled"],
                p=[0.9, 0.1],
            ),
            "program_end_date": (
                application_date
                + pd.DateOffset(months=np.random.randint(6, 36))
            ).date(),
            "annual_tuition": np.random.choice(
                [0, 3000, 8000, 12000, 15000, 20000],
                p=[0.2, 0.15, 0.2, 0.2, 0.15, 0.1],
            ),
            "annual_living_cost": np.random.randint(9000, 18000),
            "savings": np.random.choice(
                [0, 1000, 3000, 6000, 10000, 15000],
                p=[0.1, 0.15, 0.25, 0.2, 0.2, 0.1],
            ),
            "monthly_part_time_income": np.random.choice(
                [0, 300, 500, 700, 900],
                p=[0.3, 0.2, 0.2, 0.2, 0.1],
            ),
            "family_support_annual": np.random.choice(
                [0, 2000, 5000, 8000, 12000],
                p=[0.2, 0.2, 0.25, 0.2, 0.15],
            ),
            "existing_debt": np.random.choice(
                [0, 1000, 3000, 6000],
                p=[0.5, 0.2, 0.2, 0.1],
            ),
            "requested_loan_amount": np.random.choice(
                [500, 1000, 2000, 3000, 4000],
                p=[0.10, 0.20, 0.30, 0.25, 0.15],
            ),
            "loan_duration_months": np.random.choice(
                [3, 6, 9, 12, 15, 18],
                p=[0.10, 0.15, 0.20, 0.25, 0.15, 0.15],
            ),
            "guarantor_exists": guarantor_exists,
            "guarantor_french_resident": guarantor_french_resident,
            "guarantor_annual_income": guarantor_annual_income,
            "application_date": application_date.date(),
        }
    )

df = pd.DataFrame(rows)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)

print("Created 150 synthetic short-term micro-loan applications.")
print(f"Saved file to: {OUTPUT_PATH}")
print(df.head())