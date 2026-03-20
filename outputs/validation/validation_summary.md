# Validation Summary

This report summarizes dataset-level validation checks for interim source tables.

## Overall Summary

- Total checks run: 15
- Total checks passed: 15
- Total failed: 0

## accounts.csv

- Total checks: 4
- Passed: 4
- Failed: 0

| Check Type | Column | Passed | Details |
|---|---|---|---|
| unique | account | True | unique_count=85 of 85 |

## metadata.csv

- Total checks: 0
- Passed: 0
- Failed: 0

| Check Type | Column | Passed | Details |
|---|---|---|---|
- No validation rules configured for this table.

## products.csv

- Total checks: 4
- Passed: 4
- Failed: 0

| Check Type | Column | Passed | Details |
|---|---|---|---|
| unique | product | True | unique_count=7 of 7 |

## sales_pipeline.csv

- Total checks: 5
- Passed: 5
- Failed: 0

| Check Type | Column | Passed | Details |
|---|---|---|---|
| unique | opportunity_id | True | unique_count=8800 of 8800 |

## sales_teams.csv

- Total checks: 2
- Passed: 2
- Failed: 0

| Check Type | Column | Passed | Details |
|---|---|---|---|
| unique | sales_agent | True | unique_count=35 of 35 |
