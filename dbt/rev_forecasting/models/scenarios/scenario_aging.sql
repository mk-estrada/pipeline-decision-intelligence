with baseline_open as (

    select *
    from {{ ref('fct_pipeline_forecast') }}

),

aging_candidates as (

    select 
        *,
        row_number() over (order by opportunity_id) as rn,
        count(*) over () as total_aging_candidates
    from baseline_open
    where deal_age_days > 120

),

aging_treated as (

    select
        opportunity_id
    from aging_candidates
    where rn <= total_aging_candidates * 0.5

),

scenario_aging as (

    select 
        base.*,

        case 
            when aging_treated.opportunity_id is not null
                then round(base.deal_age_days * 0.7, 0)
            else base.deal_age_days
        end as scenario_deal_age_days,

        case 
            when aging_treated.opportunity_id is not null then 1
            else 0
        end as was_treated

    from baseline_open as base
    left join aging_treated
        on base.opportunity_id = aging_treated.opportunity_id

),

scenario_bucketed as (
    select * ,

    case
            when scenario_deal_age_days is null then 'unknown'
            when scenario_deal_age_days <= 60 then 'healthy'
            when scenario_deal_age_days <= 120 then 'slightly_aged'
            when scenario_deal_age_days <= 200 then 'aging'
            else 'stale'
     end as scenario_age_bucket

    from scenario_aging
),

scenario_age_multiplier as (
    select 
        *,
        case 
            when scenario_age_bucket = 'healthy' then 1.0
            when scenario_age_bucket = 'slightly_aged' then 0.85
            when scenario_age_bucket = 'aging' then 0.65
            when scenario_age_bucket = 'stale' then 0.35
            when scenario_age_bucket = 'unknown' then 0.5
            else null
        end as scenario_age_multiplier
    from scenario_bucketed

),

scenario_with_adjusted_probability as (

    select
        *,
        base_win_rate_by_size * scenario_age_multiplier as scenario_adjusted_close_probability
    from scenario_age_multiplier

),

final_scenario as (
    select 
        *,
        estimated_deal_value * scenario_adjusted_close_probability as scenario_expected_revenue_90d,

        case 
            when scenario_age_bucket in ('unknown', 'aging', 'stale') then 1
            else 0
        end as scenario_is_at_risk_flag
        
    from scenario_with_adjusted_probability
)

select 
    'aging' as scenario_name,
    sum(expected_revenue_90d) as baseline_expected_revenue,
    sum(scenario_expected_revenue_90d) as scenario_expected_revenue,
    sum(scenario_expected_revenue_90d) - sum(expected_revenue_90d) as revenue_delta,
    (sum(scenario_expected_revenue_90d) - sum(expected_revenue_90d))
        / nullif(sum(expected_revenue_90d), 0) as pct_change,
    sum(was_treated) as affected_opportunity_count
from final_scenario