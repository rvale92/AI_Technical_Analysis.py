from datetime import datetime
import pandas as pd

def validate_dates(start_date: str, end_date: str) -> bool:
    """Validate date inputs"""
    try:
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        return start < end
    except:
        return False

def format_date(date: datetime) -> str:
    """Format date for display"""
    return date.strftime('%Y-%m-%d')

def validate_ticker(ticker: str) -> str:
    """Validate and format ticker symbol"""
    return ticker.strip().upper()

SUGGESTED_TICKERS = [
    "TSLA", "SMCI", "CSO", "IBM", "INTC", "AMD", "META", "MSTR", "NVDA", "MSFT",
    "NET", "GOOG", "BIDI", "BABA", "SHOP", "AMZN", "BTDR", "RIOT", "MARA", "EXOD",
    "BTC", "GSOL", "ARKK", "FDIG", "ETHE", "GBTC", "COIN"
] 