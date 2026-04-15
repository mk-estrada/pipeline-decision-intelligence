with baseline_open as (

    select *
    from {{ ref('fct_pipeline_forecast') }}

),

product_win_rate as (

    select
        product_name,
        sum(case when deal_stage = 'Won' then 1 else 0 end) as won_opps,
        count(*) as total_closed_opps,
        sum(case when deal_stage = 'Won' then 1 else 0 end) * 1.0
            / nullif(count(*), 0) as product_win_rate
    from {{ ref('int_sales_pipeline_enriched') }}
    where deal_stage in ('Won', 'Lost')
      and product_name is not null
    group by 1

),
product_candidates as (
    select 
        *,
        row_number() over (order by opportunity_id) as rn,
        count(*) over () as total_product_candidates
    from baseline_open
    where product_name in ('MG Advanced', 'GTX Plus Basic')
),
product_treated as (
    select 
        opportunity_id,
        rn,
        total_product_candidates
    from product_candidates
    where rn <= total_product_candidates * 0.15
),
scenario_product_mix as (
    select 
        base.*,
    
    case 
        when product_treated.opportunity_id is not null then 1
        else 0
    end as was_treated,

    case 
        when product_treated.opportunity_id is not null then 'GTXPro'
        else base.product_name
    end as scenario_product_name

    from baseline_open as base
    left join product_treated
        on base.opportunity_id = product_treated.opportunity_id


),
scenario_product_multiplier as (

    select 
        spm.*,
        pwr_original.product_win_rate as original_product_win_rate,
        pwr_scenario.product_win_rate as scenario_product_win_rate,
        pwr_scenario.product_win_rate / nullif(pwr_original.product_win_rate, 0) as scenario_product_multiplier

    from scenario_product_mix as spm
    left join product_win_rate as pwr_original
        on spm.product_name = pwr_original.product_name
    left join product_win_rate as pwr_scenario
        on spm.scenario_product_name = pwr_scenario.product_name

),
product_adjusted_close_probability as (
    select 
        *,
        adjusted_close_probability * scenario_product_multiplier as scenario_adjusted_close_probability 
    
    from scenario_product_multiplier
),
final_scenario as (
    select 
        *,

        estimated_deal_value * scenario_adjusted_close_probability as scenario_expected_revenue_90d

    from product_adjusted_close_probability
)

select 
    'product' as scenario_name,
    sum(expected_revenue_90d) as baseline_expected_revenue,
    sum(scenario_expected_revenue_90d) as scenario_expected_revenue,
    sum(scenario_expected_revenue_90d) - sum(expected_revenue_90d) as revenue_delta,
    (sum(scenario_expected_revenue_90d) - sum(expected_revenue_90d))
        / nullif(sum(expected_revenue_90d), 0) as pct_change,
    sum(was_treated) as affected_opportunity_count
from final_scenario