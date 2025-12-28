import os
import requests
import pandas as pd
from dotenv import load_dotenv
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

AV_KEY = os.getenv("ALPHAVANTAGE_KEY")
MS_KEY = os.getenv("MARKETSTACK_KEY")

def fetch_alpha(symbol: str) -> pd.DataFrame:
    """
    Primary – AlphaVantage India
    """
    if not AV_KEY:
        raise ValueError("ALPHAVANTAGE_KEY not found in environment")
        
    url = (
        f"https://www.alphavantage.co/query?"
        f"function=TIME_SERIES_DAILY_ADJUSTED"
        f"&symbol={symbol}.BSE"
        f"&outputsize=full"
        f"&apikey={AV_KEY}"
    )
    
    response = requests.get(url)
    response.raise_for_status()
    data_json = response.json()
    
    if "Time Series (Daily)" not in data_json:
        error_msg = data_json.get("Note", data_json.get("Error Message", "Unknown error fetching from AlphaVantage"))
        raise Exception(f"AlphaVantage Error: {error_msg}")
        
    data = data_json["Time Series (Daily)"]
    df = pd.DataFrame(data).T.astype(float).reset_index()
    df.rename(columns={
        "index": "date",
        "1. open": "open",
        "2. high": "high",
        "3. low": "low",
        "4. close": "price",
        "6. volume": "volume"
    }, inplace=True)
    return df.sort_values("date")


def fetch_marketstack(symbol: str) -> pd.DataFrame:
    """
    Backup – MarketStack
    """
    if not MS_KEY:
        raise ValueError("MARKETSTACK_KEY not found in environment")
        
    url = f"http://api.marketstack.com/v1/eod?access_key={MS_KEY}&symbols={symbol}.XNSE&limit=1000"
    response = requests.get(url)
    response.raise_for_status()
    data_json = response.json()
    
    if "data" not in data_json:
        raise Exception("MarketStack Error: No data field in response")
        
    data = data_json["data"]
    df = pd.DataFrame(data)
    
    if df.empty:
        raise Exception(f"MarketStack Error: No data returned for symbol {symbol}")
        
    df.rename(columns={
        "date": "date",
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "price",
        "volume": "volume"
    }, inplace=True)
    return df.sort_values("date")


def fetch_ohlc(symbol: str) -> pd.DataFrame:
    """
    Unified collector with failover logic
    """
    try:
        logger.info(f"Attempting to fetch data for {symbol} from AlphaVantage...")
        return fetch_alpha(symbol)
    except Exception as e:
        logger.warning(f"AlphaVantage failed: {e}. Trying MarketStack...")
        try:
            return fetch_marketstack(symbol)
        except Exception as e2:
            logger.error(f"Both providers failed for {symbol}: {e2}")
            raise Exception(f"Failed to fetch market data for {symbol} from all providers.")
