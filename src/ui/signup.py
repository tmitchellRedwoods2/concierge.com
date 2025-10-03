"""
Signup UI Components
"""
import streamlit as st
from src.managers.client_intake import ClientIntakeManager
from src.config.constants import SERVICE_PLANS


def render_signup_form():
    """Render the signup form with client intake"""
    # Initialize session state for signup data
    if 'signup_data' not in st.session_state:
        st.session_state.signup_data = {}
    
    # Step indicator
    if 'signup_step' not in st.session_state:
        st.session_state.signup_step = 1
    
    # Progress bar
    progress = (st.session_state.signup_step - 1) / 4
    st.progress(progress)
    st.write(f"**Step {st.session_state.signup_step} of 5**")
    st.markdown("---")
    
    # Initialize intake manager
    intake_manager = ClientIntakeManager()
    
    # Step 1: Account Information
    if st.session_state.signup_step == 1:
        render_account_info_step(intake_manager)
    
    # Step 2: Financial Profile
    elif st.session_state.signup_step == 2:
        render_financial_profile_step(intake_manager)
    
    # Step 3: Goals and Objectives
    elif st.session_state.signup_step == 3:
        render_goals_step(intake_manager)
    
    # Step 4: Service Selection
    elif st.session_state.signup_step == 4:
        render_service_selection_step(intake_manager)
    
    # Step 5: Plan Recommendation and Account Creation
    elif st.session_state.signup_step == 5:
        render_plan_recommendation_step(intake_manager)


def render_account_info_step(intake_manager):
    """Render account information step"""
    st.markdown("**Step 1: Account Information**")
    
    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("Choose Username", value=st.session_state.signup_data.get('username', ''), key="signup_username_step1")
        email = st.text_input("Email Address", value=st.session_state.signup_data.get('email', ''), key="signup_email_step1")
        password = st.text_input("Create Password", type="password", value=st.session_state.signup_data.get('password', ''), key="signup_password_step1")
    
    with col2:
        first_name = st.text_input("First Name", value=st.session_state.signup_data.get('first_name', ''), key="signup_firstname_step1")
        last_name = st.text_input("Last Name", value=st.session_state.signup_data.get('last_name', ''), key="signup_lastname_step1")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_step1")
    
    if st.button("Next →", use_container_width=True, type="primary"):
        if all([username, email, password, first_name, last_name]):
            if password == confirm_password:
                st.session_state.signup_data.update({
                    'username': username,
                    'email': email,
                    'password': password,
                    'first_name': first_name,
                    'last_name': last_name
                })
                st.session_state.signup_step = 2
                st.rerun()
            else:
                st.error("Passwords do not match")
        else:
            st.error("Please fill in all required fields")


def render_financial_profile_step(intake_manager):
    """Render financial profile step"""
    st.markdown("**Step 2: Financial Profile**")
    
    col1, col2 = st.columns(2)
    with col1:
        net_worth = st.number_input(
            "Estimated Net Worth ($)", 
            min_value=0, 
            step=10000, 
            value=st.session_state.signup_data.get('net_worth', 100000),
            key="signup_net_worth_step2"
        )
        annual_income = st.number_input(
            "Annual Income ($)", 
            min_value=0, 
            step=10000, 
            value=st.session_state.signup_data.get('annual_income', 50000),
            key="signup_annual_income_step2"
        )
    
    with col2:
        employment_status = st.selectbox(
            "Employment Status",
            ["Employed", "Self-Employed", "Retired", "Student", "Unemployed", "Other"],
            index=["Employed", "Self-Employed", "Retired", "Student", "Unemployed", "Other"].index(
                st.session_state.signup_data.get('employment_status', 'Employed')
            ),
            key="signup_employment_step2"
        )
        family_size = st.number_input(
            "Family Size", 
            min_value=1, 
            max_value=20, 
            value=st.session_state.signup_data.get('family_size', 1),
            key="signup_family_size_step2"
        )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Previous", use_container_width=True):
            st.session_state.signup_step = 1
            st.rerun()
    
    with col2:
        if st.button("Next →", use_container_width=True, type="primary"):
            st.session_state.signup_data.update({
                'net_worth': net_worth,
                'annual_income': annual_income,
                'employment_status': employment_status,
                'family_size': family_size
            })
            st.session_state.signup_step = 3
            st.rerun()


def render_goals_step(intake_manager):
    """Render goals and objectives step"""
    st.markdown("**Step 3: Goals and Objectives**")
    
    goals = st.multiselect(
        "Select your primary goals (choose all that apply):",
        [
            "Health and Wellness Management",
            "Wealth Management and Investment",
            "Tax Optimization",
            "Legal Planning and Protection",
            "Insurance Management",
            "Expense Tracking and Budgeting",
            "Business Management",
            "Estate Planning",
            "Retirement Planning",
            "Family Planning",
            "Travel and Lifestyle",
            "Personal Development"
        ],
        default=st.session_state.signup_data.get('goals', []),
        key="signup_goals_step3"
    )
    
    st.text_area(
        "Additional goals or specific needs:",
        value=st.session_state.signup_data.get('additional_goals', ''),
        height=100,
        key="signup_additional_goals_step3"
    )
    
    priority_level = st.select_slider(
        "How important is having a dedicated concierge service?",
        options=["Low", "Medium", "High", "Critical"],
        value=st.session_state.signup_data.get('priority_level', 'Medium'),
        key="signup_priority_step3"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Previous", use_container_width=True):
            st.session_state.signup_step = 2
            st.rerun()
    
    with col2:
        if st.button("Next →", use_container_width=True, type="primary"):
            if goals:
                st.session_state.signup_data.update({
                    'goals': goals,
                    'additional_goals': st.session_state.signup_additional_goals,
                    'priority_level': priority_level
                })
                st.session_state.signup_step = 4
                st.rerun()
            else:
                st.error("Please select at least one goal")


def render_service_selection_step(intake_manager):
    """Render service selection step"""
    st.markdown("**Step 4: Service Selection**")
    
    available_services = [
        "Health Management",
        "Investment Management", 
        "Expense Tracking",
        "Insurance Management",
        "Legal Services",
        "Tax Management",
        "Travel Planning",
        "Personal Assistant"
    ]
    
    selected_services = st.multiselect(
        "Select services (choose all that apply):",
        available_services,
        default=st.session_state.signup_data.get('selected_services', []),
        key="signup_services_step4"
    )
    
    # Show service descriptions
    if selected_services:
        st.markdown("**Selected Services:**")
        service_descriptions = {
            "Health Management": "Medical appointment scheduling, prescription management, health tracking",
            "Investment Management": "Portfolio monitoring, investment advice, broker coordination",
            "Expense Tracking": "Budget analysis, expense categorization, financial reporting",
            "Insurance Management": "Policy review, claims assistance, coverage optimization",
            "Legal Services": "Document review, legal consultation, case management",
            "Tax Management": "Tax preparation, filing assistance, optimization strategies",
            "Travel Planning": "Trip coordination, booking management, itinerary planning",
            "Personal Assistant": "Daily task management, scheduling, personal errands"
        }
        
        for service in selected_services:
            st.write(f"• **{service}**: {service_descriptions.get(service, '')}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Previous", use_container_width=True):
            st.session_state.signup_step = 3
            st.rerun()
    
    with col2:
        if st.button("Next →", use_container_width=True, type="primary"):
            if selected_services:
                st.session_state.signup_data.update({
                    'selected_services': selected_services
                })
                st.session_state.signup_step = 5
                st.rerun()
            else:
                st.error("Please select at least one service")


def render_plan_recommendation_step(intake_manager):
    """Render plan recommendation and account creation step"""
    st.markdown("**Step 5: Your Personalized Plan & Account Creation**")
    
    # Get signup data
    signup_data = st.session_state.signup_data
    net_worth = signup_data.get('net_worth', 0)
    goals = signup_data.get('goals', [])
    selected_services = signup_data.get('selected_services', [])
    
    # Recommend plan
    recommended_plan, complexity_score = intake_manager.recommend_plan(
        net_worth, goals, selected_services
    )
    
    # Calculate pricing
    pricing = intake_manager.calculate_pricing(
        net_worth, selected_services, recommended_plan
    )
    
    # Display recommendation
    st.success(f"🎉 **Recommended Plan: {recommended_plan.title()}**")
    st.write(f"*Based on your complexity score: {complexity_score}/10*")
    
    # Show plan features
    features = intake_manager.get_plan_features(recommended_plan)
    st.markdown("**Plan Features:**")
    for feature in features:
        st.write(feature)
    
    # Show pricing
    st.markdown("**💰 Pricing:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Monthly Price", f"${pricing['monthly_price']}")
    with col2:
        st.metric("Annual Price", f"${pricing['annual_price']}")
    with col3:
        st.metric("Annual Savings", f"${pricing['annual_savings']}")
    
    # Account summary
    st.markdown("**📋 Account Summary:**")
    st.write(f"**Name:** {signup_data.get('first_name', '')} {signup_data.get('last_name', '')}")
    st.write(f"**Email:** {signup_data.get('email', '')}")
    st.write(f"**Username:** {signup_data.get('username', '')}")
    st.write(f"**Net Worth:** ${net_worth:,}")
    st.write(f"**Goals:** {', '.join(goals)}")
    st.write(f"**Services:** {', '.join(selected_services)}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Previous", use_container_width=True):
            st.session_state.signup_step = 4
            st.rerun()
    
    with col2:
        if st.button("✅ Create Account & Complete Setup", use_container_width=True, type="primary"):
            # Save client intake data
            client = intake_manager.add_client(signup_data)
            
            # Create user account (demo implementation)
            st.success("🎉 **Account created successfully!**")
            st.balloons()
            
            st.markdown("**Welcome to Concierge.com!**")
            st.write("1. Your account has been created")
            st.write("2. Our team will review your intake within 24 hours")
            st.write("3. You'll receive a personalized welcome package")
            st.write("4. Your dedicated concierge will contact you to begin services")
            
            # Reset signup state
            st.session_state.signup_step = 1
            st.session_state.signup_data = {}
            
            st.markdown("---")
            if st.button("🔐 Sign In to Your Account", use_container_width=True):
                st.session_state.signup_step = 1
                st.session_state.signup_data = {}
                st.rerun()
