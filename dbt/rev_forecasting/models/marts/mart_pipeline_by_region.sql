-- mart_pipeline_by_region
-- Purpose: Compare pipeline volume, conversion, value, and health across regions
-- Grain: 1 row per regional_office

-- Key Insight: Pipeline Performance by Region
-- Conversion performance is consistent across regions, with win rates around 60% and no clear outlier in closing effectiveness. Differences emerge, however, in pipeline composition and health.
-- The West region has the largest volume of opportunities and the highest share of aging pipeline, with approximately 62% of open deals classified as stale or requiring review. This indicates both a significant revenue opportunity and elevated risk, as a large portion of pipeline value may not be actively progressing.
-- The Central region stands out for data quality concerns, with over 50% of its open opportunities lacking sufficient date information to assess deal age. This suggests potential gaps in CRM hygiene or process consistency, limiting visibility into true pipeline health.
-- Across regions, closed deals move efficiently, with similar average sales cycles of ~47–48 days. However, open opportunities—particularly in the East and West—are significantly older, averaging roughly 50 days longer than those in Central. This gap highlights a disconnect between deal velocity and pipeline management, suggesting that while teams close deals quickly, a portion of the open pipeline may be stalled or deprioritized.
-- Overall, the analysis indicates that improving pipeline hygiene, deal progression, and rep-level validation may unlock additional value without requiring increased top-of-funnel volume.
-- Notably, a meaningful portion of total open pipeline value is concentrated in aging opportunities, reinforcing the need to assess whether these deals remain viable.

select 
    coalesce(epipeline.regional_office, 'unknown') as regional_office,
    count(epipeline.opportunity_id) as total_opportunities,

    sum(case
        when epipeline.pipeline_status = 'open' then coalesce(epipeline.close_value_amount, epipeline.sales_price, 0)
        else 0
    end) as estimated_open_pipeline_value,

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
     end) as avg_open_deal_age_days,

    sum(case 
        when epipeline.pipeline_status = 'open' 
        and deal_age_days > 180 then 1
        else 0
    end) as stale_or_review_opportunities,

    sum(case 
        when epipeline.pipeline_status = 'open' 
        and deal_age_days is null then 1
        else 0
    end) as unknown_opportunities

from {{ ref('int_sales_pipeline_enriched') }} as epipeline
group by coalesce(epipeline.regional_office, 'unknown')