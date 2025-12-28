def position_size(confidence: float, max_risk: float = 0.02) -> float:
    """
    Calculates position size based on confidence level.
    Uses a simple risk scaling factor.
    """
    return min(max((confidence - 0.5) * 2 * max_risk, 0), max_risk)

def stop_loss(volatility: float) -> float:
    """
    Calculates stop loss percentage based on asset volatility (ATR).
    Uses a 2.5x ATR multiplier for dynamic stops.
    """
    return volatility * 2.5
