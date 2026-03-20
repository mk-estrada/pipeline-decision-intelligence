# metadata profile

## Dataset summary
- Rows: 21
- Columns: 3
- Potential Unique fields: None identified
- Likely join fields: table, field

## Column summary

| Column | Dtype | Null Count | Null % | Unique Count |
|---|---|---:|---:|---:|
| table | str | 0 | 0.0 | 4 |
| field | str | 0 | 0.0 | 18 |
| description | str | 0 | 0.0 | 18 |

## Notes
- This table functions as a metadata/data dictionary describing tables and fields in the dataset.
- It is not intended for use in analytical joins or modeling.
- The combination of `table` and `field` likely represents the grain of the dataset.
- This table can be useful for documentation, field interpretation, and validating assumptions during analysis.