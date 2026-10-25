# Trading Research Agent — MVP

A read-only research tool for US stocks and ETFs. It fetches daily OHLCV bars from Alpaca, calculates simple indicators, and writes a deterministic Markdown report. It does **not** use an LLM or place orders yet; the goal is to establish a reliable, testable data/report pipeline before adding an AI layer.

## Requirements

- Python 3.11+
- Alpaca market-data API credentials for live API fetches
- The feed available to your account (the default here is `iex`)

See the [Alpaca historical bars documentation](https://docs.alpaca.markets/us/reference/stockbars) for supported request parameters and data-feed limitations.

## Setup

```bash
git clone <your-repository-url>
cd trading-research-agent
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
cp .env.example .env
```

Add your Alpaca API key and secret to `.env`. Use market-data credentials only; this MVP does not need brokerage/trading credentials. Do not commit `.env`.

## Run

```bash
trading-research AAPL --start 2025-01-01 --end 2025-12-31
```

The end date is inclusive in this CLI. It is converted to an exclusive midnight boundary for the API request, then output is filtered back to the requested date range. The report is written under `reports/` by default.

You can also run it as a module:

```bash
python -m trading_agent.cli AAPL --start 2025-01-01 --end 2025-12-31
```

## Run tests

```bash
pytest
```

Tests use synthetic/local data and do not call Alpaca or require API keys.

## Current behavior and limitations

- Daily bars only; no real-time trading, broker integration, or order submission.
- The `close` values are those returned by the selected feed and adjustment setting. This starter requests split-adjusted bars. It does not guarantee a point-in-time historical dataset suitable for unbiased backtesting.
- A 20-day volatility estimate uses daily close-to-close returns and annualizes with `sqrt(252)`.
- Indicators are descriptive, not buy/sell recommendations.
- The report includes a `NO ACTION` default. No score or indicator should be interpreted as a forecast.
- API feed access, historical depth and rate limits depend on your Alpaca plan.

## Next steps

1. Add saved source metadata and raw response snapshots.
2. Add SEC filing/news retrieval with published-at timestamps.
3. Add a Pydantic evidence-backed thesis schema.
4. Add the LLM research step with read-only tools.
5. Build an evaluation set of dated research cases before judging output quality.
