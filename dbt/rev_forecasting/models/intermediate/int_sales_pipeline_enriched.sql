-- Set an analysis date to account for historical dates in dataset
with analysis_date as (
    select max(close_date) as as_of_date
    from {{ ref('stg_sales_pipeline') }}
)

select
    pipeline.opportunity_id,
    pipeline.sales_agent_name,
    sales_team.manager_name,
    sales_team.regional_office,
    pipeline.product_name,
    products.series,
    products.sales_price,
    pipeline.account_name,
    accounts.sector,
    accounts.office_location,
    pipeline.deal_stage,
    pipeline.engage_date,
    pipeline.close_date,
    pipeline.close_value_amount,

    case
        when pipeline.deal_stage = 'Won' then 'won'
        when pipeline.deal_stage = 'Lost' then 'lost'
        else 'open'
    end as pipeline_status,

    case
        when pipeline.deal_stage = 'Won' then 1
        else 0
    end as is_won,

    case
        when pipeline.deal_stage = 'Lost' then 1
        else 0
    end as is_lost,

    case
        when pipeline.deal_stage in ('Won', 'Lost') then 1
        else 0
    end as is_closed,

    case
        when pipeline.deal_stage in ('Prospecting', 'Engaging')
            and pipeline.engage_date is not null
        then datediff(day, pipeline.engage_date, ad.as_of_date)
        else null
    end as deal_age_days,

    case
        when pipeline.deal_stage in ('Won', 'Lost')
            and pipeline.engage_date is not null
            and pipeline.close_date is not null
        then datediff(day, pipeline.engage_date, pipeline.close_date)
        else null
    end as sales_cycle_days,

    case 
        when pipeline.close_value_amount is null then 'unknown'
        when pipeline.close_value_amount < 5000 then 'small'
        when pipeline.close_value_amount < 20000 then 'medium'
        else 'large'
    end as deal_size_band

from {{ ref('stg_sales_pipeline') }} as pipeline
cross join analysis_date as ad
left join {{ ref('stg_sales_teams') }} as sales_team on pipeline.sales_agent_name = sales_team.sales_agent_name
left join {{ ref('stg_products') }} as products on pipeline.product_name = products.product_name
left join {{ ref('stg_accounts') }} as accounts on pipeline.account_name = accounts.account_name
