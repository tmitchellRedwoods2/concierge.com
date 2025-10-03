"""
Application constants and configuration
"""

# Page Configuration
PAGE_CONFIG = {
    "page_title": "Concierge.com",
    "page_icon": "🏆",
    "layout": "wide"
}

# Service Plans
SERVICE_PLANS = {
    'basic': {
        'name': 'Basic',
        'price': 29,
        'features': [
            '✅ Core service management',
            '✅ Mobile app access',
            '✅ Email support (24-48 hours)',
            '✅ Basic reporting',
            '✅ Up to 3 services',
            '❌ No AI assistance',
            '❌ No dedicated concierge',
            '❌ No priority support'
        ]
    },
    'premium': {
        'name': 'Premium',
        'price': 99,
        'features': [
            '✅ Everything in Basic, PLUS:',
            '✅ AI-powered recommendations',
            '✅ Priority support (4-8 hours)',
            '✅ Advanced analytics',
            '✅ Up to 6 services',
            '✅ Phone support',
            '✅ Quarterly strategy calls',
            '❌ No dedicated concierge'
        ]
    },
    'elite': {
        'name': 'Elite',
        'price': 299,
        'features': [
            '✅ Everything in Premium, PLUS:',
            '✅ Dedicated personal concierge',
            '✅ 24/7 priority support (1-2 hours)',
            '✅ Unlimited services',
            '✅ White-glove service',
            '✅ Monthly strategy sessions',
            '✅ Direct CPA & legal counsel',
            '✅ Exclusive partner discounts'
        ]
    }
}

# AI Agent Types
AI_AGENTS = {
    'expense_agent': {'name': '💰 Expense AI', 'status': 'active', 'tasks_completed': 0},
    'travel_agent': {'name': '✈️ Travel AI', 'status': 'active', 'tasks_completed': 0},
    'medical_agent': {'name': '🏥 Medical AI', 'status': 'active', 'tasks_completed': 0},
    'insurance_agent': {'name': '🛡️ Insurance AI', 'status': 'active', 'tasks_completed': 0},
    'tax_agent': {'name': '📊 Tax AI', 'status': 'active', 'tasks_completed': 0},
    'communication_agent': {'name': '💬 Communication AI', 'status': 'active', 'tasks_completed': 0}
}

# AI Insights
AI_INSIGHTS = {
    'expense_patterns': ['High spending on dining', 'Subscription optimization needed', 'Budget alerts'],
    'travel_preferences': ['Business class preferred', 'Hotel loyalty programs', 'Early morning flights'],
    'health_reminders': ['Annual checkup due', 'Prescription refills needed', 'Insurance claims pending'],
    'communication_style': ['Prefers email', 'Quick responses', 'Detailed follow-ups']
}

# Service Pricing
SERVICE_PRICING = {
    'Health Management': 20,
    'Investment Management': 50,
    'Expense Tracking': 15,
    'Insurance Management': 25,
    'Legal Services': 75,
    'Tax Management': 40,
    'Travel Planning': 30,
    'Personal Assistant': 100
}

# Net Worth Multipliers
NET_WORTH_MULTIPLIERS = {
    10000000: 2.5,  # $10M+
    5000000: 2.0,   # $5M+
    2000000: 1.7,   # $2M+
    1000000: 1.4,   # $1M+
    500000: 1.2     # $500K+
}

# Admin Roles and Permissions
ADMIN_ROLES = {
    'super_admin': ['user_management', 'system_monitoring', 'analytics', 'settings', 'logs'],
    'manager': ['user_management', 'analytics', 'logs'],
    'support': ['user_management', 'logs'],
    'analyst': ['analytics', 'logs']
}

# Default Admin Users
DEFAULT_ADMIN_USERS = {
    'admin': {'password': 'SecureAdmin2024!', 'role': 'super_admin', 'name': 'System Administrator'},
    'manager': {'password': 'Manager2024!', 'role': 'manager', 'name': 'Operations Manager'},
    'support': {'password': 'Support2024!', 'role': 'support', 'name': 'Support Staff'},
    'analyst': {'password': 'Analyst2024!', 'role': 'analyst', 'name': 'Data Analyst'}
}

# System Metrics
DEFAULT_SYSTEM_METRICS = {
    'total_users': 0,
    'active_sessions': 0,
    'messages_sent': 0,
    'prescriptions_managed': 0,
    'ai_tasks_completed': 0
}

# File Paths
DATA_FILES = {
    'client_intakes': 'client_intakes.json',
    'chat_history': 'chat_history.json',
    'prescriptions': 'prescriptions.json',
    'admin_data': 'admin_data.json',
    'expenses': 'expenses.json',
    'investments': 'investments.json'
}
