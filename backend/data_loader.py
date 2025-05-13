import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import time

class DataLoader:
    @staticmethod
    def get_market_data(symbol, period='1y', interval='1d', max_retries=3):
        """Fetch market data from Yahoo Finance with enhanced error handling and fallbacks."""
        
        # Convert period to valid yfinance format
        period_map = {
            '1mo': '1mo',
            '3mo': '3mo',
            '6mo': '6mo',
            '1y': '1y',
            '2y': '2y',
            '5y': '5y'
        }
        
        # Get the actual period value or default to '1y'
        actual_period = period_map.get(period, '1y')
        
        # For crypto, append -USD if not already present
        if symbol.upper() in ["BTC", "ETH"] and not symbol.endswith("-USD"):
            symbol = f"{symbol}-USD"
        
        # Try different methods with retries
        for attempt in range(max_retries):
            # Method 1: Try using Ticker.history()
            try:
                ticker = yf.Ticker(symbol)
                data = ticker.history(
                    period=actual_period,
                    interval=interval,
                    auto_adjust=True,
                    actions=True,
                    prepost=True
                )
                
                if not data.empty and len(data) > 0:
                    st.success(f"Successfully fetched data for {symbol}")
                    return data
                
                # Wait before trying the next method
                time.sleep(0.5)
            except Exception as e:
                st.debug(f"Method 1 error for {symbol}: {str(e)}")
                time.sleep(0.5)
            
            # Method 2: Try using yf.download() which can be more reliable
            try:
                data = yf.download(
                    symbol,
                    period=actual_period,
                    interval=interval,
                    auto_adjust=True,
                    prepost=True,
                    progress=False,
                    show_errors=False
                )
                
                if not data.empty and len(data) > 0:
                    st.success(f"Successfully fetched data for {symbol} using alternate method")
                    return data
                
                # Wait before retry
                time.sleep(0.5)
            except Exception as e:
                st.debug(f"Method 2 error for {symbol}: {str(e)}")
                
            # Try a different period as fallback
            if attempt == max_retries - 2:
                try:
                    st.info(f"Trying fallback period 'max' for {symbol}...")
                    data = yf.download(
                        symbol,
                        period="max",
                        interval=interval,
                        auto_adjust=True,
                        progress=False,
                        show_errors=False
                    )
                    
                    if not data.empty and len(data) > 0:
                        st.success(f"Successfully fetched data for {symbol} using fallback period")
                        # Filter to requested timeframe
                        if period == '1mo':
                            data = data.iloc[-30:]
                        elif period == '3mo':
                            data = data.iloc[-90:]
                        elif period == '6mo':
                            data = data.iloc[-180:]
                        elif period == '1y':
                            data = data.iloc[-365:]
                        elif period == '2y':
                            data = data.iloc[-730:]
                        return data
                except Exception as e:
                    st.debug(f"Fallback error for {symbol}: {str(e)}")
            
            time.sleep(1)  # Wait before retrying
        
        # If all methods failed
        st.error(f"Failed to fetch data for {symbol} after multiple attempts. Please check your network connection and try again later.")
        
        # Return some demo data for testing purposes
        start_date = datetime.now() - timedelta(days=365)
        if period == '1mo':
            start_date = datetime.now() - timedelta(days=30)
        elif period == '3mo':
            start_date = datetime.now() - timedelta(days=90)
        elif period == '6mo':
            start_date = datetime.now() - timedelta(days=180)
        
        # Generate synthetic data for testing
        index = pd.date_range(start=start_date, end=datetime.now(), freq='D')
        demo_data = pd.DataFrame({
            'Open': [150 + i * 0.1 for i in range(len(index))],
            'High': [155 + i * 0.1 for i in range(len(index))],
            'Low': [145 + i * 0.1 for i in range(len(index))],
            'Close': [152 + i * 0.1 for i in range(len(index))],
            'Volume': [1000000 + i * 1000 for i in range(len(index))]
        }, index=index)
        
        st.warning(f"Using demo data for {symbol} as real data couldn't be fetched")
        return demo_data

    @staticmethod
    def get_technical_indicators(data):
        """Calculate technical indicators with enhanced error handling."""
        if data is None or len(data) == 0:
            st.error("No data available for technical analysis.")
            return None
        
        try:
            df = data.copy()
            
            # Calculate moving averages with minimum periods
            df['SMA20'] = df['Close'].rolling(window=20, min_periods=5).mean()
            df['SMA50'] = df['Close'].rolling(window=50, min_periods=10).mean()
            
            # Calculate RSI with proper gain/loss handling
            delta = df['Close'].diff()
            gain = delta.where(delta > 0, 0).rolling(window=14, min_periods=1).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14, min_periods=1).mean()
            rs = gain / loss.replace(0, float('inf'))  # Handle division by zero
            df['RSI'] = 100 - (100 / (1 + rs))
            
            # Calculate MACD with proper spans
            exp1 = df['Close'].ewm(span=12, adjust=False, min_periods=12).mean()
            exp2 = df['Close'].ewm(span=26, adjust=False, min_periods=26).mean()
            df['MACD'] = exp1 - exp2
            df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False, min_periods=9).mean()
            
            # Forward fill NaN values at the beginning of the dataset
            df = df.fillna(method='ffill')
            
            # Backward fill any remaining NaN values
            df = df.fillna(method='bfill')
            
            # Set any remaining NaN values to 0
            df = df.fillna(0)
            
            return df
            
        except Exception as e:
            st.error(f"Error calculating technical indicators: {str(e)}")
            return None 