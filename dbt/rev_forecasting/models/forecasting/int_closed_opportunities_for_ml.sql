-- The heuristic model uses current deal age to estimate likelihood, while the ML model learns from historical sales cycle behavior to estimate close probability.

select
    opportunity_id,
    pipeline_status,
    estimated_deal_size_band,
    regional_office,

   case
    when pipeline_status in ('won','lost')
        and engage_date is not null
        and close_date is not null
    then datediff(day, engage_date, close_date)
    else null
    end as deal_age_days,

    product_name,

    case
        when pipeline_status = 'won' then 1
        when pipeline_status = 'lost' then 0
        else null
    end as won_flag

from {{ ref('int_sales_pipeline_enriched') }}
where pipeline_status in ('won', 'lost')