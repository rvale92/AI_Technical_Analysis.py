import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import logging
import ta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Print debug information
logger.info("Starting Streamlit application...")

# Configure Streamlit page
st.set_page_config(
    page_title="Stock Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

logger.info("Page config set...")

# Add custom CSS for better styling
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 Stock Technical Analysis")
logger.info("Title set...")

# Sidebar inputs
st.sidebar.header("Stock Selection")
ticker = st.sidebar.text_input("Enter Stock Ticker:", "AAPL").upper()

# Technical Indicators Selection
st.sidebar.header("Technical Indicators")
show_sma = st.sidebar.checkbox("Show SMA", True)
show_ema = st.sidebar.checkbox("Show EMA", True)
show_bbands = st.sidebar.checkbox("Show Bollinger Bands", False)
show_rsi = st.sidebar.checkbox("Show RSI", False)
show_macd = st.sidebar.checkbox("Show MACD", False)

# Date range selection
today = datetime.now()
start_date = st.sidebar.date_input("Start Date", value=today - timedelta(days=365))
end_date = st.sidebar.date_input("End Date", value=today)

logger.info("Sidebar inputs created...")

def calculate_technical_indicators(data):
    # Calculate SMAs
    data['SMA20'] = ta.trend.sma_indicator(data['Close'], window=20)
    data['SMA50'] = ta.trend.sma_indicator(data['Close'], window=50)
    
    # Calculate EMAs
    data['EMA20'] = ta.trend.ema_indicator(data['Close'], window=20)
    data['EMA50'] = ta.trend.ema_indicator(data['Close'], window=50)
    
    # Calculate Bollinger Bands
    indicator_bb = ta.volatility.BollingerBands(close=data["Close"], window=20, window_dev=2)
    data['BB_upper'] = indicator_bb.bollinger_hband()
    data['BB_lower'] = indicator_bb.bollinger_lband()
    data['BB_middle'] = indicator_bb.bollinger_mavg()
    
    # Calculate RSI
    data['RSI'] = ta.momentum.rsi(data['Close'], window=14)
    
    # Calculate MACD
    indicator_macd = ta.trend.MACD(close=data["Close"])
    data['MACD'] = indicator_macd.macd()
    data['MACD_signal'] = indicator_macd.macd_signal()
    
    return data

# Button to fetch data
if st.sidebar.button("Analyze Stock"):
    logger.info(f"Analyzing stock: {ticker}")
    try:
        # Show loading message
        with st.spinner(f"Fetching data for {ticker}..."):
            logger.info("Fetching stock data...")
            # Fetch stock data
            data = yf.download(ticker, start=start_date, end=end_date)
            logger.info(f"Data fetched. Shape: {data.shape}")
            
            if len(data) > 0:
                st.success(f"Successfully loaded data for {ticker}")
                logger.info("Processing data...")
                
                # Calculate technical indicators
                data = calculate_technical_indicators(data)
                
                # Calculate metrics
                current_price = float(data['Close'].iloc[-1])
                previous_close = float(data['Close'].iloc[-2]) if len(data) > 1 else current_price
                price_change = current_price - previous_close
                price_change_pct = (price_change / previous_close) * 100
                
                # Display metrics in columns
                col1, col2, col3 = st.columns(3)
                col1.metric(
                    "Current Price",
                    f"${current_price:.2f}",
                    f"{price_change_pct:+.2f}%",
                    delta_color="normal"
                )
                col2.metric(
                    "Volume",
                    f"{int(data['Volume'].iloc[-1]):,}",
                    ""
                )
                col3.metric(
                    "RSI",
                    f"{data['RSI'].iloc[-1]:.1f}",
                    ""
                )
                
                logger.info("Creating price chart...")
                # Create main price chart
                fig = go.Figure()
                
                # Add candlestick chart
                fig.add_trace(go.Candlestick(
                    x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'],
                    name="OHLC"
                ))
                
                # Add selected technical indicators
                if show_sma:
                    fig.add_trace(go.Scatter(x=data.index, y=data['SMA20'], 
                                           name='SMA 20', line=dict(color='orange')))
                    fig.add_trace(go.Scatter(x=data.index, y=data['SMA50'], 
                                           name='SMA 50', line=dict(color='blue')))
                
                if show_ema:
                    fig.add_trace(go.Scatter(x=data.index, y=data['EMA20'], 
                                           name='EMA 20', line=dict(color='purple')))
                    fig.add_trace(go.Scatter(x=data.index, y=data['EMA50'], 
                                           name='EMA 50', line=dict(color='cyan')))
                
                if show_bbands:
                    fig.add_trace(go.Scatter(x=data.index, y=data['BB_upper'], 
                                           name='BB Upper', line=dict(color='gray', dash='dash')))
                    fig.add_trace(go.Scatter(x=data.index, y=data['BB_lower'], 
                                           name='BB Lower', line=dict(color='gray', dash='dash')))
                    fig.add_trace(go.Scatter(x=data.index, y=data['BB_middle'], 
                                           name='BB Middle', line=dict(color='gray')))
                
                # Update layout
                fig.update_layout(
                    title=f"{ticker} Stock Price",
                    yaxis_title="Price ($)",
                    xaxis_title="Date",
                    template="plotly_dark",
                    xaxis_rangeslider_visible=False,
                    height=600
                )
                
                logger.info("Displaying price chart...")
                # Display the chart
                st.plotly_chart(fig, use_container_width=True)
                
                # Show RSI if selected
                if show_rsi:
                    rsi_fig = go.Figure()
                    rsi_fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], name='RSI'))
                    rsi_fig.add_hline(y=70, line_color='red', line_dash='dash')
                    rsi_fig.add_hline(y=30, line_color='green', line_dash='dash')
                    rsi_fig.update_layout(
                        title="Relative Strength Index (RSI)",
                        yaxis_title="RSI",
                        template="plotly_dark",
                        height=300
                    )
                    st.plotly_chart(rsi_fig, use_container_width=True)
                
                # Show MACD if selected
                if show_macd:
                    macd_fig = go.Figure()
                    macd_fig.add_trace(go.Scatter(x=data.index, y=data['MACD'], name='MACD'))
                    macd_fig.add_trace(go.Scatter(x=data.index, y=data['MACD_signal'], name='Signal Line'))
                    macd_fig.update_layout(
                        title="Moving Average Convergence Divergence (MACD)",
                        yaxis_title="MACD",
                        template="plotly_dark",
                        height=300
                    )
                    st.plotly_chart(macd_fig, use_container_width=True)
                
                logger.info("Creating volume chart...")
                # Volume chart
                st.subheader("Volume Analysis")
                volume_fig = go.Figure()
                
                # Add volume bars
                colors = ['red' if close < open else 'green' 
                         for close, open in zip(data['Close'], data['Open'])]
                
                volume_fig.add_trace(
                    go.Bar(
                        x=data.index,
                        y=data['Volume'],
                        marker_color=colors,
                        name="Volume"
                    )
                )
                
                # Update volume chart layout
                volume_fig.update_layout(
                    title=f"{ticker} Trading Volume",
                    yaxis_title="Volume",
                    xaxis_title="Date",
                    template="plotly_dark",
                    height=400
                )
                
                logger.info("Displaying volume chart...")
                # Display volume chart
                st.plotly_chart(volume_fig, use_container_width=True)
                
            else:
                st.error(f"No data available for {ticker}. Please verify the ticker symbol.")
                logger.error(f"No data found for {ticker}")
                
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        logger.error(f"Error processing data: {str(e)}")
        st.info("Please check the ticker symbol and try again.")
else:
    st.info("👈 Enter a stock ticker and click 'Analyze Stock' to begin the analysis.")

logger.info("Application setup complete.") 