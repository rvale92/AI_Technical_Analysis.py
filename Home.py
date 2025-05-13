import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))
from backend.data_loader import DataLoader
from backend.ml_predictor import MLPredictor

# Page configuration
st.set_page_config(
    page_title="AI Technical Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/AI_Technical_Analysis',
        'Report a bug': "https://github.com/yourusername/AI_Technical_Analysis/issues",
        'About': "# AI Technical Analysis\nAn AI-powered technical analysis platform."
    }
)

# Custom CSS for dark theme
st.markdown("""
    <style>
    .stApp {
        background-color: #222831;
        color: #FFFFFF;
    }
    .stButton>button {
        background-color: #00ADB5;
        color: #FFFFFF;
    }
    .stProgress .st-bo {
        background-color: #00ADB5;
    }
    .stSelectbox {
        color: #FFFFFF;
    }
    div[data-testid="stSidebarNav"] {
        background-color: #393E46;
    }
    input[type="text"] {
        autocomplete: "off";
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'data_loader' not in st.session_state:
    st.session_state.data_loader = DataLoader()
if 'ml_predictor' not in st.session_state:
    st.session_state.ml_predictor = MLPredictor()

# Main content
st.title("AI Technical Analysis")
st.subheader("Welcome to the AI-powered Technical Analysis Platform")

# Asset selection
col1, col2 = st.columns(2)
with col1:
    asset_type = st.radio("Asset Type", ["Stocks", "Crypto"], key="asset_type")
    symbol = st.text_input(
        "Enter Symbol",
        value="AAPL" if asset_type == "Stocks" else "BTC-USD",
        key="symbol_input",
        autocomplete="off"
    )

with col2:
    timeframe = st.selectbox(
        "Select Timeframe",
        ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        key="timeframe_select"
    )

# Fetch initial data
if symbol:
    with st.spinner("Loading market data..."):
        data = st.session_state.data_loader.get_market_data(symbol, timeframe)
        if data is not None:
            data = st.session_state.data_loader.get_technical_indicators(data)
            if data is not None:
                # Display current price and metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(
                        "Current Price",
                        f"${data['Close'].iloc[-1]:.2f}",
                        f"{((data['Close'].iloc[-1] / data['Close'].iloc[-2]) - 1):.2%}"
                    )
                with col2:
                    st.metric(
                        "Volume",
                        f"{data['Volume'].iloc[-1]:,.0f}",
                        f"{((data['Volume'].iloc[-1] / data['Volume'].iloc[-2]) - 1):.2%}"
                    )
                with col3:
                    st.metric(
                        "RSI",
                        f"{data['RSI'].iloc[-1]:.2f}",
                        "Overbought" if data['RSI'].iloc[-1] > 70 else "Oversold" if data['RSI'].iloc[-1] < 30 else "Neutral"
                    )

                # Display candlestick chart
                st.subheader("Price Action")
                fig = go.Figure(data=[go.Candlestick(
                    x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close']
                )])
                fig.update_layout(
                    template="plotly_dark",
                    plot_bgcolor="#222831",
                    paper_bgcolor="#222831",
                    title=f"{symbol} Price Action",
                    xaxis_title="Date",
                    yaxis_title="Price ($)",
                    showlegend=True
                )
                st.plotly_chart(fig, use_container_width=True)

# Feature cards
st.subheader("Available Features")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 📈 ML Predictions
    Access machine learning-powered market predictions and insights.
    """)
    if st.button("Go to ML Predictions", key="ml_pred_btn"):
        st.switch_page("pages/1_🤖_ML_Predictions.py")

with col2:
    st.markdown("""
    ### 🤖 Trading Strategies
    Explore and backtest various trading strategies.
    """)
    if st.button("Go to Strategies", key="strat_btn"):
        st.switch_page("pages/2_📈_Trading_Strategies.py")

with col3:
    st.markdown("""
    ### 📊 Market Metrics
    View detailed market metrics and indicators.
    """)
    if st.button("Go to Metrics", key="metrics_btn"):
        st.switch_page("pages/3_📊_Market_Metrics.py")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #FFFFFF;'>"
    "© 2024 AI Technical Analysis. All rights reserved.</div>",
    unsafe_allow_html=True
) 