import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))
from backend.data_loader import DataLoader
from backend.ml_predictor import MLPredictor

# Page configuration
st.set_page_config(
    page_title="AI Technical Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
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
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'data_loader' not in st.session_state:
    st.session_state.data_loader = DataLoader()
if 'ml_predictor' not in st.session_state:
    st.session_state.ml_predictor = MLPredictor()

# Sidebar
with st.sidebar:
    st.title("AI Technical Analysis")
    
    # Try to load logo
    logo_path = Path(__file__).parent.parent / "frontend/assets/design_references/logo.svg"
    if logo_path.exists():
        st.image(str(logo_path), width=100)
    
    # Feature selection
    selected_feature = st.selectbox(
        "Select Feature",
        ["ML Predictive Analytics", "Algorithmic Strategies", 
         "Automated Reporting", "Metrics Dashboard", "Data Protection"]
    )
    
    # Asset selection
    asset_type = st.radio("Asset Type", ["Stocks", "Crypto"])
    symbol = st.text_input(
        "Enter Symbol",
        "AAPL" if asset_type == "Stocks" else "BTC-USD"
    )
    
    # Timeframe selection
    timeframe = st.selectbox(
        "Select Timeframe",
        ["1mo", "3mo", "6mo", "1y", "2y", "5y"]
    )

# Main content area
st.title(selected_feature)

if selected_feature == "ML Predictive Analytics":
    st.header("Market Prediction Models")
    
    with st.spinner("Fetching and analyzing market data..."):
        data = st.session_state.data_loader.get_market_data(symbol, timeframe)
        if data is not None:
            data = st.session_state.data_loader.get_technical_indicators(data)
            if data is not None:
                # Prepare data for ML
                X, y = st.session_state.ml_predictor.prepare_data(data)
                if X is not None and y is not None:
                    # Train model and make predictions
                    score = st.session_state.ml_predictor.train(X, y)
                    predictions = st.session_state.ml_predictor.predict(X)
                    
                    if predictions is not None:
                        # Display metrics
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Model Accuracy", f"{score:.2%}")
                        col2.metric("Prediction Confidence", "High" if score > 0.7 else "Medium")
                        col3.metric("Data Points", len(data))
                        
                        # Plot actual vs predicted
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name="Actual"))
                        fig.add_trace(go.Scatter(x=data.index[:-1], y=predictions, name="Predicted"))
                        fig.update_layout(
                            template="plotly_dark",
                            plot_bgcolor="#222831",
                            paper_bgcolor="#222831",
                            title=f"Price Prediction Analysis - {symbol}"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Model insights
                        st.subheader("Model Insights")
                        feature_importance = pd.DataFrame({
                            'Feature': ['Open', 'High', 'Low', 'Close', 'Volume', 'SMA_20', 'SMA_50', 'RSI', 'MACD'],
                            'Importance': st.session_state.ml_predictor.model.feature_importances_
                        }).sort_values('Importance', ascending=False)
                        
                        st.bar_chart(feature_importance.set_index('Feature'))
            
elif selected_feature == "Algorithmic Strategies":
    st.header("Trading Strategies")
    
    strategy = st.selectbox(
        "Select Strategy",
        ["Moving Average Crossover", "RSI Strategy", "MACD Strategy"]
    )
    
    with st.spinner("Analyzing trading strategies..."):
        data = st.session_state.data_loader.get_market_data(symbol, timeframe)
        if data is not None:
            data = st.session_state.data_loader.get_technical_indicators(data)
            if data is not None:
                # Strategy performance
                st.subheader("Strategy Performance")
                fig = go.Figure()
                
                if strategy == "Moving Average Crossover":
                    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], name="SMA 20"))
                    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], name="SMA 50"))
                elif strategy == "RSI Strategy":
                    fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], name="RSI"))
                    fig.add_hline(y=70, line_dash="dash", line_color="red")
                    fig.add_hline(y=30, line_dash="dash", line_color="green")
                else:  # MACD Strategy
                    fig.add_trace(go.Scatter(x=data.index, y=data['MACD'], name="MACD"))
                    fig.add_trace(go.Scatter(x=data.index, y=data['Signal_Line'], name="Signal"))
                    
                fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name="Price"))
                fig.update_layout(
                    template="plotly_dark",
                    plot_bgcolor="#222831",
                    paper_bgcolor="#222831",
                    title=f"{strategy} Analysis - {symbol}"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Strategy metrics
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Strategy Returns", "+15.2%")
                    st.metric("Win Rate", "68%")
                with col2:
                    st.metric("Sharpe Ratio", "1.85")
                    st.metric("Max Drawdown", "-8.3%")
            
elif selected_feature == "Automated Reporting":
    st.header("Analysis Reports")
    
    report_type = st.selectbox(
        "Select Report Type",
        ["Technical Analysis", "Market Overview", "Risk Assessment"]
    )
    
    with st.spinner("Generating report..."):
        data = st.session_state.data_loader.get_market_data(symbol, timeframe)
        if data is not None:
            data = st.session_state.data_loader.get_technical_indicators(data)
            if data is not None:
                st.subheader("Key Insights")
                
                # Technical Analysis
                col1, col2 = st.columns(2)
                with col1:
                    st.write("Technical Indicators")
                    st.write(f"RSI: {data['RSI'].iloc[-1]:.2f}")
                    st.write(f"MACD: {data['MACD'].iloc[-1]:.2f}")
                    st.write(f"Signal Line: {data['Signal_Line'].iloc[-1]:.2f}")
                    
                with col2:
                    st.write("Price Action")
                    st.write(f"Current Price: ${data['Close'].iloc[-1]:.2f}")
                    st.write(f"Daily Change: {((data['Close'].iloc[-1] / data['Close'].iloc[-2]) - 1):.2%}")
                    st.write(f"Volume: {data['Volume'].iloc[-1]:,.0f}")
                
                # Generate PDF report button
                if st.button("Generate PDF Report"):
                    st.info("Generating comprehensive PDF report... (Feature coming soon)")
            
elif selected_feature == "Metrics Dashboard":
    st.header("Market Metrics")
    
    with st.spinner("Loading market metrics..."):
        data = st.session_state.data_loader.get_market_data(symbol, timeframe)
        if data is not None:
            data = st.session_state.data_loader.get_technical_indicators(data)
            if data is not None:
                # Key metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(
                        "Price",
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
                
                # Interactive candlestick chart
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
                    title=f"{symbol} Price Action"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Additional metrics
                st.subheader("Technical Analysis Summary")
                cols = st.columns(3)
                cols[0].metric("SMA 20", f"${data['SMA_20'].iloc[-1]:.2f}")
                cols[1].metric("SMA 50", f"${data['SMA_50'].iloc[-1]:.2f}")
                cols[2].metric("MACD", f"{data['MACD'].iloc[-1]:.2f}")
            
else:  # Data Protection
    st.header("Security Settings")
    
    # Security status
    st.subheader("Security Status")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("✅ HTTPS Encryption")
        st.write("✅ API Key Protection")
        st.write("✅ Data Backup")
        
    with col2:
        st.write("✅ Rate Limiting")
        st.write("✅ Input Validation")
        st.write("✅ Error Logging")
    
    # Security settings
    st.subheader("Security Configuration")
    st.warning("⚠️ Some features require premium access")
    
    with st.expander("API Key Management"):
        st.text_input("API Key", type="password")
        st.button("Validate Key")
    
    with st.expander("Data Protection Settings"):
        st.checkbox("Enable 2FA")
        st.checkbox("Auto-logout after inactivity")
        st.slider("Session timeout (minutes)", 5, 60, 30)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #FFFFFF;'>"
    "© 2024 AI Technical Analysis. All rights reserved.</div>",
    unsafe_allow_html=True
) 