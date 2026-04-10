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

),
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
--scenario_win_rate_by_size ()
-- base win rate size
select *
from scenario_data_quality