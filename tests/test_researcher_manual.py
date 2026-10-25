from trading_agent.schemas import MarketSnapshot
from trading_agent.analysis.researcher import generate_research_report

snapshot = MarketSnapshot(
    ticker="AAPL",
    requested_start="2025-01-01",
    requested_end="2025-03-31",
    observations=60,
    first_bar_date="2025-01-02",
    last_bar_date="2025-03-31",
    latest_close=222.06,
    sma20=221.91,
    sma50=230.24,
    return_20d=-0.0673,
    volatility_20d_annualized=0.3093,
    trend_vs_sma20="close_above_sma20",
)

report = generate_research_report(
    snapshot=snapshot,
    model_name="YOUR_INSTALLED_MODEL",
)

print(report.model_dump_json(indent=2))
