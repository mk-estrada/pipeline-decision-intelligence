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

    
    
    # TEMPORARY DATA CHECK
    if data is not None:
  
        # KPI cards
        st.markdown("**PIPELINE SUMMARY**")
        metrics = calculate_executive_metrics(data["forecast"])

        cols = st.columns(5)
        kpis = [
                ("Open pipeline",    format_currency(metrics["open_pipeline"]),    False),
                ("Expected revenue", format_currency(metrics["expected_revenue"]), False),
                ("Forecast ratio",   format_percent(metrics["forecast_ratio"]),   False),
                ("At-risk revenue",  format_currency(metrics["at_risk_revenue"]),  True),
                ("Stale pipeline",   format_percent(metrics["stale_pipeline_pct"]),   True),
            ]

        for col, (label, value, is_risk) in zip(cols, kpis):
            with col:
                if is_risk:
                    st.markdown(
                f"""<div style="background:#FCEBEB;border-radius:8px;padding:14px 16px;">
                        <p style="font-size:14px;color:#791F1F;margin:0 0 4px;">{label}</p>
                        <p style="font-size:24px;font-weight:500;color:#A32D2D;margin:0;">{value}</p>
                        </div>""",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                f"""<div style="background:#eeee;border-radius:8px;padding:14px 16px;">
                        <p style="font-size:14px;color:#000;margin:0 0 4px;">{label}</p>
                        <p style="font-size:24px;font-weight:500;color:#000;margin:0;">{value}</p>
                        </div>""",
                        unsafe_allow_html=True,
                    )
        st.divider()

        # Action cards
        st.markdown("**RECOMMENDED ACTIONS**")

        cols = st.columns(3)
        pill_styles = {
            "high": ("background:#EAF3DE;color:#3B6D11", "↑"),
            "med":  ("background:#E6F1FB;color:#185FA5", "↑"),
            "low":  ("background:#F1EFE8;color:#5F5E5A", "–"),
        }
        
        actions=[
        {"title": "Reduce aging pipeline",          "desc": "Prioritize opportunities older than 120 days.",                          "impact": "+12%",   "priority": "high"},
        {"title": "Improve data quality",            "desc": "Classify missing deal-size values to improve forecast confidence.",      "impact": "+10.3%", "priority": "med"},
        {"title": "Defer product mix optimization",  "desc": "Lower near-term upside vs aging and data quality actions.",             "impact": "+0.3%",  "priority": "low"},
        ]
        
        for i, (col, action) in enumerate(zip(cols, actions), 1):
            style, arrow = pill_styles[action["priority"]]
            with col:
                st.markdown(
                    f"""<div style="border:0.5px solid #ddd;border-radius:12px;padding:1rem 1.25rem;height:100%;">
                    <p style="font-size:15px;color:#888;margin:0 0 6px;letter-spacing:.04em;">PRIORITY {i}</p>
                    <p style="font-size:20px;font-weight:500;margin:0 0 6px;">{action["title"]}</p>
                    <p style="font-size:15px;color:#666;margin:0 0 12px;">{action["desc"]}</p>
                    <span style="font-size:13px;font-weight:500;padding:3px 10px;border-radius:99px;{style}">
                    {arrow} {action["impact"]} forecast lift
                    </span>
                    </div>""",
                    unsafe_allow_html=True,
                )

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

        # Dynamic slider label
        slider_descriptions = {
            "Pipeline Aging Reduction": (
                f"At {intensity_pct}% intensity, "
                f"**{intensity_pct}% of aging deals (>120 days)** are assumed to be re-engaged or closed out."
            ),
            "Data Quality Improvement": (
                f"At {intensity_pct}% intensity, "
                f"**{intensity_pct}% of deals with missing size values** are assumed to be classified."
            ),
            "Product Mix Optimization": (
                f"At {intensity_pct}% intensity, "
                f"**{intensity_pct}% of low-performing deals** are assumed to be shifted to higher-value products."
            ),
        }
        st.caption(slider_descriptions[scenario_name])

        scenario_results = calculate_independent_scenario(
            baseline_expected_revenue=baseline_expected_revenue,
            scenario_name=scenario_name,
            intensity_pct=intensity_pct,
        )

        st.divider()
        st.subheader("Scenario Impact")

        
        impact = [
                ("Baseline Expected Revenue", format_currency(baseline_expected_revenue), None, False),
                ("Scenario Expected Revenue", format_currency(scenario_results["scenario_expected_revenue"]), format_currency(scenario_results["revenue_delta"]), True),
                ("Forecast Lift", format_percent(scenario_results["lift_pct"]), None, False ),
            ]

        cols = st.columns(3)
        for col, (label, value, delta, is_highlight) in zip(cols, impact):
            with col:
                delta_html = (
                    f'<p style="font-size:14px;font-weight:500;color:#3B6D11;'
                    f'background:#EAF3DE;display:inline-block;padding:2px 10px;'
                    f'border-radius:99px;margin:6px 0 0;">↑ {delta}</p>'
                    if delta else '<p style="margin:6px 0 0;min-height:24px;"></p>'
                )
                st.markdown(
                    f"""<div style="background:#eeee;border-radius:8px;
                    padding:14px 16px;border:0.5px solid rgba(0,0,0,0.1);
                    min-height:110px;">
                    <p style="font-size:13px;color:#666;margin:0 0 4px;">{label}</p>
                    <p style="font-size:24px;font-weight:500;margin:0;">{value}</p>
                    {delta_html}
                    </div>""",
                    unsafe_allow_html=True,
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