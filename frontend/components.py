import streamlit as st
import plotly.graph_objects as go
from typing import List, Dict
import pandas as pd

def render_candlestick_chart(data: pd.DataFrame, indicators: Dict[str, pd.Series] = None) -> go.Figure:
    """Render candlestick chart with optional indicators"""
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name="Candlestick"
    )])
    
    if indicators:
        for name, series in indicators.items():
            if isinstance(series, tuple):
                # For indicators that return multiple lines (e.g., Bollinger Bands)
                for i, line in enumerate(series):
                    fig.add_trace(go.Scatter(
                        x=data.index,
                        y=line,
                        mode='lines',
                        name=f'{name} {i+1}'
                    ))
            else:
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=series,
                    mode='lines',
                    name=name
                ))
    
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig

def display_forecast_analysis(analysis: Dict) -> None:
    """Display the forecast analysis results"""
    st.write("**Analysis:**")
    
    # Trend Analysis
    st.write(f"The AI predicts a {analysis['trend']['description']} trend in the stock price.")
    
    # Seasonality Analysis
    if analysis['seasonality']['weekly']:
        st.write("There is a significant positive weekly seasonality.")
    
    # Volatility Analysis
    st.write(f"The forecast has a {analysis['uncertainty']['level']} degree of uncertainty.") 