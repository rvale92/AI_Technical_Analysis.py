import streamlit as st
from typing import Any, Optional

class SessionState:
    """Handles Streamlit session state management"""
    
    @staticmethod
    def init_state(key: str, default_value: Any) -> None:
        """Initialize a session state variable if it doesn't exist"""
        if key not in st.session_state:
            st.session_state[key] = default_value
    
    @staticmethod
    def get_state(key: str, default_value: Any = None) -> Any:
        """Get a value from session state with optional default"""
        return st.session_state.get(key, default_value)
    
    @staticmethod
    def set_state(key: str, value: Any) -> None:
        """Set a value in session state"""
        st.session_state[key] = value
    
    @staticmethod
    def delete_state(key: str) -> None:
        """Delete a value from session state"""
        if key in st.session_state:
            del st.session_state[key]
    
    @staticmethod
    def clear_all() -> None:
        """Clear all session state variables"""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
            
    @staticmethod
    def get_all() -> dict:
        """Get all session state variables"""
        return dict(st.session_state) 