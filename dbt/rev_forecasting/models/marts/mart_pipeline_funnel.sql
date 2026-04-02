-- mart_pipeline_funnel
-- Purpose: Summarize opportunity distribution across funnel stages
-- Grain: 1 row per stage
--
-- Notes:
-- - Dataset is outcome-heavy (majority of opportunities are closed)
-- - Used for conversion and performance analysis, not real-time pipeline monitoring

select 
    epipeline.deal_stage as stage, 

    case
        when epipeline.deal_stage = 'Prospecting' then 1
        when epipeline.deal_stage = 'Engaging' then 2
        when epipeline.deal_stage = 'Won' then 3
        when epipeline.deal_stage = 'Lost' then 4
        else 99
    end as stage_order,

    count(*) as opportunity_count,

    count(*)*1.0 / sum(count(*)) over () as pct_of_total
from {{ ref('int_sales_pipeline_enriched') }} as epipeline
group by stage,
        stage_order