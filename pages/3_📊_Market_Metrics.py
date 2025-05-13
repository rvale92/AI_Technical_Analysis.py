import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))
from backend.data_loader import DataLoader

# Page configuration
st.set_page_config(
    page_title="Market Metrics - AI Technical Analysis",
    page_icon="📊",
    layout="wide"
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
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'data_loader' not in st.session_state:
    st.session_state.data_loader = DataLoader()

st.title("Market Metrics")
st.subheader("Technical Analysis Dashboard")

# Asset selection
col1, col2 = st.columns(2)
with col1:
    symbol = st.text_input("Enter Symbol", "AAPL", key="metrics_symbol_input", autocomplete="off")
with col2:
    timeframe = st.selectbox(
        "Select Timeframe",
        ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        key="metrics_timeframe_select"
    )

if st.button("Analyze", key="analyze_metrics_btn"):
    with st.spinner("Calculating metrics..."):
        # Get market data
        data = st.session_state.data_loader.get_market_data(symbol, timeframe)
        if data is not None:
            # Calculate technical indicators
            data = st.session_state.data_loader.get_technical_indicators(data)
            
            # Display main metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(
                    "Current Price",
                    f"${data['Close'].iloc[-1]:.2f}",
                    f"{((data['Close'].iloc[-1] / data['Close'].iloc[-2]) - 1):.2%}"
                )
            with col2:
                st.metric(
                    "RSI",
                    f"{data['RSI'].iloc[-1]:.2f}",
                    "Overbought" if data['RSI'].iloc[-1] > 70 else "Oversold" if data['RSI'].iloc[-1] < 30 else "Neutral"
                )
            with col3:
                st.metric(
                    "MACD",
                    f"{data['MACD'].iloc[-1]:.2f}",
                    f"{(data['MACD'].iloc[-1] - data['Signal_Line'].iloc[-1]):.2f}"
                )
            with col4:
                volatility = data['Close'].pct_change().std() * (252 ** 0.5)
                st.metric("Volatility", f"{volatility:.2%}")
            
            # Technical Analysis Charts
            st.subheader("Technical Analysis")
            
            # Price and Moving Averages
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(
                x=data.index,
                y=data['Close'],
                name="Price",
                line=dict(color="#00ADB5")
            ))
            fig1.add_trace(go.Scatter(
                x=data.index,
                y=data['SMA20'],
                name="SMA20",
                line=dict(color="#FF5722", dash='dash')
            ))
            fig1.add_trace(go.Scatter(
                x=data.index,
                y=data['SMA50'],
                name="SMA50",
                line=dict(color="#4CAF50", dash='dash')
            ))
            fig1.update_layout(
                template="plotly_dark",
                plot_bgcolor="#222831",
                paper_bgcolor="#222831",
                title="Price and Moving Averages"
            )
            st.plotly_chart(fig1, use_container_width=True)
            
            # RSI Chart
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=data.index,
                y=data['RSI'],
                name="RSI",
                line=dict(color="#00ADB5")
            ))
            fig2.add_hline(y=70, line_dash="dash", line_color="red")
            fig2.add_hline(y=30, line_dash="dash", line_color="green")
            fig2.update_layout(
                template="plotly_dark",
                plot_bgcolor="#222831",
                paper_bgcolor="#222831",
                title="Relative Strength Index (RSI)"
            )
            st.plotly_chart(fig2, use_container_width=True)
            
            # MACD Chart
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(
                x=data.index,
                y=data['MACD'],
                name="MACD",
                line=dict(color="#00ADB5")
            ))
            fig3.add_trace(go.Scatter(
                x=data.index,
                y=data['Signal_Line'],
                name="Signal Line",
                line=dict(color="#FF5722")
            ))
            fig3.update_layout(
                template="plotly_dark",
                plot_bgcolor="#222831",
                paper_bgcolor="#222831",
                title="MACD"
            )
            st.plotly_chart(fig3, use_container_width=True)
            
            # Additional metrics
            st.subheader("Additional Metrics")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("Volume Analysis")
                avg_volume = data['Volume'].mean()
                vol_change = (data['Volume'].iloc[-1] / avg_volume) - 1
                st.metric(
                    "Average Volume",
                    f"{avg_volume:,.0f}",
                    f"{vol_change:.2%}"
                )
                
            with col2:
                st.write("Trend Analysis")
                trend = "Uptrend" if data['SMA20'].iloc[-1] > data['SMA50'].iloc[-1] else "Downtrend"
                strength = abs(data['SMA20'].iloc[-1] - data['SMA50'].iloc[-1]) / data['Close'].iloc[-1]
                st.metric(
                    "Trend Direction",
                    trend,
                    f"Strength: {strength:.2%}"
                ) 