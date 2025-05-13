import streamlit as st
from typing import Any, Callable
from functools import wraps
import pandas as pd
from datetime import datetime, timedelta

class CacheManager:
    """Manages caching for data and computations"""
    
    @staticmethod
    def cache_data(ttl_seconds: int = 3600):
        """Decorator for caching data with time-to-live"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Create a cache key based on function name and arguments
                cache_key = f"cache_{func.__name__}_{str(args)}_{str(kwargs)}"
                
                # Check if data exists in cache and is still valid
                if cache_key in st.session_state:
                    cached_data = st.session_state[cache_key]
                    cached_time = cached_data.get('timestamp')
                    if cached_time and (datetime.now() - cached_time).seconds < ttl_seconds:
                        return cached_data.get('data')
                
                # If not in cache or expired, compute and cache the result
                result = func(*args, **kwargs)
                st.session_state[cache_key] = {
                    'data': result,
                    'timestamp': datetime.now()
                }
                return result
            return wrapper
        return decorator
    
    @staticmethod
    def clear_cache(pattern: str = None) -> None:
        """Clear cached data, optionally filtered by pattern"""
        keys_to_delete = []
        for key in st.session_state.keys():
            if key.startswith('cache_'):
                if pattern is None or pattern in key:
                    keys_to_delete.append(key)
        
        for key in keys_to_delete:
            del st.session_state[key]
    
    @staticmethod
    def get_cache_info() -> dict:
        """Get information about cached items"""
        cache_info = {}
        for key in st.session_state.keys():
            if key.startswith('cache_'):
                cache_data = st.session_state[key]
                if isinstance(cache_data, dict) and 'timestamp' in cache_data:
                    cache_info[key] = {
                        'timestamp': cache_data['timestamp'],
                        'age_seconds': (datetime.now() - cache_data['timestamp']).seconds
                    }
        return cache_info 