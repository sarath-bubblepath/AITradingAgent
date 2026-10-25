from __future__ import annotations

from datetime import date, datetime, timezone
from pathlib import Path

from trading_agent.schemas import MarketSnapshot


def _fmt_number(value: float | None, digits: int = 2) -> str:
    return "N/A" if value is None else f"{value:,.{digits}f}"


def _fmt_pct(value: float | None) -> str:
    return "N/A" if value is None else f"{value:.2%}"


def build_markdown_report(snapshot: MarketSnapshot) -> str:
    """Create a deterministic, non-advisory summary from validated market data."""
    generated_at = datetime.now(timezone.utc).isoformat()
    return f"""# Market Research Snapshot: {snapshot.ticker}

- **Generated at (UTC):** {generated_at}
- **Requested period:** {snapshot.requested_start} through {snapshot.requested_end}
- **Observed bars:** {snapshot.observations}
- **Data coverage:** {snapshot.first_bar_date} through {snapshot.last_bar_date}
- **Latest close:** ${snapshot.latest_close:,.2f}

## Indicators

| Metric | Value |
|---|---:|
| 20-day simple moving average | {_fmt_number(snapshot.sma20)} |
| 50-day simple moving average | {_fmt_number(snapshot.sma50)} |
| 20-session return | {_fmt_pct(snapshot.return_20d)} |
| 20-day annualized realized volatility | {_fmt_pct(snapshot.volatility_20d_annualized)} |
| Close vs. 20-day SMA | `{snapshot.trend_vs_sma20}` |

## Deterministic observations

- Trend label: `{snapshot.trend_vs_sma20}`.
- 20-session return: {_fmt_pct(snapshot.return_20d)}.
- Annualized realized volatility estimate: {_fmt_pct(snapshot.volatility_20d_annualized)}.

## Research status

**Default action: NO ACTION.**

This report summarizes historical data only. It does not include company fundamentals, news, valuation, transaction costs, or an AI-generated thesis. Indicators are descriptive and do not predict future returns. Verify data coverage and source/feed limitations before relying on the report.
"""


def save_report(markdown: str, ticker: str, start: date, end: date, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{ticker.upper()}_{start.isoformat()}_{end.isoformat()}.md"
    path = output_dir / filename
    path.write_text(markdown, encoding="utf-8")
    return path
