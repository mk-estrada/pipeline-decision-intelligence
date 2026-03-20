# sales_pipeline profile

## Dataset summary
- Rows: 8800
- Columns: 8
- Potential Unique fields: opportunity_id
- Likely join fields: opportunity_id, sales_agent, product, account

## Column summary

| Column | Dtype | Null Count | Null % | Unique Count |
|---|---|---:|---:|---:|
| opportunity_id | str | 0 | 0.0 | 8800 |
| sales_agent | str | 0 | 0.0 | 30 |
| product | str | 0 | 0.0 | 7 |
| account | str | 1425 | 16.19 | 85 |
| deal_stage | str | 0 | 0.0 | 4 |
| engage_date | str | 500 | 5.68 | 421 |
| close_date | str | 2089 | 23.74 | 306 |
| close_value | float64 | 2089 | 23.74 | 2051 |

## Notes
- `opportunity_id` appears to be the primary key, indicating this table is at the opportunity (deal) grain.
- This table functions as a transactional fact table capturing sales pipeline activity.
- Missingness in `close_date` and `close_value` (~24%) likely corresponds to open or unclosed opportunities rather than data quality issues.
- `account` has moderate missingness (~16%), which may impact join completeness with the accounts table and should be evaluated before modeling.
- `engage_date` has relatively low missingness and likely represents the start of the sales process, though missing values may require validation.
- `sales_agent`, `product`, and `account` appear to be key foreign keys for joining to dimension tables.
- This table is suitable as the central fact table in downstream modeling and analytics.
- This table will likely drive revenue forecasting and pipeline performance analysis in downstream use cases.