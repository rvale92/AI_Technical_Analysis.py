import streamlit as st
import pandas as pd
from datetime import datetime

# Import backend modules
from backend.data_loader import fetch_stock_data
from backend.indicators import (
    calculate_sma, calculate_ema, calculate_bollinger_bands,
    calculate_vwap, calculate_rsi, calculate_macd
)
from backend.ai_model import prepare_data_for_prophet, train_prophet_model, make_predictions
from backend.utils import validate_dates, validate_ticker, SUGGESTED_TICKERS

# Import frontend modules
from frontend.components import render_candlestick_chart, display_forecast_analysis
from frontend.layout import setup_page, setup_sidebar, show_success, show_error, show_loading

# Import memory management modules
from memorybank.mdc.session_state import SessionState
from memorybank.mdc.cache_manager import CacheManager
from memorybank.mdc.input_history import InputHistory
from memorybank.mdc.user_notes import UserNotes
from memorybank.mdc.progress import Progress, ProgressStatus
from memorybank.mdc.tasks import TaskManager, TaskStatus

def initialize_app():
    """Initialize app state and components"""
    Progress.start_analysis()
    Progress.add_step("data_fetch", "Fetching stock data")
    Progress.add_step("indicators", "Calculating technical indicators")
    Progress.add_step("ai_analysis", "Running AI analysis")
    
    # Initialize session state variables
    SessionState.init_state("current_ticker", None)
    SessionState.init_state("analysis_complete", False)

@CacheManager.cache_data(ttl_seconds=3600)
def fetch_cached_stock_data(ticker: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """Fetch stock data with caching"""
    return fetch_stock_data(ticker, start_date, end_date)

def main():
    # Setup page layout
    setup_page()
    setup_sidebar()
    initialize_app()
    
    # Sidebar inputs
    ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL):", "AAPL")
    
    # Show recent tickers from history
    recent_tickers = InputHistory.get_recent_inputs("ticker", limit=5)
    if recent_tickers:
        st.sidebar.write("Recent tickers:", ", ".join(recent_tickers))
    
    st.sidebar.markdown("**Suggestions:** " + ", ".join(SUGGESTED_TICKERS))
    
    start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
    end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2024-12-14"))
    
    # Notes section in sidebar
    if st.sidebar.checkbox("Show Notes"):
        note_text = st.sidebar.text_area("Add a note:")
        if st.sidebar.button("Save Note"):
            UserNotes.add_note(ticker, note_text)
            show_success("Note saved!")
        
        # Display existing notes
        notes = UserNotes.get_notes(ticker)
        if notes.get(ticker):
            st.sidebar.write("**Notes for", ticker + ":**")
            for note in notes[ticker]:
                st.sidebar.text(f"{note['timestamp'].strftime('%Y-%m-%d %H:%M')}: {note['text']}")
    
    # Validate inputs
    ticker = validate_ticker(ticker)
    if not validate_dates(start_date, end_date):
        show_error("Invalid date range")
        return
    
    # Fetch data button
    if st.sidebar.button("Fetch Data"):
        try:
            Progress.start_step("data_fetch")
            
            # Create and start data fetch task
            task_id = TaskManager.create_task(
                "fetch_data",
                f"Fetching data for {ticker}"
            )
            TaskManager.start_task(task_id)
            
            # Fetch data with caching
            data = fetch_cached_stock_data(ticker, start_date, end_date)
            
            # Store in session state
            SessionState.set_state("stock_data", data)
            SessionState.set_state("current_ticker", ticker)
            
            # Record input history
            InputHistory.add_input("ticker", ticker)
            
            # Update task and progress
            TaskManager.complete_task(task_id, {"rows": len(data)})
            Progress.complete_step("data_fetch")
            
            show_success("Stock data loaded successfully!")
        except Exception as e:
            Progress.fail_step("data_fetch", str(e))
            show_error(f"Error fetching data: {str(e)}")
            return
    
    # Process data if available
    if SessionState.get_state("stock_data") is not None:
        data = SessionState.get_state("stock_data")
        
        # Technical indicators selection
        st.sidebar.subheader("Technical Indicators")
        indicators = st.sidebar.multiselect(
            "Select Indicators:",
            ["20-Day SMA", "50-Day SMA", "20-Day EMA", "50-Day EMA", 
             "20-Day Bollinger Bands", "VWAP", "RSI", "MACD"],
            default=["20-Day SMA"]
        )
        
        Progress.start_step("indicators")
        # Calculate selected indicators
        indicator_data = {}
        try:
            for indicator in indicators:
                if "SMA" in indicator:
                    window = int(indicator.split("-")[0])
                    indicator_data[f"SMA ({window})"] = calculate_sma(data, window)
                elif "EMA" in indicator:
                    span = int(indicator.split("-")[0])
                    indicator_data[f"EMA ({span})"] = calculate_ema(data, span)
                elif "Bollinger" in indicator:
                    indicator_data["Bollinger Bands"] = calculate_bollinger_bands(data)
                elif indicator == "VWAP":
                    indicator_data["VWAP"] = calculate_vwap(data)
                elif indicator == "RSI":
                    indicator_data["RSI"] = calculate_rsi(data)
                elif indicator == "MACD":
                    indicator_data["MACD"] = calculate_macd(data)
            Progress.complete_step("indicators")
        except Exception as e:
            Progress.fail_step("indicators", str(e))
            show_error(f"Error calculating indicators: {str(e)}")
        
        # Render chart
        fig = render_candlestick_chart(data, indicator_data)
        st.plotly_chart(fig)
        
        # AI Analysis section
        st.subheader("AI-Powered Analysis")
        if st.button("Run AI Analysis"):
            Progress.start_step("ai_analysis")
            task_id = TaskManager.create_task(
                "ai_analysis",
                f"Running AI analysis for {ticker}"
            )
            TaskManager.start_task(task_id)
            
            with show_loading("Analyzing the chart, please wait..."):
                try:
                    # Prepare and analyze data
                    prophet_data = prepare_data_for_prophet(data)
                    model = train_prophet_model(prophet_data)
                    forecast, analysis = make_predictions(model)
                    
                    # Display results
                    st.write("**Forecast:**")
                    st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30))
                    
                    # Plot forecast
                    fig_forecast = model.plot(forecast)
                    st.plotly_chart(fig_forecast)
                    
                    # Display analysis
                    display_forecast_analysis(analysis)
                    
                    TaskManager.complete_task(task_id, analysis)
                    Progress.complete_step("ai_analysis")
                    SessionState.set_state("analysis_complete", True)
                except Exception as e:
                    TaskManager.fail_task(task_id, str(e))
                    Progress.fail_step("ai_analysis", str(e))
                    show_error(f"Error in AI analysis: {str(e)}")
        
        # Display progress
        progress = Progress.get_progress()
        with st.sidebar.expander("Analysis Progress"):
            for step_id, step in progress['steps'].items():
                status_color = {
                    ProgressStatus.NOT_STARTED: "⚪",
                    ProgressStatus.IN_PROGRESS: "🔵",
                    ProgressStatus.COMPLETED: "✅",
                    ProgressStatus.ERROR: "❌"
                }
                st.write(f"{status_color[step['status']]} {step['description']}")
                if step['error']:
                    st.write(f"Error: {step['error']}")

if __name__ == "__main__":
    main() 