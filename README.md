# Student Loan Eligibility & Risk-Screening Tool

A rule-based tool that helps bank credit analysts assess whether an international
student is eligible for a student loan in France.

The tool checks applicant information against predefined eligibility rules,
identifies missing documents or risk factors, and returns one of three decisions:

- Eligible
- Conditionally eligible
- Not eligible

## Problem

International students in France may face difficulty obtaining student loans because
banks often require a French-resident guarantor and apply strict eligibility criteria.

This project creates a simple decision-support workflow for bank staff to assess
student-loan applications consistently.

## Scope

This is Version 1 of the project:

- Synthetic student-loan application data
- PostgreSQL database design
- Python rule-based eligibility engine
- Decision output: Eligible / Conditional / Not eligible
- SQL analysis of approval patterns and rejection reasons

This is not a production credit-scoring model and does not make final lending decisions.

## Tools

- Python
- Pandas
- PostgreSQL
- SQL
- Git & GitHub

## Project structure

student-loan-eligibility-tool/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── sql/
│   └── create_tables.sql
│
├── python/
│   ├── generate_data.py
│   └── eligibility_checker.py
│
├── README.md
└── requirements.txt

## Data

The dataset is synthetic and contains no real personal or financial data.
