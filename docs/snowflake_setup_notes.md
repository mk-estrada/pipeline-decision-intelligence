# Snowflake Environment Decisions

## Database
REV_FORECASTING

## Warehouse
REV_FORECASTING_WH

## Schemas
RAW
ANALYTICS
SANDBOX

## Purpose
- RAW: loaded source/interim data from local Python pipeline
- ANALYTICS: dbt models for transformed business-ready tables
- SANDBOX: scratch space for exploratory SQL

## Naming convention
Use descriptive lowercase table names like:
- accounts_raw
- products_raw
- sales_pipeline_raw
- sales_teams_raw

## Snowflake UI orientation

### Worksheets
Used to run setup SQL, validation SQL, and later ad hoc queries.

### Warehouses
REV_FORECASTING_WH is the compute engine for loading and querying data.

### Database
REV_FORECASTING is the top-level project container.

### Schemas
- RAW: landing area for loaded interim/source data
- ANALYTICS: dbt-generated transformed models
- SANDBOX: optional scratch area for exploratory SQL

### Query History
Useful for debugging failed queries, reviewing loads, and checking executed SQL.

## Local-to-warehouse mapping

The local Python pipeline was used to:
- standardize columns
- normalize nulls
- profile source tables
- validate key data quality rules

Snowflake will now be used to:
- store clean landed source/interim data in RAW
- support reproducible SQL transformations
- provide source tables for dbt
- enable downstream analytics modeling in ANALYTICS

This avoids unnecessary duplication:
local Python established understanding and data quality,
while Snowflake becomes the warehouse layer for scalable transformation.
