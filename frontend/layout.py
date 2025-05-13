import streamlit as st

def setup_page():
    """Configure the main page layout and styling"""
    st.set_page_config(layout="wide")
    st.title("AI-Powered Technical Stock Analysis Dashboard")
    
    # Custom CSS for styling
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] > div:first-child {
            visibility: hidden;
        }
        [data-testid="stSidebar"] > div:first-child + div {
            padding-top: 0.5rem;
        }
        [data-testid="stSidebar"] > div:first-child + div > button {
            display: flex;
            align-items: center;
            font-size: 1.2rem;
        }
        [data-testid="stSidebar"] > div:first-child + div > button:before {
            content: 'Tickers';
            margin-right: 0.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def setup_sidebar():
    """Configure the sidebar layout"""
    st.sidebar.title("Controls")
    
def show_success(message: str):
    """Display a success message"""
    st.success(message)
    
def show_error(message: str):
    """Display an error message"""
    st.error(message)
    
def show_loading(message: str):
    """Display a loading spinner with message"""
    return st.spinner(message) 