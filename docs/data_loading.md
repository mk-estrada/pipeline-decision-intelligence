# Data Loading Plan

## Interim file to RAW tables mapping
accounts.csv -> accounts_raw
products.csv -> products_raw
sales_pipeline.csv -> sales_pipeline_raw
sales_teams.csv -> sales_teams_raw

## Loader design

The RAW loading step uses a Python script with:
- explicit file-to-table mapping
- pandas for reading interim CSVs
- Snowflake write_pandas for warehouse loading
- overwrite behavior for repeatable reloads

This keeps the ingestion layer simple and reproducible before dbt staging.

## Naming note

Tables loaded via write_pandas were created as quoted lowercase identifiers in Snowflake.
Example:
"sales_teams_raw"

This means RAW validation queries currently need quoted table references.
This can be cleaned up later if desired, but it does not block staging/modeling.


## Confirm Loaded SQL
select count(*) from REV_FORECASTING.RAW."sales_teams_raw";
select count(*) from REV_FORECASTING.RAW."accounts_raw";
select count(*) from REV_FORECASTING.RAW."products_raw";
select count(*) from REV_FORECASTING.RAW."sales_pipeline_raw";

## Outcome

Clean interim datasets are now loaded into Snowflake RAW and can serve as source tables for dbt.
Snowflake is now the warehouse landing layer for the project.

