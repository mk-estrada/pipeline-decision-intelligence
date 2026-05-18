from pathlib import Path
import plotly.graph_objects as go

# -----------------------------
# Forecast bridge values
# -----------------------------
open_pipeline = 3_360_000
expected_revenue = 1_205_000

# These reductions should eventually come from forecast output,

aging_risk_adjustment = -1_100_000
probability_adjustment = -1_060_000

# -----------------------------
# Create output folder
# -----------------------------
output_dir = Path("images")
output_dir.mkdir(exist_ok=True)

# -----------------------------
# Build waterfall chart
# -----------------------------
fig = go.Figure(
    go.Waterfall(
        orientation="v",
        measure=[
            "relative",
            "relative",
            "relative",
            "total",
        ],
        x=[
            "Open Pipeline",
            "Base Win Probability",
            "Pipeline Aging Risk",
            "Expected 90-Day Revenue",
        ],
        y=[
            open_pipeline,
            probability_adjustment,
            aging_risk_adjustment,
            expected_revenue,
        ],
        text=[
            "$3.3M",
            "-$1.1M",
            "-$1.06M",
            "$1.2M",
        ],
        textposition="outside",
        connector={"line": {"color": "gray"}},

        # Positive / starting bar
        increasing={
            "marker": {
                "color": "#4C78A8"
            }
        },

        # Negative adjustments
        decreasing={
            "marker": {
                "color": "#D9534F"
            }
        },

        # Final total bar
        totals={
            "marker": {
                "color": "#2E8B57"
            }
        },
    )
)


fig.update_layout(
    title={
        "text": "Forecast Bridge: From Raw Pipeline to Expected Revenue",
        "x": 0.5,
        "xanchor": "center",
    },
    yaxis_title="Revenue",
    yaxis_tickprefix="$",
    yaxis_tickformat=",.0f",
    showlegend=False,
    width=1100,
    height=650,
    margin=dict(l=80, r=80, t=100, b=120),
)

fig.add_annotation(
    text="Raw open pipeline overstates realistic near-term revenue by ~60% after risk and probability adjustments.",
    xref="paper",
    yref="paper",
    x=0.5,
    y=-0.22,
    showarrow=False,
    font=dict(size=14),
)


# -----------------------------
# Save outputs
# -----------------------------
fig.write_html(output_dir / "forecast_bridge.html")
fig.write_image(output_dir / "forecast_bridge.png", scale=2)

print("Saved forecast bridge chart to images/forecast_bridge.png")