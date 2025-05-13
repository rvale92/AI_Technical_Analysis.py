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
    page_title="Trading Strategies - AI Technical Analysis",
    page_icon="🤖",
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

st.title("Trading Strategies")
st.subheader("Automated Strategy Analysis")

# Strategy selection
col1, col2 = st.columns(2)
with col1:
    symbol = st.text_input("Enter Symbol", "AAPL", key="strategy_symbol_input", autocomplete="off")
    strategy = st.selectbox(
        "Select Strategy",
        ["Moving Average Crossover", "RSI Strategy", "MACD Strategy"],
        key="strategy_select"
    )
with col2:
    timeframe = st.selectbox(
        "Select Timeframe",
        ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        key="strategy_timeframe_select"
    )
    
if st.button("Run Backtest", key="run_backtest_btn"):
    with st.spinner("Running strategy backtest..."):
        # Get historical data
        data = st.session_state.data_loader.get_market_data(symbol, timeframe)
        if data is not None:
            # Add technical indicators
            data = st.session_state.data_loader.get_technical_indicators(data)
            
            # Create strategy signals
            if strategy == "Moving Average Crossover":
                data['Signal'] = (data['SMA20'] > data['SMA50']).astype(int)
            elif strategy == "RSI Strategy":
                data['Signal'] = ((data['RSI'] < 30) | (data['RSI'] > 70)).astype(int)
            else:  # MACD Strategy
                data['Signal'] = (data['MACD'] > data['Signal_Line']).astype(int)
            
            # Calculate returns
            data['Strategy_Returns'] = data['Signal'].shift(1) * data['Close'].pct_change()
            
            # Plot strategy performance
            fig = go.Figure()
            
            # Price chart
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['Close'],
                name="Price",
                line=dict(color="#00ADB5")
            ))
            
            # Buy signals
            buy_points = data[data['Signal'] == 1]
            fig.add_trace(go.Scatter(
                x=buy_points.index,
                y=buy_points['Close'],
                mode='markers',
                name="Buy Signal",
                marker=dict(color="green", size=8)
            ))
            
            # Sell signals
            sell_points = data[data['Signal'] == 0]
            fig.add_trace(go.Scatter(
                x=sell_points.index,
                y=sell_points['Close'],
                mode='markers',
                name="Sell Signal",
                marker=dict(color="red", size=8)
            ))
            
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor="#222831",
                paper_bgcolor="#222831",
                title=f"{symbol} Strategy Performance",
                xaxis_title="Date",
                yaxis_title="Price ($)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Strategy metrics
            total_return = data['Strategy_Returns'].sum()
            sharpe_ratio = data['Strategy_Returns'].mean() / data['Strategy_Returns'].std() * (252 ** 0.5)
            max_drawdown = (data['Close'] / data['Close'].cummax() - 1).min()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Return", f"{total_return:.2%}")
            with col2:
                st.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")
            with col3:
                st.metric("Max Drawdown", f"{max_drawdown:.2%}")
            
            # Strategy description
            st.subheader("Strategy Details")
            if strategy == "Moving Average Crossover":
                st.write("""
                This strategy uses two moving averages (20-day and 50-day) to generate trading signals:
                - Buy when the shorter MA crosses above the longer MA
                - Sell when the shorter MA crosses below the longer MA
                """)
            elif strategy == "RSI Strategy":
                st.write("""
                This strategy uses the Relative Strength Index (RSI) to identify overbought and oversold conditions:
                - Buy when RSI falls below 30 (oversold)
                - Sell when RSI rises above 70 (overbought)
                """)
            else:
                st.write("""
                This strategy uses the MACD indicator to identify trend changes:
                - Buy when MACD crosses above the signal line
                - Sell when MACD crosses below the signal line
                """) 