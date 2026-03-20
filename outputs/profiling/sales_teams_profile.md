# sales_teams profile

## Dataset summary
- Rows: 35
- Columns: 3
- Potential Unique fields: sales_agent
- Likely join fields: sales_agent

## Column summary

| Column | Dtype | Null Count | Null % | Unique Count |
|---|---|---:|---:|---:|
| sales_agent | str | 0 | 0.0 | 35 |
| manager | str | 0 | 0.0 | 6 |
| regional_office | str | 0 | 0.0 | 3 |

## Notes
## Notes
- `sales_agent` appears to be the practical business key for this table.
- This table functions as a dimension table describing the sales organization at the agent level.
- `manager` and `regional_office` define a hierarchical grouping (agent → manager → region) that can support aggregation and performance analysis.
- This table is suitable for use as a sales team dimension, with `sales_agent` serving as the join key to the sales pipeline fact table.