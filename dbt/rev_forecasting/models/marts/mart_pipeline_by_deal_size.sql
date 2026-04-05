-- mart_pipeline_by_deal_size
-- Purpose: Compare pipeline performance and health across estimated deal size segments
-- Grain: 1 row per estimated_deal_size_band

select 
    coalesce(epipeline.estimated_deal_size_band, 'unknown') as estimated_deal_size_band,
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
        when epipeline.pipeline_status = 'open' 
        and epipeline.deal_age_days > 180 then 1
        else 0
    end) as stale_or_review_opportunities,

    sum(case
        when epipeline.pipeline_status = 'open'
             and epipeline.deal_age_days is null then 1
        else 0
    end) as unknown_opportunities,

    sum(case 
        when epipeline.is_won = 1 then 1
        else 0 end)*1.0
        / nullif(sum(case 
                    when epipeline.is_closed = 1 then 1 
                    else 0 
                    end),
                    0
                ) as win_rate, -- defined as won / closed opportunities

    sum(case
        when epipeline.pipeline_status = 'open' then coalesce(epipeline.close_value_amount, epipeline.sales_price, 0)
        else 0
        end) as estimated_open_pipeline_value, -- estimated value of open pipeline

    avg(case
        when epipeline.is_closed = 1 then epipeline.sales_cycle_days
        else null
        end) as avg_sales_cycle_days,

    avg(case
        when epipeline.pipeline_status = 'open' then epipeline.deal_age_days
        else null
        end) as avg_open_deal_age_days,

    avg(case
    when epipeline.pipeline_status = 'open'
    then coalesce(nullif(epipeline.close_value_amount, 0), epipeline.sales_price, null)
    else null
    end) as avg_estimated_open_deal_value


from {{ ref('int_sales_pipeline_enriched') }} as epipeline
group by coalesce(epipeline.estimated_deal_size_band, 'unknown')