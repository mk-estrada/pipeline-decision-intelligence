def calculate_independent_scenario(
    baseline_expected_revenue: float,
    scenario_name: str,
    intensity_pct: int,
) -> dict:
    """
    MVP independent scenario simulator.

    Each scenario is evaluated separately against the same baseline.
    """

    scenario_impacts = {
        "Pipeline Aging Reduction": {
            "baseline_intensity": 50,
            "impact_pct": 0.12,
        },
        "Data Quality Improvement": {
            "baseline_intensity": 50,
            "impact_pct": 0.103,
        },
        "Product Mix Optimization": {
            "baseline_intensity": 15,
            "impact_pct": 0.003,
        },
    }

    selected = scenario_impacts[scenario_name]

    scaled_lift_pct = (
        intensity_pct / selected["baseline_intensity"]
    ) * selected["impact_pct"]

    scenario_expected_revenue = baseline_expected_revenue * (1 + scaled_lift_pct)
    revenue_delta = scenario_expected_revenue - baseline_expected_revenue

    return {
        "scenario_expected_revenue": scenario_expected_revenue,
        "revenue_delta": revenue_delta,
        "lift_pct": scaled_lift_pct,
    }