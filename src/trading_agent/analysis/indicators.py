from __future__ import annotations

import math
import pandas as pd

from trading_agent.data.market_data import validate_bars


def calculate_indicators(bars: pd.DataFrame) -> dict[str, float | int | str | None]:
    """Calculate descriptive indicators using only bars supplied by the caller."""
    clean = validate_bars(bars)
    close = clean["close"].astype(float)
    returns = close.pct_change().dropna()

    latest_close = float(close.iloc[-1])
    sma20_series = close.rolling(window=20, min_periods=20).mean()
    sma50_series = close.rolling(window=50, min_periods=50).mean()
    sma20 = float(sma20_series.iloc[-1]) if pd.notna(sma20_series.iloc[-1]) else None
    sma50 = float(sma50_series.iloc[-1]) if pd.notna(sma50_series.iloc[-1]) else None

    return_20d = None
    if len(close) >= 21 and close.iloc[-21] != 0:
        return_20d = float(close.iloc[-1] / close.iloc[-21] - 1.0)

    volatility_20d = None
    if len(returns) >= 20:
        volatility_20d = float(returns.tail(20).std(ddof=1) * math.sqrt(252))

    if sma20 is None:
        trend = "insufficient_data"
    elif latest_close > sma20:
        trend = "close_above_sma20"
    elif latest_close < sma20:
        trend = "close_below_sma20"
    else:
        trend = "close_at_sma20"

    return {
        "observations": int(len(clean)),
        "first_bar_date": clean.index[0].date().isoformat(),
        "last_bar_date": clean.index[-1].date().isoformat(),
        "latest_close": latest_close,
        "sma20": sma20,
        "sma50": sma50,
        "return_20d": return_20d,
        "volatility_20d_annualized": volatility_20d,
        "trend_vs_sma20": trend,
    }
