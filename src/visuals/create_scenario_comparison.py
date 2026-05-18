from pathlib import Path
import plotly.graph_objects as go

# ---------------------------------
# Output directory
# ---------------------------------
output_dir = Path("images")
output_dir.mkdir(exist_ok=True)

# ---------------------------------
# Scenario data
# ---------------------------------
scenarios = [
    "Pipeline Aging Reduction",
    "Data Quality Improvement",
    "Product Mix Optimization"
]

revenue_lift = [12.0, 10.3, 0.3]

# ---------------------------------
# Create chart
# ---------------------------------
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=revenue_lift,
        y=scenarios,
        orientation='h',

        text=[
            "+12.0%",
            "+10.3%",
            "+0.3%"
        ],

        textposition='outside',

        marker=dict(
            color=[
                "#4C78A8",
                "#6B93C4",
                "#B0B0B0"
            ]
        ),
    )
)

# ---------------------------------
# Layout styling
# ---------------------------------
fig.update_layout(
    title={
        "text": "Scenario Impact on Expected Revenue",
        "x": 0.5,
        "xanchor": "center"
    },

    xaxis_title="Increase in Expected Revenue (%)",

    yaxis=dict(
        autorange="reversed"
    ),

    template="plotly_white",

    width=1100,
    height=650,

    margin=dict(
        l=120,
        r=80,
        t=100,
        b=120
    ),

    showlegend=False,
)

# ---------------------------------
# Executive annotation
# ---------------------------------
fig.add_annotation(
    text=(
        "Operational execution and data quality improvements "
        "produce substantially larger forecast gains than "
        "product mix optimization."
    ),

    xref="paper",
    yref="paper",

    x=0.5,
    y=-0.22,

    showarrow=False,

    font=dict(size=14)
)

# ---------------------------------
# Export outputs
# ---------------------------------
fig.write_html(output_dir / "scenario_comparison.html")
fig.write_image(output_dir / "scenario_comparison.png", scale=2)

print("Saved scenario comparison chart to images/scenario_comparison.png")