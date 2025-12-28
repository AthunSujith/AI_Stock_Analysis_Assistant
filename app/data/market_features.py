import ta
import pandas as pd

def build_market_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes institutional technical indicators and market regime features.
    
    Returns:
        pd.DataFrame: DataFrame with added features, with NaNs removed.
    """
    if len(df) < 60:
        raise ValueError("Not enough market data for institutional indicators (minimum 60 periods required)")

    # 1. Basic Returns
    df["ret"] = df["price"].pct_change()

    # 2. Trend Indicators
    df["ema_fast"] = ta.trend.ema_indicator(df["price"], 20)
    df["ema_slow"] = ta.trend.ema_indicator(df["price"], 50)
    df["trend_strength"] = ta.trend.adx(df["high"], df["low"], df["price"], 14)
    df["trend_regime"] = (df["ema_fast"] > df["ema_slow"]).astype(int)

    # 3. Volatility Indicators
    df["atr"] = ta.volatility.average_true_range(df["high"], df["low"], df["price"], 14)
    df["vol_regime"] = (df["atr"] > df["atr"].rolling(50).mean()).astype(int)

    # 4. Volume Analysis (Z-Score)
    df["vol_z"] = (df["volume"] - df["volume"].rolling(30).mean()) / df["volume"].rolling(30).std()
    df["accumulation"] = (df["vol_z"] > 1).astype(int)
    df["distribution"] = (df["vol_z"] < -1).astype(int)

    # 5. Momentum Indicators
    df["rsi"] = ta.momentum.rsi(df["price"], 14)
    df["exhaustion"] = ((df["rsi"] > 75) | (df["rsi"] < 25)).astype(int)

    # 6. Range and Breakout Detection
    df["range_high"] = df["price"].rolling(20).max()
    df["range_low"] = df["price"].rolling(20).min()
    df["breakout"] = ((df["price"] > df["range_high"]) & (df["accumulation"] == 1)).astype(int)

    return df.dropna()
