-- mart_pipeline_summary
-- Purpose: Executive-level summary of sales pipeline performance
-- Grain: 1 row (entire pipeline)
--
-- Key metrics:
-- - Opportunity volume (total, open, won, lost)
-- - Pipeline value (open pipeline, won revenue)
-- - Conversion (win rate)
-- - Process efficiency (sales cycle, deal aging)
--
-- Source: int_sales_pipeline_enriched

select 

    count(epipeline.opportunity_id) as total_opportunities,

    sum(case
        when epipeline.pipeline_status = 'open' then 1 
        else 0 
        end) as open_opportunities,

    sum(case
        when epipeline.is_won = 1 then 1 
        else 0 
        end) as won_opportunities,

    sum(case
        when epipeline.is_lost = 1 then 1 
        else 0 
        end) as lost_opportunities,

    sum(case
        when epipeline.pipeline_status = 'open' then coalesce(epipeline.close_value_amount, epipeline.sales_price, 0)
        else 0
        end) as estimated_open_pipeline_value, -- estimated value of open pipeline

    sum(case 
        when epipeline.is_won = 1 then epipeline.close_value_amount 
        else 0 
        end) as total_won_value,

    avg(case
        when epipeline.is_closed = 1 then epipeline.close_value_amount
        else null
        end) as avg_close_value,

    sum(case 
        when epipeline.is_won = 1 then 1
        else 0 end)*1.0
        / nullif(sum(case 
                    when epipeline.is_closed = 1 then 1 
                    else 0 
                    end),
                    0
                ) as win_rate, -- defined as won / closed opportunities

    avg(case
        when epipeline.is_closed = 1 then epipeline.sales_cycle_days
        else null
        end) as avg_sales_cycle_days,

    avg(case
        when epipeline.pipeline_status = 'open' then epipeline.deal_age_days
        else null
        end) as avg_open_deal_age_days

    

from {{ ref('int_sales_pipeline_enriched') }} as epipeline