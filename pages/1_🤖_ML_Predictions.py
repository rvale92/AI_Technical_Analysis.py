import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))
from backend.ml_predictor import MLPredictor
from backend.data_loader import DataLoader

# Page configuration
st.set_page_config(
    page_title="ML Predictions - AI Technical Analysis",
    page_icon="📈",
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
if 'ml_predictor' not in st.session_state:
    st.session_state.ml_predictor = MLPredictor()
if 'data_loader' not in st.session_state:
    st.session_state.data_loader = DataLoader()

st.title("ML Predictions")
st.subheader("AI-Powered Market Analysis")

# Asset selection
col1, col2 = st.columns(2)
with col1:
    symbol = st.text_input("Enter Symbol", "AAPL", key="ml_symbol_input", autocomplete="off")
with col2:
    prediction_days = st.slider("Prediction Days", 1, 30, 7, key="prediction_days_slider")

if st.button("Generate Prediction", key="generate_pred_btn"):
    with st.spinner("Analyzing market data..."):
        # Get historical data
        data = st.session_state.data_loader.get_market_data(symbol, "1y")
        if data is not None:
            # Generate prediction
            prediction = st.session_state.ml_predictor.predict(data, prediction_days)
            
            # Display prediction chart
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['Close'],
                name="Historical",
                line=dict(color="#00ADB5")
            ))
            
            # Prediction
            fig.add_trace(go.Scatter(
                x=prediction.index,
                y=prediction['Predicted'],
                name="Prediction",
                line=dict(color="#FF5722", dash='dash')
            ))
            
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor="#222831",
                paper_bgcolor="#222831",
                title=f"{symbol} Price Prediction",
                xaxis_title="Date",
                yaxis_title="Price ($)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "Current Price",
                    f"${data['Close'].iloc[-1]:.2f}"
                )
            with col2:
                st.metric(
                    "Predicted Price (End of Period)",
                    f"${prediction['Predicted'].iloc[-1]:.2f}",
                    f"{((prediction['Predicted'].iloc[-1] / data['Close'].iloc[-1]) - 1):.2%}"
                )
            
            # Model insights
            st.subheader("Model Insights")
            st.write("""
            The prediction is based on various factors including:
            - Historical price patterns
            - Volume analysis
            - Technical indicators
            - Market sentiment
            """)
            
            # Confidence metrics
            st.subheader("Prediction Confidence")
            confidence = st.session_state.ml_predictor.get_confidence_metrics(data)
            st.json(confidence) 