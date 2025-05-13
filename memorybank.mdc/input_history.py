import streamlit as st
from typing import List, Dict, Any
from datetime import datetime

class InputHistory:
    """Manages user input history"""
    
    HISTORY_KEY = "input_history"
    MAX_HISTORY = 50  # Maximum number of history items to keep
    
    @classmethod
    def init_history(cls) -> None:
        """Initialize history in session state if it doesn't exist"""
        if cls.HISTORY_KEY not in st.session_state:
            st.session_state[cls.HISTORY_KEY] = []
    
    @classmethod
    def add_input(cls, input_type: str, value: Any) -> None:
        """Add a new input to history"""
        cls.init_history()
        history_item = {
            'type': input_type,
            'value': value,
            'timestamp': datetime.now()
        }
        
        # Add new item and maintain max size
        history = st.session_state[cls.HISTORY_KEY]
        history.insert(0, history_item)
        if len(history) > cls.MAX_HISTORY:
            history = history[:cls.MAX_HISTORY]
        st.session_state[cls.HISTORY_KEY] = history
    
    @classmethod
    def get_history(cls, input_type: str = None) -> List[Dict]:
        """Get input history, optionally filtered by type"""
        cls.init_history()
        history = st.session_state[cls.HISTORY_KEY]
        if input_type:
            return [item for item in history if item['type'] == input_type]
        return history
    
    @classmethod
    def clear_history(cls, input_type: str = None) -> None:
        """Clear history, optionally only for specific input type"""
        cls.init_history()
        if input_type:
            st.session_state[cls.HISTORY_KEY] = [
                item for item in st.session_state[cls.HISTORY_KEY]
                if item['type'] != input_type
            ]
        else:
            st.session_state[cls.HISTORY_KEY] = []
    
    @classmethod
    def get_recent_inputs(cls, input_type: str, limit: int = 5) -> List[Any]:
        """Get most recent unique inputs of a specific type"""
        history = cls.get_history(input_type)
        unique_values = []
        seen = set()
        
        for item in history:
            value = item['value']
            if value not in seen and len(unique_values) < limit:
                unique_values.append(value)
                seen.add(value)
        
        return unique_values 