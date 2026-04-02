-- mart_open_pipeline_health
-- Purpose:
-- Grain: 1 row per stage
--
-- Note: Older open opportunities are classified as stale_or_review rather than stale,
-- since age alone may reflect stalled deals, duplicate records, or CRM data quality issues.
-- Key Insight:
-- A significant portion of the open pipeline may require intervention before it can be relied on for forecasting. Roughly $1.37M of estimated open pipeline value is tied to aged opportunities, while an additional set of open deals lacks sufficient date information to assess pipeline health. Together, this suggests that pipeline quality, record hygiene, and rep-level validation may be as important as conversion performance in evaluating revenue potential.


select 
    epipeline.opportunity_id,
    epipeline.sales_agent_name,
    epipeline.manager_name,
    epipeline.regional_office,
    epipeline.product_name,
    epipeline.account_name,
    epipeline.deal_stage,
    epipeline.engage_date,
    epipeline.deal_age_days,
    epipeline.sales_price,
    epipeline.close_value_amount,
    epipeline.deal_size_band,

    coalesce(epipeline.close_value_amount, epipeline.sales_price, 0) as pipeline_value_estimate,

    case 
        when epipeline.deal_age_days is null then 'unknown'
        when epipeline.deal_age_days <= 30 then '0-30 Days'
        when epipeline.deal_age_days <= 90 then '31-90 Days'
        when epipeline.deal_age_days <= 180 then '91-180 Days'
        else '180+ Days'
    end as deal_age_band,

    case 
        when epipeline.deal_age_days is null then 'unknown'
        when epipeline.deal_age_days <= 90 then 'healthy'
        when epipeline.deal_age_days <= 180 then 'watch'
        else 'stale_or_review'
    end as pipeline_health_status

from {{ ref('int_sales_pipeline_enriched') }} as epipeline
where epipeline.pipeline_status = 'open'