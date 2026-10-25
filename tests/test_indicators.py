import numpy as np
import pandas as pd
import pytest

from trading_agent.analysis.indicators import calculate_indicators
from trading_agent.data.market_data import MarketDataError, validate_bars


def make_bars(n: int = 60) -> pd.DataFrame:
    index = pd.date_range("2025-01-01", periods=n, freq="B", tz="UTC")
    close = np.arange(100.0, 100.0 + n)
    return pd.DataFrame(
        {
            "open": close - 0.5,
            "high": close + 1.0,
            "low": close - 1.0,
            "close": close,
            "volume": np.full(n, 1000),
        },
        index=index,
    )


def test_indicators_calculate_expected_moving_averages():
    result = calculate_indicators(make_bars(60))
    assert result["observations"] == 60
    assert result["latest_close"] == pytest.approx(159.0)
    assert result["sma20"] == pytest.approx(np.mean(np.arange(140.0, 160.0)))
    assert result["sma50"] == pytest.approx(np.mean(np.arange(110.0, 160.0)))
    assert result["return_20d"] == pytest.approx(159 / 139 - 1)
    assert result["trend_vs_sma20"] == "close_above_sma20"


def test_short_history_returns_none_for_long_window_indicators():
    result = calculate_indicators(make_bars(10))
    assert result["sma20"] is None
    assert result["sma50"] is None
    assert result["return_20d"] is None
    assert result["volatility_20d_annualized"] is None
    assert result["trend_vs_sma20"] == "insufficient_data"


def test_empty_bars_raise():
    with pytest.raises(MarketDataError, match="No daily bars"):
        validate_bars(pd.DataFrame())


def test_invalid_high_low_raises():
    bars = make_bars(3)
    bars.iloc[0, bars.columns.get_loc("high")] = 1
    with pytest.raises(MarketDataError, match="high is below"):
        validate_bars(bars)


def test_duplicate_timestamps_raise():
    bars = make_bars(3)
    bars.index = [bars.index[0], bars.index[1], bars.index[1]]
    with pytest.raises(MarketDataError, match="Duplicate"):
        validate_bars(bars)
