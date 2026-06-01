import streamlit as st
from src.data_loader import load_all_data
from src.metrics import (
    calculate_executive_metrics,
    format_currency,
    format_percent
)
from src.charts import (
    aging_distribution_chart,
    regional_risk_chart,
    deal_size_risk_chart
)

from src.scenarios import calculate_independent_scenario

# Page Configuration
st.set_page_config(
    page_title="Decision Intelligence: Revenue Forecasting",
    page_icon="📊",
    layout="wide"
    
)

#Load all data
try:
    data = load_all_data()
except FileNotFoundError as e:
    st.warning("Data files are not loaded yet.")
    st.code(str(e))
    data = None

# Sidebar Navigation
st.sidebar.title("Decision Intelligence")
st.sidebar.caption("Revenue Forecasting System")

page = st.sidebar.radio(
    "Navigate",
    [
        "Executive Overview",
        "Pipeline Risk Explorer",
        "Scenario Simulator"
    ]
)


# -----------------------------
# Page 1: Executive Overview
# -----------------------------
if page == "Executive Overview":
    st.title("Executive Overview")

    st.markdown(
        """
        **Decision Question:**  
        What is the current 90-day revenue forecast, and where should leadership focus?
        """
    )

    #st.info("This page will show executive KPIs, forecast health, and recommended actions.")

    
    # TEMPORARY DATA CHECK
    if data is not None:

        #st.write(data["forecast"].columns.tolist())

        metrics = calculate_executive_metrics(data["forecast"])

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Open Pipeline", format_currency(metrics["open_pipeline"]))
        col2.metric("Expected Revenue", format_currency(metrics["expected_revenue"]))
        col3.metric("Forecast Ratio", format_percent(metrics["forecast_ratio"]))
        col4.metric("At-Risk Revenue", format_currency(metrics["at_risk_revenue"]))
        col5.metric("Stale Pipeline", format_percent(metrics["stale_pipeline_pct"]))

    st.divider()

    st.subheader("Recommended Actions")

    rec1, rec2, rec3 = st.columns(3)

    with rec1:
        st.markdown("### 1. Reduce Aging Pipeline")
        st.write("Prioritize opportunities older than 120 days.")
        st.metric("Estimated Impact", "+12%")

    with rec2:
        st.markdown("### 2. Improve Data Quality")
        st.write("Classify missing deal-size values to improve forecast confidence.")
        st.metric("Estimated Impact", "+10.3%")

    with rec3:
        st.markdown("### 3. Defer Product Mix Optimization")
        st.write("Lower near-term upside compared with aging and data quality actions.")
        st.metric("Estimated Impact", "+0.3%")

# -----------------------------
# Page 2: Pipeline Risk Explorer
# -----------------------------
elif page == "Pipeline Risk Explorer":
    st.title("Pipeline Risk Explorer")

    st.markdown(
        """
        **Decision Question:**  
        Where is pipeline risk concentrated by age, region, and deal size?
        """
    )

    #st.info("This page will show aging distribution, regional risk, and deal-size risk.")
    if data is not None:
        forecast_df = data["forecast"].copy()

        region_options = ["All"] + sorted(forecast_df["regional_office"].dropna().unique())
        size_options = ["All", "small", "medium", "large"]

        filter_col1, filter_col2 = st.columns(2)

        with filter_col1:
            selected_region = st.selectbox("Region", region_options)

        with filter_col2:
            selected_size = st.selectbox("Deal Size", size_options)

        filtered_df = forecast_df[
            forecast_df["estimated_deal_size_band"] != "unknown"
        ].copy()

        if selected_region != "All":
            filtered_df = filtered_df[filtered_df["regional_office"] == selected_region]

        if selected_size != "All":
            filtered_df = filtered_df[filtered_df["estimated_deal_size_band"] == selected_size]


        st.divider()

        st.plotly_chart(
            aging_distribution_chart(filtered_df),
            use_container_width=True,
        )

        st.divider()


        risk_df = filtered_df[
        filtered_df["age_bucket"].isin(["aging", "stale"])
        ]
        
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.plotly_chart(
                regional_risk_chart(risk_df),
                use_container_width=True,
            )

        with chart_col2:
            st.plotly_chart(
                deal_size_risk_chart(risk_df),
                use_container_width=True,
            )




# -----------------------------
# Page 3: Scenario Simulator
# -----------------------------
elif page == "Scenario Simulator":
    st.title("Scenario Simulator")

    st.markdown(
        """
        **Decision Question:**  
        Which operational intervention has the strongest expected revenue impact?
        """
    )

    if data is not None:
        forecast_df = data["forecast"].copy()
        baseline_expected_revenue = forecast_df["expected_revenue_90d"].sum()

        st.divider()

        st.subheader("Select Scenario")

        scenario_name = st.selectbox(
            "Scenario",
            [
                "Pipeline Aging Reduction",
                "Data Quality Improvement",
                "Product Mix Optimization",
            ],
        )

        if scenario_name == "Product Mix Optimization":
            max_intensity = 30
            default_intensity = 15
        else:
            max_intensity = 100
            default_intensity = 50

        intensity_pct = st.slider(
            "Scenario Intensity",
            min_value=0,
            max_value=max_intensity,
            value=default_intensity,
            step=5,
        )

        scenario_results = calculate_independent_scenario(
            baseline_expected_revenue=baseline_expected_revenue,
            scenario_name=scenario_name,
            intensity_pct=intensity_pct,
        )

        st.divider()

        st.subheader("Scenario Impact")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Baseline Expected Revenue",
                format_currency(baseline_expected_revenue),
            )

        with col2:
            st.metric(
                "Scenario Expected Revenue",
                format_currency(scenario_results["scenario_expected_revenue"]),
                delta=format_currency(scenario_results["revenue_delta"]),
            )

        with col3:
            st.metric(
                "Forecast Lift",
                format_percent(scenario_results["lift_pct"]),
            )

        st.divider()

        st.subheader("Interpretation")

        st.markdown(
            f"""
            This scenario evaluates **{scenario_name}** independently against the baseline forecast.

            At the selected intensity, this scenario increases expected 90-day revenue by  
            **{format_currency(scenario_results["revenue_delta"])}**, or  
            **{format_percent(scenario_results["lift_pct"])}** versus baseline.
            """
        )