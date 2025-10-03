"""
Session state management utilities
"""
import streamlit as st
from datetime import datetime


def initialize_session_state():
    """Initialize all session state variables"""
    if 'user_logged_in' not in st.session_state:
        st.session_state.user_logged_in = False
    if 'user_plan' not in st.session_state:
        st.session_state.user_plan = 'basic'
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    if 'show_messaging' not in st.session_state:
        st.session_state.show_messaging = False
    if 'show_message_history' not in st.session_state:
        st.session_state.show_message_history = False
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False
    if 'admin_role' not in st.session_state:
        st.session_state.admin_role = None
    if 'intake_step' not in st.session_state:
        st.session_state.intake_step = 1
    if 'intake_data' not in st.session_state:
        st.session_state.intake_data = {}


def get_user_plan():
    """Get current user plan"""
    return st.session_state.get('user_plan', 'basic')


def get_user_data():
    """Get current user data"""
    return st.session_state.get('user_data', {})


def is_admin_logged_in():
    """Check if admin is logged in"""
    return st.session_state.get('admin_logged_in', False)


def get_admin_role():
    """Get current admin role"""
    return st.session_state.get('admin_role', None)


def reset_session_state():
    """Reset all session state variables"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    initialize_session_state()
