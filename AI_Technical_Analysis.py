import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from prophet import Prophet

# Set up Streamlit app
st.set_page_config(layout="wide")
st.title("AI-Powered Technical Stock Analysis Dashboard")
st.sidebar.header("Configuration")

# Input for stock ticker and date range
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL):", "AAPL")

# --- Add ticker suggestions ---
ticker_suggestions = ["TSLA", "SMCI", "CSO", "IBM", "INTC", "AMD", "META", "MSTR", "NVDA", "MSFT",
                      "NET", "GOOG", "BIDI", "BABA", "SHOP", "AMZN", "BTDR", "RIOT", "MARA", "EXOD",
                      "BTC", "GSOL", "ARKK", "FDIG", "ETHE", "GBTC", "COIN"]
st.sidebar.markdown("**Suggestions:** " + ", ".join(ticker_suggestions))

start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2024-12-14"))

# Fetch stock data
if st.sidebar.button("Fetch Data"):
    st.session_state["stock_data"] = yf.download(ticker, start=start_date, end=end_date)
    st.success("Stock data loaded successfully!")

# Check if data is available
if "stock_data" in st.session_state:
    data = st.session_state["stock_data"]

    # Plot candlestick chart
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name="Candlestick"
    )])

    # Sidebar: Select technical indicators
    st.sidebar.subheader("Technical Indicators")
    indicators = st.sidebar.multiselect(
        "Select Indicators:",
        ["20-Day SMA", "50-Day SMA", "20-Day EMA", "50-Day EMA", "20-Day Bollinger Bands", "VWAP", "RSI", "MACD"],
        default=["20-Day SMA"]
    )

    # Helper function to add indicators to the chart
    def add_indicator(indicator):
        if indicator == "20-Day SMA":
            sma = data['Close'].rolling(window=20).mean()
            fig.add_trace(go.Scatter(x=data.index, y=sma, mode='lines', name='SMA (20)'))
        elif indicator == "50-Day SMA":
            sma = data['Close'].rolling(window=50).mean()
            fig.add_trace(go.Scatter(x=data.index, y=sma, mode='lines', name='SMA (50)'))
        elif indicator == "20-Day EMA":
            ema = data['Close'].ewm(span=20).mean()
            fig.add_trace(go.Scatter(x=data.index, y=ema, mode='lines', name='EMA (20)'))
        elif indicator == "50-Day EMA":
            ema = data['Close'].ewm(span=50).mean()
            fig.add_trace(go.Scatter(x=data.index, y=ema, mode='lines', name='EMA (50)'))
        elif indicator == "20-Day Bollinger Bands":
            sma = data['Close'].rolling(window=20).mean()
            std = data['Close'].rolling(window=20).std()
            bb_upper = sma + 2 * std
            bb_lower = sma - 2 * std
            fig.add_trace(go.Scatter(x=data.index, y=bb_upper, mode='lines', name='BB Upper'))
            fig.add_trace(go.Scatter(x=data.index, y=bb_lower, mode='lines', name='BB Lower'))
        elif indicator == "VWAP":
            data['VWAP'] = (data['Close'] * data['Volume']).cumsum() / data['Volume'].cumsum()
            fig.add_trace(go.Scatter(x=data.index, y=data['VWAP'], mode='lines', name='VWAP'))
        elif indicator == "RSI":
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            fig.add_trace(go.Scatter(x=data.index, y=rsi, mode='lines', name='RSI'))
        elif indicator == "MACD":
            ema_12 = data['Close'].ewm(span=12).mean()
            ema_26 = data['Close'].ewm(span=26).mean()
            macd = ema_12 - ema_26
            signal = macd.ewm(span=9).mean()
            fig.add_trace(go.Scatter(x=data.index, y=macd, mode='lines', name='MACD'))
            fig.add_trace(go.Scatter(x=data.index, y=signal, mode='lines', name='Signal'))

    # Add selected indicators to the chart
    for indicator in indicators:
        add_indicator(indicator)

    fig.update_layout(xaxis_rangeslider_visible=False)
    st.plotly_chart(fig)

    # Analyze chart with Prophet
    st.subheader("AI-Powered Analysis")
    if st.button("Run AI Analysis"):
        with st.spinner("Analyzing the chart, please wait..."):
            # Prepare data for Prophet
            df = pd.DataFrame({'ds': data.index, 'y': data['Close']})

            # Create and fit Prophet model
            model = Prophet()
            model.fit(df)

            # Make future predictions (e.g., for the next 30 days)
            future = model.make_future_dataframe(periods=30)
            forecast = model.predict(future)

            # Display the forecast
            st.write("**Forecast:**")
            st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30))

            # Plot the forecast
            fig_forecast = model.plot(forecast)
            st.plotly_chart(fig_forecast)

            # --- Automated Descriptive Analysis ---
            st.write("**Analysis:**")

            # 1. Trend Analysis
            trend_slope = (forecast['yhat'].iloc[-1] - forecast['yhat'].iloc[0]) / len(forecast)
            if trend_slope > 0.1:
                st.write("The AI predicts a strong upward trend in the stock price.")
            elif trend_slope < -0.1:
                st.write("The AI predicts a strong downward trend in the stock price.")
            else:
                st.write("The AI predicts a relatively stable trend in the stock price.")

            # 2. Seasonality Analysis (Example with Weekly Seasonality)
            if 'weekly' in forecast.columns and forecast['weekly'].mean() > 0.2:
                st.write("There is a significant positive weekly seasonality.")

            # 3. Volatility Analysis (using yhat_lower and yhat_upper)
            uncertainty = forecast['yhat_upper'].mean() - forecast['yhat_lower'].mean()
            if uncertainty > 0.5:
                st.write("The forecast has a high degree of uncertainty.")
            elif uncertainty < 0.2:
                st.write("The forecast has a low degree of uncertainty.")
            else:
                st.write("The forecast has a moderate degree of uncertainty.")