def format_currency(value):
    if value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    if value >= 1_000:
        return f"${value / 1_000:.1f}K"
    return f"${value:,.1f}"


def format_percent(value):
    return f"{value:.1%}"


def calculate_executive_metrics(forecast_df):
    open_pipeline = forecast_df["estimated_deal_value"].sum()
    expected_revenue = forecast_df["expected_revenue_90d"].sum()

    forecast_ratio = expected_revenue / open_pipeline if open_pipeline else 0

    at_risk_df = forecast_df[
        forecast_df["age_bucket"].isin(["aging", "stale"])
    ]

    at_risk_revenue = at_risk_df["estimated_deal_value"].sum()
    stale_pipeline_pct = (
        forecast_df.loc[forecast_df["age_bucket"] == "stale", "estimated_deal_value"].sum()
        / open_pipeline
        if open_pipeline
        else 0
    )

    return {
        "open_pipeline": open_pipeline,
        "expected_revenue": expected_revenue,
        "forecast_ratio": forecast_ratio,
        "at_risk_revenue": at_risk_revenue,
        "stale_pipeline_pct": stale_pipeline_pct,
    }