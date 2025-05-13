import pandas as pd
import numpy as np

def calculate_sma(data: pd.DataFrame, window: int) -> pd.Series:
    """Calculate Simple Moving Average"""
    return data['Close'].rolling(window=window).mean()

def calculate_ema(data: pd.DataFrame, span: int) -> pd.Series:
    """Calculate Exponential Moving Average"""
    return data['Close'].ewm(span=span).mean()

def calculate_bollinger_bands(data: pd.DataFrame, window: int = 20) -> tuple:
    """Calculate Bollinger Bands"""
    sma = data['Close'].rolling(window=window).mean()
    std = data['Close'].rolling(window=window).std()
    bb_upper = sma + 2 * std
    bb_lower = sma - 2 * std
    return bb_upper, bb_lower

def calculate_vwap(data: pd.DataFrame) -> pd.Series:
    """Calculate Volume Weighted Average Price"""
    return (data['Close'] * data['Volume']).cumsum() / data['Volume'].cumsum()

def calculate_rsi(data: pd.DataFrame, window: int = 14) -> pd.Series:
    """Calculate Relative Strength Index"""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(data: pd.DataFrame) -> tuple:
    """Calculate MACD and Signal Line"""
    ema_12 = data['Close'].ewm(span=12).mean()
    ema_26 = data['Close'].ewm(span=26).mean()
    macd = ema_12 - ema_26
    signal = macd.ewm(span=9).mean()
    return macd, signal 