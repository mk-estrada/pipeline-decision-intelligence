

select
    "product" as product_name,
    "series" as series,
    "sales_price" as sales_price

from {{ source('raw', 'products_raw') }}