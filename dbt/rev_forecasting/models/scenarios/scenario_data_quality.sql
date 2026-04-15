with baseline_open as (

    select *
    from {{ ref('fct_pipeline_forecast') }}

),


size_band_averages as (

    select
        estimated_deal_size_band,
        avg(estimated_deal_value) as avg_estimated_deal_value
    from baseline_open
    where estimated_deal_size_band in ('small', 'medium')
    group by 1

),
small_avg as (

    select avg_estimated_deal_value as small_avg_value
    from size_band_averages
    where estimated_deal_size_band = 'small'

),

medium_avg as (

    select avg_estimated_deal_value as medium_avg_value
    from size_band_averages
    where estimated_deal_size_band = 'medium'

),
unknown_candidates as (

    select 
        *, 
        row_number() over (order by opportunity_id) as rn,
        count(*) over () as total_unknown_candidates
    from baseline_open
    where estimated_deal_size_band = 'unknown'
      and (
            estimated_deal_value is null
            or sales_price is null
          )

),
-- Treat 50% of unknown deals; within treated set, assign 80% to small and 20% to medium
unknown_treated as (

    select
        opportunity_id,
        rn,
        total_unknown_candidates
    from unknown_candidates
    where rn <= total_unknown_candidates * 0.5

),
scenario_data_quality as (

        select 
        base.*, 

        case 
            when unknown_treated.opportunity_id is not null then 1
            else 0
        end as was_treated,

        case 
            when unknown_treated.opportunity_id is not null
                 and unknown_treated.rn <= unknown_treated.total_unknown_candidates * 0.4
                then 'small'
            when unknown_treated.opportunity_id is not null
                then 'medium'
            else base.estimated_deal_size_band
        end as scenario_estimated_deal_size_band,

        case 
            when unknown_treated.opportunity_id is not null
                 and unknown_treated.rn <= unknown_treated.total_unknown_candidates * 0.4
                then small_avg.small_avg_value
            when unknown_treated.opportunity_id is not null
                then medium_avg.medium_avg_value
            else base.estimated_deal_value
        end as scenario_estimated_deal_value
    
    from baseline_open as base
    left join unknown_treated 
        on base.opportunity_id = unknown_treated.opportunity_id
    cross join small_avg
    cross join medium_avg
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
scenario_win_rate_by_size as (
    
    select 
        sdq.*,

        coalesce(dsw.deal_size_win_rate, owr.overall_win_rate) as scenario_base_win_rate_by_size


    from scenario_data_quality as sdq
    left join deal_size_win_rate as dsw
        on sdq.scenario_estimated_deal_size_band = dsw.estimated_deal_size_band
    cross join overall_win_rate as owr
),

scenario_with_adjusted_probability as (

    select
        *,
        scenario_base_win_rate_by_size * age_multiplier as scenario_adjusted_close_probability
    from scenario_win_rate_by_size

),

final_scenario as (
    select 
        *,
        scenario_estimated_deal_value * scenario_adjusted_close_probability as scenario_expected_revenue_90d

        
    from scenario_with_adjusted_probability
)
select 
    'data_quality' as scenario_name,
    sum(expected_revenue_90d) as baseline_expected_revenue,
    sum(scenario_expected_revenue_90d) as scenario_expected_revenue,
    sum(scenario_expected_revenue_90d) - sum(expected_revenue_90d) as revenue_delta,
    (sum(scenario_expected_revenue_90d) - sum(expected_revenue_90d))
        / nullif(sum(expected_revenue_90d), 0) as pct_change,
    sum(was_treated) as affected_opportunity_count
from final_scenario