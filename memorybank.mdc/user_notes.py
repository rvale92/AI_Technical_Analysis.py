import streamlit as st
from typing import List, Dict, Optional
from datetime import datetime

class UserNotes:
    """Manages user notes and annotations"""
    
    NOTES_KEY = "user_notes"
    
    @classmethod
    def init_notes(cls) -> None:
        """Initialize notes in session state if they don't exist"""
        if cls.NOTES_KEY not in st.session_state:
            st.session_state[cls.NOTES_KEY] = {}
    
    @classmethod
    def add_note(cls, ticker: str, note: str, category: str = "general") -> None:
        """Add a note for a specific ticker"""
        cls.init_notes()
        if ticker not in st.session_state[cls.NOTES_KEY]:
            st.session_state[cls.NOTES_KEY][ticker] = []
            
        note_entry = {
            'text': note,
            'category': category,
            'timestamp': datetime.now(),
            'id': len(st.session_state[cls.NOTES_KEY][ticker])
        }
        
        st.session_state[cls.NOTES_KEY][ticker].append(note_entry)
    
    @classmethod
    def get_notes(cls, ticker: str = None, category: str = None) -> Dict[str, List[Dict]]:
        """Get notes, optionally filtered by ticker and/or category"""
        cls.init_notes()
        if ticker:
            notes = {ticker: st.session_state[cls.NOTES_KEY].get(ticker, [])}
        else:
            notes = st.session_state[cls.NOTES_KEY]
            
        if category:
            filtered_notes = {}
            for tick, tick_notes in notes.items():
                filtered_notes[tick] = [
                    note for note in tick_notes
                    if note['category'] == category
                ]
            return filtered_notes
            
        return notes
    
    @classmethod
    def delete_note(cls, ticker: str, note_id: int) -> bool:
        """Delete a specific note"""
        cls.init_notes()
        if ticker in st.session_state[cls.NOTES_KEY]:
            notes = st.session_state[cls.NOTES_KEY][ticker]
            for i, note in enumerate(notes):
                if note['id'] == note_id:
                    notes.pop(i)
                    return True
        return False
    
    @classmethod
    def clear_notes(cls, ticker: str = None) -> None:
        """Clear all notes for a ticker or all notes if ticker is None"""
        cls.init_notes()
        if ticker:
            if ticker in st.session_state[cls.NOTES_KEY]:
                st.session_state[cls.NOTES_KEY][ticker] = []
        else:
            st.session_state[cls.NOTES_KEY] = {} 