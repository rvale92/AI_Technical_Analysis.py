import streamlit as st
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum, auto

class ProgressStatus(Enum):
    """Enum for progress status"""
    NOT_STARTED = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    ERROR = auto()

class Progress:
    """Tracks progress of analysis tasks"""
    
    PROGRESS_KEY = "analysis_progress"
    
    @classmethod
    def init_progress(cls) -> None:
        """Initialize progress tracking"""
        if cls.PROGRESS_KEY not in st.session_state:
            st.session_state[cls.PROGRESS_KEY] = {
                'steps': {},
                'current_step': None,
                'start_time': None,
                'last_update': None
            }
    
    @classmethod
    def start_analysis(cls) -> None:
        """Start a new analysis session"""
        cls.init_progress()
        st.session_state[cls.PROGRESS_KEY] = {
            'steps': {},
            'current_step': None,
            'start_time': datetime.now(),
            'last_update': datetime.now()
        }
    
    @classmethod
    def add_step(cls, step_id: str, description: str) -> None:
        """Add a new step to track"""
        cls.init_progress()
        st.session_state[cls.PROGRESS_KEY]['steps'][step_id] = {
            'description': description,
            'status': ProgressStatus.NOT_STARTED,
            'start_time': None,
            'end_time': None,
            'error': None
        }
    
    @classmethod
    def start_step(cls, step_id: str) -> None:
        """Mark a step as started"""
        cls.init_progress()
        if step_id in st.session_state[cls.PROGRESS_KEY]['steps']:
            st.session_state[cls.PROGRESS_KEY]['steps'][step_id].update({
                'status': ProgressStatus.IN_PROGRESS,
                'start_time': datetime.now(),
                'end_time': None,
                'error': None
            })
            st.session_state[cls.PROGRESS_KEY]['current_step'] = step_id
            st.session_state[cls.PROGRESS_KEY]['last_update'] = datetime.now()
    
    @classmethod
    def complete_step(cls, step_id: str) -> None:
        """Mark a step as completed"""
        cls.init_progress()
        if step_id in st.session_state[cls.PROGRESS_KEY]['steps']:
            st.session_state[cls.PROGRESS_KEY]['steps'][step_id].update({
                'status': ProgressStatus.COMPLETED,
                'end_time': datetime.now()
            })
            if st.session_state[cls.PROGRESS_KEY]['current_step'] == step_id:
                st.session_state[cls.PROGRESS_KEY]['current_step'] = None
            st.session_state[cls.PROGRESS_KEY]['last_update'] = datetime.now()
    
    @classmethod
    def fail_step(cls, step_id: str, error: str) -> None:
        """Mark a step as failed"""
        cls.init_progress()
        if step_id in st.session_state[cls.PROGRESS_KEY]['steps']:
            st.session_state[cls.PROGRESS_KEY]['steps'][step_id].update({
                'status': ProgressStatus.ERROR,
                'end_time': datetime.now(),
                'error': error
            })
            if st.session_state[cls.PROGRESS_KEY]['current_step'] == step_id:
                st.session_state[cls.PROGRESS_KEY]['current_step'] = None
            st.session_state[cls.PROGRESS_KEY]['last_update'] = datetime.now()
    
    @classmethod
    def get_progress(cls) -> Dict:
        """Get current progress status"""
        cls.init_progress()
        return st.session_state[cls.PROGRESS_KEY]
    
    @classmethod
    def get_step_status(cls, step_id: str) -> Optional[Dict]:
        """Get status of a specific step"""
        cls.init_progress()
        return st.session_state[cls.PROGRESS_KEY]['steps'].get(step_id) 