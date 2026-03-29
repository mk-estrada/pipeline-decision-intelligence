

select
    "sales_agent" as sales_agent_name,
    "manager" as manager_name,
    "regional_office" as regional_office

from {{ source('raw', 'sales_teams_raw') }}