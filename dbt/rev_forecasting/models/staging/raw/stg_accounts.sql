


select
    "account" as account_name,
    "sector" as sector,
    "year_established" as year_established,
    "revenue" as revenue,
    "employees" as employee_count,
    "office_location" as office_location, 
    "subsidiary_of" as subsidiary_of

from {{ source('raw', 'accounts_raw') }}