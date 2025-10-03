"""
Authentication UI Components
"""
import streamlit as st
from datetime import datetime
from src.managers.admin import AdminSystem
from src.config.constants import DEFAULT_ADMIN_USERS


def login_user(username, plan='basic'):
    """Login user and set session state"""
    st.session_state.user_logged_in = True
    st.session_state.user_plan = plan
    st.session_state.user_data = {
        'username': username,
        'plan': plan,
        'login_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


def logout_user():
    """Logout user and clear session state"""
    st.session_state.user_logged_in = False
    st.session_state.user_plan = 'basic'
    st.session_state.user_data = {}
    st.session_state.show_messaging = False
    st.session_state.show_message_history = False


def login_admin(username, password):
    """Login admin user"""
    admin_system = AdminSystem()
    auth_result = admin_system.authenticate_admin(username, password)
    
    if auth_result['authenticated']:
        st.session_state.admin_logged_in = True
        st.session_state.admin_role = auth_result['role']
        st.session_state.admin_name = auth_result['name']
        return True
    return False


def logout_admin():
    """Logout admin user"""
    st.session_state.admin_logged_in = False
    st.session_state.admin_role = None
    st.session_state.admin_name = None


def render_login_page():
    """Render the login/signup page"""
    st.title("🏆 Concierge.com")
    st.subheader("Your Personal Life Management Platform")
    st.markdown("**Making your life easier, one service at a time**")
    
    # Create tabs for Login and Sign Up
    tab1, tab2 = st.tabs(["🔐 Sign In", "📝 Sign Up"])
    
    with tab1:
        st.subheader("Welcome Back!")
        st.write("Sign in to access your dashboard")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("🔐 Sign In", use_container_width=True, type="primary"):
                if username and password:
                    login_user(username, 'premium')  # Demo: auto-login as premium
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Please enter both username and password")
        
        with col2:
            st.markdown("**Demo Credentials:**")
            st.code("Username: demo\nPassword: demo123")
            st.markdown("*Use any credentials for demo*")
    
    with tab2:
        st.subheader("Join Concierge.com")
        st.write("Create your account and get personalized recommendations")
        
        # Import signup form from signup module
        from src.ui.signup import render_signup_form
        render_signup_form()


def render_admin_login():
    """Render admin login form"""
    st.title("🔧 Admin Login")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Administrator Access")
        admin_username = st.text_input("Admin Username", key="admin_username")
        admin_password = st.text_input("Admin Password", type="password", key="admin_password")
        
        if st.button("🔐 Login Admin", use_container_width=True, type="primary"):
            if admin_username and admin_password:
                if login_admin(admin_username, admin_password):
                    st.success("Admin login successful!")
                    st.rerun()
                else:
                    st.error("Invalid admin credentials")
            else:
                st.error("Please enter both username and password")
    
    with col2:
        st.markdown("**Demo Admin Credentials:**")
        st.code("Username: admin\nPassword: SecureAdmin2024!")
        st.markdown("**Available Roles:**")
        for username, user_data in DEFAULT_ADMIN_USERS.items():
            st.write(f"• {user_data['role'].title()}: {username} / {user_data['password']}")
