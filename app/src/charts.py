import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Color maps
AGING_COLORS = {
    "healthy":       "#639922",  # green
    "slightly_aged": "#BA7517",  # amber
    "aging":         "#D85A30",  # coral/orange-red
    "stale":         "#A32D2D",  # red
    "unknown":       "#888780",  # gray
}

AT_RISK_COLOR = "#D85A30"  # consistent coral for at-risk charts

def aging_distribution_chart(df):
    chart_df = (
        df.groupby("age_bucket", as_index=False)
        .agg(
            opportunity_count=("opportunity_id", "count"),
            pipeline_value=("estimated_deal_value", "sum"),
        )
    )

    # Enforce display order
    bucket_order = ["healthy", "slightly_aged", "aging", "stale", "unknown"]
    chart_df["age_bucket"] = pd.Categorical(
        chart_df["age_bucket"], categories=bucket_order, ordered=True
    )
    chart_df = chart_df.sort_values("age_bucket")
    chart_df["color"] = chart_df["age_bucket"].map(AGING_COLORS)

    fig = go.Figure(
        go.Bar(
            x=chart_df["age_bucket"],
            y=chart_df["pipeline_value"],
            marker_color=chart_df["color"],
            hovertemplate="<b>%{x}</b><br>Pipeline Value: $%{y:,.0f}<extra></extra>",
        )
    )
    fig.update_layout(
        title="Pipeline Value by Aging Bucket",
        xaxis_title="Aging Bucket",
        yaxis_title="Pipeline Value",
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_yaxes(gridcolor="rgba(0,0,0,0.06)")
    return fig


# Risk By Region 
def regional_risk_chart(df):
    chart_df = (
        df.groupby("regional_office", as_index=False)
        .agg(at_risk_revenue=("estimated_deal_value", "sum"))
        .sort_values("at_risk_revenue", ascending=False)
    )

    fig = go.Figure(
        go.Bar(
            x=chart_df["regional_office"],
            y=chart_df["at_risk_revenue"],
            marker_color=AT_RISK_COLOR,
            hovertemplate="<b>%{x}</b><br>At-Risk Revenue: $%{y:,.0f}<extra></extra>",
        )
    )
    fig.update_layout(
        title="At-Risk Pipeline by Region",
        xaxis_title="Region",
        yaxis_title="At-Risk Revenue",
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_yaxes(gridcolor="rgba(0,0,0,0.06)")
    return fig



# Risk by Deal Size
def deal_size_risk_chart(df):
    chart_df = (
        df.groupby("estimated_deal_size_band", as_index=False)
        .agg(at_risk_revenue=("estimated_deal_value", "sum"))
    )

    size_order = ["small", "medium", "large"]
    chart_df["estimated_deal_size_band"] = pd.Categorical(
        chart_df["estimated_deal_size_band"], categories=size_order, ordered=True
    )
    chart_df = chart_df.sort_values("estimated_deal_size_band")

    fig = go.Figure(
        go.Bar(
            x=chart_df["estimated_deal_size_band"],
            y=chart_df["at_risk_revenue"],
            marker_color=AT_RISK_COLOR,
            hovertemplate="<b>%{x}</b><br>At-Risk Revenue: $%{y:,.0f}<extra></extra>",
        )
    )
    fig.update_layout(
        title="At-Risk Pipeline by Deal Size",
        xaxis_title="Deal Size",
        yaxis_title="At-Risk Revenue",
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_yaxes(gridcolor="rgba(0,0,0,0.06)")
    return fig