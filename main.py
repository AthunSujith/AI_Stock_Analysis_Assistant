import logging
from fastapi import FastAPI
from app.api.market import router as market_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="NSE AI Market Intelligence Engine",
    description="Institution-grade AI market inference system for Indian Equities",
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.on_event("startup")
async def startup_event():
    logger.info("NSE AI Market Intelligence Engine starting up...")

app.include_router(market_router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "engine": "NSE AI Market Intelligence",
        "version": "1.1.0",
        "endpoints": ["/market/analyze/{symbol}"]
    }
