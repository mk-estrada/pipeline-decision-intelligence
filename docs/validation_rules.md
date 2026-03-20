# Validation Rules

## sales_pipeline
- opportunity_id must be unique and not null
- sales_agent must not be null
- product must not be null
- deal_stage must not be null
- account can be null, but track % missing
- engage_date can be null, but missing values should be evaluated relative to deal_stage
- close_date can be null
- close_value can be null

## accounts 
- account must be unique and not null
- sector must not be null
- office_location must not be null
- subsidiary_of can be null

## products
- product must be unique and not null
- series must not be null
- sales_price must not be null

## sales_teams 
- sales_agent must be unique and not null

## metadata
- no validation rules (documentation table)