import yfinance as yf
import pandas as pd
import time
import sys
from pathlib import Path

print("Testing AAPL data fetching...")

# Try different fetch configurations
def test_fetch(ticker_symbol, period="1mo"):
    print(f"\nAttempting to fetch {ticker_symbol} data for period {period}")
    
    # Try direct ticker history method
    try:
        ticker = yf.Ticker(ticker_symbol)
        data = ticker.history(
            period=period,
            interval="1d",
            auto_adjust=True,
            actions=True,
            prepost=False,
            proxy=None
        )
        
        if data.empty:
            print(f"No data returned for {ticker_symbol} using ticker.history() with period={period}")
        else:
            print(f"SUCCESS! Got {len(data)} rows of data for {ticker_symbol}")
            print(f"Date range: {data.index[0]} to {data.index[-1]}")
            print(f"Columns: {data.columns.tolist()}")
            return data
    except Exception as e:
        print(f"Error using ticker.history(): {str(e)}")

    # Try download method as fallback
    try:
        print(f"Trying alternate method: yf.download()...")
        data = yf.download(
            ticker_symbol,
            period=period,
            interval="1d",
            auto_adjust=True,
            prepost=False,
            proxy=None
        )
        
        if data.empty:
            print(f"No data returned for {ticker_symbol} using yf.download() with period={period}")
        else:
            print(f"SUCCESS with yf.download()! Got {len(data)} rows of data")
            print(f"Date range: {data.index[0]} to {data.index[-1]}")
            print(f"Columns: {data.columns.tolist()}")
            return data
    except Exception as e:
        print(f"Error using yf.download(): {str(e)}")
    
    return None

# Test with different periods and methods
test_fetch("AAPL", "1mo")
time.sleep(1)
test_fetch("AAPL", "1d")
time.sleep(1)
test_fetch("AAPL", "max")
time.sleep(1)

# Try with a different symbol to see if it's AAPL-specific
test_fetch("MSFT", "1mo")

print("\nTest complete. Check the output above to see which method worked.") 