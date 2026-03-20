# accounts profile

## Dataset summary
- Rows: 85
- Columns: 7
- Potential Unique fields: account, revenue, employees
- Likely join fields: account

## Column summary

| Column | Dtype | Null Count | Null % | Unique Count |
|---|---|---:|---:|---:|
| account | str | 0 | 0.0 | 85 |
| sector | str | 0 | 0.0 | 10 |
| year_established | int64 | 0 | 0.0 | 35 |
| revenue | float64 | 0 | 0.0 | 85 |
| employees | int64 | 0 | 0.0 | 85 |
| office_location | str | 0 | 0.0 | 15 |
| subsidiary_of | str | 70 | 82.35 | 7 |

## Notes
- `account` appears to be the practical business key for this table.
- `subsidiary_of` has high missingness and likely represents an optional parent-company relationship.
- This table appears suitable for use as an account dimension in downstream modeling.