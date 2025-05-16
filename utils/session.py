import streamlit as st

def init_session_state():
    """Initialize session state variables"""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if 'test_results' not in st.session_state:
        st.session_state.test_results = None
    if 'current_lesson' not in st.session_state:
        st.session_state.current_lesson = None
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0
    if 'current_quiz_step' not in st.session_state:
        st.session_state.current_quiz_step = 0
    if 'completed_lessons' not in st.session_state:
        st.session_state.completed_lessons = set()

def clear_session():
    """Clear all session state variables"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]