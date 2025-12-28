from fastapi import APIRouter
from app.pipelines.market_inference import MarketInferenceEngine

router = APIRouter(prefix="/market", tags=["Market AI"])

engine = MarketInferenceEngine()


@router.get("/analyze/{symbol}")
def analyze_market(symbol: str):
    """
    Full AI Market Intelligence Endpoint
    """
    return engine.analyze(symbol)
