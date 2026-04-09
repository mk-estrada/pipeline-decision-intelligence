-- mart_forecast_by_deal_size summarizes forecastable revenue, risk, and conversion efficiency by commercial segment

with forecast as (

    select *
    from {{ ref('fct_pipeline_forecast') }}

)

select
    estimated_deal_size_band,
    count(*) as open_opportunity_count,
    sum(estimated_deal_value) as total_open_pipeline_value,
    sum(expected_revenue_90d) as total_expected_revenue_90d,
    avg(adjusted_close_probability) as avg_adjusted_close_probability,
    sum(case when is_at_risk_flag = 1 then estimated_deal_value else 0 end) as at_risk_pipeline_value,
    sum(case when is_at_risk_flag = 1 then 1 else 0 end) as at_risk_opportunity_count,
    sum(expected_revenue_90d) / nullif(sum(estimated_deal_value), 0) as expected_revenue_to_pipeline_ratio
from forecast
group by estimated_deal_size_band
order by total_open_pipeline_value desc