-- mart_forecast_by_region summarizes forecastable revenue and pipeline risk by regional office

with forecast as (

    select *
    from {{ ref('fct_pipeline_forecast') }}

)
select
    regional_office,
    count(*) as open_opportunity_count,
    sum(estimated_deal_value) as total_open_pipeline_value,
    sum(expected_revenue_90d) as total_expected_revenue_90d,
    avg(adjusted_close_probability) as avg_adjusted_close_probability,
    sum(case when is_at_risk_flag = 1 then estimated_deal_value else 0 end) as at_risk_pipeline_value,
    sum(case when is_at_risk_flag = 1 then 1 else 0 end) as at_risk_opportunity_count,
    sum(expected_revenue_90d) / nullif(sum(estimated_deal_value), 0) as expected_revenue_to_pipeline_ratio
from forecast
group by regional_office
order by total_open_pipeline_value desc

