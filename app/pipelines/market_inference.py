import numpy as np
import logging
from typing import Dict, Any
from services.nse_collector import fetch_ohlc
from app.data.market_features import build_market_features
from app.core.alpha_engine import (
    momentum_alpha,
    mean_reversion_alpha,
    breakout_alpha
)
from app.core.risk_engine import position_size, stop_loss
from app.core.llm_reasoner import reason
from app.core.verdict_parser import parse

logger = logging.getLogger(__name__)

class MarketInferenceEngine:
    """
    Central Market Intelligence Brain
    ---------------------------------
    Coordinates data collection, feature engineering, alpha signal generation,
    risk assessment, and LLM-based cognitive arbitration.
    """

    def analyze(self, symbol: str) -> Dict[str, Any]:
        """
        Performs a full market analysis for a given symbol.
        """
        try:
            # 1. Load & build market state
            df = fetch_ohlc(symbol)
            df = build_market_features(df)

            # 2. Alpha models (regime filtered)
            a_mom = momentum_alpha(df).iloc[-1]
            a_mr  = mean_reversion_alpha(df).iloc[-1]
            a_bo  = breakout_alpha(df).iloc[-1]

            alpha_probability = float(np.mean([a_mom, a_mr, a_bo]))

            # 3. Risk metrics
            atr = float(df['atr'].iloc[-1])
            stop = float(stop_loss(atr))

            # 4. LLM arbitration payload
            llm_payload = {
                "symbol": symbol,
                "alpha_probability": alpha_probability,
                "market_state": {
                    "trend_regime": int(df["trend_regime"].iloc[-1]),
                    "volatility_regime": int(df["vol_regime"].iloc[-1]),
                    "accumulation": int(df["accumulation"].iloc[-1]),
                    "distribution": int(df["distribution"].iloc[-1]),
                    "breakout": int(df["breakout"].iloc[-1]),
                    "exhaustion": int(df["exhaustion"].iloc[-1]),
                },
                "recent_prices": df.tail(20)["price"].tolist()
            }

            logger.info(f"Generating LLM reasoning for {symbol}...")
            llm_text = reason(llm_payload)
            verdict  = parse(llm_text)

            # 5. Risk-aware sizing
            size = float(position_size(verdict["confidence"]))

            # 6. Final intelligence object
            return {
                "symbol": symbol,
                "verdict": verdict["verdict"],
                "confidence": round(verdict["confidence"], 3),
                "position_size": round(size, 4),
                "stop_loss_pct": round(stop, 4),
                "market_state": llm_payload["market_state"],
                "llm_reasoning": verdict["raw_reasoning"]
            }
        except Exception as e:
            logger.error(f"Analysis failed for {symbol}: {e}")
            return {
                "symbol": symbol,
                "error": str(e),
                "verdict": "ERROR",
                "status": "failed"
            }
