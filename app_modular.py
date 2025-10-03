"""
Concierge.com - Modular Streamlit Application
Main application file using modular architecture
"""
import streamlit as st
import os
import sys

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config.constants import PAGE_CONFIG
from src.utils.session import initialize_session_state
from src.ui.auth import render_login_page, render_admin_login
from src.managers.ai_agent import AIAgentSystem
from src.managers.messaging import MessagingSystem
from src.managers.admin import AdminSystem
from src.managers.client_intake import ClientIntakeManager
from src.managers.prescription import PrescriptionManager
from src.managers.investment import InvestmentManager
from src.managers.expense import ExpenseManager

# Set page configuration
st.set_page_config(**PAGE_CONFIG)

# Initialize session state
initialize_session_state()

# Initialize managers
ai_system = AIAgentSystem()
messaging_system = MessagingSystem()
admin_system = AdminSystem()
intake_manager = ClientIntakeManager()
prescription_manager = PrescriptionManager()
investment_manager = InvestmentManager()
expense_manager = ExpenseManager()

# Main App Logic
if not st.session_state.user_logged_in and not st.session_state.admin_logged_in:
    # Login/Signup Page
    render_login_page()
    
elif st.session_state.admin_logged_in:
    # Admin Dashboard
    render_admin_dashboard()
    
else:
    # User Dashboard
    render_user_dashboard()


def render_admin_dashboard():
    """Render admin dashboard"""
    from src.ui.auth import logout_admin
    
    admin_name = st.session_state.get('admin_name', 'Admin')
    st.title(f"🛠️ Admin Dashboard - {admin_name}")
    
    # Admin role and permissions
    permissions = admin_system.get_admin_permissions(st.session_state.admin_role)
    st.sidebar.write(f"**Role:** {st.session_state.admin_role.title()}")
    st.sidebar.write(f"**Permissions:** {', '.join(permissions)}")
    
    if st.sidebar.button("🚪 Logout Admin"):
        logout_admin()
        st.rerun()
    
    # Admin tabs based on permissions
    admin_tabs = []
    if 'user_management' in permissions:
        admin_tabs.append("👥 User Management")
    if 'system_monitoring' in permissions:
        admin_tabs.append("📊 System Monitoring")
    if 'analytics' in permissions:
        admin_tabs.append("📈 Analytics")
    if 'settings' in permissions:
        admin_tabs.append("⚙️ Settings")
    if 'logs' in permissions:
        admin_tabs.append("📋 System Logs")
    
    if admin_tabs:
        st.write(f"**Available Tabs:** {admin_tabs}")
        
        # Display system metrics
        st.subheader("📊 System Overview")
        metrics = admin_system.get_user_analytics()
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Users", metrics['total_users'])
        with col2:
            st.metric("Active Sessions", metrics['active_sessions'])
        with col3:
            st.metric("Messages Sent", metrics['messages_sent'])
        with col4:
            st.metric("Prescriptions", metrics['prescriptions_managed'])
        with col5:
            st.metric("AI Tasks", metrics['ai_tasks_completed'])


def render_user_dashboard():
    """Render user dashboard"""
    from src.ui.auth import logout_user
    
    username = st.session_state.user_data.get('username', 'User')
    st.title(f"🚀 Welcome back, {username}!")
    
    # Sidebar
    st.sidebar.title("🏆 Concierge.com")
    st.sidebar.write(f"**Plan:** {st.session_state.user_plan.title()}")
    
    if st.sidebar.button("🚪 Logout"):
        logout_user()
        st.rerun()
    
    # Main dashboard content
    st.subheader("📊 Dashboard Overview")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("AI Tasks Completed", ai_system.agents['expense_agent']['tasks_completed'])
    
    with col2:
        unread_count = messaging_system.get_unread_count()
        st.metric("Unread Messages", unread_count)
    
    with col3:
        active_prescriptions = len(prescription_manager.get_prescriptions())
        st.metric("Active Prescriptions", active_prescriptions)
    
    with col4:
        portfolio_summary = investment_manager.get_portfolio_summary()
        st.metric("Portfolio Value", f"${portfolio_summary['total_value']:,.0f}")
    
    # Service tabs
    st.subheader("🔧 Services")
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "💰 Expenses", "📈 Investments", "🏥 Health", 
        "💬 Messages", "🤖 AI Agents", "⚙️ Settings"
    ])
    
    with tab1:
        render_expense_tab()
    
    with tab2:
        render_investment_tab()
    
    with tab3:
        render_health_tab()
    
    with tab4:
        render_messaging_tab()
    
    with tab5:
        render_ai_agents_tab()
    
    with tab6:
        render_settings_tab()


def render_expense_tab():
    """Render expense management tab"""
    st.subheader("💰 Expense Management")
    
    # Expense summary
    summary = expense_manager.get_expense_summary()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Expenses", f"${summary['total_expenses']:,.2f}")
    with col2:
        st.metric("Remaining Budget", f"${summary['remaining_budget']:,.2f}")
    with col3:
        st.metric("Monthly Trend", f"{summary['monthly_trend']['change_percent']:.1f}%")
    
    # Add expense form
    with st.expander("➕ Add New Expense"):
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Category", ["food", "transportation", "entertainment", "utilities", "other"])
            amount = st.number_input("Amount", min_value=0.0, step=0.01)
        with col2:
            description = st.text_input("Description")
            date = st.date_input("Date")
        
        if st.button("Add Expense"):
            expense_manager.add_expense(category, amount, description, str(date))
            st.success("Expense added successfully!")
            st.rerun()


def render_investment_tab():
    """Render investment management tab"""
    st.subheader("📈 Investment Management")
    
    # Portfolio summary
    summary = investment_manager.get_portfolio_summary()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Portfolio Value", f"${summary['total_value']:,.2f}")
    with col2:
        st.metric("Total Investments", summary['total_investments'])
    with col3:
        st.metric("Daily Change", f"${summary['daily_change']:,.2f}")
    
    # Available brokers
    st.subheader("🏦 Available Brokers")
    brokers = investment_manager.get_available_brokers()
    
    for broker_key in brokers:
        broker_info = investment_manager.get_broker_info(broker_key)
        with st.expander(f"📊 {broker_info['name']}"):
            st.write(f"**Website:** {broker_info['website']}")
            st.write(f"**Features:** {', '.join(broker_info['features'])}")
            st.write(f"**Commission:** {broker_info['commission']}")


def render_health_tab():
    """Render health management tab"""
    st.subheader("🏥 Health Management")
    
    # Prescription summary
    prescriptions = prescription_manager.get_prescriptions()
    reminders = prescription_manager.get_refill_reminders()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Active Prescriptions", len(prescriptions))
    with col2:
        st.metric("Refill Reminders", len(reminders))
    
    # Refill reminders
    if reminders:
        st.subheader("⚠️ Refill Reminders")
        for reminder in reminders:
            prescription = reminder['prescription']
            days = reminder['days_until']
            urgent = reminder['urgent']
            
            if urgent:
                st.error(f"🚨 **{prescription['name']}** - Due in {days} days")
            else:
                st.warning(f"⚠️ **{prescription['name']}** - Due in {days} days")
    
    # Add prescription form
    with st.expander("💊 Add New Prescription"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Medication Name")
            dosage = st.text_input("Dosage")
            frequency = st.text_input("Frequency")
        with col2:
            quantity = st.number_input("Quantity", min_value=1)
            refill_date = st.date_input("Next Refill Date")
            pharmacy = st.selectbox("Pharmacy", list(prescription_manager.pharmacies.keys()))
        
        doctor = st.text_input("Prescribing Doctor")
        
        if st.button("Add Prescription"):
            prescription_manager.add_prescription(
                name, dosage, frequency, quantity, str(refill_date), pharmacy, doctor
            )
            st.success("Prescription added successfully!")
            st.rerun()


def render_messaging_tab():
    """Render messaging tab"""
    st.subheader("💬 Messaging System")
    
    # Message channels
    channels = ["concierge", "ai_agent", "support"]
    selected_channel = st.selectbox("Select Channel", channels)
    
    # Display messages
    messages = messaging_system.get_messages(selected_channel)
    
    if messages:
        st.subheader(f"📨 Messages - {selected_channel.title()}")
        for message in messages[-10:]:  # Show last 10 messages
            timestamp = message['timestamp']
            if hasattr(timestamp, 'strftime'):
                timestamp = timestamp.strftime('%Y-%m-%d %H:%M')
            
            st.write(f"**{message['sender']}** ({timestamp}): {message['message']}")
    
    # Send message
    st.subheader("✍️ Send Message")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        message_text = st.text_input("Message", key=f"message_{selected_channel}")
    
    with col2:
        if st.button("Send", key=f"send_{selected_channel}"):
            if message_text:
                messaging_system.add_message("user", selected_channel, message_text, "user", selected_channel)
                st.success("Message sent!")
                st.rerun()


def render_ai_agents_tab():
    """Render AI agents tab"""
    st.subheader("🤖 AI Agents")
    
    # Agent status
    agents = ai_system.get_agent_status()
    
    for agent_id, agent_data in agents.items():
        with st.expander(f"{agent_data['name']} - {agent_data['status'].title()}"):
            st.write(f"**Tasks Completed:** {agent_data['tasks_completed']}")
            
            # Simulate task
            if st.button(f"Simulate Task - {agent_id}"):
                result = ai_system.simulate_ai_task(agent_id, "Sample task")
                st.success(result)
                st.rerun()
    
    # AI insights
    st.subheader("🧠 AI Insights")
    categories = ["expense_patterns", "travel_preferences", "health_reminders", "communication_style"]
    
    for category in categories:
        insights = ai_system.get_ai_insights(category)
        if insights:
            st.write(f"**{category.replace('_', ' ').title()}:**")
            for insight in insights:
                st.write(f"• {insight}")


def render_settings_tab():
    """Render settings tab"""
    st.subheader("⚙️ Settings")
    
    # User plan info
    st.write(f"**Current Plan:** {st.session_state.user_plan.title()}")
    
    # Plan features
    from src.config.constants import SERVICE_PLANS
    plan_features = SERVICE_PLANS.get(st.session_state.user_plan, {}).get('features', [])
    
    st.write("**Plan Features:**")
    for feature in plan_features:
        st.write(feature)
    
    # Upgrade options
    if st.session_state.user_plan != 'elite':
        st.subheader("🚀 Upgrade Options")
        
        if st.session_state.user_plan == 'basic':
            if st.button("Upgrade to Premium"):
                st.session_state.user_plan = 'premium'
                st.success("Upgraded to Premium!")
                st.rerun()
        
        if st.session_state.user_plan == 'premium':
            if st.button("Upgrade to Elite"):
                st.session_state.user_plan = 'elite'
                st.success("Upgraded to Elite!")
                st.rerun()


if __name__ == "__main__":
    # This allows the app to be run directly
    pass
