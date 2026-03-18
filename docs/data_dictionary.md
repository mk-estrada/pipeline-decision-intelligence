# Data Dictionary

This document defines the structure, meaning, and analytical use of datasets used in the revenue forecasting system. It is intended to support data understanding, quality validation, and downstream modeling.

## 1. Dataset Overview

### sales_pipeline.csv
- **Business purpose:** Stores opportunity-level pipeline data used to evaluate pipeline health, conversion dynamics, and forecast expected revenue outcomes.
- **Grain:** One row per opportunity
- **Primary key:** `opportunity_id` 
- **Potential join keys:** `sales_agent`, `product`, `account`
- **Notes:** Primary analytical dataset for forecast and pipeline health analysis.

---

## 2. Column Definitions — sales_pipeline.csv

| Column Name | Description | Data Type | Example | Notes |
|-------------|-------------|-----------|---------|-------|
| opportunity_id | Unique identifier for each opportunity | string | 1C1I7A6R | Should be unique |
| sales_agent | Identifier for Assigned sales representative or account owner responsible for progressing the opportunity | string | Moses Frase | Likely joins to sales_teams table |
| product | Identifier for product | string | GTX Plus Basic | Likely joins to products table. May want to split product for more detail (ex. GTX Plus vs GTXPro) |
| account | Identifier for account | string | Cancity | Likely joins to accounts table |
| deal_stage | Current lifecycle stage of the opportunity, used to assess pipeline progression, conversion likelihood, and forecast confidence. | str | Won | May need futher definition about what each stage means/signifies |
| engage_date | Date when the opportunity entered the pipeline, used for stage aging and sales cycle analysis. | str | 2016-10-25 | May need date conversion and breakout by year, month, day |
| close_date | Date when the opportunity is expected or was actually closed, used for revenue timing and forecasting alignment. | str | 2017-03-11 | May need date conversion and breakout by year, month, day |
| close_value | Estimated or realized revenue associated with the opportunity, used as the primary input for revenue forecasting and pipeline valuation. | float64 | 4514.0 | Primary metric used for pipeline valuation and revenue forecasting |

---

## 3. Initial Data Quality Observations — sales_pipeline.csv

- Missing values observed in: `close_date`, `close_value`, `account`, `engage_date`
- `deal_stage` contains four primary categories (Won, Lost, Engaging, Prospecting), suggesting a simplified pipeline model
- Opportunity-level grain appears consistent (one row per opportunity)
- Potential ambiguity in `close_value` (unclear whether it represents forecasted vs realized revenue)
- Date fields (`engage_date`, `close_date`) require type conversion and validation for temporal analysis

---

## 4. Open Questions / Assumptions — sales_pipeline.csv

- Assume one row represents one pipeline opportunity 
- Assume `close_value` is gross opportunity value in USD unless documentation indicates otherwise
- Assume `close_date` is forecasted close date unless business logic suggests actual close date

---

## 5. Analytical Considerations
- `deal_stage` and `engage_date` together enable stage duration and pipeline velocity analysis
- `close_value` combined with stage progression can support weighted pipeline forecasting
- Joining with `sales_teams` enables performance segmentation by rep, manager, and region
- Financial fields may use different unit scales across datasets (e.g., `sales_price` in USD vs. `revenue` potentially in millions), requiring normalization prior to aggregation and forecasting
---
## 6. Additional Datasets

### accounts.csv
- **Business purpose:** Contains account-level information for customers associated with opportunities
- **Grain:** One row per account (assumed)
- **Primary key:** `account` (assumed; no surrogate key provided)
- **Potential join keys:** `account`

| Column Name | Description | Data Type | Example | Notes |
|-------------|-------------|-----------|---------|-------|
| account | Customer account identifier | str | Acme Corporation | Likely join key. May want to establish an ID column |
| sector | Customer industry classification | str | technology | May have inconsistent categories |
| year_established | Year account was established | int64 | 1996 | Confirm this is company-based vs relationship-based |
| revenue | Customer account revenue | float64 | 251.41 | Confirm if this is company-based or relationship-based |
| employees | Customer account number of employees | int64 | 2822 | Check ranges for company size |
| office_location | Primary geographic location of the account | str | United States | Confirm consistency of location formatting
| subsidiary_of | Identifier for parent company if the account is a subsidiary | str | Acme Corporation | Null values observed |

### Notes (Data Quality Observations /  Questions / Assumptions) — accounts.csv
- Confirmed account is unique
- Is the year_established a company or relationship data point?
- Need more information about the revenue field
- Is or how is the employee field used?
- Most offices are in the US
- Most accounts are not subsidiaries
- Account attributes (sector, revenue, employees) can support segmentation analysis for pipeline performance and deal sizing




### metadata.csv
- **Business purpose:** Description of each of the columns in each raw data file
- **Grain:** One row per column per raw data file
- **Primary key:** None
- **Potential join keys:** `Table`

| Column Name | Description | Data Type | Example | Notes |
|-------------|-------------|-----------|---------|-------|
| Table | Table name within the raw datasets | str | accounts | Includes accounts, sales_teams and sales_pipeline details |
| Field | Column name within the dataset | str | sector | Metadata coverage appears incomplete and may not fully describe all fields present in the raw datasets. |
| Description | Description of what the column represents | str | Annual revenue (in millions of USD) | Helps to address some questions  |

### Notes (Data Quality Observations /  Questions / Assumptions) — metadata.csv
- Metadata coverage appears incomplete and may not fully describe all fields used in analysis
- May require manual supplementation during data modeling




### products.csv
- **Business purpose:** Contains product-level information used to enrich opportunity data with pricing and product categorization
- **Grain:** One row per product
- **Primary key:** product
- **Potential join keys:** product, series

| Column Name | Description | Data Type | Example | Notes |
|-------------|-------------|-----------|---------|-------|
| product | Product name identifier | str | GTX Basic | Likely join key |
| series | Series name identifier | str | GTX | Likely only 2 series values |
| sales_price | price of the product | str | 550 | Price assumed to be as is, not in millions |

### Notes (Data Quality Observations /  Questions / Assumptions) — products.csv
- Sales price is recorded in USD (not scaled), unlike certain aggregate financial fields




### sales_teams.csv
- **Business purpose:** Contains sales team hierarchy and regional assignment data used to analyze performance across sales agents, managers, and regions.
- **Grain:** One row per sales agent
- **Primary key:** sales_agent
- **Potential join keys:** sales_agent, regional_office

| Column Name | Description | Data Type | Example | Notes |
|-------------|-------------|-----------|---------|-------|
| sales_agent | sales agent identifier | str | Anna Snelling | Likely join key |
| manager | sales manager identifier | str | Dustin Brinkmann | 6 managers |
| regional_office | sales office identifier | str | Central | 3 regional offices |

### Notes (Data Quality Observations /  Questions / Assumptions) — sales_teams.csv
- No null values, all sales_agents unique
 

