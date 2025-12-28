import pandas as pd

def momentum_alpha(df: pd.DataFrame) -> pd.Series:
    """
    Tactical Momentum Alpha.
    Conditions on trending regime and positive 10-period returns.
    """
    return ((df["trend_regime"] == 1) & (df["ret"].rolling(10).mean() > 0)).astype(int)

def mean_reversion_alpha(df: pd.DataFrame) -> pd.Series:
    """
    Mean Reversion Alpha.
    Conditions on range-bound regime and oversold RSI.
    """
    return ((df["trend_regime"] == 0) & (df["rsi"] < 30)).astype(int)

def breakout_alpha(df: pd.DataFrame) -> pd.Series:
    """
    Breakout Alpha.
    Directly uses the breakout indicator from feature engineering.
    """
    return df["breakout"]
