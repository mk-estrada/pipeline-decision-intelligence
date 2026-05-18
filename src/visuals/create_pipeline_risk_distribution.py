from pathlib import Path
import plotly.graph_objects as go

# ---------------------------------
# Output directory
# ---------------------------------
output_dir = Path("images")
output_dir.mkdir(exist_ok=True)

# ---------------------------------
# Pipeline risk data
# ---------------------------------
age_buckets = [
    "Healthy",
    "Slightly Aged",
    "Aging",
    "Stale",
    "Unknown",
]

opportunity_counts = [
    57,
    156,
    727,
    649,
    500,
]

# Optional: use actual pipeline value instead of counts later
# pipeline_value = [450000, 380000, 1100000, 1200000, 170000]

# ---------------------------------
# Colors by risk level
# ---------------------------------
colors = [
    "#2E8B57",  # Healthy - green
    "#B0B0B0",  # Slightly aged - gray
    "#F0AD4E",  # Aging - amber
    "#D9534F",  # Stale - red
    "#7A7A7A",  # Unknown - dark gray
]

# ---------------------------------
# Create chart
# ---------------------------------
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=age_buckets,
        y=opportunity_counts,
        text=[f"{count:,}" for count in opportunity_counts],
        textposition="outside",
        marker=dict(color=colors),
    )
)

# ---------------------------------
# Layout
# ---------------------------------
fig.update_layout(
    title={
        "text": "Open Pipeline Risk Distribution by Deal Age",
        "x": 0.5,
        "xanchor": "center",
    },
    xaxis_title="Deal Age Bucket",
    yaxis_title="Number of Open Opportunities",
    template="plotly_white",
    width=1100,
    height=650,
    margin=dict(l=80, r=80, t=100, b=120),
    showlegend=False,
)

fig.update_yaxes(
    showgrid=True,
    gridcolor="rgba(0,0,0,0.08)",
)

# ---------------------------------
# Executive annotation
# ---------------------------------
fig.add_annotation(
    text=(
        "A large share of open opportunities are aging or stale, "
        "reinforcing pipeline velocity as a key operational risk driver."
    ),
    xref="paper",
    yref="paper",
    x=0.5,
    y=-0.22,
    showarrow=False,
    font=dict(size=14),
)

# ---------------------------------
# Export
# ---------------------------------
fig.write_html(output_dir / "pipeline_risk_distribution.html")
fig.write_image(output_dir / "pipeline_risk_distribution.png", scale=2)

print("Saved pipeline risk distribution chart to images/pipeline_risk_distribution.png")