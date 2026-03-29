

select
    "opportunity_id" as opportunity_id,
    "sales_agent" as sales_agent_name,
    "product" as product_name,
    "account" as account_name,
    "deal_stage" as deal_stage,
    try_to_date("engage_date") as engage_date,
    try_to_date("close_date") as close_date,
    "close_value"::number(18,2) as close_value_amount

from {{ source('raw', 'sales_pipeline_raw') }}