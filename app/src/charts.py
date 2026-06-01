import plotly.express as px


def aging_distribution_chart(df):
    chart_df = (
        df.groupby("age_bucket", as_index=False)
        .agg(
            opportunity_count=("opportunity_id", "count"),
            pipeline_value=("estimated_deal_value", "sum"),
        )
    )

    fig = px.bar(
        chart_df,
        x="age_bucket",
        y="pipeline_value",
        title="Pipeline Value by Aging Bucket",
        labels={
            "age_bucket": "Aging Bucket",
            "pipeline_value": "Pipeline Value",
        },
    )

    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
    )

    return fig


# Risk By Region 
def regional_risk_chart(df):
    chart_df = (
        df.groupby("regional_office", as_index=False)
        .agg(
            at_risk_revenue=("estimated_deal_value", "sum")
        )
        .sort_values("at_risk_revenue", ascending=False)
    )

    fig = px.bar(
        chart_df,
        x="regional_office",
        y="at_risk_revenue",
        title="At-Risk Pipeline by Region",
        labels={
            "regional_office": "Region",
            "at_risk_revenue": "At-Risk Revenue",
        },
    )

    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
    )

    return fig


# Risk by Deal Size
def deal_size_risk_chart(df):
    chart_df = (
        df.groupby("estimated_deal_size_band", as_index=False)
        .agg(
            at_risk_revenue=("estimated_deal_value", "sum")
        )
    )

    fig = px.bar(
        chart_df,
        x="estimated_deal_size_band",
        y="at_risk_revenue",
        title="At-Risk Pipeline by Deal Size",
        labels={
            "estimated_deal_size_band": "Deal Size",
            "at_risk_revenue": "At-Risk Revenue",
        },
    )

    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
    )

    return fig