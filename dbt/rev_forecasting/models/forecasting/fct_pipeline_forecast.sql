
-- forecasting/
--  fct_pipeline_forecast.sql
--  mart_forecast_summary.sql
--  mart_forecast_by_segment.sql


with base_opportunities as (

    select
        opportunity_id,
        regional_office,
        product_name,
        estimated_deal_value,
        estimated_deal_size_band,       
        deal_age_days,
        pipeline_status

    from {{ ref('int_sales_pipeline_enriched') }}
    where pipeline_status = 'open'

),

opportunities_with_age_bucket as (

    select
        opportunity_id,
        regional_office,
        product_name,
        estimated_deal_value,
        estimated_deal_size_band,
        deal_age_days,
        pipeline_status,

        case
            when deal_age_days is null then 'unknown'
            when deal_age_days <= 60 then 'healthy'
            when deal_age_days <= 120 then 'slightly_aged'
            when deal_age_days <= 200 then 'aging'
            else 'stale'
        end as age_bucket

    from base_opportunities

),

overall_win_rate as (

    select
        win_rate as overall_win_rate
    from {{ ref('mart_pipeline_summary') }}

),

deal_size_win_rate as (

    select
        estimated_deal_size_band,
        win_rate as deal_size_win_rate
    from {{ ref('mart_pipeline_by_deal_size') }}

),
opportunities_with_base_probability as (

    select
        o.opportunity_id,
        o.regional_office,
        o.product_name,
        o.estimated_deal_value,
        o.estimated_deal_size_band,
        o.deal_age_days,
        o.pipeline_status,
        o.age_bucket,

        case
            when o.estimated_deal_size_band is null then ow.overall_win_rate
            when o.estimated_deal_size_band = 'unknown' then ow.overall_win_rate
            else dsw.deal_size_win_rate
        end as base_win_rate_by_size

    from opportunities_with_age_bucket as o
    left join deal_size_win_rate dsw
        on o.estimated_deal_size_band = dsw.estimated_deal_size_band
    cross join overall_win_rate ow

),
opportunities_with_multiplier as (
    select 
        *,
        case 
            when age_bucket = 'healthy' then 1.0
            when age_bucket = 'slightly_aged' then 0.85
            when age_bucket = 'aging' then 0.65
            when age_bucket = 'stale' then 0.35
            when age_bucket = 'unknown' then 0.5
            else null
        end as age_multiplier
    from opportunities_with_base_probability
),

opportunities_with_adjusted_probability as (

    select
        *,
        base_win_rate_by_size * age_multiplier as adjusted_close_probability
    from opportunities_with_multiplier

)
select 
    *,
    estimated_deal_value * adjusted_close_probability as expected_revenue_90d,

    case 
        when age_bucket in ('unknown', 'aging', 'stale') then 1
        else 0
    end as is_at_risk_flag
    
from opportunities_with_adjusted_probability 