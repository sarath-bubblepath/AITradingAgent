from datetime import datetime, timezone

from trading_agent.reporting import build_markdown_report, save_report
from trading_agent.schemas import MarketSnapshot


def snapshot() -> MarketSnapshot:
    return MarketSnapshot(
        ticker="AAPL",
        requested_start="2025-01-01",
        requested_end="2025-03-31",
        retrieved_at=datetime(2025, 4, 1, tzinfo=timezone.utc),
        observations=60,
        first_bar_date="2025-01-02",
        last_bar_date="2025-03-31",
        latest_close=210.25,
        sma20=205.0,
        sma50=198.0,
        return_20d=0.04,
        volatility_20d_annualized=0.22,
        trend_vs_sma20="close_above_sma20",
    )


def test_report_includes_metrics_and_no_action():
    report = build_markdown_report(snapshot())
    assert "Market Research Snapshot: AAPL" in report
    assert "$210.25" in report
    assert "4.00%" in report
    assert "Default action: NO ACTION" in report


def test_save_report_creates_markdown(tmp_path):
    path = save_report(
        build_markdown_report(snapshot()),
        "AAPL",
        __import__("datetime").date(2025, 1, 1),
        __import__("datetime").date(2025, 3, 31),
        tmp_path,
    )
    assert path.exists()
    assert path.suffix == ".md"
    assert "AAPL" in path.read_text(encoding="utf-8")
