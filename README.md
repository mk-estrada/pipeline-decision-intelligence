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

## Executive Summary (Pipeline)
- The pipeline reflects strong historical performance (≈60%+ win rate, ~48-day sales cycle), but current pipeline quality is materially weaker, with over $1.3M in aged or stalled opportunities and average open deal age (~198 days) far exceeding typical cycle times.
- As a result, headline pipeline value likely overstates near-term revenue potential, since a significant portion of open opportunities may not be actively progressing or realistically convertible.
- Pipeline risk is driven less by conversion performance and more by pipeline quality and data integrity, with over half of open opportunities classified as stale or unknown and gaps in key deal-level fields limiting visibility.
- These risks are not evenly distributed—they are concentrated in specific regions (e.g., West aging, Central data gaps) and segments (e.g., small deal volume, large deal unpredictability), indicating that targeted interventions will be more effective than broad process changes.
- The pipeline reflects distinct commercial motions across deal sizes, requiring a segmented approach to forecasting and management rather than a single, uniform assumption for conversion and timing.
Improving pipeline hygiene, deal progression discipline, and segmentation quality represents a near-term opportunity to increase forecast accuracy and unlock additional value without requiring increased top-of-funnel volume.
- The primary risks to revenue performance are:
    -  inflated pipeline value due to aged or stalled opportunities
    - incomplete or inconsistent data reducing visibility into deal quality and progression

This analysis informs the forecasting approach described in the [Forecast Design](#forecast-design) section.

## Forecast Design

### Objective

The goal of the forecasting model is to estimate probability-weighted expected revenue from the current open pipeline over a 90-day horizon. The forecast is designed to reflect both historical conversion performance and the current condition of each opportunity, with results segmented by deal size and region.

---

### Forecast Outputs

The model produces:

- Total expected revenue over the next 90 days  
- Expected revenue segmented by deal size and region  
- Pipeline value at risk due to aging or stalled opportunities  

These outputs are designed to support leadership decision-making by providing both a headline forecast and visibility into where revenue risk is concentrated.

---

### Key Drivers of Deal Outcomes

Based on pipeline analysis, the most important drivers of deal conversion include:

- Deal size segment  
- Deal age relative to expected sales cycle  
- Pipeline health (active vs stale vs unknown)  
- Regional differences in pipeline quality and data completeness  

---

### Probability Framework

Each opportunity is assigned an adjusted probability of closing based on:

> **Adjusted Probability = Base Win Rate × Age Multiplier**

- Base win rate is determined by historical conversion performance within each deal-size segment  
- Age multiplier adjusts probability based on how far a deal has progressed relative to expected sales cycle timing  

This approach reflects the observation that open pipeline behavior differs significantly from closed deal performance.

---

### Deal Age Segmentation

Opportunities are classified based on deal age:

- **Healthy:** ≤ 60 days  
- **Slightly Aged:** 61–120 days  
- **Aging:** 121–200 days  
- **Stale:** > 200 days  
- **Unknown:** Missing deal age  

This segmentation is designed to reflect increasing risk as deals exceed the typical ~48-day sales cycle.

---

### Age-Based Probability Adjustments

Each age bucket is assigned a multiplier:

- **Healthy:** 1.0  
- **Slightly Aged:** 0.85  
- **Aging:** 0.65  
- **Stale:** 0.35  
- **Unknown:** 0.5  

These multipliers represent decreasing confidence in deal conversion as opportunities age or lack sufficient data.

---

### Forecast Calculation

At the deal level:

> **Expected Revenue = Estimated Deal Value × Adjusted Close Probability**

Where:

> **Adjusted Close Probability = Base Win Rate × Age Multiplier**

This produces a probability-weighted estimate of revenue that accounts for both historical performance and current pipeline conditions.

---

### Key Assumptions

- Historical win rates are a reasonable baseline for future conversion  
- Deal age is a strong indicator of likelihood to close  
- Aging and stale opportunities are less likely to convert within the forecast horizon  
- Missing or incomplete data reduces forecast confidence  
- Forecast accuracy improves with segmentation by deal size and region  

## Forecast Findings

The forecasting model reveals a significant gap between headline pipeline value and realistically expected near-term revenue.

- While the open pipeline totals approximately **$3.3M**, the probability-weighted forecast estimates only **~$1.2M** in expected revenue over the next 90 days, reflecting a ~60% reduction after adjusting for deal age and pipeline quality.

- Approximately **90% of open opportunities are classified as at risk**, driven by aging deals, stalled progression, or missing data. This indicates that pipeline risk is widespread rather than isolated.

- **Pipeline risk is highly concentrated in aging, stale, and unknown opportunities**, which together account for nearly the entire pipeline value. These segments drive the majority of forecast uncertainty and revenue discounting.

- **Medium-sized deals emerge as the most forecast-efficient segment**, with the highest expected-revenue-to-pipeline ratio, while **large deals are the least predictable**, reinforcing the need for differentiated forecasting approaches by deal size.

- Regional analysis highlights distinct risk profiles:
  - **West** carries the largest pipeline but the lowest forecast efficiency, with a high concentration of stale opportunities.
  - **Central** shows the highest forecast ratio but is **100% at risk**, driven by a mix of unknown and aging deals, indicating low confidence due to data gaps and delayed progression.
  - **East** appears more balanced, with moderate forecast efficiency and lower overall exposure.

Overall, the model demonstrates that **raw pipeline value is not a reliable proxy for expected revenue**, and that incorporating deal condition, segmentation, and data quality provides a more realistic and actionable forecast.

These findings are derived from the forecasting approach described in the [Forecast Design](#forecast-design) section.

## ML Findings (Lightweight Enhancement)

To complement the rule-based forecast, a lightweight logistic regression model was trained on historical closed opportunities using deal size, region, product, and deal age.

The model achieved an ROC AUC of **0.729**, indicating that historical opportunity features provide meaningful signal for distinguishing won from lost deals. Its value was strongest as a **probability-ranking tool** rather than a strict binary classifier.

Key findings from the model include:

- **Unknown deal size** was a strongly negative signal, reinforcing the importance of complete segmentation and CRM discipline.
- **Deal size** carried meaningful predictive value, supporting the use of segmented forecasting assumptions rather than one uniform win-rate assumption.
- **Product mix** appeared to matter significantly, with some product lines associated with stronger close outcomes than others.
- **Region** had a comparatively smaller effect in the historical win/loss model, suggesting that geography may matter more for current pipeline quality than for baseline close probability.
- **Deal age** behaved differently in the ML model than in the rule-based forecast, highlighting the difference between completed sales-cycle duration and aging in the current open pipeline.

Overall, the ML model served as a lightweight, interpretable enhancement that helped identify the historical drivers of close probability and provided a useful complement to the rule-based forecasting framework.