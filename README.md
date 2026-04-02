# Decision Intelligence System for Revenue Forecasting

## Executive Summary

This project simulates a decision intelligence system designed to improve revenue forecasting and pipeline visibility using CRM opportunity data.

Rather than focusing only on predictive modeling, the project evaluates the operational drivers of pipeline performance and provides actionable recommendations to improve forecast reliability.

### Executive Summary: Pipeline Performance

The pipeline is currently weighted toward historical activity, with approximately 80% of opportunities already closed and only 20% remaining open. Despite this, conversion performance is strong, with a win rate of ~63%, indicating an effective sales motion once deals reach closure.

From a value perspective, the pipeline is driven primarily by high-volume, lower-value deals, with limited contribution from large opportunities. To date, the business has generated approximately $1M in won revenue, while the current open pipeline represents ~$3.3M in potential value. If historical conversion rates hold, this suggests an additional ~$2M in expected revenue, effectively doubling realized performance.

However, there is a notable disconnect between sales velocity and pipeline aging. While closed deals move efficiently, with an average cycle time of ~50 days, open opportunities have an average age of nearly 200 days. This gap suggests a portion of the pipeline may be stalled or lower quality, representing an opportunity for improved pipeline management, qualification, or prioritization.

## Business Problem

Organizations often struggle to forecast revenue accurately due to inconsistent pipeline progression and limited visibility into deal conversion patterns.

This project explores how analytics can help leadership understand pipeline health and anticipate expected revenue outcomes.

## Project Objectives

• Assess pipeline health and conversion performance  
• Identify operational drivers of forecast volatility  
• Develop predictive revenue forecasts  
• Provide actionable recommendations based on scenario analysis  

## Analytical Workflow

1. Data ingestion and validation
2. Exploratory analysis of pipeline performance
3. Feature engineering reflecting sales process dynamics
4. Predictive modeling and forecast generation
5. Scenario analysis and recommendations

## Repository Structure
data/              raw and processed datasets
notebooks/         exploratory analysis
src/               data pipelines and analytics logic
sql/               analytical SQL queries
outputs/           charts, tables, model outputs
deliverables/      executive memo and stakeholder materials
dashboard/         visualization components


## Data Pipeline: Ingestion, Profiling, and Validation

This project follows a structured data pipeline approach to ensure data is reliable and decision-ready before modeling and analysis.

### 1. Ingestion (Local Python)

Raw CSV files are ingested and standardized into a clean intermediate layer.

Key steps:
- Standardize column names to snake_case
- Normalize null values (e.g., "", "NA", "null")
- Trim whitespace from string fields
- Coerce numeric and date fields to appropriate types
- Output cleaned datasets to `data/interim/`

This establishes a reproducible and consistent foundation for downstream processing.

---

### 2. Data Profiling

Each dataset is profiled to understand structure, quality, and modeling readiness.

Outputs:
- Row and column counts
- Null counts and percentages
- Unique value counts
- Identification of potential keys and join fields
- Table-level interpretation and modeling implications

Profiling results are written to:
`outputs/validation/validation_summary.md`


This ensures that:
- key identifiers are reliable
- critical fields meet expectations
- data is trustworthy for modeling and decision-making

---

### Summary

This layered approach ensures that data is:
- Clean (ingestion)
- Understood (profiling)
- Trusted (validation)

before being used in downstream analytics, forecasting, and decision intelligence.

This design mirrors modern analytics engineering practices, where data quality is enforced early in the pipeline before transformation and modeling.

## RAW tables
accounts.csv -> accounts_raw
products.csv -> products_raw
sales_pipeline.csv -> sales_pipeline_raw
sales_teams.csv -> sales_teams_raw

## Technology Stack

Python (pandas) 
SQL  
Snowflake  
dbt  
scikit-learn  
Plotly / dashboards


## Data Architecture

staging → intermediate → marts

- staging: cleaned source data
- intermediate: enriched opportunity-level model
- marts: decision-ready metrics and analytics

## Key Models

### int_sales_pipeline_enriched
Canonical opportunity-level dataset with lifecycle, timing, and enrichment fields.

### mart_pipeline_summary
Executive KPI layer summarizing pipeline performance, conversion, value, and velocity.

## Key Metrics

- Win Rate = Won / Closed Opportunities
- Estimated Open Pipeline Value = proxy using sales price and available deal values
- Avg Sales Cycle = avg days from engage to close (closed deals)
- Avg Open Deal Age = age of open deals as of dataset analysis date