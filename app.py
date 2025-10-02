import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import json
import os
import random
from datetime import datetime
import uuid

st.set_page_config(page_title="Concierge.com", page_icon="🏆", layout="wide")

# Initialize session state
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

# AI Agent System for Concierge Scaling
class AIAgentSystem:
    def __init__(self):
        self.agents = {
            'expense_agent': {'name': '💰 Expense AI', 'status': 'active', 'tasks_completed': 0},
            'travel_agent': {'name': '✈️ Travel AI', 'status': 'active', 'tasks_completed': 0},
            'medical_agent': {'name': '🏥 Medical AI', 'status': 'active', 'tasks_completed': 0},
            'insurance_agent': {'name': '🛡️ Insurance AI', 'status': 'active', 'tasks_completed': 0},
            'tax_agent': {'name': '📊 Tax AI', 'status': 'active', 'tasks_completed': 0},
            'communication_agent': {'name': '💬 Communication AI', 'status': 'active', 'tasks_completed': 0}
        }
        self.ai_insights = {
            'expense_patterns': ['High spending on dining', 'Subscription optimization needed', 'Budget alerts'],
            'travel_preferences': ['Business class preferred', 'Hotel loyalty programs', 'Early morning flights'],
            'health_reminders': ['Annual checkup due', 'Prescription refills needed', 'Insurance claims pending'],
            'communication_style': ['Prefers email', 'Quick responses', 'Detailed follow-ups']
        }
    
    def get_agent_status(self):
        return self.agents
    
    def simulate_ai_task(self, agent_type, task_description):
        """Simulate AI agent completing a task"""
        if agent_type in self.agents:
            self.agents[agent_type]['tasks_completed'] += 1
            return f"✅ AI Agent completed: {task_description}"
        return "❌ Agent not found"
    
    def get_ai_insights(self, category):
        """Get AI-generated insights for a category"""
        return self.ai_insights.get(category, [])
    
    def generate_ai_recommendations(self, user_plan, service_type):
        """Generate AI-powered recommendations based on user data"""
        recommendations = {
            'expense': [
                'AI detected 15% increase in dining expenses - consider meal planning',
                'Subscription audit: 3 unused services found, potential $45/month savings',
                'Budget optimization: Move 20% of dining budget to savings'
            ],
            'travel': [
                'AI found 25% cheaper flights for your preferred routes',
                'Hotel loyalty program: You\'re 2 stays away from Gold status',
                'Travel insurance recommendation: Comprehensive coverage for $12/month'
            ],
            'medical': [
                'AI scheduled your annual checkup for next Tuesday at 2 PM',
                'Prescription refill reminder: 3 medications due in 5 days',
                'Insurance claim status: $450 reimbursement approved',
                'AI optimized your prescription schedule for maximum effectiveness',
                'Prescription cost analysis: potential savings of $180/year identified',
                'Medication adherence tracking: 94% compliance rate achieved',
                'AI coordinated with pharmacy for automatic refill of blood pressure medication',
                'Health monitoring: 2 prescriptions approaching refill date'
            ],
            'insurance': [
                'AI comparison: Auto insurance could save $200/year with new provider',
                'Home insurance review: Coverage gap identified in natural disasters',
                'Life insurance recommendation: $500K term policy for $35/month'
            ],
            'tax': [
                'AI tax optimization: Charitable donations could reduce liability by $800',
                'Quarterly estimated tax: $2,400 payment due in 2 weeks',
                'Tax document collection: 3 forms still needed for filing'
            ]
        }
        return recommendations.get(service_type, ['AI analysis in progress...'])

# Prescription Management System
class PrescriptionManager:
    def __init__(self):
        self.prescriptions = []
        self.refill_reminders = []
        self.pharmacies = {
            'cvs': {'name': 'CVS Pharmacy', 'phone': '(555) 123-4567', 'address': '123 Main St', 'type': 'traditional'},
            'walgreens': {'name': 'Walgreens', 'phone': '(555) 234-5678', 'address': '456 Oak Ave', 'type': 'traditional'},
            'rite_aid': {'name': 'Rite Aid', 'phone': '(555) 345-6789', 'address': '789 Pine St', 'type': 'traditional'},
            'local': {'name': 'Local Pharmacy', 'phone': '(555) 456-7890', 'address': '321 Elm St', 'type': 'traditional'},
            'fullscript': {'name': 'Fullscript', 'phone': '(555) 567-8901', 'address': 'Online Platform', 'type': 'supplement', 'website': 'https://fullscript.com', 'app_available': True}
        }
        self.load_prescriptions()
    
    def load_prescriptions(self):
        """Load prescriptions from storage"""
        try:
            if os.path.exists("prescriptions.json"):
                with open("prescriptions.json", 'r') as f:
                    data = json.load(f)
                    self.prescriptions = data.get('prescriptions', [])
                    self.refill_reminders = data.get('refill_reminders', [])
        except Exception as e:
            print(f"Error loading prescriptions: {e}")
    
    def save_prescriptions(self):
        """Save prescriptions to storage"""
        try:
            data = {
                'prescriptions': self.prescriptions,
                'refill_reminders': self.refill_reminders
            }
            with open("prescriptions.json", 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving prescriptions: {e}")
    
    def add_prescription(self, name, dosage, frequency, quantity, refill_date, pharmacy, doctor):
        """Add a new prescription"""
        prescription = {
            'id': str(uuid.uuid4()),
            'name': name,
            'dosage': dosage,
            'frequency': frequency,
            'quantity': quantity,
            'refill_date': refill_date,
            'pharmacy': pharmacy,
            'doctor': doctor,
            'status': 'active',
            'refills_remaining': 3,
            'last_refill': None,
            'next_refill_due': refill_date
        }
        self.prescriptions.append(prescription)
        self.save_prescriptions()
        return prescription['id']
    
    def get_prescriptions(self):
        """Get all active prescriptions"""
        return [p for p in self.prescriptions if p['status'] == 'active']
    
    def get_refill_reminders(self):
        """Get prescriptions due for refill"""
        today = datetime.now().date()
        reminders = []
        for prescription in self.prescriptions:
            if prescription['status'] == 'active':
                refill_date = datetime.strptime(prescription['next_refill_due'], '%Y-%m-%d').date()
                days_until = (refill_date - today).days
                if days_until <= 7:  # Due within 7 days
                    reminders.append({
                        'prescription': prescription,
                        'days_until': days_until,
                        'urgent': days_until <= 2
                    })
        return reminders
    
    def request_refill(self, prescription_id, pharmacy_preference=None):
        """Request a prescription refill"""
        prescription = next((p for p in self.prescriptions if p['id'] == prescription_id), None)
        if prescription:
            # Update prescription
            prescription['last_refill'] = datetime.now().strftime('%Y-%m-%d')
            prescription['refills_remaining'] -= 1
            prescription['next_refill_due'] = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
            
            # Create refill request
            refill_request = {
                'id': str(uuid.uuid4()),
                'prescription_id': prescription_id,
                'request_date': datetime.now().strftime('%Y-%m-%d'),
                'pharmacy': pharmacy_preference or prescription['pharmacy'],
                'status': 'pending',
                'estimated_ready': (datetime.now() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M')
            }
            self.refill_reminders.append(refill_request)
            self.save_prescriptions()
            return refill_request
        return None
    
    def get_pharmacy_info(self, pharmacy_key):
        """Get pharmacy contact information"""
        return self.pharmacies.get(pharmacy_key, {})
    
    def is_fullscript_prescription(self, prescription):
        """Check if prescription is from Fullscript"""
        return prescription.get('pharmacy', '').lower() == 'fullscript'
    
    def get_fullscript_prescriptions(self):
        """Get all Fullscript prescriptions"""
        return [p for p in self.prescriptions if self.is_fullscript_prescription(p)]
    
    def get_supplement_categories(self):
        """Get supplement categories for Fullscript"""
        return {
            'vitamins': ['Vitamin D3', 'Vitamin B12', 'Vitamin C', 'Multivitamin'],
            'minerals': ['Magnesium', 'Zinc', 'Iron', 'Calcium'],
            'omega': ['Omega-3', 'Fish Oil', 'DHA', 'EPA'],
            'probiotics': ['Probiotic Blend', 'Lactobacillus', 'Bifidobacterium'],
            'herbs': ['Turmeric', 'Ginger', 'Ashwagandha', 'Rhodiola'],
            'protein': ['Whey Protein', 'Plant Protein', 'Collagen', 'BCAA'],
            'specialty': ['CBD', 'Melatonin', 'CoQ10', 'NAC']
        }
    
    def get_fullscript_analytics(self):
        """Get Fullscript-specific analytics"""
        fullscript_prescriptions = self.get_fullscript_prescriptions()
        if not fullscript_prescriptions:
            return {}
        
        categories = {}
        total_cost = 0
        adherence_rate = 0
        
        for prescription in fullscript_prescriptions:
            # Categorize supplements
            name = prescription['name'].lower()
            for category, supplements in self.get_supplement_categories().items():
                if any(supp.lower() in name for supp in supplements):
                    categories[category] = categories.get(category, 0) + 1
                    break
            
            # Simulate cost and adherence data
            total_cost += np.random.randint(25, 150)
            adherence_rate += np.random.randint(80, 100)
        
        if fullscript_prescriptions:
            adherence_rate = adherence_rate / len(fullscript_prescriptions)
        
        return {
            'total_supplements': len(fullscript_prescriptions),
            'categories': categories,
            'total_cost': total_cost,
            'adherence_rate': round(adherence_rate, 1),
            'most_popular_category': max(categories.items(), key=lambda x: x[1])[0] if categories else None
        }
    
    def request_fullscript_refill(self, prescription_id, delivery_preference='standard'):
        """Request Fullscript refill with delivery options"""
        prescription = next((p for p in self.prescriptions if p['id'] == prescription_id), None)
        if prescription and self.is_fullscript_prescription(prescription):
            # Fullscript-specific refill request
            refill_request = {
                'id': str(uuid.uuid4()),
                'prescription_id': prescription_id,
                'request_date': datetime.now().strftime('%Y-%m-%d'),
                'pharmacy': 'Fullscript',
                'status': 'pending',
                'delivery_preference': delivery_preference,
                'estimated_ready': (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M'),
                'tracking_available': True,
                'app_notification': True
            }
            self.refill_reminders.append(refill_request)
            self.save_prescriptions()
            return refill_request
        return None

# Admin Management System
class AdminSystem:
    def __init__(self):
        self.admin_users = {
            'admin': {'password': 'SecureAdmin2024!', 'role': 'super_admin', 'name': 'System Administrator'},
            'manager': {'password': 'Manager2024!', 'role': 'manager', 'name': 'Operations Manager'},
            'support': {'password': 'Support2024!', 'role': 'support', 'name': 'Support Staff'},
            'analyst': {'password': 'Analyst2024!', 'role': 'analyst', 'name': 'Data Analyst'}
        }
        self.user_sessions = []
        self.system_metrics = {
            'total_users': 0,
            'active_sessions': 0,
            'messages_sent': 0,
            'prescriptions_managed': 0,
            'ai_tasks_completed': 0
        }
        self.load_admin_data()
    
    def load_admin_data(self):
        """Load admin data from storage"""
        try:
            if os.path.exists("admin_data.json"):
                with open("admin_data.json", 'r') as f:
                    data = json.load(f)
                    self.user_sessions = data.get('user_sessions', [])
                    self.system_metrics = data.get('system_metrics', self.system_metrics)
        except Exception as e:
            print(f"Error loading admin data: {e}")
    
    def save_admin_data(self):
        """Save admin data to storage"""
        try:
            data = {
                'user_sessions': self.user_sessions,
                'system_metrics': self.system_metrics
            }
            with open("admin_data.json", 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving admin data: {e}")
    
    def authenticate_admin(self, username, password):
        """Authenticate admin user"""
        if username in self.admin_users:
            if self.admin_users[username]['password'] == password:
                return {
                    'authenticated': True,
                    'role': self.admin_users[username]['role'],
                    'name': self.admin_users[username]['name']
                }
        return {'authenticated': False}
    
    def get_admin_permissions(self, role):
        """Get permissions for admin role"""
        permissions = {
            'super_admin': ['user_management', 'system_monitoring', 'analytics', 'settings', 'logs'],
            'manager': ['user_management', 'analytics', 'logs'],
            'support': ['user_management', 'logs'],
            'analyst': ['analytics', 'logs']
        }
        return permissions.get(role, [])
    
    def get_system_metrics(self):
        """Get current system metrics"""
        return self.system_metrics
    
    def update_metrics(self, metric_type, value):
        """Update system metrics"""
        if metric_type in self.system_metrics:
            self.system_metrics[metric_type] += value
            self.save_admin_data()
    
    def get_user_analytics(self):
        """Get user analytics for admin dashboard"""
        return {
            'total_users': self.system_metrics['total_users'],
            'active_sessions': self.system_metrics['active_sessions'],
            'messages_sent': self.system_metrics['messages_sent'],
            'prescriptions_managed': self.system_metrics['prescriptions_managed'],
            'ai_tasks_completed': self.system_metrics['ai_tasks_completed']
        }
    
    def get_staff_members(self):
        """Get all staff members"""
        return self.admin_users
    
    def add_staff_member(self, username, password, role, name, email=None, phone=None, department=None):
        """Add a new staff member"""
        if username in self.admin_users:
            return False, "Username already exists"
        
        self.admin_users[username] = {
            'password': password,
            'role': role,
            'name': name,
            'email': email,
            'phone': phone,
            'department': department,
            'created_date': datetime.now().strftime('%Y-%m-%d'),
            'last_login': None,
            'status': 'active'
        }
        self.save_admin_data()
        return True, "Staff member added successfully"
    
    def update_staff_member(self, username, **updates):
        """Update staff member information"""
        if username not in self.admin_users:
            return False, "Staff member not found"
        
        for key, value in updates.items():
            if key in self.admin_users[username]:
                self.admin_users[username][key] = value
        
        self.save_admin_data()
        return True, "Staff member updated successfully"
    
    def deactivate_staff_member(self, username):
        """Deactivate a staff member"""
        if username not in self.admin_users:
            return False, "Staff member not found"
        
        self.admin_users[username]['status'] = 'inactive'
        self.save_admin_data()
        return True, "Staff member deactivated"
    
    def get_staff_analytics(self):
        """Get staff analytics"""
        total_staff = len(self.admin_users)
        active_staff = len([user for user in self.admin_users.values() if user.get('status') == 'active'])
        inactive_staff = total_staff - active_staff
        
        # Role distribution
        role_distribution = {}
        for user in self.admin_users.values():
            role = user.get('role', 'unknown')
            role_distribution[role] = role_distribution.get(role, 0) + 1
        
        return {
            'total_staff': total_staff,
            'active_staff': active_staff,
            'inactive_staff': inactive_staff,
            'role_distribution': role_distribution
        }
    
    def get_staff_activity_logs(self):
        """Get staff activity logs"""
        return [
            "2024-01-15 10:30:15 - Admin 'admin' accessed user management",
            "2024-01-15 10:25:42 - Manager 'manager' generated analytics report",
            "2024-01-15 10:20:18 - Support 'support' responded to user inquiry",
            "2024-01-15 10:15:33 - Analyst 'analyst' exported data report",
            "2024-01-15 10:10:21 - Admin 'admin' updated system settings",
            "2024-01-15 10:05:12 - Manager 'manager' managed user accounts"
        ]
    
    def get_staff_by_department(self, department=None):
        """Get staff members filtered by department"""
        if department:
            return {k: v for k, v in self.admin_users.items() if v.get('department') == department}
        return self.admin_users
    
    def get_departments(self):
        """Get list of all departments"""
        departments = set()
        for user in self.admin_users.values():
            if user.get('department'):
                departments.add(user['department'])
        return sorted(list(departments))
    
    def search_staff(self, search_term):
        """Search staff by name, username, or email"""
        results = {}
        search_term = search_term.lower()
        for username, user_info in self.admin_users.items():
            if (search_term in username.lower() or 
                search_term in user_info.get('name', '').lower() or
                search_term in user_info.get('email', '').lower()):
                results[username] = user_info
        return results
    
    def get_staff_performance_metrics(self):
        """Get staff performance metrics"""
        return {
            'total_staff': len(self.admin_users),
            'active_staff': len([u for u in self.admin_users.values() if u.get('status') == 'active']),
            'departments': len(self.get_departments()),
            'avg_login_frequency': 12.5,
            'response_time_avg': '2.3 min',
            'tasks_completed_today': 156
        }

# Initialize admin system
admin_system = AdminSystem()

# Initialize prescription manager
prescription_manager = PrescriptionManager()

# Investment Management System
class InvestmentManager:
    def __init__(self):
        self.investments = []
        self.accounts = []
        self.brokers = {
            'charles_schwab': {
                'name': 'Charles Schwab',
                'website': 'https://www.schwab.com',
                'api_available': True,
                'features': ['Trading', 'Research', 'Advisory', 'Banking'],
                'min_deposit': 0,
                'commission': 'Commission-free trades'
            },
            'morgan_stanley': {
                'name': 'Morgan Stanley',
                'website': 'https://www.morganstanley.com',
                'api_available': True,
                'features': ['Wealth Management', 'Investment Banking', 'Advisory'],
                'min_deposit': 5000,
                'commission': 'Full-service brokerage'
            },
            'edward_jones': {
                'name': 'Edward Jones',
                'website': 'https://www.edwardjones.com',
                'api_available': True,
                'features': ['Financial Planning', 'Advisory', 'Retirement Planning'],
                'min_deposit': 1000,
                'commission': 'Fee-based advisory'
            },
            'fidelity': {
                'name': 'Fidelity Investments',
                'website': 'https://www.fidelity.com',
                'api_available': True,
                'features': ['Trading', 'Research', 'Advisory', 'Retirement'],
                'min_deposit': 0,
                'commission': 'Commission-free trades'
            },
            'vanguard': {
                'name': 'Vanguard',
                'website': 'https://www.vanguard.com',
                'api_available': True,
                'features': ['Index Funds', 'ETFs', 'Advisory', 'Retirement'],
                'min_deposit': 1000,
                'commission': 'Low-cost investing'
            },
            'etrade': {
                'name': 'E*TRADE',
                'website': 'https://www.etrade.com',
                'api_available': True,
                'features': ['Online Trading', 'Research', 'Advisory'],
                'min_deposit': 0,
                'commission': 'Commission-free trades'
            }
        }
        self.load_investments()
    
    def load_investments(self):
        """Load investments from storage"""
        try:
            if os.path.exists('investments.json'):
                with open('investments.json', 'r') as f:
                    data = json.load(f)
                    self.investments = data.get('investments', [])
                    self.accounts = data.get('accounts', [])
        except Exception as e:
            st.error(f"Error loading investments: {e}")
    
    def save_investments(self):
        """Save investments to storage"""
        try:
            data = {
                'investments': self.investments,
                'accounts': self.accounts
            }
            with open('investments.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            st.error(f"Error saving investments: {e}")
    
    def add_investment_account(self, broker, account_name, account_type, balance=0):
        """Add a new investment account"""
        account = {
            'id': len(self.accounts) + 1,
            'broker': broker,
            'account_name': account_name,
            'account_type': account_type,
            'balance': balance,
            'created_date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'active'
        }
        self.accounts.append(account)
        self.save_investments()
        return account
    
    def add_investment(self, symbol, name, shares, price, account_id, investment_type='stock'):
        """Add a new investment"""
        investment = {
            'id': len(self.investments) + 1,
            'symbol': symbol,
            'name': name,
            'shares': shares,
            'price': price,
            'current_value': shares * price,
            'account_id': account_id,
            'investment_type': investment_type,
            'purchase_date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'active'
        }
        self.investments.append(investment)
        self.save_investments()
        return investment
    
    def get_portfolio_summary(self):
        """Get portfolio summary"""
        total_value = sum(inv['current_value'] for inv in self.investments if inv['status'] == 'active')
        total_investments = len([inv for inv in self.investments if inv['status'] == 'active'])
        total_accounts = len([acc for acc in self.accounts if acc['status'] == 'active'])
        
        return {
            'total_value': total_value,
            'total_investments': total_investments,
            'total_accounts': total_accounts,
            'daily_change': 1250.50,  # Mock data
            'percent_change': 2.5
        }
    
    def get_broker_info(self, broker_key):
        """Get broker information"""
        return self.brokers.get(broker_key, {})
    
    def get_available_brokers(self):
        """Get list of available brokers"""
        return list(self.brokers.keys())
    
    def get_investment_performance(self):
        """Get investment performance data"""
        return {
            'top_performers': [
                {'symbol': 'AAPL', 'name': 'Apple Inc.', 'return': 15.2, 'value': 25000},
                {'symbol': 'MSFT', 'name': 'Microsoft Corp.', 'return': 12.8, 'value': 18000},
                {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'return': 8.5, 'value': 12000}
            ],
            'sector_allocation': {
                'Technology': 45.2,
                'Healthcare': 20.1,
                'Financial': 15.8,
                'Consumer': 10.5,
                'Other': 8.4
            },
            'asset_allocation': {
                'Stocks': 70.0,
                'Bonds': 20.0,
                'Cash': 5.0,
                'Alternatives': 5.0
            }
        }

# Initialize investment manager
investment_manager = InvestmentManager()

# Expense Management System
class ExpenseManager:
    def __init__(self):
        self.expenses = []
        self.budgets = []
        self.expense_apps = {
            'ynab': {
                'name': 'YNAB (You Need A Budget)',
                'website': 'https://www.youneedabudget.com',
                'api_available': True,
                'features': ['Zero-based budgeting', 'Credit card handling', 'Goal tracking', 'Debt planning'],
                'cost': '$14.99/month or $109/year',
                'rating': 4.8,
                'description': 'Life-changing budgeting app with excellent credit card handling'
            },
            'everydollar': {
                'name': 'EveryDollar',
                'website': 'https://www.everydollar.com',
                'api_available': True,
                'features': ['Zero-based budget', 'Spending tracking', 'Saving goals', 'Bill reminders'],
                'cost': 'Free basic, $17.99/month premium',
                'rating': 4.2,
                'description': 'Dave Ramsey\'s zero-based budgeting approach'
            },
            'expensify': {
                'name': 'Expensify',
                'website': 'https://www.expensify.com',
                'api_available': True,
                'features': ['Receipt scanning', 'Automatic categorization', 'Business & personal', 'Mileage tracking'],
                'cost': 'Free to custom pricing',
                'rating': 4.3,
                'description': 'Combines personal and business expense tracking with receipt scanning'
            },
            'rocket_money': {
                'name': 'Rocket Money',
                'website': 'https://www.rocketmoney.com',
                'api_available': True,
                'features': ['Subscription tracking', 'Bill negotiation', 'Expense tracking', 'Credit monitoring'],
                'cost': 'Free, $6-12/month premium',
                'rating': 4.5,
                'description': 'Tracks expenses and finds/cancels unused subscriptions'
            },
            'monarch_money': {
                'name': 'Monarch Money',
                'website': 'https://www.monarchmoney.com',
                'api_available': True,
                'features': ['Account aggregation', 'Budget tracking', 'Net worth monitoring', 'Goal setting'],
                'cost': '$14.99/month',
                'rating': 4.6,
                'description': 'Comprehensive financial tracking and budgeting'
            },
            'money_manager': {
                'name': 'Money Manager & Expenses',
                'website': 'https://play.google.com/store/apps/details?id=com.realbyteinc.moneymanager',
                'api_available': True,
                'features': ['Daily expense tracking', 'Budget management', 'Multiple accounts', 'Real-time reports'],
                'cost': 'Free with ads, $3.99 premium',
                'rating': 4.7,
                'description': 'Clean display with personalization options'
            },
            'andromoney': {
                'name': 'AndroMoney',
                'website': 'https://play.google.com/store/apps/details?id=com.andromoney',
                'api_available': True,
                'features': ['Daily expenses', 'Budget alerts', 'Multiple accounts', 'Expense reports'],
                'cost': 'Free, $3.99 premium',
                'rating': 4.4,
                'description': 'Versatile app for tracking daily expenses and budgets'
            }
        }
        self.load_expenses()
    
    def load_expenses(self):
        """Load expenses from storage"""
        try:
            if os.path.exists('expenses.json'):
                with open('expenses.json', 'r') as f:
                    data = json.load(f)
                    self.expenses = data.get('expenses', [])
                    self.budgets = data.get('budgets', [])
        except Exception as e:
            st.error(f"Error loading expenses: {e}")
    
    def save_expenses(self):
        """Save expenses to storage"""
        try:
            data = {
                'expenses': self.expenses,
                'budgets': self.budgets
            }
            with open('expenses.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            st.error(f"Error saving expenses: {e}")
    
    def add_expense(self, category, amount, description, date, app_source=None):
        """Add a new expense"""
        expense = {
            'id': len(self.expenses) + 1,
            'category': category,
            'amount': amount,
            'description': description,
            'date': date,
            'app_source': app_source,
            'created_date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'active'
        }
        self.expenses.append(expense)
        self.save_expenses()
        return expense
    
    def get_expense_summary(self):
        """Get expense summary"""
        total_expenses = sum(exp['amount'] for exp in self.expenses if exp['status'] == 'active')
        total_budgets = sum(budget['amount'] for budget in self.budgets if budget['status'] == 'active')
        
        # Category breakdown
        categories = {}
        for exp in self.expenses:
            if exp['status'] == 'active':
                cat = exp['category']
                categories[cat] = categories.get(cat, 0) + exp['amount']
        
        return {
            'total_expenses': total_expenses,
            'total_budgets': total_budgets,
            'remaining_budget': total_budgets - total_expenses,
            'categories': categories,
            'monthly_trend': self.get_monthly_trend()
        }
    
    def get_monthly_trend(self):
        """Get monthly expense trend"""
        # Mock data for demonstration
        return {
            'current_month': 3200,
            'last_month': 2800,
            'change_percent': 14.3,
            'projected_monthly': 3500
        }
    
    def get_app_info(self, app_key):
        """Get expense app information"""
        return self.expense_apps.get(app_key, {})
    
    def get_available_apps(self):
        """Get list of available expense apps"""
        return list(self.expense_apps.keys())
    
    def sync_with_app(self, app_key, sync_type='import'):
        """Sync with external expense app"""
        app_info = self.get_app_info(app_key)
        if sync_type == 'import':
            # Mock import from app
            return f"Imported expenses from {app_info['name']}"
        elif sync_type == 'export':
            # Mock export to app
            return f"Exported expenses to {app_info['name']}"
        else:
            return f"Synced with {app_info['name']}"

# Initialize expense manager
expense_manager = ExpenseManager()

# Insurance Management System
class InsuranceManager:
    def __init__(self):
        self.policies = []
        self.claims = []
        self.insurance_companies = {
            'allstate': {
                'name': 'Allstate Insurance',
                'website': 'https://www.allstate.com',
                'api_available': True,
                'features': ['Auto Insurance', 'Home Insurance', 'Life Insurance', 'Business Insurance', 'Renters Insurance'],
                'rating': 4.3,
                'description': 'You\'re in good hands with Allstate',
                'contact': '1-800-ALLSTATE',
                'mobile_app': True,
                'online_portal': True
            },
            'state_farm': {
                'name': 'State Farm Insurance',
                'website': 'https://www.statefarm.com',
                'api_available': True,
                'features': ['Auto Insurance', 'Home Insurance', 'Life Insurance', 'Health Insurance', 'Business Insurance'],
                'rating': 4.4,
                'description': 'Like a good neighbor, State Farm is there',
                'contact': '1-800-STATE-FARM',
                'mobile_app': True,
                'online_portal': True
            },
            'farmers': {
                'name': 'Farmers Insurance',
                'website': 'https://www.farmers.com',
                'api_available': True,
                'features': ['Auto Insurance', 'Home Insurance', 'Life Insurance', 'Business Insurance', 'Motorcycle Insurance'],
                'rating': 4.2,
                'description': 'We know a thing or two because we\'ve seen a thing or two',
                'contact': '1-800-FARMERS',
                'mobile_app': True,
                'online_portal': True
            },
            'progressive': {
                'name': 'Progressive Insurance',
                'website': 'https://www.progressive.com',
                'api_available': True,
                'features': ['Auto Insurance', 'Home Insurance', 'Life Insurance', 'Business Insurance', 'Boat Insurance'],
                'rating': 4.5,
                'description': 'Progressive - The name says it all',
                'contact': '1-800-PROGRESSIVE',
                'mobile_app': True,
                'online_portal': True
            },
            'geico': {
                'name': 'GEICO Insurance',
                'website': 'https://www.geico.com',
                'api_available': True,
                'features': ['Auto Insurance', 'Home Insurance', 'Life Insurance', 'Business Insurance', 'Motorcycle Insurance'],
                'rating': 4.6,
                'description': '15 minutes could save you 15% or more on car insurance',
                'contact': '1-800-GEICO',
                'mobile_app': True,
                'online_portal': True
            },
            'liberty_mutual': {
                'name': 'Liberty Mutual Insurance',
                'website': 'https://www.libertymutual.com',
                'api_available': True,
                'features': ['Auto Insurance', 'Home Insurance', 'Life Insurance', 'Business Insurance', 'Renters Insurance'],
                'rating': 4.1,
                'description': 'Only pay for what you need',
                'contact': '1-800-LIBERTY',
                'mobile_app': True,
                'online_portal': True
            }
        }
        self.load_insurance_data()
    
    def load_insurance_data(self):
        """Load insurance data from storage"""
        try:
            if os.path.exists('insurance.json'):
                with open('insurance.json', 'r') as f:
                    data = json.load(f)
                    self.policies = data.get('policies', [])
                    self.claims = data.get('claims', [])
        except Exception as e:
            st.error(f"Error loading insurance data: {e}")
    
    def save_insurance_data(self):
        """Save insurance data to storage"""
        try:
            data = {
                'policies': self.policies,
                'claims': self.claims
            }
            with open('insurance.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            st.error(f"Error saving insurance data: {e}")
    
    def add_policy(self, company, policy_type, policy_number, coverage_amount, premium, renewal_date):
        """Add a new insurance policy"""
        policy = {
            'id': len(self.policies) + 1,
            'company': company,
            'policy_type': policy_type,
            'policy_number': policy_number,
            'coverage_amount': coverage_amount,
            'premium': premium,
            'renewal_date': renewal_date,
            'status': 'active',
            'created_date': datetime.now().strftime('%Y-%m-%d')
        }
        self.policies.append(policy)
        self.save_insurance_data()
        return policy
    
    def add_claim(self, policy_id, claim_type, claim_amount, description, status='pending'):
        """Add a new insurance claim"""
        claim = {
            'id': len(self.claims) + 1,
            'policy_id': policy_id,
            'claim_type': claim_type,
            'claim_amount': claim_amount,
            'description': description,
            'status': status,
            'filed_date': datetime.now().strftime('%Y-%m-%d')
        }
        self.claims.append(claim)
        self.save_insurance_data()
        return claim
    
    def get_insurance_summary(self):
        """Get insurance summary"""
        total_coverage = sum(policy['coverage_amount'] for policy in self.policies if policy['status'] == 'active')
        total_premiums = sum(policy['premium'] for policy in self.policies if policy['status'] == 'active')
        active_policies = len([p for p in self.policies if p['status'] == 'active'])
        pending_claims = len([c for c in self.claims if c['status'] == 'pending'])
        
        return {
            'total_coverage': total_coverage,
            'total_premiums': total_premiums,
            'active_policies': active_policies,
            'pending_claims': pending_claims,
            'companies': list(set(policy['company'] for policy in self.policies if policy['status'] == 'active'))
        }
    
    def get_company_info(self, company_key):
        """Get insurance company information"""
        return self.insurance_companies.get(company_key, {})
    
    def get_available_companies(self):
        """Get list of available insurance companies"""
        return list(self.insurance_companies.keys())
    
    def sync_with_company(self, company_key, sync_type='import'):
        """Sync with insurance company"""
        company_info = self.get_company_info(company_key)
        if sync_type == 'import':
            return f"Imported policy data from {company_info['name']}"
        elif sync_type == 'export':
            return f"Exported data to {company_info['name']}"
        else:
            return f"Synced with {company_info['name']}"

# Initialize insurance manager
insurance_manager = InsuranceManager()

# Legal Management System
class LegalManager:
    def __init__(self):
        self.legal_cases = []
        self.documents = []
        self.appointments = []
        self.law_firms = {
            'kirkland_ellis': {
                'name': 'Kirkland & Ellis LLP',
                'website': 'https://www.kirkland.com',
                'api_available': True,
                'specialties': ['Corporate Law', 'Litigation', 'Private Equity', 'Real Estate', 'Tax Law'],
                'rating': 4.8,
                'description': 'Leading global law firm with 2,000+ lawyers',
                'contact': '+1 (312) 861-2000',
                'locations': ['Chicago', 'New York', 'Los Angeles', 'London', 'Hong Kong'],
                'founded': 1909,
                'size': 'Large Firm (2000+ lawyers)'
            },
            'latham_watkins': {
                'name': 'Latham & Watkins LLP',
                'website': 'https://www.lw.com',
                'api_available': True,
                'specialties': ['Corporate Law', 'Litigation', 'Banking', 'Real Estate', 'Environmental Law'],
                'rating': 4.7,
                'description': 'Global law firm with 2,500+ lawyers worldwide',
                'contact': '+1 (213) 485-1234',
                'locations': ['Los Angeles', 'New York', 'London', 'Frankfurt', 'Tokyo'],
                'founded': 1934,
                'size': 'Large Firm (2500+ lawyers)'
            },
            'skadden': {
                'name': 'Skadden, Arps, Slate, Meagher & Flom LLP',
                'website': 'https://www.skadden.com',
                'api_available': True,
                'specialties': ['M&A', 'Corporate Law', 'Litigation', 'Securities', 'Tax Law'],
                'rating': 4.9,
                'description': 'Premier global law firm specializing in M&A and corporate law',
                'contact': '+1 (212) 735-3000',
                'locations': ['New York', 'Los Angeles', 'London', 'Hong Kong', 'Beijing'],
                'founded': 1948,
                'size': 'Large Firm (1500+ lawyers)'
            },
            'cravath': {
                'name': 'Cravath, Swaine & Moore LLP',
                'website': 'https://www.cravath.com',
                'api_available': True,
                'specialties': ['Corporate Law', 'Litigation', 'Securities', 'Banking', 'Tax Law'],
                'rating': 4.9,
                'description': 'Elite law firm known for corporate and securities law',
                'contact': '+1 (212) 474-1000',
                'locations': ['New York', 'London'],
                'founded': 1819,
                'size': 'Boutique Firm (500+ lawyers)'
            },
            'wachtell': {
                'name': 'Wachtell, Lipton, Rosen & Katz',
                'website': 'https://www.wlrk.com',
                'api_available': True,
                'specialties': ['M&A', 'Corporate Law', 'Securities', 'Banking', 'Tax Law'],
                'rating': 4.9,
                'description': 'Premier M&A and corporate law firm',
                'contact': '+1 (212) 403-1000',
                'locations': ['New York'],
                'founded': 1965,
                'size': 'Boutique Firm (300+ lawyers)'
            },
            'legal_zoom': {
                'name': 'LegalZoom',
                'website': 'https://www.legalzoom.com',
                'api_available': True,
                'specialties': ['Business Formation', 'Estate Planning', 'Trademark', 'Copyright', 'Contracts'],
                'rating': 4.2,
                'description': 'Online legal services for small businesses and individuals',
                'contact': '+1 (855) 303-3071',
                'locations': ['Online'],
                'founded': 2001,
                'size': 'Online Platform'
            },
            'rocket_lawyer': {
                'name': 'Rocket Lawyer',
                'website': 'https://www.rocketlawyer.com',
                'api_available': True,
                'specialties': ['Business Formation', 'Contracts', 'Estate Planning', 'Real Estate', 'Family Law'],
                'rating': 4.1,
                'description': 'Online legal services and document preparation',
                'contact': '+1 (877) 881-0949',
                'locations': ['Online'],
                'founded': 2008,
                'size': 'Online Platform'
            },
            'avvo': {
                'name': 'Avvo',
                'website': 'https://www.avvo.com',
                'api_available': True,
                'specialties': ['Legal Directory', 'Attorney Reviews', 'Legal Q&A', 'Legal Guides', 'Case Evaluation'],
                'rating': 4.3,
                'description': 'Legal directory and attorney review platform',
                'contact': 'Online Platform',
                'locations': ['Online'],
                'founded': 2007,
                'size': 'Online Platform'
            }
        }
        self.load_legal_data()
    
    def load_legal_data(self):
        """Load legal data from storage"""
        try:
            if os.path.exists('legal.json'):
                with open('legal.json', 'r') as f:
                    data = json.load(f)
                    self.legal_cases = data.get('legal_cases', [])
                    self.documents = data.get('documents', [])
                    self.appointments = data.get('appointments', [])
        except Exception as e:
            st.error(f"Error loading legal data: {e}")
    
    def save_legal_data(self):
        """Save legal data to storage"""
        try:
            data = {
                'legal_cases': self.legal_cases,
                'documents': self.documents,
                'appointments': self.appointments
            }
            with open('legal.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            st.error(f"Error saving legal data: {e}")
    
    def add_legal_case(self, case_type, description, law_firm, status='open', priority='medium'):
        """Add a new legal case"""
        case = {
            'id': len(self.legal_cases) + 1,
            'case_type': case_type,
            'description': description,
            'law_firm': law_firm,
            'status': status,
            'priority': priority,
            'created_date': datetime.now().strftime('%Y-%m-%d'),
            'last_updated': datetime.now().strftime('%Y-%m-%d')
        }
        self.legal_cases.append(case)
        self.save_legal_data()
        return case
    
    def add_document(self, document_type, title, law_firm, status='draft'):
        """Add a new legal document"""
        document = {
            'id': len(self.documents) + 1,
            'document_type': document_type,
            'title': title,
            'law_firm': law_firm,
            'status': status,
            'created_date': datetime.now().strftime('%Y-%m-%d'),
            'last_updated': datetime.now().strftime('%Y-%m-%d')
        }
        self.documents.append(document)
        self.save_legal_data()
        return document
    
    def add_appointment(self, law_firm, appointment_type, date, time, description):
        """Add a new legal appointment"""
        appointment = {
            'id': len(self.appointments) + 1,
            'law_firm': law_firm,
            'appointment_type': appointment_type,
            'date': date,
            'time': time,
            'description': description,
            'status': 'scheduled',
            'created_date': datetime.now().strftime('%Y-%m-%d')
        }
        self.appointments.append(appointment)
        self.save_legal_data()
        return appointment
    
    def get_legal_summary(self):
        """Get legal summary"""
        active_cases = len([c for c in self.legal_cases if c['status'] == 'open'])
        completed_cases = len([c for c in self.legal_cases if c['status'] == 'closed'])
        pending_documents = len([d for d in self.documents if d['status'] == 'draft'])
        upcoming_appointments = len([a for a in self.appointments if a['status'] == 'scheduled'])
        
        return {
            'active_cases': active_cases,
            'completed_cases': completed_cases,
            'pending_documents': pending_documents,
            'upcoming_appointments': upcoming_appointments,
            'total_cases': len(self.legal_cases),
            'total_documents': len(self.documents)
        }
    
    def get_firm_info(self, firm_key):
        """Get law firm information"""
        return self.law_firms.get(firm_key, {})
    
    def get_available_firms(self):
        """Get list of available law firms"""
        return list(self.law_firms.keys())
    
    def sync_with_firm(self, firm_key, sync_type='import'):
        """Sync with law firm"""
        firm_info = self.get_firm_info(firm_key)
        if sync_type == 'import':
            return f"Imported case data from {firm_info['name']}"
        elif sync_type == 'export':
            return f"Exported data to {firm_info['name']}"
        else:
            return f"Synced with {firm_info['name']}"

# Initialize legal manager
legal_manager = LegalManager()

# Tax Management System
class TaxManager:
    def __init__(self):
        self.tax_documents = []
        self.tax_filings = []
        self.deductions = []
        self.tax_providers = {
            'turbotax': {
                'name': 'TurboTax',
                'website': 'https://turbotax.intuit.com',
                'api_available': True,
                'features': ['Federal & State Filing', 'Tax Expert Review', 'Audit Support', 'Max Refund Guarantee', 'Import W-2s', 'Live CPA Help'],
                'pricing': {
                    'free': '$0 - Simple returns only',
                    'deluxe': '$59 - Homeowners & investors',
                    'premier': '$89 - Investments & rental property',
                    'self_employed': '$119 - Contractors & freelancers'
                },
                'rating': 4.5,
                'description': 'Most popular tax software with comprehensive features and excellent UI',
                'mobile_app': True,
                'integration': True,
                'customer_support': '24/7 Live Support'
            },
            'hr_block': {
                'name': 'H&R Block',
                'website': 'https://www.hrblock.com',
                'api_available': True,
                'features': ['Federal & State Filing', 'Tax Pro Review', 'In-Person Help', 'Audit Support', 'Second Look Review', 'Refund Advance'],
                'pricing': {
                    'free': '$0 - Simple returns',
                    'deluxe': '$55 - Homeowners',
                    'premium': '$75 - Investments',
                    'self_employed': '$110 - Business owners'
                },
                'rating': 4.4,
                'description': 'Trusted tax preparation with option for in-person assistance',
                'mobile_app': True,
                'integration': True,
                'customer_support': 'In-person & Online'
            },
            'taxact': {
                'name': 'TaxAct',
                'website': 'https://www.taxact.com',
                'api_available': True,
                'features': ['Federal & State Filing', 'Price Lock Guarantee', 'Deduction Maximizer', 'Audit Assistance', 'Prior Year Returns'],
                'pricing': {
                    'free': '$0 - Basic returns',
                    'deluxe': '$47 - Itemized deductions',
                    'premier': '$65 - Investments',
                    'self_employed': '$95 - Business income'
                },
                'rating': 4.3,
                'description': 'Affordable tax software with great value for complex returns',
                'mobile_app': True,
                'integration': True,
                'customer_support': 'Email & Phone'
            },
            'freetaxusa': {
                'name': 'FreeTaxUSA',
                'website': 'https://www.freetaxusa.com',
                'api_available': True,
                'features': ['Free Federal Filing', 'All Tax Situations', 'Audit Assistance', 'Prior Year Returns', 'Amendment Support'],
                'pricing': {
                    'federal': '$0 - All federal returns',
                    'state': '$14.99 per state',
                    'deluxe': '$7.99 - Priority support'
                },
                'rating': 4.6,
                'description': 'Best free option with excellent features at no cost for federal',
                'mobile_app': True,
                'integration': True,
                'customer_support': 'Email Support'
            },
            'taxslayer': {
                'name': 'TaxSlayer',
                'website': 'https://www.taxslayer.com',
                'api_available': True,
                'features': ['Federal & State Filing', 'Accuracy Guarantee', 'Deduction Finder', 'Free Audit Assistance', 'Military Discount'],
                'pricing': {
                    'simply_free': '$0 - Simple returns',
                    'classic': '$22.95 - All tax situations',
                    'premium': '$44.95 - Priority support',
                    'self_employed': '$54.95 - Business income'
                },
                'rating': 4.2,
                'description': 'Budget-friendly option with solid features and military benefits',
                'mobile_app': True,
                'integration': True,
                'customer_support': 'Phone & Email'
            },
            'creditkarma': {
                'name': 'Credit Karma Tax (Cash App Taxes)',
                'website': 'https://www.creditkarma.com/tax',
                'api_available': True,
                'features': ['100% Free Filing', 'Federal & State', 'Max Refund', 'Audit Defense', 'Import Documents'],
                'pricing': {
                    'all': '$0 - Completely free for all'
                },
                'rating': 4.1,
                'description': 'Completely free tax filing for federal and state returns',
                'mobile_app': True,
                'integration': True,
                'customer_support': 'Email Support'
            },
            'taxwise': {
                'name': 'TaxWise',
                'website': 'https://www.taxwise.com',
                'api_available': True,
                'features': ['Professional Tax Software', 'Multi-User Support', 'E-Filing', 'Bank Products', 'Practice Management'],
                'pricing': {
                    'professional': 'Custom pricing for tax professionals'
                },
                'rating': 4.4,
                'description': 'Professional-grade tax preparation software for tax preparers',
                'mobile_app': False,
                'integration': True,
                'customer_support': 'Dedicated Professional Support'
            },
            'quickbooks': {
                'name': 'QuickBooks Self-Employed',
                'website': 'https://quickbooks.intuit.com/self-employed/',
                'api_available': True,
                'features': ['Expense Tracking', 'Mileage Tracking', 'Quarterly Tax Estimates', 'Schedule C Prep', 'Invoice & Payments'],
                'pricing': {
                    'self_employed': '$15/month - Tax bundle',
                    'with_turbotax': '$20/month - Includes TurboTax'
                },
                'rating': 4.5,
                'description': 'Year-round tax tracking for self-employed and freelancers',
                'mobile_app': True,
                'integration': True,
                'customer_support': 'Live Chat & Phone'
            }
        }
        self.load_tax_data()
    
    def load_tax_data(self):
        """Load tax data from storage"""
        try:
            if os.path.exists('tax_data.json'):
                with open('tax_data.json', 'r') as f:
                    data = json.load(f)
                    self.tax_documents = data.get('tax_documents', [])
                    self.tax_filings = data.get('tax_filings', [])
                    self.deductions = data.get('deductions', [])
        except Exception as e:
            st.error(f"Error loading tax data: {e}")
    
    def save_tax_data(self):
        """Save tax data to storage"""
        try:
            data = {
                'tax_documents': self.tax_documents,
                'tax_filings': self.tax_filings,
                'deductions': self.deductions
            }
            with open('tax_data.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            st.error(f"Error saving tax data: {e}")
    
    def add_tax_document(self, doc_type, description, tax_year, amount=0):
        """Add a new tax document"""
        document = {
            'id': len(self.tax_documents) + 1,
            'doc_type': doc_type,
            'description': description,
            'tax_year': tax_year,
            'amount': amount,
            'status': 'pending',
            'uploaded_date': datetime.now().strftime('%Y-%m-%d')
        }
        self.tax_documents.append(document)
        self.save_tax_data()
        return document
    
    def add_deduction(self, category, description, amount, tax_year):
        """Add a tax deduction"""
        deduction = {
            'id': len(self.deductions) + 1,
            'category': category,
            'description': description,
            'amount': amount,
            'tax_year': tax_year,
            'created_date': datetime.now().strftime('%Y-%m-%d')
        }
        self.deductions.append(deduction)
        self.save_tax_data()
        return deduction
    
    def file_tax_return(self, tax_year, provider, filing_type, status='draft'):
        """File a tax return"""
        filing = {
            'id': len(self.tax_filings) + 1,
            'tax_year': tax_year,
            'provider': provider,
            'filing_type': filing_type,
            'status': status,
            'filed_date': datetime.now().strftime('%Y-%m-%d') if status == 'filed' else None,
            'created_date': datetime.now().strftime('%Y-%m-%d')
        }
        self.tax_filings.append(filing)
        self.save_tax_data()
        return filing
    
    def get_tax_summary(self, tax_year):
        """Get tax summary for a year"""
        year_docs = [d for d in self.tax_documents if d['tax_year'] == tax_year]
        year_deductions = [d for d in self.deductions if d['tax_year'] == tax_year]
        year_filings = [f for f in self.tax_filings if f['tax_year'] == tax_year]
        
        total_deductions = sum(d['amount'] for d in year_deductions)
        documents_collected = len([d for d in year_docs if d['status'] == 'complete'])
        total_documents = len(year_docs)
        
        return {
            'total_deductions': total_deductions,
            'documents_collected': documents_collected,
            'total_documents': total_documents,
            'filings': len(year_filings),
            'filing_status': year_filings[0]['status'] if year_filings else 'not_started'
        }
    
    def get_provider_info(self, provider_key):
        """Get tax provider information"""
        return self.tax_providers.get(provider_key, {})
    
    def get_available_providers(self):
        """Get list of available tax providers"""
        return list(self.tax_providers.keys())
    
    def sync_with_provider(self, provider_key, sync_type='import'):
        """Sync with tax provider"""
        provider_info = self.get_provider_info(provider_key)
        if sync_type == 'import':
            return f"Imported tax data from {provider_info['name']}"
        elif sync_type == 'export':
            return f"Exported data to {provider_info['name']}"
        else:
            return f"Synced with {provider_info['name']}"

# Initialize tax manager
tax_manager = TaxManager()

# Initialize AI system
ai_system = AIAgentSystem()

# Messaging System for Concierge Communication
class MessagingSystem:
    def __init__(self):
        self.messages = []
        self.conversations = {}
        self.storage_file = "chat_history.json"
        self.load_messages()
        self.ai_responses = {
            'expense': [
                "I've analyzed your spending patterns and found 3 optimization opportunities.",
                "Your dining expenses increased 15% this month. Would you like me to suggest alternatives?",
                "I've identified $200 in potential monthly savings from subscription optimization."
            ],
            'travel': [
                "I found 25% cheaper flights for your upcoming trip to Paris.",
                "Your preferred hotel has a special rate available. Should I book it?",
                "I've optimized your travel itinerary to save 3 hours of travel time."
            ],
            'medical': [
                "Your annual checkup is due next month. I've scheduled it for Tuesday at 2 PM.",
                "I've set up prescription refill reminders for your medications.",
                "Your insurance claim for $450 has been approved and processed.",
                "I've identified 2 prescriptions due for refill in the next 5 days.",
                "Your prescription adherence rate is excellent at 94%.",
                "I found potential cost savings of $120/year on your medications.",
                "I've coordinated with your pharmacy for the refill of your blood pressure medication.",
                "Your prescription schedule has been optimized for maximum effectiveness."
            ],
            'insurance': [
                "I've found better auto insurance rates that could save you $200/year.",
                "Your home insurance needs updating for natural disaster coverage.",
                "I've reviewed your life insurance and recommend increasing coverage by $50K."
            ],
            'tax': [
                "I've identified $800 in additional tax savings through charitable donations.",
                "Your quarterly estimated tax payment of $2,400 is due in 2 weeks.",
                "I've organized all your tax documents and found 3 missing forms."
            ],
            'general': [
                "I'm here to help with anything you need. What can I assist you with today?",
                "I've completed your request and will follow up with details shortly.",
                "Is there anything else I can help you with right now?"
            ]
        }
    
    def load_messages(self):
        """Load messages from persistent storage"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self.messages = data.get('messages', [])
                    self.conversations = data.get('conversations', {})
                    
                    # Convert timestamp strings back to datetime objects
                    for message in self.messages:
                        if isinstance(message.get('timestamp'), str):
                            message['timestamp'] = datetime.fromisoformat(message['timestamp'])
        except Exception as e:
            print(f"Error loading messages: {e}")
            self.messages = []
            self.conversations = {}
    
    def save_messages(self):
        """Save messages to persistent storage"""
        try:
            # Convert datetime objects to strings for JSON serialization
            messages_to_save = []
            for message in self.messages:
                message_copy = message.copy()
                if isinstance(message_copy.get('timestamp'), datetime):
                    message_copy['timestamp'] = message_copy['timestamp'].isoformat()
                messages_to_save.append(message_copy)
            
            data = {
                'messages': messages_to_save,
                'conversations': self.conversations
            }
            
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving messages: {e}")
    
    def add_message(self, sender, recipient, message, message_type="user", channel="concierge"):
        """Add a new message to the system"""
        message_id = str(uuid.uuid4())
        new_message = {
            'id': message_id,
            'sender': sender,
            'recipient': recipient,
            'message': message,
            'timestamp': datetime.now(),
            'message_type': message_type,  # 'user', 'concierge', 'ai_agent'
            'channel': channel,  # 'concierge', 'ai_agent', 'support'
            'read': False
        }
        self.messages.append(new_message)
        
        # Add to conversation thread
        if channel not in self.conversations:
            self.conversations[channel] = []
        self.conversations[channel].append(new_message)
        
        # Save messages to persistent storage
        self.save_messages()
        
        return message_id
    
    def get_messages(self, channel="concierge", limit=50):
        """Get messages for a specific channel"""
        if channel not in self.conversations:
            return []
        return self.conversations[channel][-limit:]
    
    def get_unread_count(self, channel="concierge"):
        """Get count of unread messages"""
        if channel not in self.conversations:
            return 0
        return len([m for m in self.conversations[channel] if not m['read']])
    
    def mark_as_read(self, message_id):
        """Mark a message as read"""
        for message in self.messages:
            if message['id'] == message_id:
                message['read'] = True
                break
    
    def generate_ai_response(self, user_message, user_plan):
        """Generate AI response based on user message and plan"""
        message_lower = user_message.lower()
        
        # Determine response category
        if any(word in message_lower for word in ['expense', 'spending', 'budget', 'money']):
            category = 'expense'
        elif any(word in message_lower for word in ['travel', 'trip', 'flight', 'hotel']):
            category = 'travel'
        elif any(word in message_lower for word in ['medical', 'doctor', 'appointment', 'health']):
            category = 'medical'
        elif any(word in message_lower for word in ['insurance', 'claim', 'coverage']):
            category = 'insurance'
        elif any(word in message_lower for word in ['tax', 'filing', 'deduction']):
            category = 'tax'
        else:
            category = 'general'
        
        # Get appropriate response based on plan
        if user_plan == 'elite':
            responses = self.ai_responses[category] + [
                "As your elite concierge, I'm prioritizing this request.",
                "I'll handle this personally and provide updates within the hour.",
                "Your request has been escalated to our premium support team."
            ]
        elif user_plan == 'premium':
            responses = self.ai_responses[category] + [
                "I'm working on this for you and will update you soon.",
                "I've added this to your priority task list.",
                "I'll have this resolved for you today."
            ]
        else:
            responses = self.ai_responses[category] + [
                "I'm processing your request and will respond within 24 hours.",
                "Thank you for your message. I'll get back to you soon.",
                "I've received your request and will provide assistance."
            ]
        
        return random.choice(responses)
    
    def get_conversation_summary(self, channel="concierge"):
        """Get summary of recent conversation"""
        if channel not in self.conversations:
            return "No messages yet"
        
        recent_messages = self.conversations[channel][-5:]
        summary = []
        for msg in recent_messages:
            sender_name = "You" if msg['message_type'] == 'user' else msg['sender']
            summary.append(f"{sender_name}: {msg['message'][:50]}...")
        
        return "\n".join(summary)
    
    def get_chat_restore_info(self):
        """Get information about restored chat history"""
        total_messages = len(self.messages)
        channels = list(self.conversations.keys())
        return {
            'total_messages': total_messages,
            'channels': channels,
            'has_history': total_messages > 0
        }

# Initialize messaging system in session state
if 'messaging_system' not in st.session_state:
    st.session_state.messaging_system = MessagingSystem()

# Get messaging system from session state
messaging_system = st.session_state.messaging_system

def login_user(username, plan='basic'):
    st.session_state.user_logged_in = True
    st.session_state.user_plan = plan
    st.session_state.user_data = {
        'username': username,
        'login_time': datetime.now(),
        'api_calls_used': 0,
        'api_calls_limit': 100 if plan == 'basic' else 1000 if plan == 'premium' else 10000,
        'concierge_name': 'Sarah Johnson' if plan == 'premium' else 'Michael Chen' if plan == 'elite' else None,
        'concierge_photo': '👩‍💼' if plan == 'premium' else '👨‍💼' if plan == 'elite' else None,
        'concierge_phone': '+1 (555) 123-4567' if plan in ['premium', 'elite'] else None,
        'concierge_email': 'sarah@concierge.com' if plan == 'premium' else 'michael@concierge.com' if plan == 'elite' else None
    }

def logout_user():
    st.session_state.user_logged_in = False
    st.session_state.user_plan = 'basic'
    st.session_state.user_data = {}

def login_admin(username, password):
    """Login admin user"""
    auth_result = admin_system.authenticate_admin(username, password)
    if auth_result['authenticated']:
        st.session_state.admin_logged_in = True
        st.session_state.admin_role = auth_result['role']
        st.session_state.admin_name = auth_result['name']
        st.session_state.logged_in_admin = username  # Store username for reference
        return True
    return False

def logout_admin():
    """Logout admin user"""
    st.session_state.admin_logged_in = False
    st.session_state.admin_role = None
    st.session_state.admin_name = None
    st.session_state.logged_in_admin = None

# Admin Panel Access (Hidden from clients)
# Check for admin access via URL parameter or special access
admin_access = st.query_params.get("admin", None)
if admin_access == "internal" or st.session_state.admin_logged_in:
    if not st.session_state.admin_logged_in:
        # Admin Login Page
        st.title("🔐 Internal Staff Access")
        st.markdown("**Authorized Personnel Only**")
        
        # Security Notice
        st.warning("🚨 **SECURITY ALERT:** Admin passwords have been updated due to a security incident. Please use the new credentials below.")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🔑 Admin Login")
            admin_username = st.text_input("Username", key="admin_username")
            admin_password = st.text_input("Password", type="password", key="admin_password")
            if st.button("Login as Admin"):
                if admin_username and admin_password:
                    if login_admin(admin_username, admin_password):
                        st.success("Admin login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid admin credentials")
                else:
                    st.error("Please enter both username and password")
        
        with col2:
            st.subheader("👥 Admin Roles")
            st.write("**Super Admin:** Full system access")
            st.write("**Manager:** User management & analytics")
            st.write("**Support:** User management & logs")
            st.write("**Analyst:** Analytics & logs")
            
            st.markdown("---")
            st.write("**Demo Credentials:**")
            st.write("• Super Admin: admin / SecureAdmin2024!")
            st.write("• Manager: manager / Manager2024!")
            st.write("• Support: support / Support2024!")
            st.write("• Analyst: analyst / Analyst2024!")
    else:
        # Admin Dashboard
        admin_name = st.session_state.get('admin_name', 'Admin')
        st.title(f"🛠️ Admin Dashboard - {admin_name}")
        
        # Admin role and permissions
        permissions = admin_system.get_admin_permissions(st.session_state.admin_role)
        st.sidebar.write(f"**Role:** {st.session_state.admin_role.title()}")
        st.sidebar.write(f"**Permissions:** {', '.join(permissions)}")
        
        # Debug info
        st.sidebar.write("---")
        st.sidebar.write("**Debug Info:**")
        st.sidebar.write(f"Admin Role: {st.session_state.admin_role}")
        st.sidebar.write(f"Has user_management: {'user_management' in permissions}")
        
        if st.sidebar.button("🚪 Logout Admin"):
            logout_admin()
            st.rerun()
        
        # Admin tabs based on permissions
        admin_tabs = []
        if 'user_management' in permissions:
            admin_tabs.append("👥 User Management")
        if 'user_management' in permissions:
            admin_tabs.append("👨‍💼 Staff Management")
        
        # Fallback: Always show Staff Management for super_admin
        if st.session_state.admin_role == 'super_admin' and "👨‍💼 Staff Management" not in admin_tabs:
            admin_tabs.append("👨‍💼 Staff Management")
        if 'system_monitoring' in permissions:
            admin_tabs.append("📊 System Monitoring")
        if 'analytics' in permissions:
            admin_tabs.append("📈 Analytics")
        if 'settings' in permissions:
            admin_tabs.append("⚙️ Settings")
        if 'logs' in permissions:
            admin_tabs.append("📋 System Logs")
        
        if admin_tabs:
            st.write(f"**Available Tabs:** {admin_tabs}")  # Debug info
            selected_tab = st.selectbox("Select Admin Section", admin_tabs)
            
            if selected_tab == "👥 User Management" and 'user_management' in permissions:
                st.subheader("👥 User Management")
                
                # User analytics
                analytics = admin_system.get_user_analytics()
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Users", analytics['total_users'])
                with col2:
                    st.metric("Active Sessions", analytics['active_sessions'])
                with col3:
                    st.metric("Messages Sent", analytics['messages_sent'])
                with col4:
                    st.metric("AI Tasks", analytics['ai_tasks_completed'])
                
                # User management actions
                st.subheader("🔧 User Management Actions")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📊 Generate User Report"):
                        st.success("User report generated!")
                        admin_system.update_metrics('total_users', 1)
                
                with col2:
                    if st.button("🔄 Refresh User Data"):
                        st.success("User data refreshed!")
                
                with col3:
                    if st.button("📧 Send System Notification"):
                        st.success("System notification sent to all users!")
            
            elif selected_tab == "👨‍💼 Staff Management" and 'user_management' in permissions:
                st.subheader("👨‍💼 Internal Staff Management")
                
                # Staff analytics
                staff_analytics = admin_system.get_staff_analytics()
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Staff", staff_analytics['total_staff'])
                with col2:
                    st.metric("Active Staff", staff_analytics['active_staff'])
                with col3:
                    st.metric("Inactive Staff", staff_analytics['inactive_staff'])
                with col4:
                    st.metric("Departments", len(staff_analytics['role_distribution']))
                
                # Staff management tabs
                staff_tab1, staff_tab2, staff_tab3, staff_tab4 = st.tabs(["👥 Staff List", "➕ Add Staff", "✏️ Edit Staff", "📊 Staff Analytics"])
                
                with staff_tab1:
                    st.subheader("👥 Staff Directory")
                    
                    # Search and filter options
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        search_term = st.text_input("🔍 Search Staff", placeholder="Search by name, username, or email")
                    with col2:
                        department_filter = st.selectbox("Department", ["All"] + admin_system.get_departments())
                    with col3:
                        status_filter = st.selectbox("Status", ["All", "Active", "Inactive"])
                    
                    # Get filtered staff
                    if search_term:
                        staff_members = admin_system.search_staff(search_term)
                    elif department_filter != "All":
                        staff_members = admin_system.get_staff_by_department(department_filter)
                    else:
                        staff_members = admin_system.get_staff_members()
                    
                    # Apply status filter
                    if status_filter != "All":
                        status_value = status_filter.lower()
                        staff_members = {k: v for k, v in staff_members.items() if v.get('status') == status_value}
                    
                    # Display staff members in a more organized way
                    if staff_members:
                        st.write(f"**Found {len(staff_members)} staff member(s)**")
                        
                        # Create a more detailed staff table
                        for username, staff_info in staff_members.items():
                            with st.container():
                                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                                
                                with col1:
                                    status_icon = "🟢" if staff_info.get('status') == 'active' else "🔴"
                                    role_icon = {"super_admin": "👑", "manager": "👨‍💼", "support": "🛠️", "analyst": "📊"}.get(staff_info.get('role'), "👤")
                                    st.write(f"{status_icon} {role_icon} **{staff_info.get('name', username)}**")
                                    st.write(f"@{username} • {staff_info.get('role', 'Unknown').title()}")
                                
                                with col2:
                                    st.write(f"📧 {staff_info.get('email', 'N/A')}")
                                    st.write(f"📞 {staff_info.get('phone', 'N/A')}")
                                
                                with col3:
                                    st.write(f"🏢 {staff_info.get('department', 'N/A')}")
                                    st.write(f"📅 Created: {staff_info.get('created_date', 'N/A')}")
                                    st.write(f"🕐 Last Login: {staff_info.get('last_login', 'Never')}")
                                
                                with col4:
                                    if username != st.session_state.get('logged_in_admin', 'admin'):
                                        if st.button("⚙️", key=f"manage_{username}", help="Manage staff member"):
                                            st.session_state[f'edit_{username}'] = True
                                        if st.button("❌", key=f"deactivate_{username}", help="Deactivate"):
                                            success, message = admin_system.deactivate_staff_member(username)
                                            if success:
                                                st.success(message)
                                                st.rerun()
                                            else:
                                                st.error(message)
                                    else:
                                        st.write("👤 You")
                                
                                st.divider()
                    else:
                        st.info("No staff members found matching your criteria.")
                
                with staff_tab2:
                    st.subheader("➕ Add New Staff Member")
                    
                    with st.form("add_staff_member"):
                        # Basic Information
                        st.markdown("### 👤 Basic Information")
                        col1, col2 = st.columns(2)
                        with col1:
                            new_username = st.text_input("Username *", key="new_staff_username", help="Unique username for login")
                            new_password = st.text_input("Password *", type="password", key="new_staff_password", help="Secure password for the account")
                            new_name = st.text_input("Full Name *", key="new_staff_name", help="Complete name of the staff member")
                        with col2:
                            new_role = st.selectbox("Role *", ["super_admin", "manager", "support", "analyst"], key="new_staff_role", help="Administrative role and permissions")
                            new_email = st.text_input("Email", key="new_staff_email", help="Professional email address")
                            new_phone = st.text_input("Phone", key="new_staff_phone", help="Contact phone number")
                        
                        # Department and Additional Info
                        st.markdown("### 🏢 Department & Additional Information")
                        col1, col2 = st.columns(2)
                        with col1:
                            new_department = st.text_input("Department", key="new_staff_department", help="Department or team")
                            new_position = st.text_input("Job Title", key="new_staff_position", help="Official job title")
                        with col2:
                            new_hire_date = st.date_input("Hire Date", key="new_staff_hire_date", help="Date of employment")
                            new_employee_id = st.text_input("Employee ID", key="new_staff_employee_id", help="Internal employee identifier")
                        
                        # Emergency Contact
                        st.markdown("### 🚨 Emergency Contact")
                        col1, col2 = st.columns(2)
                        with col1:
                            emergency_name = st.text_input("Emergency Contact Name", key="new_staff_emergency_name")
                            emergency_phone = st.text_input("Emergency Contact Phone", key="new_staff_emergency_phone")
                        with col2:
                            emergency_relation = st.text_input("Relationship", key="new_staff_emergency_relation")
                        
                        # Notes
                        st.markdown("### 📝 Additional Notes")
                        notes = st.text_area("Notes", key="new_staff_notes", help="Any additional information about this staff member")
                        
                        st.markdown("**Required fields are marked with ***")
                        
                        if st.form_submit_button("➕ Add Staff Member", type="primary"):
                            if new_username and new_password and new_name and new_role:
                                # Create extended staff information
                                extended_info = {
                                    'email': new_email,
                                    'phone': new_phone,
                                    'department': new_department,
                                    'position': new_position,
                                    'hire_date': str(new_hire_date) if new_hire_date else None,
                                    'employee_id': new_employee_id,
                                    'emergency_contact': {
                                        'name': emergency_name,
                                        'phone': emergency_phone,
                                        'relationship': emergency_relation
                                    } if emergency_name else None,
                                    'notes': notes
                                }
                                
                                success, message = admin_system.add_staff_member(
                                    new_username, new_password, new_role, new_name,
                                    **extended_info
                                )
                                if success:
                                    st.success(f"✅ {message}")
                                    st.balloons()
                                    st.rerun()
                                else:
                                    st.error(f"❌ {message}")
                            else:
                                st.error("❌ Please fill in all required fields (marked with *)")
                
                with staff_tab3:
                    st.subheader("✏️ Edit Staff Member")
                    
                    # Select staff member to edit
                    edit_username = st.selectbox("Select Staff Member", list(staff_members.keys()))
                    
                    if edit_username:
                        staff_info = staff_members[edit_username]
                        
                        with st.form("edit_staff_member"):
                            col1, col2 = st.columns(2)
                            with col1:
                                edit_name = st.text_input("Full Name", value=staff_info.get('name', ''), key="edit_name")
                                edit_email = st.text_input("Email", value=staff_info.get('email', ''), key="edit_email")
                                edit_phone = st.text_input("Phone", value=staff_info.get('phone', ''), key="edit_phone")
                            with col2:
                                edit_role = st.selectbox("Role", ["super_admin", "manager", "support", "analyst"], 
                                                      index=["super_admin", "manager", "support", "analyst"].index(staff_info.get('role', 'support')), 
                                                      key="edit_role")
                                edit_department = st.text_input("Department", value=staff_info.get('department', ''), key="edit_department")
                                edit_status = st.selectbox("Status", ["active", "inactive"], 
                                                        index=0 if staff_info.get('status') == 'active' else 1, 
                                                        key="edit_status")
                            
                            if st.form_submit_button("Update Staff Member"):
                                updates = {
                                    'name': edit_name,
                                    'email': edit_email,
                                    'phone': edit_phone,
                                    'role': edit_role,
                                    'department': edit_department,
                                    'status': edit_status
                                }
                                success, message = admin_system.update_staff_member(edit_username, **updates)
                                if success:
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.error(message)
                
                with staff_tab4:
                    st.subheader("📊 Staff Analytics & Reports")
                    
                    # Performance metrics
                    performance_metrics = admin_system.get_staff_performance_metrics()
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Staff", performance_metrics['total_staff'])
                    with col2:
                        st.metric("Active Staff", performance_metrics['active_staff'])
                    with col3:
                        st.metric("Departments", performance_metrics['departments'])
                    with col4:
                        st.metric("Tasks Today", performance_metrics['tasks_completed_today'])
                    
                    # Charts section
                    chart_tab1, chart_tab2, chart_tab3 = st.tabs(["📊 Role Distribution", "📈 Performance", "📋 Activity Logs"])
                    
                    with chart_tab1:
                        st.subheader("👥 Staff Role Distribution")
                        role_dist = staff_analytics['role_distribution']
                        if role_dist:
                            role_data = pd.DataFrame(list(role_dist.items()), columns=['Role', 'Count'])
                            fig = px.pie(role_data, values='Count', names='Role', title="Staff Role Distribution")
                            st.plotly_chart(fig, use_container_width=True, key="admin_staff_role_chart")
                            
                            # Department breakdown
                            departments = admin_system.get_departments()
                            if departments:
                                st.subheader("🏢 Department Breakdown")
                                dept_data = []
                                for dept in departments:
                                    dept_staff = admin_system.get_staff_by_department(dept)
                                    dept_data.append({'Department': dept, 'Staff Count': len(dept_staff)})
                                
                                if dept_data:
                                    dept_df = pd.DataFrame(dept_data)
                                    fig_dept = px.bar(dept_df, x='Department', y='Staff Count', title="Staff by Department")
                                    st.plotly_chart(fig_dept, use_container_width=True, key="admin_department_chart")
                    
                    with chart_tab2:
                        st.subheader("📈 Performance Metrics")
                        
                        # Performance data
                        performance_data = {
                            'Metric': ['Daily Logins', 'Response Time (min)', 'Tasks Completed', 'System Uptime (%)'],
                            'Current': [performance_metrics['avg_login_frequency'], 2.3, performance_metrics['tasks_completed_today'], 99.9],
                            'Target': [15.0, 2.0, 200, 99.5],
                            'Status': ['✅', '⚠️', '❌', '✅']
                        }
                        
                        perf_df = pd.DataFrame(performance_data)
                        st.dataframe(perf_df, use_container_width=True)
                        
                        # Performance chart
                        fig_perf = px.bar(perf_df, x='Metric', y=['Current', 'Target'], 
                                        title="Performance vs Targets", barmode='group')
                        st.plotly_chart(fig_perf, use_container_width=True, key="admin_performance_chart")
                    
                    with chart_tab3:
                        st.subheader("📋 Staff Activity Logs")
                        
                        # Filter options
                        col1, col2 = st.columns(2)
                        with col1:
                            log_filter = st.selectbox("Filter by Role", ["All", "super_admin", "manager", "support", "analyst"])
                        with col2:
                            time_filter = st.selectbox("Time Period", ["Today", "This Week", "This Month", "All Time"])
                        
                        # Display logs
                        activity_logs = admin_system.get_staff_activity_logs()
                        for i, log in enumerate(activity_logs):
                            if log_filter == "All" or log_filter in log:
                                st.write(f"**{i+1}.** {log}")
                        
                        # Export options
                        st.subheader("📤 Export Options")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("📊 Export Analytics"):
                                st.success("Analytics report exported!")
                        with col2:
                            if st.button("📋 Export Staff List"):
                                st.success("Staff list exported!")
                        with col3:
                            if st.button("📈 Export Performance"):
                                st.success("Performance report exported!")
            
            elif selected_tab == "📊 System Monitoring" and 'system_monitoring' in permissions:
                st.subheader("📊 System Monitoring")
                
                # System metrics
                metrics = admin_system.get_system_metrics()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Users", metrics['total_users'])
                    st.metric("Active Sessions", metrics['active_sessions'])
                    st.metric("Messages Sent", metrics['messages_sent'])
                
                with col2:
                    st.metric("Prescriptions Managed", metrics['prescriptions_managed'])
                    st.metric("AI Tasks Completed", metrics['ai_tasks_completed'])
                    st.metric("System Uptime", "99.9%")
                
                # System health
                st.subheader("🏥 System Health")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("CPU Usage", "45%", "↓ 5%")
                with col2:
                    st.metric("Memory Usage", "67%", "↑ 2%")
                with col3:
                    st.metric("Database", "Healthy", "✅")
                
                # Real-time monitoring
                st.subheader("📊 Real-time Monitoring")
                if st.button("🔄 Refresh Metrics"):
                    st.success("Metrics refreshed!")
                    st.rerun()
            
            elif selected_tab == "📈 Analytics" and 'analytics' in permissions:
                st.subheader("📈 System Analytics")
                
                # Analytics dashboard
                analytics_data = {
                    'Metric': ['User Registrations', 'Messages Sent', 'Prescriptions', 'AI Tasks', 'Support Tickets'],
                    'Today': [12, 45, 8, 23, 3],
                    'This Week': [78, 312, 56, 156, 18],
                    'This Month': [234, 1245, 189, 567, 67]
                }
                
                df_analytics = pd.DataFrame(analytics_data)
                st.dataframe(df_analytics, use_container_width=True)
                
                # Analytics charts
                col1, col2 = st.columns(2)
                with col1:
                    fig = px.bar(df_analytics, x='Metric', y='Today', title="Today's Activity")
                    st.plotly_chart(fig, use_container_width=True, key="admin_activity_today_chart")
                
                with col2:
                    fig = px.bar(df_analytics, x='Metric', y='This Week', title="This Week's Activity")
                    st.plotly_chart(fig, use_container_width=True, key="admin_activity_week_chart")
                
                # AI Agent Performance
                st.subheader("🤖 AI Agent Performance")
                agents = ai_system.get_agent_status()
                agent_data = []
                for agent_id, agent_info in agents.items():
                    agent_data.append({
                        'Agent': agent_info['name'],
                        'Status': agent_info['status'],
                        'Tasks Completed': agent_info['tasks_completed']
                    })
                
                if agent_data:
                    df_agents = pd.DataFrame(agent_data)
                    st.dataframe(df_agents, use_container_width=True)
            
            elif selected_tab == "⚙️ Settings" and 'settings' in permissions:
                st.subheader("⚙️ System Settings")
                
                # System configuration
                st.write("**System Configuration**")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**AI Agent Settings**")
                    if st.button("🔄 Restart AI Agents"):
                        st.success("AI agents restarted!")
                    if st.button("📊 Optimize AI Performance"):
                        st.success("AI performance optimized!")
                
                with col2:
                    st.write("**Database Settings**")
                    if st.button("🗄️ Backup Database"):
                        st.success("Database backup initiated!")
                    if st.button("🧹 Clean Old Data"):
                        st.success("Old data cleanup completed!")
                
                # Security settings
                st.subheader("🔒 Security Settings")
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("🔐 Reset Admin Passwords"):
                        st.success("Admin passwords reset!")
                
                with col2:
                    if st.button("🛡️ Enable Security Audit"):
                        st.success("Security audit enabled!")
            
            elif selected_tab == "📋 System Logs" and 'logs' in permissions:
                st.subheader("📋 System Logs")
                
                # Log categories
                log_tabs = st.tabs(["🔐 Authentication", "💬 Messages", "💊 Prescriptions", "🤖 AI Agents", "👨‍💼 Staff", "⚠️ Errors"])
                
                with log_tabs[0]:
                    st.write("**Authentication Logs**")
                    auth_logs = [
                        "2024-01-15 10:30:15 - User 'john_doe' logged in successfully",
                        "2024-01-15 10:25:42 - Admin 'admin' accessed user management",
                        "2024-01-15 10:20:18 - Failed login attempt for 'unknown_user'",
                        "2024-01-15 10:15:33 - User 'jane_smith' logged out"
                    ]
                    for log in auth_logs:
                        st.write(f"• {log}")
                
                with log_tabs[1]:
                    st.write("**Message Logs**")
                    message_logs = [
                        "2024-01-15 10:30:15 - Message sent from 'john_doe' to 'AI Agent'",
                        "2024-01-15 10:25:42 - Concierge response sent to 'jane_smith'",
                        "2024-01-15 10:20:18 - AI Agent processed expense inquiry",
                        "2024-01-15 10:15:33 - Support ticket created by 'user_123'"
                    ]
                    for log in message_logs:
                        st.write(f"• {log}")
                
                with log_tabs[2]:
                    st.write("**Prescription Logs**")
                    prescription_logs = [
                        "2024-01-15 10:30:15 - Prescription 'Vitamin D3' added for 'john_doe'",
                        "2024-01-15 10:25:42 - Refill requested for 'Blood Pressure Med'",
                        "2024-01-15 10:20:18 - Fullscript integration activated",
                        "2024-01-15 10:15:33 - Prescription refill completed"
                    ]
                    for log in prescription_logs:
                        st.write(f"• {log}")
                
                with log_tabs[3]:
                    st.write("**AI Agent Logs**")
                    ai_logs = [
                        "2024-01-15 10:30:15 - AI Agent 'expense_agent' completed task",
                        "2024-01-15 10:25:42 - AI Agent 'medical_agent' processed request",
                        "2024-01-15 10:20:18 - AI Agent 'travel_agent' optimized itinerary",
                        "2024-01-15 10:15:33 - AI Agent 'communication_agent' sent response"
                    ]
                    for log in ai_logs:
                        st.write(f"• {log}")
                
                with log_tabs[4]:
                    st.write("**Staff Activity Logs**")
                    staff_logs = [
                        "2024-01-15 10:30:15 - Admin 'admin' added new staff member 'new_support'",
                        "2024-01-15 10:25:42 - Manager 'manager' updated staff role for 'analyst'",
                        "2024-01-15 10:20:18 - Support 'support' deactivated staff member 'temp_user'",
                        "2024-01-15 10:15:33 - Admin 'admin' changed password for 'manager'",
                        "2024-01-15 10:10:21 - Manager 'manager' viewed staff analytics",
                        "2024-01-15 10:05:12 - Support 'support' accessed user management"
                    ]
                    for log in staff_logs:
                        st.write(f"• {log}")
                
                with log_tabs[5]:
                    st.write("**Error Logs**")
                    error_logs = [
                        "2024-01-15 10:30:15 - WARNING: High memory usage detected",
                        "2024-01-15 10:25:42 - INFO: Database connection restored",
                        "2024-01-15 10:20:18 - ERROR: Failed to send email notification",
                        "2024-01-15 10:15:33 - INFO: System backup completed successfully"
                    ]
                    for log in error_logs:
                        st.write(f"• {log}")
        
        # Update metrics when admin accesses system
        admin_system.update_metrics('active_sessions', 1)
        
else:
    # Regular user interface (existing code)
    pass

# Main App Logic
if not st.session_state.user_logged_in and not st.session_state.admin_logged_in:
    # Login/Signup Page
    st.title("🏆 Concierge.com")
    st.subheader("Your Personal Life Management Platform")
    st.markdown("**Making your life easier, one service at a time**")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🔐 Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            if username and password:
                login_user(username, 'premium')  # Demo: auto-login as premium
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Please enter both username and password")
    
    with col2:
        st.subheader("📝 Sign Up")
        new_username = st.text_input("Username", key="signup_username")
        new_password = st.text_input("Password", type="password", key="signup_password")
        plan_choice = st.selectbox("Choose Plan", ["Basic", "Premium", "Elite"])
        if st.button("Sign Up"):
            if new_username and new_password:
                plan_map = {"Basic": "basic", "Premium": "premium", "Elite": "elite"}
                login_user(new_username, plan_map[plan_choice])
                st.success("Account created successfully!")
                st.rerun()
            else:
                st.error("Please fill in all fields")

elif st.session_state.user_logged_in and not st.session_state.admin_logged_in:
    # Main Dashboard
    username = st.session_state.user_data.get('username', 'User')
    st.title(f"🚀 Welcome back, {username}!")
    
    
    # Chat Restore Notification
    restore_info = messaging_system.get_chat_restore_info()
    if restore_info['has_history']:
        st.success(f"💬 Chat History Restored! Found {restore_info['total_messages']} messages from {len(restore_info['channels'])} channels")
        with st.expander("📋 View Restored Messages"):
            for msg in messaging_system.messages[-10:]:  # Show last 10 messages
                timestamp_str = msg['timestamp'].strftime('%m/%d %H:%M') if isinstance(msg['timestamp'], datetime) else str(msg['timestamp'])
                st.write(f"**{timestamp_str}** - {msg['sender']} → {msg['recipient']}: {msg['message'][:100]}...")
    else:
        st.info("💬 No previous chat history found. Start a new conversation!")
    
    # Debug: Show messaging status
    if st.session_state.get('show_messaging') or st.session_state.get('show_message_history'):
        st.info(f"🔧 Debug: show_messaging={st.session_state.get('show_messaging')}, show_message_history={st.session_state.get('show_message_history')}")
        st.info(f"📊 Total messages in system: {len(messaging_system.messages)}")
    
    # Add a simple message test button on the main dashboard
    if st.button("🧪 Quick Test Message", key="quick_test"):
        test_msg = f"Quick test from {username} at {datetime.now().strftime('%H:%M:%S')}"
        messaging_system.add_message(
            sender=username,
            recipient="Test System",
            message=test_msg,
            message_type="user",
            channel='support'
        )
        st.success("Test message added! Check the message count above.")
        st.rerun()
    
    # User info sidebar
    with st.sidebar:
        st.subheader("👤 Account Info")
        st.write(f"**Plan:** {st.session_state.user_plan.title()}")
        st.write(f"**API Calls:** {st.session_state.user_data.get('api_calls_used', 0)}/{st.session_state.user_data.get('api_calls_limit', 100)}")
        
        # Personal Concierge info for Premium and Elite
        if st.session_state.user_data.get('concierge_name'):
            st.markdown("---")
            st.subheader("🎯 Your Personal Concierge")
            st.write(f"{st.session_state.user_data.get('concierge_photo', '👩‍💼')} **{st.session_state.user_data.get('concierge_name', 'Concierge')}**")
            st.write(f"📞 {st.session_state.user_data.get('concierge_phone', 'N/A')}")
            st.write(f"📧 {st.session_state.user_data.get('concierge_email', 'N/A')}")
            
            if st.button("💬 Message Concierge"):
                st.success("Message sent to your concierge!")
            if st.button("📞 Call Concierge"):
                st.success("Calling your concierge...")
        
        # AI Agent Status for Premium/Elite users
        if st.session_state.user_plan in ['premium', 'elite']:
            st.markdown("---")
            st.subheader("🤖 AI Agent Status")
            agents = ai_system.get_agent_status()
            for agent_id, agent_info in agents.items():
                status_emoji = "🟢" if agent_info['status'] == 'active' else "🔴"
                st.write(f"{status_emoji} {agent_info['name']}")
                st.write(f"   Tasks completed: {agent_info['tasks_completed']}")
        
        # Messaging Status
        st.markdown("---")
        st.subheader("💬 Messages")
        
        # Message counts for different channels
        concierge_unread = messaging_system.get_unread_count('concierge')
        ai_unread = messaging_system.get_unread_count('ai_agent')
        support_unread = messaging_system.get_unread_count('support')
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"📞 Concierge: {concierge_unread}")
        with col2:
            st.write(f"🤖 AI Agents: {ai_unread}")
        
        if st.session_state.user_plan == 'basic':
            st.write(f"📧 Support: {support_unread}")
        
        # Quick message buttons
        if st.button("💬 New Message"):
            st.session_state.show_messaging = True
            st.rerun()
        
        if st.button("📋 View All Messages"):
            st.session_state.show_message_history = True
            st.rerun()
        
        # Debug: Add test message
        if st.button("🧪 Test Message"):
            test_message = f"Test message from {username} at {datetime.now().strftime('%H:%M:%S')}"
            messaging_system.add_message(
                sender=username,
                recipient="Test System",
                message=test_message,
                message_type="user",
                channel='support'
            )
            st.success("Test message added!")
            st.rerun()
        
        # Fullscript Integration Info
        st.markdown("---")
        st.subheader("🌿 Fullscript Integration")
        fullscript_prescriptions = prescription_manager.get_fullscript_prescriptions()
        if fullscript_prescriptions:
            st.write(f"**Active Supplements:** {len(fullscript_prescriptions)}")
            st.write("📱 **Fullscript App Available**")
            if st.button("Open Fullscript App"):
                st.success("Opening Fullscript app...")
        else:
            st.write("No Fullscript prescriptions yet")
            st.info("💡 Add supplements through Fullscript for enhanced wellness tracking!")
        
        # Debug info
        with st.expander("🔧 Debug Info"):
            st.write(f"**Total Messages:** {len(messaging_system.messages)}")
            st.write(f"**Conversations:** {list(messaging_system.conversations.keys())}")
            st.write(f"**User Plan:** {st.session_state.user_plan}")
            st.write(f"**Username:** {st.session_state.user_data.get('username', 'None')}")
            
            if messaging_system.messages:
                st.write("**Recent Messages:**")
                for msg in messaging_system.messages[-3:]:
                    st.write(f"- {msg['sender']} → {msg['recipient']}: {msg['message'][:50]}...")
        
        if st.button("🚪 Logout"):
            logout_user()
            st.rerun()
    
    # Messaging Interface
    if st.session_state.get('show_messaging', False):
        st.subheader("💬 Send Message")
        
        # Message channel selection
        if st.session_state.user_plan in ['premium', 'elite']:
            channel_options = ["Concierge", "AI Agent", "Support"]
        else:
            channel_options = ["Support", "AI Agent"]
        
        selected_channel = st.selectbox("Send to:", channel_options)
        
        # Message type selection
        message_types = {
            "Concierge": ["General Question", "Urgent Request", "Service Request", "Feedback"],
            "AI Agent": ["Expense Help", "Travel Planning", "Medical Reminder", "Insurance Question", "Tax Assistance"],
            "Support": ["Technical Issue", "Account Question", "Billing Inquiry", "Feature Request"]
        }
        
        message_type = st.selectbox("Message Type:", message_types.get(selected_channel, ["General"]))
        
        # Message content
        message_content = st.text_area("Your Message:", placeholder="Type your message here...", height=100)
        
        # Priority selection for Premium/Elite
        if st.session_state.user_plan in ['premium', 'elite']:
            priority = st.selectbox("Priority:", ["Normal", "High", "Urgent"])
        else:
            priority = "Normal"
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📤 Send Message", key="send_message_btn"):
                if message_content.strip():
                    try:
                        # Determine recipient
                        if selected_channel == "Concierge":
                            recipient = st.session_state.user_data.get('concierge_name', 'Concierge Team')
                            channel = 'concierge'
                        elif selected_channel == "AI Agent":
                            recipient = "AI Assistant"
                            channel = 'ai_agent'
                        else:
                            recipient = "Support Team"
                            channel = 'support'
                        
                        # Add message
                        message_id = messaging_system.add_message(
                            sender=st.session_state.user_data['username'],
                            recipient=recipient,
                            message=message_content,
                            message_type="user",
                            channel=channel
                        )
                        
                        st.success(f"✅ Message sent to {recipient}!")
                        
                        # Generate AI response if AI Agent
                        if selected_channel == "AI Agent":
                            ai_response = messaging_system.generate_ai_response(
                                message_content, 
                                st.session_state.user_plan
                            )
                            messaging_system.add_message(
                                sender="AI Assistant",
                                recipient=st.session_state.user_data['username'],
                                message=ai_response,
                                message_type="ai_agent",
                                channel='ai_agent'
                            )
                            st.info(f"🤖 AI Response: {ai_response}")
                        
                        # Simulate concierge response for Premium/Elite
                        elif selected_channel == "Concierge" and st.session_state.user_plan in ['premium', 'elite']:
                            concierge_responses = [
                                "Thank you for your message. I'll handle this personally and get back to you within the hour.",
                                "I've received your request and will prioritize this for you. Expect an update soon.",
                                "I'm working on this right now and will provide you with a detailed response shortly."
                            ]
                            concierge_response = random.choice(concierge_responses)
                            messaging_system.add_message(
                                sender=st.session_state.user_data.get('concierge_name', 'Your Concierge'),
                                recipient=st.session_state.user_data['username'],
                                message=concierge_response,
                                message_type="concierge",
                                channel='concierge'
                            )
                            st.info(f"👩‍💼 {st.session_state.user_data.get('concierge_name', 'Your Concierge')}: {concierge_response}")
                        
                        # Don't close messaging interface, let user send more messages
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error sending message: {str(e)}")
                else:
                    st.error("Please enter a message")
        
        with col2:
            if st.button("❌ Cancel"):
                st.session_state.show_messaging = False
                st.rerun()
        
        with col3:
            if st.button("📋 View Messages"):
                st.session_state.show_message_history = True
                st.rerun()
    
    # Message History Interface
    elif st.session_state.get('show_message_history', False):
        st.subheader("📋 Message History")
        
        # Channel selection for viewing messages
        view_channel = st.selectbox("View Messages From:", ["All", "Concierge", "AI Agent", "Support"])
        
        # Get messages based on selection
        if view_channel == "All":
            all_messages = []
            for channel in ['concierge', 'ai_agent', 'support']:
                all_messages.extend(messaging_system.get_messages(channel))
            messages = sorted(all_messages, key=lambda x: x['timestamp'], reverse=True)
        else:
            channel_map = {"Concierge": "concierge", "AI Agent": "ai_agent", "Support": "support"}
            messages = messaging_system.get_messages(channel_map[view_channel])
        
        # Display messages
        if messages:
            for message in messages[:20]:  # Show last 20 messages
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        sender_emoji = "👤" if message['message_type'] == 'user' else "🤖" if message['message_type'] == 'ai_agent' else "👩‍💼"
                        st.write(f"{sender_emoji} **{message['sender']}**")
                        st.write(message['message'])
                    
                    with col2:
                        st.write(f"📅 {message['timestamp'].strftime('%m/%d %H:%M')}")
                    
                    with col3:
                        if not message['read'] and message['message_type'] != 'user':
                            st.write("🔴 Unread")
                        else:
                            st.write("✅ Read")
                    
                    st.markdown("---")
        else:
            st.info("No messages yet. Send your first message to get started!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💬 New Message"):
                st.session_state.show_message_history = False
                st.session_state.show_messaging = True
                st.rerun()
        
        with col2:
            if st.button("🔙 Back to Dashboard"):
                st.session_state.show_message_history = False
                st.rerun()
    
    # Main content based on plan
    elif st.session_state.user_plan == 'basic':
        st.subheader("🏠 Basic Plan - Essential Life Management")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Services", "3/5 Available")
        with col2:
            st.metric("Monthly Tasks", "10")
        with col3:
            st.metric("Support", "Email")
        
        # Concierge information for Basic plan
        st.subheader("🎯 Your Support Contact")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.write("**📧 Email Support**")
            st.write("support@concierge.com")
            st.write("**Response Time:** 24-48 hours")
        
        with col2:
            st.write("**Basic Plan Features:**")
            st.write("• Self-service tools and dashboards")
            st.write("• Email support for questions")
            st.write("• Basic expense and medical tracking")
            st.write("• Limited travel planning")
            st.write("")
            st.info("💡 **Upgrade to Premium for a dedicated personal concierge who will manage everything for you!**")
        
        # Basic services
        st.subheader("🏠 Your Basic Services")
        
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏥 Health", "📈 Investments", "💰 Expenses", "✈️ Travel", "📞 Contact Support"])
        
        with tab1:
            st.subheader("🏥 Health Management")
            st.write("Track your health and wellness with basic tools")
            
            # Health tabs
            health_tab1, health_tab2, health_tab3 = st.tabs(["📊 Health Metrics", "💊 Prescriptions", "🏥 Appointments"])
            
            with health_tab1:
                # Sample health data
                health_metrics = pd.DataFrame({
                'Metric': ['Weight', 'Steps', 'Sleep Hours', 'Water Intake', 'Exercise'],
                'Current': [165, 8500, 7.5, 6, 3],
                'Target': [160, 10000, 8, 8, 5],
                'Unit': ['lbs', 'steps', 'hours', 'glasses', 'days/week']
                })
                
                fig = px.bar(health_metrics, x='Metric', y='Current', title="Health Metrics")
                st.plotly_chart(fig, use_container_width=True, key="basic_health_metrics_chart")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("BMI", "22.5", "↓ 0.3")
                with col2:
                    st.metric("Weekly Goal", "85% Complete")
            
            with health_tab2:
                st.subheader("💊 Prescription Management")
                
                # Prescription overview
                prescriptions = prescription_manager.get_prescriptions()
                refill_reminders = prescription_manager.get_refill_reminders()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Active Prescriptions", len(prescriptions))
                with col2:
                    st.metric("Due for Refill", len(refill_reminders))
                with col3:
                    urgent_count = len([r for r in refill_reminders if r['urgent']])
                    st.metric("Urgent Refills", urgent_count, delta=f"{urgent_count} urgent" if urgent_count > 0 else None)
                
                # Refill reminders
                if refill_reminders:
                    st.subheader("🔔 Refill Reminders")
                    for reminder in refill_reminders:
                        prescription = reminder['prescription']
                        urgency_color = "🔴" if reminder['urgent'] else "🟡"
                        days_text = f"{reminder['days_until']} days" if reminder['days_until'] > 0 else "OVERDUE"
                        
                        with st.container():
                            col1, col2, col3 = st.columns([3, 1, 1])
                            with col1:
                                st.write(f"{urgency_color} **{prescription['name']}** ({prescription['dosage']})")
                                st.write(f"Pharmacy: {prescription['pharmacy']} | Doctor: {prescription['doctor']}")
                            with col2:
                                st.write(f"**{days_text}**")
                            with col3:
                                if st.button("Request Refill", key=f"refill_{prescription['id']}"):
                                    refill_request = prescription_manager.request_refill(prescription['id'])
                                    if refill_request:
                                        st.success(f"Refill requested! Ready by {refill_request['estimated_ready']}")
                                        st.rerun()
                            st.markdown("---")
                
                # Current prescriptions
                if prescriptions:
                    st.subheader("📋 Current Prescriptions")
                    for prescription in prescriptions:
                        is_fullscript = prescription_manager.is_fullscript_prescription(prescription)
                        icon = "🌿" if is_fullscript else "💊"
                        
                        with st.expander(f"{icon} {prescription['name']} - {prescription['dosage']}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Frequency:** {prescription['frequency']}")
                                st.write(f"**Quantity:** {prescription['quantity']}")
                                st.write(f"**Pharmacy:** {prescription['pharmacy']}")
                                if is_fullscript:
                                    st.write("🌿 **Supplement/Wellness Product**")
                            with col2:
                                st.write(f"**Doctor:** {prescription['doctor']}")
                                st.write(f"**Refills Remaining:** {prescription['refills_remaining']}")
                                st.write(f"**Next Refill Due:** {prescription['next_refill_due']}")
                                if is_fullscript:
                                    st.write("📱 **Fullscript App Available**")
                
                # Add new prescription
                st.subheader("➕ Add New Prescription")
                with st.form("add_prescription"):
                    col1, col2 = st.columns(2)
                    with col1:
                        name = st.text_input("Medication Name")
                        dosage = st.text_input("Dosage (e.g., 10mg)")
                        frequency = st.selectbox("Frequency", ["Once daily", "Twice daily", "Three times daily", "As needed"])
                    with col2:
                        quantity = st.number_input("Quantity", min_value=1, value=30)
                        refill_date = st.date_input("Next Refill Date", value=datetime.now().date() + timedelta(days=30))
                        pharmacy = st.selectbox("Pharmacy", ["CVS Pharmacy", "Walgreens", "Rite Aid", "Local Pharmacy", "Fullscript"])
                    
                    doctor = st.text_input("Prescribing Doctor")
                    
                    if st.form_submit_button("Add Prescription"):
                        if name and dosage and doctor:
                            prescription_manager.add_prescription(
                                name, dosage, frequency, quantity, 
                                refill_date.strftime('%Y-%m-%d'), pharmacy, doctor
                            )
                            st.success(f"Prescription for {name} added successfully!")
                            st.rerun()
                        else:
                            st.error("Please fill in all required fields")
            
            with health_tab3:
                st.subheader("🏥 Medical Appointments")
                st.write("Track your upcoming medical appointments")
                
                # Sample appointments
                appointments = pd.DataFrame({
                    'Date': ['2024-02-15', '2024-02-20', '2024-03-01'],
                    'Time': ['10:00 AM', '2:30 PM', '9:00 AM'],
                    'Doctor': ['Dr. Smith', 'Dr. Johnson', 'Dr. Williams'],
                    'Type': ['Annual Checkup', 'Dermatology', 'Cardiology'],
                    'Status': ['Scheduled', 'Confirmed', 'Pending']
                })
                
                st.dataframe(appointments, use_container_width=True)
                
                if st.button("Schedule New Appointment"):
                    st.success("Appointment scheduling feature coming soon!")
        
        with tab2:
            st.subheader("📈 Investment Management")
            st.write("Track your investments and portfolio performance with broker integration")
            
            
            # Investment tabs
            inv_tab1, inv_tab2, inv_tab3, inv_tab4 = st.tabs(["📊 Portfolio", "🏦 Broker Accounts", "📈 Performance", "➕ Add Investment"])
            
            with inv_tab1:
                st.subheader("📊 Portfolio Overview")
                
                # Portfolio summary
                portfolio_summary = investment_manager.get_portfolio_summary()
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Value", f"${portfolio_summary['total_value']:,.2f}", f"${portfolio_summary['daily_change']:,.2f}")
                with col2:
                    st.metric("Total Investments", portfolio_summary['total_investments'])
                with col3:
                    st.metric("Active Accounts", portfolio_summary['total_accounts'])
                with col4:
                    st.metric("Daily Change", f"{portfolio_summary['percent_change']}%")
                
                # Current investments
                if investment_manager.investments:
                    st.subheader("💼 Current Investments")
                    inv_data = []
                    for inv in investment_manager.investments:
                        if inv['status'] == 'active':
                            inv_data.append({
                                'Symbol': inv['symbol'],
                                'Name': inv['name'],
                                'Shares': inv['shares'],
                                'Price': f"${inv['price']:.2f}",
                                'Value': f"${inv['current_value']:,.2f}",
                                'Type': inv['investment_type'].title()
                            })
                    
                    if inv_data:
                        inv_df = pd.DataFrame(inv_data)
                        st.dataframe(inv_df, use_container_width=True)
                    else:
                        st.info("No investments found. Add your first investment!")
                else:
                    st.info("No investments found. Add your first investment!")
            
            with inv_tab2:
                st.subheader("🏦 Broker Accounts")
                
                # Available brokers
                st.subheader("🔗 Supported Brokers")
                brokers = investment_manager.get_available_brokers()
                
                col1, col2 = st.columns(2)
                for i, broker_key in enumerate(brokers):
                    broker_info = investment_manager.get_broker_info(broker_key)
                    with col1 if i % 2 == 0 else col2:
                        with st.container():
                            st.write(f"**{broker_info['name']}**")
                            st.write(f"🌐 {broker_info['website']}")
                            st.write(f"💰 Min Deposit: ${broker_info['min_deposit']:,}")
                            st.write(f"💳 {broker_info['commission']}")
                            st.write(f"✨ Features: {', '.join(broker_info['features'])}")
                            if st.button(f"Connect to {broker_info['name']}", key=f"connect_{broker_key}"):
                                st.success(f"Connecting to {broker_info['name']}...")
                            st.divider()
                
                # Add new account
                st.subheader("➕ Add Investment Account")
                with st.form("add_investment_account"):
                    col1, col2 = st.columns(2)
                    with col1:
                        broker_choice = st.selectbox("Select Broker", brokers)
                        account_name = st.text_input("Account Name")
                    with col2:
                        account_type = st.selectbox("Account Type", ["Individual", "Joint", "IRA", "Roth IRA", "401k"])
                        balance = st.number_input("Initial Balance", value=0.0, step=100.0)
                    
                    if st.form_submit_button("Add Account"):
                        if account_name:
                            account = investment_manager.add_investment_account(
                                broker_choice, account_name, account_type, balance
                            )
                            st.success(f"Account '{account_name}' added successfully!")
                            st.rerun()
                        else:
                            st.error("Please enter an account name")
            
            with inv_tab3:
                st.subheader("📈 Performance Analysis")
                
                # Performance data
                performance = investment_manager.get_investment_performance()
                
                # Top performers
                st.subheader("🏆 Top Performers")
                top_performers = performance['top_performers']
                for performer in top_performers:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.write(f"**{performer['symbol']}**")
                    with col2:
                        st.write(performer['name'])
                    with col3:
                        st.write(f"**{performer['return']}%**")
                    with col4:
                        st.write(f"${performer['value']:,}")
                
                # Sector allocation
                st.subheader("🏢 Sector Allocation")
                sector_data = performance['sector_allocation']
                sector_df = pd.DataFrame(list(sector_data.items()), columns=['Sector', 'Percentage'])
                fig_sector = px.pie(sector_df, values='Percentage', names='Sector', title="Sector Allocation")
                st.plotly_chart(fig_sector, use_container_width=True, key="basic_investment_sector_chart")
                
                # Asset allocation
                st.subheader("📊 Asset Allocation")
                asset_data = performance['asset_allocation']
                asset_df = pd.DataFrame(list(asset_data.items()), columns=['Asset Class', 'Percentage'])
                fig_asset = px.bar(asset_df, x='Asset Class', y='Percentage', title="Asset Allocation")
                st.plotly_chart(fig_asset, use_container_width=True, key="basic_investment_asset_chart")
            
            with inv_tab4:
                st.subheader("➕ Add New Investment")
                
                with st.form("add_investment"):
                    col1, col2 = st.columns(2)
                    with col1:
                        symbol = st.text_input("Symbol", placeholder="AAPL")
                        name = st.text_input("Company/Asset Name", placeholder="Apple Inc.")
                        shares = st.number_input("Number of Shares", value=1.0, step=0.1)
                    with col2:
                        price = st.number_input("Price per Share", value=0.0, step=0.01)
                        investment_type = st.selectbox("Investment Type", ["Stock", "ETF", "Bond", "Mutual Fund", "Crypto", "Other"])
                        account_id = st.selectbox("Account", [acc['id'] for acc in investment_manager.accounts if acc['status'] == 'active'])
                    
                    if st.form_submit_button("Add Investment"):
                        if symbol and name and shares and price:
                            investment = investment_manager.add_investment(
                                symbol, name, shares, price, account_id, investment_type
                            )
                            st.success(f"Investment '{symbol}' added successfully!")
                            st.rerun()
                        else:
                            st.error("Please fill in all required fields")
        
        with tab3:
            st.subheader("💰 Expense Management")
            st.write("Track your monthly expenses and get spending insights with popular expense apps")
            
            # Expense tabs
            exp_tab1, exp_tab2, exp_tab3, exp_tab4 = st.tabs(["📊 Overview", "📱 App Integration", "📈 Analytics", "➕ Add Expense"])
            
            with exp_tab1:
                st.subheader("📊 Expense Overview")
                
                # Expense summary
                expense_summary = expense_manager.get_expense_summary()
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Expenses", f"${expense_summary['total_expenses']:,.2f}")
                with col2:
                    st.metric("Budget", f"${expense_summary['total_budgets']:,.2f}")
                with col3:
                    st.metric("Remaining", f"${expense_summary['remaining_budget']:,.2f}")
                with col4:
                    trend = expense_summary['monthly_trend']
                    st.metric("Monthly Trend", f"{trend['change_percent']}%")
                
                # Current expenses
                if expense_manager.expenses:
                    st.subheader("💼 Recent Expenses")
                    exp_data = []
                    for exp in expense_manager.expenses[-10:]:  # Show last 10
                        if exp['status'] == 'active':
                            exp_data.append({
                                'Category': exp['category'],
                                'Amount': f"${exp['amount']:.2f}",
                                'Description': exp['description'],
                                'Date': exp['date'],
                                'Source': exp.get('app_source', 'Manual')
                            })
                    
                    if exp_data:
                        exp_df = pd.DataFrame(exp_data)
                        st.dataframe(exp_df, use_container_width=True)
                    else:
                        st.info("No expenses found. Add your first expense!")
                else:
                    st.info("No expenses found. Add your first expense!")
            
            with exp_tab2:
                st.subheader("📱 Expense App Integration")
                
                # Available expense apps
                st.subheader("🔗 Supported Expense Apps")
                apps = expense_manager.get_available_apps()
                
                # Top-rated apps section
                st.subheader("⭐ Top-Rated Apps")
                top_apps = ['ynab', 'monarch_money', 'money_manager']
                for app_key in top_apps:
                    app_info = expense_manager.get_app_info(app_key)
                    with st.expander(f"🏆 {app_info['name']} - Rating: {app_info['rating']}/5"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Cost:** {app_info['cost']}")
                            st.write(f"**Website:** {app_info['website']}")
                            st.write(f"**Description:** {app_info['description']}")
                        with col2:
                            st.write("**Features:**")
                            for feature in app_info['features']:
                                st.write(f"• {feature}")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button(f"Connect to {app_info['name']}", key=f"connect_{app_key}"):
                                st.success(f"Connecting to {app_info['name']}...")
                        with col2:
                            if st.button(f"Import from {app_info['name']}", key=f"import_{app_key}"):
                                result = expense_manager.sync_with_app(app_key, 'import')
                                st.success(result)
                        with col3:
                            if st.button(f"Export to {app_info['name']}", key=f"export_{app_key}"):
                                result = expense_manager.sync_with_app(app_key, 'export')
                                st.success(result)
                
                # All apps section
                st.subheader("📱 All Available Apps")
                for app_key in apps:
                    if app_key not in top_apps:
                        app_info = expense_manager.get_app_info(app_key)
                        with st.expander(f"{app_info['name']} - Rating: {app_info['rating']}/5"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Cost:** {app_info['cost']}")
                                st.write(f"**Website:** {app_info['website']}")
                            with col2:
                                st.write("**Features:**")
                                for feature in app_info['features']:
                                    st.write(f"• {feature}")
                            
                            if st.button(f"Connect to {app_info['name']}", key=f"connect_all_{app_key}"):
                                st.success(f"Connecting to {app_info['name']}...")
            
            with exp_tab3:
                st.subheader("📈 Expense Analytics")
                
                # Category breakdown
                expense_summary = expense_manager.get_expense_summary()
                if expense_summary['categories']:
                    st.subheader("🏷️ Spending by Category")
                    categories = expense_summary['categories']
                    cat_df = pd.DataFrame(list(categories.items()), columns=['Category', 'Amount'])
                    fig_basic_cat = px.pie(cat_df, values='Amount', names='Category', title="Expense Categories")
                    st.plotly_chart(fig_basic_cat, use_container_width=True, key="basic_expense_categories_chart")
                
                # Monthly trend
                st.subheader("📊 Monthly Trend")
                trend = expense_summary['monthly_trend']
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Current Month", f"${trend['current_month']:,}")
                with col2:
                    st.metric("Last Month", f"${trend['last_month']:,}")
                with col3:
                    st.metric("Projected", f"${trend['projected_monthly']:,}")
                
                # Budget vs Actual
                st.subheader("💰 Budget vs Actual")
                budget_data = pd.DataFrame({
                    'Type': ['Budget', 'Actual'],
                    'Amount': [expense_summary['total_budgets'], expense_summary['total_expenses']]
                })
                fig_basic_budget = px.bar(budget_data, x='Type', y='Amount', title="Budget vs Actual Spending")
                st.plotly_chart(fig_basic_budget, use_container_width=True, key="basic_expense_budget_chart")
            
            with exp_tab4:
                st.subheader("➕ Add New Expense")
                
                with st.form("add_expense"):
                    col1, col2 = st.columns(2)
                    with col1:
                        category = st.selectbox("Category", ["Groceries", "Gas", "Dining", "Utilities", "Entertainment", "Healthcare", "Transportation", "Shopping", "Other"])
                        amount = st.number_input("Amount", value=0.0, step=0.01)
                    with col2:
                        description = st.text_input("Description")
                        date = st.date_input("Date", value=datetime.now().date())
                    
                    app_source = st.selectbox("Source App", ["Manual Entry"] + [expense_manager.get_app_info(app)['name'] for app in apps])
                    
                    if st.form_submit_button("Add Expense"):
                        if amount > 0 and description:
                            expense = expense_manager.add_expense(
                                category, amount, description, date.strftime('%Y-%m-%d'), app_source
                            )
                            st.success(f"Expense '{description}' added successfully!")
                            st.rerun()
                        else:
                            st.error("Please fill in all required fields")
        
        with tab4:
            st.subheader("✈️ Travel Planning")
            st.write("Basic travel planning and booking assistance")
            
            destination = st.text_input("Where would you like to go?")
            dates = st.date_input("Travel dates", value=(datetime.now(), datetime.now() + timedelta(days=7)))
            
            if st.button("Get Travel Options"):
                st.success(f"Searching for trips to {destination}...")
                st.info("💡 Premium users get personalized recommendations and booking assistance!")
        
        with tab5:
            st.subheader("📞 Contact Support")
            st.write("Get help with your Basic plan services")
            
            # Support contact information
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📧 Email Support")
                st.write("**Email:** support@concierge.com")
                st.write("**Response Time:** 24-48 hours")
                st.write("**Best for:** General questions, account issues")
                
                if st.button("📧 Send Email"):
                    st.success("Opening email client...")
            
            with col2:
                st.subheader("💬 Live Chat")
                st.write("**Available:** 9 AM - 5 PM EST")
                st.write("**Best for:** Quick questions, immediate help")
                
                if st.button("💬 Start Chat"):
                    st.success("Connecting to support agent...")
            
            # Support request form
            st.subheader("📝 Submit Support Request")
            issue_type = st.selectbox("What do you need help with?", [
                "Account and billing",
                "Using the expense tracker",
                "Medical appointment scheduling",
                "Travel planning",
                "Technical issues",
                "Other"
            ])
            
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
            description = st.text_area("Describe your issue:", placeholder="Please provide details about what you need help with...")
            
            if st.button("Submit Request"):
                if description:
                    st.success(f"Support request submitted ({priority} priority)")
                    st.info("Our support team will respond within 24-48 hours. For urgent issues, please call our support line.")
                else:
                    st.error("Please describe your issue")
            
            # Upgrade prompt
            st.markdown("---")
            st.subheader("🚀 Upgrade to Premium")
            st.write("Get a dedicated personal concierge who will handle everything for you!")
            st.write("**Premium Benefits:**")
            st.write("• Personal concierge (Sarah Johnson)")
            st.write("• Direct phone and email access")
            st.write("• All 5 services included")
            st.write("• Priority support")
            
            if st.button("🔄 Upgrade to Premium"):
                st.success("Redirecting to upgrade page...")
    
    elif st.session_state.user_plan == 'premium':
        st.subheader("⭐ Premium Plan - Complete Life Management")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Services", "5/5 Available")
        with col2:
            st.metric("Monthly Tasks", "50")
        with col3:
            st.metric("Support", "Priority")
        
        # Personal Concierge Introduction
        st.subheader("🎯 Your Personal Concierge")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.write(f"**{st.session_state.user_data['concierge_name']}**")
            st.write(f"{st.session_state.user_data['concierge_photo']} Your dedicated personal assistant")
            st.write("📞 Available 9 AM - 6 PM EST")
            st.write("📧 24/7 email support")
        
        with col2:
            st.write("**What your concierge does for you:**")
            st.write("• Manages all your appointments and bookings")
            st.write("• Handles insurance claims and paperwork")
            st.write("• Coordinates travel arrangements")
            st.write("• Tracks your expenses and budgets")
            st.write("• Provides personalized recommendations")
            st.write("• Acts as your single point of contact")
        
        # All services for premium users
        st.subheader("🏆 Your Premium Services")
        
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["🏥 Health", "📈 Investments", "💰 Expenses", "🛡️ Insurance", "⚖️ Legal", "📊 Taxes", "✈️ Travel", "🤖 AI Insights"])
        
        with tab1:
            st.subheader("🏥 Advanced Health Management")
            st.write("Comprehensive health tracking with AI insights")
            
            # Health management tabs
            premium_health_tab1, premium_health_tab2, premium_health_tab3, premium_health_tab4 = st.tabs(["📊 Health Metrics", "💊 Prescriptions", "🏥 Appointments", "🤖 AI Health Insights"])
            
            with premium_health_tab1:
                # Advanced health tracking
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("BMI", "22.5", "↓ 0.3")
                    st.metric("Weekly Steps", "58,500", "↑ 12%")
                    st.metric("Sleep Score", "8.2/10")
                with col2:
                    st.metric("Exercise Days", "5/7", "↑ 2 days")
                    st.metric("Water Intake", "6.5L", "↑ 0.5L")
                    st.metric("AI Insights", "3 recommendations")
            
                # Health trends
                dates = pd.date_range('2024-01-01', periods=30, freq='D')
                steps = np.random.randn(30).cumsum() * 200 + 8000
                df = pd.DataFrame({'Date': dates, 'Steps': steps})
                fig = px.line(df, x='Date', y='Steps', title="Daily Steps Trend")
                st.plotly_chart(fig, use_container_width=True, key="premium_health_steps_chart")
            
            with premium_health_tab2:
                st.subheader("💊 Advanced Prescription Management")
                
                # Prescription overview with AI insights
                prescriptions = prescription_manager.get_prescriptions()
                refill_reminders = prescription_manager.get_refill_reminders()
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Active Prescriptions", len(prescriptions))
                with col2:
                    st.metric("Due for Refill", len(refill_reminders))
                with col3:
                    urgent_count = len([r for r in refill_reminders if r['urgent']])
                    st.metric("Urgent Refills", urgent_count, delta=f"{urgent_count} urgent" if urgent_count > 0 else None)
                with col4:
                    total_refills = sum(p['refills_remaining'] for p in prescriptions)
                    st.metric("Total Refills Left", total_refills)
                
                # AI-powered refill recommendations
                if refill_reminders:
                    st.subheader("🤖 AI Refill Recommendations")
                    for reminder in refill_reminders:
                        prescription = reminder['prescription']
                        urgency_color = "🔴" if reminder['urgent'] else "🟡"
                        days_text = f"{reminder['days_until']} days" if reminder['days_until'] > 0 else "OVERDUE"
                        
                        with st.container():
                            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                            with col1:
                                st.write(f"{urgency_color} **{prescription['name']}** ({prescription['dosage']})")
                                st.write(f"Pharmacy: {prescription['pharmacy']} | Doctor: {prescription['doctor']}")
                                # AI recommendation
                                if reminder['urgent']:
                                    st.warning("🤖 AI: This prescription is urgent! Consider calling pharmacy directly.")
                                else:
                                    st.info("🤖 AI: You can request refill online or through your concierge.")
                            with col2:
                                st.write(f"**{days_text}**")
                            with col3:
                                if st.button("Request Refill", key=f"premium_refill_{prescription['id']}"):
                                    is_fullscript = prescription_manager.is_fullscript_prescription(prescription)
                                    if is_fullscript:
                                        # Fullscript-specific refill with delivery options
                                        delivery_preference = st.selectbox("Delivery Preference", ["Standard (5-7 days)", "Express (2-3 days)", "Next Day"], key=f"delivery_{prescription['id']}")
                                        refill_request = prescription_manager.request_fullscript_refill(prescription['id'], delivery_preference)
                                    else:
                                        refill_request = prescription_manager.request_refill(prescription['id'])
                                    
                                    if refill_request:
                                        if is_fullscript:
                                            st.success(f"🌿 Fullscript refill requested! Ready by {refill_request['estimated_ready']} ({refill_request['delivery_preference']})")
                                        else:
                                            st.success(f"Refill requested! Ready by {refill_request['estimated_ready']}")
                                        
                                        # Send notification to concierge
                                        messaging_system.add_message(
                                            sender="AI Health Agent",
                                            recipient=st.session_state.user_data.get('concierge_name', 'Concierge Team'),
                                            message=f"Prescription refill requested for {prescription['name']} - {refill_request['pharmacy']}",
                                            message_type="ai_agent",
                                            channel='concierge'
                                        )
                                        st.rerun()
                            with col4:
                                if st.button("Call Pharmacy", key=f"call_{prescription['id']}"):
                                    pharmacy_info = prescription_manager.get_pharmacy_info(prescription['pharmacy'].lower().replace(' ', '_'))
                                    st.success(f"Calling {pharmacy_info.get('name', prescription['pharmacy'])} at {pharmacy_info.get('phone', 'N/A')}")
            st.markdown("---")
            
            # Prescription analytics
            if prescriptions:
                st.subheader("📊 Prescription Analytics")
                
                # Fullscript analytics
                fullscript_analytics = prescription_manager.get_fullscript_analytics()
                if fullscript_analytics:
                    st.subheader("🌿 Fullscript Supplement Analytics")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Supplements", fullscript_analytics['total_supplements'])
                    with col2:
                        st.metric("Monthly Cost", f"${fullscript_analytics['total_cost']}")
                    with col3:
                        st.metric("Adherence Rate", f"{fullscript_analytics['adherence_rate']}%")
                    
                    # Supplement categories
                    if fullscript_analytics['categories']:
                        st.write("**Supplement Categories:**")
                        for category, count in fullscript_analytics['categories'].items():
                            st.write(f"• {category.title()}: {count} supplements")
                
                # Create prescription data for visualization
                prescription_data = []
                for prescription in prescriptions:
                    is_fullscript = prescription_manager.is_fullscript_prescription(prescription)
                    prescription_data.append({
                        'Medication': prescription['name'],
                        'Refills Remaining': prescription['refills_remaining'],
                        'Days Until Refill': (datetime.strptime(prescription['next_refill_due'], '%Y-%m-%d') - datetime.now()).days,
                        'Type': 'Supplement' if is_fullscript else 'Medication'
                    })
                
                if prescription_data:
                    df_prescriptions = pd.DataFrame(prescription_data)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        fig = px.bar(df_prescriptions, x='Medication', y='Refills Remaining', 
                                   title="Refills Remaining by Medication", color='Type')
                        st.plotly_chart(fig, use_container_width=True, key="premium_health_refills_chart")
                    
                    with col2:
                        fig = px.bar(df_prescriptions, x='Medication', y='Days Until Refill', 
                                   title="Days Until Refill", color='Type')
                        st.plotly_chart(fig, use_container_width=True, key="premium_health_days_chart")
                
                # Add new prescription with concierge assistance
                st.subheader("➕ Add New Prescription")
                st.info("💡 Your concierge can help coordinate with your doctor for new prescriptions!")
                
                with st.form("add_premium_prescription"):
                    col1, col2 = st.columns(2)
                    with col1:
                        name = st.text_input("Medication Name")
                        dosage = st.text_input("Dosage (e.g., 10mg)")
                        frequency = st.selectbox("Frequency", ["Once daily", "Twice daily", "Three times daily", "As needed"])
                    with col2:
                        quantity = st.number_input("Quantity", min_value=1, value=30)
                        refill_date = st.date_input("Next Refill Date", value=datetime.now().date() + timedelta(days=30))
                        pharmacy = st.selectbox("Preferred Pharmacy", ["CVS Pharmacy", "Walgreens", "Rite Aid", "Local Pharmacy", "Fullscript"])
                    
                    doctor = st.text_input("Prescribing Doctor")
                    concierge_help = st.checkbox("Ask concierge to coordinate with doctor", key="premium_concierge_help")
                    
                    # Fullscript-specific options
                    if pharmacy == "Fullscript":
                        st.info("🌿 Fullscript Integration: Your concierge can help coordinate supplement prescriptions through the Fullscript platform!")
                        supplement_category = st.selectbox("Supplement Category", ["Vitamins", "Minerals", "Omega-3", "Probiotics", "Herbs", "Protein", "Specialty"])
                        delivery_preference = st.selectbox("Delivery Preference", ["Standard (5-7 days)", "Express (2-3 days)", "Next Day"])
                    
                    if st.form_submit_button("Add Prescription"):
                        if name and dosage and doctor:
                            prescription_manager.add_prescription(
                                name, dosage, frequency, quantity, 
                                refill_date.strftime('%Y-%m-%d'), pharmacy, doctor
                            )
                            st.success(f"Prescription for {name} added successfully!")
                            
                            if concierge_help:
                                # Send message to concierge
                                messaging_system.add_message(
                                    sender=st.session_state.user_data['username'],
                                    recipient=st.session_state.user_data.get('concierge_name', 'Concierge Team'),
                                    message=f"Please coordinate with {doctor} for new prescription: {name} {dosage}",
                                    message_type="user",
                                    channel='concierge'
                                )
                                st.info("Your concierge will coordinate with your doctor!")
                            
                            st.rerun()
                        else:
                            st.error("Please fill in all required fields")
            
            with premium_health_tab3:
                st.subheader("🏥 Medical Appointments")
                st.write("Comprehensive appointment management with concierge coordination")
                
                # Appointment overview
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Upcoming Appointments", "3")
                with col2:
                    st.metric("This Month", "2")
                with col3:
                    st.metric("Concierge Managed", "1")
                
                # Sample appointments with concierge coordination
                appointments = pd.DataFrame({
                    'Date': ['2024-02-15', '2024-02-20', '2024-03-01'],
                    'Time': ['10:00 AM', '2:30 PM', '9:00 AM'],
                    'Doctor': ['Dr. Smith', 'Dr. Johnson', 'Dr. Williams'],
                    'Type': ['Annual Checkup', 'Dermatology', 'Cardiology'],
                    'Status': ['Scheduled', 'Confirmed', 'Pending'],
                    'Concierge': ['Yes', 'No', 'Yes']
                })
                
                st.dataframe(appointments, use_container_width=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Schedule New Appointment"):
                        st.success("Your concierge will coordinate the appointment!")
                with col2:
                    if st.button("Request Concierge Help"):
                        st.success("Concierge assistance requested!")
            
            with premium_health_tab4:
                # AI-Powered Health Insights
                st.subheader("🤖 AI Health Insights")
                
                ai_recommendations = ai_system.generate_ai_recommendations(st.session_state.user_plan, 'medical')
                for i, rec in enumerate(ai_recommendations, 1):
                    st.write(f"{i}. {rec}")
                
                # AI prescription insights
                st.subheader("💊 AI Prescription Insights")
                prescription_insights = [
                    "🤖 AI detected potential drug interaction between your medications",
                    "📊 Your prescription adherence rate is 94% - excellent!",
                    "💡 Consider switching to generic alternatives to save $120/year",
                    "⏰ 2 prescriptions due for refill in the next 5 days"
                ]
                
                for insight in prescription_insights:
                    st.write(insight)
                
                if st.button("🔄 Refresh AI Analysis", key="premium_health_ai"):
                    st.success("AI agents are analyzing your health patterns...")
                    # Simulate AI task completion
                    ai_system.simulate_ai_task('medical_agent', 'Advanced health pattern analysis')
                    st.rerun()
        
        with tab2:
            st.subheader("📈 Advanced Investment Management")
            st.write("Comprehensive portfolio tracking with AI insights and broker integration")
            
            # Premium investment tabs
            premium_inv_tab1, premium_inv_tab2, premium_inv_tab3, premium_inv_tab4 = st.tabs(["📊 Portfolio", "🏦 Broker Integration", "📈 AI Analysis", "🎯 Concierge Services"])
            
            with premium_inv_tab1:
                st.subheader("📊 Advanced Portfolio Overview")
                
                # Portfolio summary with enhanced metrics
                portfolio_summary = investment_manager.get_portfolio_summary()
                col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Value", f"${portfolio_summary['total_value'] + 125000:,.2f}", f"${portfolio_summary['daily_change']:,.2f}")
            with col2:
                st.metric("YTD Return", "15.3%", "↑ 2.1%")
            with col3:
                st.metric("Risk Score", "Moderate", "↓ 0.2")
            with col4:
                st.metric("Diversification", "85%", "↑ 5%")
                
                # Investment trends with AI analysis
            dates = pd.date_range('2024-01-01', periods=30, freq='D')
            portfolio_value = np.random.randn(30).cumsum() * 500 + 120000
            df = pd.DataFrame({'Date': dates, 'Portfolio Value': portfolio_value})
            fig = px.line(df, x='Date', y='Portfolio Value', title="Portfolio Performance with AI Predictions")
            st.plotly_chart(fig, use_container_width=True, key="premium_investment_portfolio_chart")
            
            # Current investments with enhanced data
            if investment_manager.investments:
                    st.subheader("💼 Investment Holdings")
                    inv_data = []
                    for inv in investment_manager.investments:
                        if inv['status'] == 'active':
                            inv_data.append({
                                'Symbol': inv['symbol'],
                                'Name': inv['name'],
                                'Shares': inv['shares'],
                                'Price': f"${inv['price']:.2f}",
                                'Value': f"${inv['current_value']:,.2f}",
                                'Return': f"+{np.random.uniform(5, 25):.1f}%",
                                'Type': inv['investment_type'].title()
                            })
                    
                    if inv_data:
                        inv_df = pd.DataFrame(inv_data)
                        st.dataframe(inv_df, use_container_width=True)
                    else:
                        st.info("No investments found. Add your first investment!")
            
            with premium_inv_tab2:
                st.subheader("🏦 Premium Broker Integration")
                
                # Enhanced broker features for Premium users
                st.subheader("🔗 Premium Broker Services")
                brokers = investment_manager.get_available_brokers()
                
                # Show premium features for each broker
                for broker_key in brokers:
                    broker_info = investment_manager.get_broker_info(broker_key)
                    with st.expander(f"🏆 {broker_info['name']} - Premium Features"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Standard Features:**")
                            st.write(f"• {', '.join(broker_info['features'])}")
                            st.write(f"• Min Deposit: ${broker_info['min_deposit']:,}")
                            st.write(f"• {broker_info['commission']}")
                        with col2:
                            st.write(f"**Premium Features:**")
                            st.write("• Real-time portfolio sync")
                            st.write("• Advanced analytics")
                            st.write("• AI-powered insights")
                            st.write("• Concierge coordination")
                        
                        if st.button(f"Connect Premium Account", key=f"premium_connect_{broker_key}"):
                            st.success(f"Premium connection to {broker_info['name']} initiated!")
                            st.info("Your concierge will coordinate the premium account setup.")
                
                # Premium account management
                st.subheader("💎 Premium Account Management")
                with st.form("premium_account_setup"):
                    col1, col2 = st.columns(2)
                    with col1:
                        broker_choice = st.selectbox("Select Premium Broker", brokers)
                        account_name = st.text_input("Account Name")
                        account_type = st.selectbox("Account Type", ["Individual", "Joint", "IRA", "Roth IRA", "401k", "Trust"])
                    with col2:
                        initial_balance = st.number_input("Initial Balance", value=0.0, step=100.0)
                        concierge_setup = st.checkbox("Have concierge assist with setup")
                        auto_sync = st.checkbox("Enable automatic portfolio sync")
                    
                    if st.form_submit_button("Setup Premium Account"):
                        if account_name:
                            account = investment_manager.add_investment_account(
                                broker_choice, account_name, account_type, initial_balance
                            )
                            st.success(f"Premium account '{account_name}' setup initiated!")
                            if concierge_setup:
                                st.info("Your concierge will contact you to complete the premium account setup.")
                            st.rerun()
                        else:
                            st.error("Please enter an account name")
            
            with premium_inv_tab3:
                st.subheader("📈 AI-Powered Investment Analysis")
                
                # AI investment insights
                st.subheader("🤖 AI Investment Insights")
            ai_recommendations = ai_system.generate_ai_recommendations(st.session_state.user_plan, 'investment')
            for i, rec in enumerate(ai_recommendations, 1):
                st.write(f"{i}. {rec}")
                
                # Advanced performance analysis
                performance = investment_manager.get_investment_performance()
                
                # Top performers with AI analysis
                st.subheader("🏆 AI-Analyzed Top Performers")
                top_performers = performance['top_performers']
                for performer in top_performers:
                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1:
                        st.write(f"**{performer['symbol']}**")
                    with col2:
                        st.write(performer['name'])
                    with col3:
                        st.write(f"**{performer['return']}%**")
                    with col4:
                        st.write(f"${performer['value']:,}")
                    with col5:
                        if performer['return'] > 10:
                            st.write("🟢 Strong Buy")
                        elif performer['return'] > 5:
                            st.write("🟡 Hold")
                        else:
                            st.write("🔴 Review")
                
                # AI-powered sector analysis
                st.subheader("🏢 AI Sector Analysis")
                sector_data = performance['sector_allocation']
                sector_df = pd.DataFrame(list(sector_data.items()), columns=['Sector', 'Percentage'])
                fig_sector = px.pie(sector_df, values='Percentage', names='Sector', title="AI-Optimized Sector Allocation")
                st.plotly_chart(fig_sector, use_container_width=True, key="premium_investment_sector_chart")
                
                # AI recommendations
                st.subheader("💡 AI Investment Recommendations")
                ai_insights = [
                    "🤖 AI suggests increasing technology allocation by 5%",
                    "📊 Consider rebalancing your portfolio for better diversification",
                    "💰 AI detected potential tax-loss harvesting opportunities",
                    "🎯 Your risk tolerance suggests adding more bonds to your portfolio"
                ]
                
                for insight in ai_insights:
                    st.write(insight)
            
            with premium_inv_tab4:
                st.subheader("🎯 Concierge Investment Services")
                
                # Concierge investment services
                st.subheader("👨‍💼 Your Investment Concierge")
                st.write("**Sarah Johnson** - Senior Investment Advisor")
                st.write("📞 +1 (555) 123-4567 | 📧 sarah@concierge.com")
                
                # Concierge services
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("📋 Available Services")
                    concierge_services = [
                        "Portfolio rebalancing",
                        "Tax optimization strategies",
                        "Retirement planning",
                        "Risk assessment",
                        "Investment research",
                        "Market analysis"
                    ]
                    for service in concierge_services:
                        st.write(f"• {service}")
                
                with col2:
                    st.subheader("💬 Contact Your Concierge")
                    if st.button("📞 Schedule Call", key="investment_schedule_call"):
                        st.success("Call scheduled with your investment concierge!")
                    if st.button("📧 Send Message", key="investment_send_message"):
                        st.success("Message sent to your investment concierge!")
                    if st.button("📊 Request Analysis", key="investment_request_analysis"):
                        st.success("Portfolio analysis requested from your concierge!")
                
                # Concierge coordination
                st.subheader("🤝 Concierge Coordination")
                with st.form("concierge_investment_request"):
                    request_type = st.selectbox("Request Type", [
                        "Portfolio Review",
                        "Investment Research",
                        "Tax Optimization",
                        "Market Analysis",
                        "Risk Assessment"
                    ])
                    priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
                    details = st.text_area("Additional Details")
                    
                    if st.form_submit_button("Submit Request"):
                        st.success("Request submitted to your investment concierge!")
                        st.info("Your concierge will respond within 24 hours.")
            
            if st.button("🔄 Refresh AI Analysis", key="investment_ai"):
                st.success("AI agents are analyzing your portfolio...")
                # Simulate AI task completion
                ai_system.simulate_ai_task('investment_agent', 'Portfolio analysis')
                st.rerun()
        
        with tab3:
            st.subheader("💰 Advanced Expense Management")
            st.write("Comprehensive financial tracking with AI insights and popular expense app integration")
            
            # Premium expense tabs
            premium_exp_tab1, premium_exp_tab2, premium_exp_tab3, premium_exp_tab4 = st.tabs(["📊 Overview", "📱 App Integration", "📈 AI Analytics", "🎯 Concierge Services"])
            
            with premium_exp_tab1:
                st.subheader("📊 Advanced Expense Overview")
                
                # Enhanced expense summary
                expense_summary = expense_manager.get_expense_summary()
                col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Monthly Budget", f"${expense_summary['total_budgets']:,.2f}")
            with col2:
                st.metric("Spent This Month", f"${expense_summary['total_expenses']:,.2f}")
            with col3:
                savings_rate = ((expense_summary['total_budgets'] - expense_summary['total_expenses']) / expense_summary['total_budgets'] * 100) if expense_summary['total_budgets'] > 0 else 0
                st.metric("Savings Rate", f"{savings_rate:.1f}%")
            with col4:
                trend = expense_summary['monthly_trend']
                st.metric("Trend", f"{trend['change_percent']}% vs last month")
                
                # Enhanced expense trends
                dates = pd.date_range('2024-01-01', periods=30, freq='D')
                expenses = np.random.randn(30).cumsum() * 50 + 2000
                df = pd.DataFrame({'Date': dates, 'Expenses': expenses})
                fig = px.line(df, x='Date', y='Expenses', title="Daily Expense Trends with AI Predictions")
                st.plotly_chart(fig, use_container_width=True, key="premium_expense_trends_chart")
                
                # Current expenses with app sources
                if expense_manager.expenses:
                    st.subheader("💼 Recent Expenses with App Sources")
                    exp_data = []
                    for exp in expense_manager.expenses[-10:]:
                        if exp['status'] == 'active':
                            exp_data.append({
                                'Category': exp['category'],
                                'Amount': f"${exp['amount']:.2f}",
                                'Description': exp['description'],
                                'Date': exp['date'],
                                'Source': exp.get('app_source', 'Manual'),
                                'Status': '✅ Synced' if exp.get('app_source') != 'Manual' else '📝 Manual'
                            })
                    
                    if exp_data:
                        exp_df = pd.DataFrame(exp_data)
                        st.dataframe(exp_df, use_container_width=True)
                    else:
                        st.info("No expenses found. Add your first expense!")
                else:
                    st.info("No expenses found. Add your first expense!")
            
            with premium_exp_tab2:
                st.subheader("📱 Premium Expense App Integration")
                
                # Premium app features
                st.subheader("🏆 Premium App Features")
                apps = expense_manager.get_available_apps()
                
                # Top-rated apps with premium features
                st.subheader("⭐ Top-Rated Apps with Premium Features")
                top_apps = ['ynab', 'monarch_money', 'expensify']
                for app_key in top_apps:
                    app_info = expense_manager.get_app_info(app_key)
                    with st.expander(f"🏆 {app_info['name']} - Rating: {app_info['rating']}/5"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Cost:** {app_info['cost']}")
                            st.write(f"**Website:** {app_info['website']}")
                            st.write(f"**Description:** {app_info['description']}")
                            st.write("**Premium Features:**")
                            st.write("• Real-time sync with concierge")
                            st.write("• AI-powered categorization")
                            st.write("• Advanced analytics")
                            st.write("• Concierge coordination")
                        with col2:
                            st.write("**Standard Features:**")
                            for feature in app_info['features']:
                                st.write(f"• {feature}")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            if st.button(f"Connect Premium", key=f"premium_connect_{app_key}"):
                                st.success(f"Premium connection to {app_info['name']} initiated!")
                                st.info("Your concierge will coordinate the premium setup.")
                        with col2:
                            if st.button(f"Import Data", key=f"premium_import_{app_key}"):
                                result = expense_manager.sync_with_app(app_key, 'import')
                                st.success(result)
                        with col3:
                            if st.button(f"Export Data", key=f"premium_export_{app_key}"):
                                result = expense_manager.sync_with_app(app_key, 'export')
                                st.success(result)
                        with col4:
                            if st.button(f"AI Analysis", key=f"premium_ai_{app_key}"):
                                st.success(f"AI analysis of {app_info['name']} data requested!")
                
                # All apps with premium integration
                st.subheader("📱 All Apps with Premium Integration")
                for app_key in apps:
                    if app_key not in top_apps:
                        app_info = expense_manager.get_app_info(app_key)
                        with st.expander(f"{app_info['name']} - Rating: {app_info['rating']}/5"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Cost:** {app_info['cost']}")
                                st.write(f"**Website:** {app_info['website']}")
                                st.write("**Premium Features:**")
                                st.write("• Concierge coordination")
                                st.write("• AI insights")
                            with col2:
                                st.write("**Features:**")
                                for feature in app_info['features']:
                                    st.write(f"• {feature}")
                            
                            if st.button(f"Connect Premium", key=f"premium_connect_all_{app_key}"):
                                st.success(f"Premium connection to {app_info['name']} initiated!")
            
            with premium_exp_tab3:
                st.subheader("📈 AI-Powered Expense Analytics")
                
                # AI expense insights
                st.subheader("🤖 AI Expense Insights")
            ai_recommendations = ai_system.generate_ai_recommendations(st.session_state.user_plan, 'expense')
            for i, rec in enumerate(ai_recommendations, 1):
                st.write(f"{i}. {rec}")
                
                # Enhanced analytics
                expense_summary = expense_manager.get_expense_summary()
                
                # Category breakdown with AI insights
                if expense_summary['categories']:
                    st.subheader("🏷️ AI-Optimized Spending Analysis")
                    categories = expense_summary['categories']
                    cat_df = pd.DataFrame(list(categories.items()), columns=['Category', 'Amount'])
                    fig_premium_cat = px.pie(cat_df, values='Amount', names='Category', title="AI-Optimized Expense Categories")
                    st.plotly_chart(fig_premium_cat, use_container_width=True, key="premium_expense_categories_chart")
                
                # AI predictions
                st.subheader("🔮 AI Spending Predictions")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Next Month Prediction", "$3,200", "↑ 5.2%")
                with col2:
                    st.metric("Savings Opportunity", "$450", "↓ 15% dining")
                with col3:
                    st.metric("AI Confidence", "87%", "↑ 3%")
                
                # Budget vs Actual with AI recommendations
                st.subheader("💰 AI Budget Optimization")
                budget_data = pd.DataFrame({
                    'Type': ['Budget', 'Actual', 'AI Recommended'],
                    'Amount': [expense_summary['total_budgets'], expense_summary['total_expenses'], expense_summary['total_budgets'] * 0.95]
                })
                fig_premium_budget = px.bar(budget_data, x='Type', y='Amount', title="Budget vs Actual vs AI Recommendations")
                st.plotly_chart(fig_premium_budget, use_container_width=True, key=f"premium_expense_ai_budget_optimization_chart_{hash(str(datetime.now()))}")
            
            with premium_exp_tab4:
                st.subheader("🎯 Concierge Expense Services")
                
                # Concierge expense services
                st.subheader("👨‍💼 Your Expense Concierge")
                st.write("**Sarah Johnson** - Senior Financial Advisor")
                st.write("📞 +1 (555) 123-4567 | 📧 sarah@concierge.com")
                
                # Concierge services
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("📋 Available Services")
                    concierge_services = [
                        "Expense categorization and optimization",
                        "Budget planning and monitoring",
                        "Subscription management",
                        "Bill negotiation and reduction",
                        "Financial goal tracking",
                        "Tax preparation assistance"
                    ]
                    for service in concierge_services:
                        st.write(f"• {service}")
                
                with col2:
                    st.subheader("💬 Contact Your Concierge")
                    if st.button("📞 Schedule Call", key="expense_schedule_call"):
                        st.success("Call scheduled with your expense concierge!")
                    if st.button("📧 Send Message", key="expense_send_message"):
                        st.success("Message sent to your expense concierge!")
                    if st.button("📊 Request Analysis", key="expense_request_analysis"):
                        st.success("Expense analysis requested from your concierge!")
                
                # Concierge coordination
                st.subheader("🤝 Concierge Coordination")
                with st.form("concierge_expense_request"):
                    request_type = st.selectbox("Request Type", [
                        "Budget Review",
                        "Expense Optimization",
                        "Subscription Audit",
                        "Financial Planning",
                        "Tax Preparation"
                    ])
                    priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
                    details = st.text_area("Additional Details")
                    
                    if st.form_submit_button("Submit Request"):
                        st.success("Request submitted to your expense concierge!")
                        st.info("Your concierge will respond within 24 hours.")
            
            if st.button("🔄 Refresh AI Analysis", key="expense_ai"):
                st.success("AI agents are analyzing your spending patterns...")
                # Simulate AI task completion
                ai_system.simulate_ai_task('expense_agent', 'Expense pattern analysis')
                st.rerun()
        
        with tab4:
            st.subheader("🛡️ Insurance Management")
            st.write("Track and manage all your insurance policies")
            
            # Insurance overview
            insurance_summary = insurance_manager.get_insurance_summary()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Active Policies", insurance_summary['active_policies'])
            with col2:
                st.metric("Total Coverage", f"${insurance_summary['total_coverage']:,}")
            with col3:
                st.metric("Monthly Premium", f"${insurance_summary['total_premiums']:,}")
            
            # Insurance company integration
            st.subheader("🏢 Insurance Company Integration")
            available_companies = insurance_manager.get_available_companies()
            
            for company_key in available_companies:
                company_info = insurance_manager.get_company_info(company_key)
                
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.write(f"**{company_info['name']}**")
                        st.write(f"⭐ Rating: {company_info['rating']}/5.0")
                        st.write(f"📞 {company_info['contact']}")
                        st.write(f"🌐 [Visit Website]({company_info['website']})")
                        
                        # Features
                        features_text = ", ".join(company_info['features'][:3])
                        if len(company_info['features']) > 3:
                            features_text += f" +{len(company_info['features'])-3} more"
                        st.write(f"**Coverage:** {features_text}")
                    
                    with col2:
                        if st.button(f"Connect to {company_info['name']}", key=f"connect_{company_key}"):
                            st.success(f"Connected to {company_info['name']}!")
                    
                    with col3:
                        if st.button(f"Import Data", key=f"import_{company_key}"):
                            result = insurance_manager.sync_with_company(company_key, 'import')
                            st.success(result)
                    
                    st.divider()
            
            # Insurance policies
            st.subheader("📋 Current Policies")
            if insurance_manager.policies:
                policies_data = []
                for policy in insurance_manager.policies:
                    policies_data.append({
                        'Policy Type': policy['policy_type'],
                        'Provider': policy['company'],
                        'Policy Number': policy['policy_number'],
                        'Coverage': f"${policy['coverage_amount']:,}",
                        'Premium': f"${policy['premium']}/month",
                        'Status': policy['status'].title(),
                        'Renewal': policy['renewal_date']
                    })
                
                policies_df = pd.DataFrame(policies_data)
                st.dataframe(policies_df, use_container_width=True)
            else:
                st.info("No policies found. Add a new policy below.")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("File Claim", key="file_claim_basic"):
                    st.success("Claim filing process initiated!")
            with col2:
                if st.button("Compare Rates", key="compare_rates_basic"):
                    st.success("Rate comparison in progress...")
            
            # Add new policy form
            st.subheader("➕ Add New Policy")
            with st.form("add_policy_form"):
                col1, col2 = st.columns(2)
                with col1:
                    company = st.selectbox("Insurance Company", [company_info['name'] for company_info in insurance_manager.insurance_companies.values()])
                    policy_type = st.selectbox("Policy Type", ["Auto Insurance", "Home Insurance", "Life Insurance", "Business Insurance", "Renters Insurance"])
                    policy_number = st.text_input("Policy Number")
                with col2:
                    coverage_amount = st.number_input("Coverage Amount ($)", min_value=0, value=100000)
                    premium = st.number_input("Monthly Premium ($)", min_value=0, value=100)
                    renewal_date = st.date_input("Renewal Date")
                
                if st.form_submit_button("Add Policy"):
                    company_key = next(key for key, info in insurance_manager.insurance_companies.items() if info['name'] == company)
                    policy = insurance_manager.add_policy(company, policy_type, policy_number, coverage_amount, premium, renewal_date.strftime('%Y-%m-%d'))
                    st.success(f"Policy added successfully! Policy ID: {policy['id']}")
                    st.rerun()
            
            # Medical records
            st.subheader("📋 Medical Records")
            records = pd.DataFrame({
                'Date': ['2024-01-15', '2024-01-20', '2024-02-01'],
                'Provider': ['Dr. Smith', 'Lab Corp', 'Dr. Johnson'],
                'Type': ['Annual Physical', 'Blood Work', 'Specialist Visit'],
                'Status': ['Completed', 'Results Ready', 'Scheduled']
            })
            
            st.dataframe(records, use_container_width=True)
        
        with tab5:
            st.subheader("⚖️ Legal Services")
            st.write("Comprehensive legal services and law firm integration")
            
            # Legal overview
            legal_summary = legal_manager.get_legal_summary()
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Active Cases", legal_summary['active_cases'])
            with col2:
                st.metric("Completed Cases", legal_summary['completed_cases'])
            with col3:
                st.metric("Pending Documents", legal_summary['pending_documents'])
            with col4:
                st.metric("Upcoming Appointments", legal_summary['upcoming_appointments'])
            
            # Law firm integration
            st.subheader("🏢 Law Firm Integration")
            available_firms = legal_manager.get_available_firms()
            
            # Categorize firms
            major_firms = ['kirkland_ellis', 'latham_watkins', 'skadden', 'cravath', 'wachtell']
            online_services = ['legal_zoom', 'rocket_lawyer', 'avvo']
            
            st.subheader("🏛️ Major Law Firms")
            for firm_key in major_firms:
                firm_info = legal_manager.get_firm_info(firm_key)
                
                with st.expander(f"{firm_info['name']} - ⭐ {firm_info['rating']}/5"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Founded:** {firm_info['founded']}")
                        st.write(f"**Size:** {firm_info['size']}")
                        st.write(f"**Contact:** {firm_info['contact']}")
                        st.write(f"**Locations:** {', '.join(firm_info['locations'][:3])}")
                        if len(firm_info['locations']) > 3:
                            st.write(f"   +{len(firm_info['locations'])-3} more locations")
                        st.write(f"**Description:** {firm_info['description']}")
                        
                        # Specialties
                        st.write("**Specialties:**")
                        for specialty in firm_info['specialties']:
                            st.write(f"• {specialty}")
                    
                    with col2:
                        if st.button(f"Connect", key=f"connect_legal_{firm_key}"):
                            st.success(f"Connected to {firm_info['name']}!")
                        
                        if st.button(f"Schedule Consultation", key=f"consult_legal_{firm_key}"):
                            st.success(f"Consultation scheduled with {firm_info['name']}!")
                        
                        if st.button(f"Import Cases", key=f"import_legal_{firm_key}"):
                            result = legal_manager.sync_with_firm(firm_key, 'import')
                            st.success(result)
            
            st.subheader("💻 Online Legal Services")
            for firm_key in online_services:
                firm_info = legal_manager.get_firm_info(firm_key)
                
                with st.expander(f"{firm_info['name']} - ⭐ {firm_info['rating']}/5"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Founded:** {firm_info['founded']}")
                        st.write(f"**Type:** {firm_info['size']}")
                        st.write(f"**Contact:** {firm_info['contact']}")
                        st.write(f"**Website:** {firm_info['website']}")
                        st.write(f"**Description:** {firm_info['description']}")
                        
                        # Specialties
                        st.write("**Services:**")
                        for specialty in firm_info['specialties']:
                            st.write(f"• {specialty}")
                    
                    with col2:
                        if st.button(f"Connect", key=f"connect_online_legal_{firm_key}"):
                            st.success(f"Connected to {firm_info['name']}!")
                        
                        if st.button(f"Start Service", key=f"start_legal_{firm_key}"):
                            st.success(f"Service started with {firm_info['name']}!")
                        
                        if st.button(f"Import Data", key=f"import_online_legal_{firm_key}"):
                            result = legal_manager.sync_with_firm(firm_key, 'import')
                            st.success(result)
            
            # Legal cases
            st.subheader("📋 Current Legal Cases")
            if legal_manager.legal_cases:
                cases_data = []
                for case in legal_manager.legal_cases:
                    cases_data.append({
                        'Case ID': case['id'],
                        'Type': case['case_type'],
                        'Description': case['description'][:50] + '...' if len(case['description']) > 50 else case['description'],
                        'Law Firm': case['law_firm'],
                        'Status': case['status'].title(),
                        'Priority': case['priority'].title(),
                        'Created': case['created_date']
                    })
                
                cases_df = pd.DataFrame(cases_data)
                st.dataframe(cases_df, use_container_width=True)
            else:
                st.info("No legal cases found. Add a new case below.")
            
            # Add new legal case
            st.subheader("➕ Add New Legal Case")
            with st.form("add_legal_case_form"):
                col1, col2 = st.columns(2)
                with col1:
                    law_firm = st.selectbox("Law Firm", [firm_info['name'] for firm_info in legal_manager.law_firms.values()])
                    case_type = st.selectbox("Case Type", ["Corporate Law", "Litigation", "Real Estate", "Tax Law", "Family Law", "Criminal Law", "Intellectual Property", "Employment Law", "Other"])
                    description = st.text_area("Case Description", placeholder="Describe your legal case...")
                with col2:
                    status = st.selectbox("Status", ["open", "pending", "closed"])
                    priority = st.selectbox("Priority", ["low", "medium", "high", "urgent"])
                
                if st.form_submit_button("Add Legal Case"):
                    case = legal_manager.add_legal_case(case_type, description, law_firm, status, priority)
                    st.success(f"Legal case added successfully! Case ID: {case['id']}")
                    st.rerun()
        
        with tab6:
            st.subheader("📊 Tax Management & Provider Integration")
            st.write("Professional tax preparation with access to leading tax software")
            
            # Tax dashboard
            tax_summary = tax_manager.get_tax_summary(2024)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Tax Year", "2024")
            with col2:
                st.metric("Documents", f"{tax_summary['documents_collected']}/{tax_summary['total_documents']}")
            with col3:
                st.metric("Deductions", f"${tax_summary['total_deductions']:,.2f}")
            with col4:
                st.metric("Status", tax_summary['filing_status'].replace('_', ' ').title())
            
            # Tax Provider Integration
            st.markdown("---")
            st.subheader("🔗 Tax Software Integration")
            st.write("Connect with leading tax preparation services")
            
            # Display available tax providers
            providers = tax_manager.get_available_providers()
            selected_provider = st.selectbox(
                "Select Tax Provider",
                options=providers,
                format_func=lambda x: tax_manager.get_provider_info(x)['name']
            )
            
            if selected_provider:
                provider_info = tax_manager.get_provider_info(selected_provider)
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**{provider_info['name']}**")
                    st.write(provider_info['description'])
                    st.write(f"⭐ Rating: {provider_info['rating']}/5.0")
                    st.write(f"🌐 Website: {provider_info['website']}")
                    st.write(f"📱 Mobile App: {'Yes' if provider_info['mobile_app'] else 'No'}")
                    st.write(f"💬 Support: {provider_info['customer_support']}")
                
                with col2:
                    st.write("**Pricing:**")
                    for tier, price in provider_info['pricing'].items():
                        st.write(f"• {tier.replace('_', ' ').title()}: {price}")
                
                st.write("**Features:**")
                for feature in provider_info['features']:
                    st.write(f"✓ {feature}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("🔗 Connect", key=f"connect_{selected_provider}"):
                        result = tax_manager.sync_with_provider(selected_provider, 'import')
                        st.success(result)
                with col2:
                    if st.button("📤 Export Data", key=f"export_{selected_provider}"):
                        result = tax_manager.sync_with_provider(selected_provider, 'export')
                        st.success(result)
                with col3:
                    if st.button("🔄 Sync", key=f"sync_{selected_provider}"):
                        result = tax_manager.sync_with_provider(selected_provider, 'sync')
                        st.success(result)
            
            # Tax categories breakdown
            st.markdown("---")
            st.subheader("📊 Tax Categories Breakdown")
            categories = ['W-2 Income', '1099 Income', 'Deductions', 'Credits', 'Other']
            amounts = [45000, 5000, 8000, 2000, 1000]
            fig = px.bar(x=categories, y=amounts, title="Tax Categories for 2024")
            st.plotly_chart(fig, use_container_width=True, key="premium_tax_categories_chart")
            
            # Add tax deduction
            st.markdown("---")
            st.subheader("➕ Add Tax Deduction")
            with st.form("add_tax_deduction"):
                col1, col2 = st.columns(2)
                with col1:
                    deduction_category = st.selectbox("Category", [
                        "Charitable Donations", "Medical Expenses", "Home Office", 
                        "Business Expenses", "Education", "State Taxes", "Other"
                    ])
                    deduction_amount = st.number_input("Amount ($)", min_value=0.0, step=100.0)
                with col2:
                    deduction_desc = st.text_area("Description")
                    tax_year = st.selectbox("Tax Year", [2024, 2023, 2022])
                
                if st.form_submit_button("Add Deduction"):
                    deduction = tax_manager.add_deduction(deduction_category, deduction_desc, deduction_amount, tax_year)
                    st.success(f"Deduction added! Deduction ID: {deduction['id']}")
                    st.rerun()
            
            # Quick actions
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📄 Upload Tax Document", key="upload_tax_doc_premium"):
                    st.info("Document upload feature - Coming soon!")
            with col2:
                if st.button("📅 Schedule CPA Consultation", key="schedule_cpa_premium"):
                    st.success("CPA consultation scheduled!")
        
        with tab7:
            st.subheader("✈️ Premium Travel Planning")
            st.write("Personalized travel planning with concierge booking")
            
            # Travel preferences
            st.subheader("🎯 Your Travel Preferences")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Preferred Airlines:** Delta, United")
                st.write("**Hotel Chains:** Marriott, Hilton")
                st.write("**Seating:** Window, Aisle")
            with col2:
                st.write("**Destinations:** Europe, Asia")
                st.write("**Travel Style:** Business, Leisure")
                st.write("**Budget Range:** $2,000-$5,000")
            
            # Trip planning
            destination = st.text_input("Where would you like to go?")
            dates = st.date_input("Travel dates", value=(datetime.now(), datetime.now() + timedelta(days=7)))
            budget = st.slider("Budget Range", 1000, 10000, 3000)
            
            if st.button("Plan My Trip"):
                st.success(f"Creating personalized itinerary for {destination}...")
                st.info("Your concierge will contact you within 24 hours!")
            
            # AI-Powered Travel Insights
            st.markdown("---")
            st.subheader("🤖 AI Travel Insights")
            
            ai_travel_recs = ai_system.generate_ai_recommendations(st.session_state.user_plan, 'travel')
            for i, rec in enumerate(ai_travel_recs, 1):
                st.write(f"{i}. {rec}")
            
            if st.button("🔄 Refresh Travel AI", key="travel_ai"):
                st.success("AI agents are analyzing travel options...")
                ai_system.simulate_ai_task('travel_agent', 'Travel optimization analysis')
                st.rerun()
        
        with tab7:
            st.subheader("🤖 AI Insights Dashboard")
            st.write("Comprehensive AI analysis across all your services")
            
            # AI Agent Performance
            st.subheader("📊 AI Agent Performance")
            agents = ai_system.get_agent_status()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Active Agents", len([a for a in agents.values() if a['status'] == 'active']))
            with col2:
                st.metric("Total Tasks", sum(a['tasks_completed'] for a in agents.values()))
            with col3:
                st.metric("AI Efficiency", "94%")
            
            # AI Insights by Category
            st.subheader("🔍 AI Insights by Category")
            
            categories = ['expense_patterns', 'travel_preferences', 'health_reminders', 'communication_style']
            selected_category = st.selectbox("Select Category", categories)
            
            insights = ai_system.get_ai_insights(selected_category)
            for insight in insights:
                st.write(f"• {insight}")
            
            # AI Recommendations Summary
            st.subheader("💡 AI Recommendations Summary")
            
            all_recommendations = []
            for service_type in ['expense', 'travel', 'medical', 'insurance', 'tax']:
                recs = ai_system.generate_ai_recommendations(st.session_state.user_plan, service_type)
                all_recommendations.extend(recs[:2])  # Take top 2 from each category
            
            for i, rec in enumerate(all_recommendations[:10], 1):  # Show top 10
                st.write(f"{i}. {rec}")
            
            if st.button("🔄 Refresh All AI Analysis"):
                st.success("All AI agents are updating their analysis...")
                for agent_id in ai_system.agents.keys():
                    ai_system.simulate_ai_task(agent_id, f'Comprehensive {agent_id} analysis')
                st.rerun()
    
    else:  # Elite
        st.subheader("👑 Elite Plan - White-Glove Concierge Service")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Services", "Unlimited")
        with col2:
            st.metric("Monthly Tasks", "Unlimited")
        with col3:
            st.metric("Support", "Dedicated Concierge")
        
        # Elite features
        st.subheader("👑 Your Elite Concierge Services")
        
        # Personal concierge dashboard
        st.subheader("🎯 Your Personal Concierge Dashboard")
        
        # Elite concierge introduction
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.write(f"**{st.session_state.user_data['concierge_name']}**")
            st.write(f"{st.session_state.user_data['concierge_photo']} Your dedicated elite concierge")
            st.write("📞 Available 24/7")
            st.write("📧 Priority response within 1 hour")
            st.write("🏆 White-glove service")
        
        with col2:
            st.write("**Elite concierge services:**")
            st.write("• 24/7 availability and priority support")
            st.write("• Proactive task management and reminders")
            st.write("• Luxury travel and lifestyle coordination")
            st.write("• Personal shopping and gift services")
            st.write("• Home and family management")
            st.write("• Complete life optimization")
            st.write("• Your single point of contact for everything")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Active Tasks", "12")
            st.metric("Completed This Month", "47")
            st.metric("Concierge Rating", "5.0 ⭐")
        with col2:
            st.metric("Next Appointment", "Today 2:00 PM")
            st.metric("Urgent Items", "2")
            st.metric("Savings Generated", "$3,250")
        
        # Elite service tabs
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs(["🏥 Health", "📈 Investments", "💰 Expenses", "🛡️ Insurance", "⚖️ Legal", "📊 Taxes", "✈️ Travel", "🎯 Personal", "💬 Contact Concierge", "🤖 AI Command Center"])
        
        with tab1:
            st.subheader("🏥 Elite Health Management")
            st.write("Complete health oversight with AI-powered insights and optimization")
            
            # Elite health management tabs
            elite_health_tab1, elite_health_tab2, elite_health_tab3, elite_health_tab4, elite_health_tab5 = st.tabs(["📊 Health Overview", "💊 Prescriptions", "🏥 Appointments", "🤖 AI Command Center", "📞 Concierge Health"])
            
            with elite_health_tab1:
                # Health overview
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("BMI", "22.5", "↓ 0.3")
                with col2:
                    st.metric("Weekly Steps", "58,500", "↑ 12%")
                with col3:
                    st.metric("Sleep Score", "8.2/10")
                with col4:
                    st.metric("Health Score", "92/100")
            
            # AI recommendations
            st.subheader("🤖 AI Health Recommendations")
            recommendations = [
                "💡 Increase daily water intake to 8 glasses - improve hydration",
                "📈 Add 30 minutes of cardio 3x/week - boost cardiovascular health",
                "💊 Schedule annual checkup - preventive care is key"
            ]
            
            for rec in recommendations:
                st.write(rec)
            
            with elite_health_tab2:
                st.subheader("💊 Elite Prescription Management")
                st.write("Complete prescription oversight with concierge coordination and AI optimization")
                
                # Elite prescription overview
                prescriptions = prescription_manager.get_prescriptions()
                refill_reminders = prescription_manager.get_refill_reminders()
                
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("Active Prescriptions", len(prescriptions))
                with col2:
                    st.metric("Due for Refill", len(refill_reminders))
                with col3:
                    urgent_count = len([r for r in refill_reminders if r['urgent']])
                    st.metric("Urgent Refills", urgent_count, delta=f"{urgent_count} urgent" if urgent_count > 0 else None)
                with col4:
                    total_refills = sum(p['refills_remaining'] for p in prescriptions)
                    st.metric("Total Refills Left", total_refills)
                with col5:
                    st.metric("Concierge Managed", "3")
                
                # Elite refill management with concierge coordination
                if refill_reminders:
                    st.subheader("🎯 Elite Refill Management")
                    for reminder in refill_reminders:
                        prescription = reminder['prescription']
                        urgency_color = "🔴" if reminder['urgent'] else "🟡"
                        days_text = f"{reminder['days_until']} days" if reminder['days_until'] > 0 else "OVERDUE"
                        
                        with st.container():
                            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
                            with col1:
                                st.write(f"{urgency_color} **{prescription['name']}** ({prescription['dosage']})")
                                st.write(f"Pharmacy: {prescription['pharmacy']} | Doctor: {prescription['doctor']}")
                                # Elite AI recommendation
                                if reminder['urgent']:
                                    st.error("🚨 ELITE AI: This is urgent! Your concierge will handle this immediately.")
                                else:
                                    st.info("🤖 ELITE AI: Your concierge can coordinate this refill for you.")
                            with col2:
                                st.write(f"**{days_text}**")
                            with col3:
                                if st.button("Auto-Refill", key=f"elite_auto_{prescription['id']}"):
                                    # Elite auto-refill with concierge coordination
                                    refill_request = prescription_manager.request_refill(prescription['id'])
                                    if refill_request:
                                        st.success(f"Elite auto-refill initiated! Ready by {refill_request['estimated_ready']}")
                                        # Send urgent message to concierge
                                        messaging_system.add_message(
                                            sender="Elite AI Health Agent",
                                            recipient=st.session_state.user_data.get('concierge_name', 'Elite Concierge'),
                                            message=f"URGENT: Elite auto-refill for {prescription['name']} - coordinate with {prescription['pharmacy']}",
                                            message_type="ai_agent",
                                            channel='concierge'
                                        )
                                        st.rerun()
                            with col4:
                                if st.button("Concierge Handle", key=f"elite_concierge_{prescription['id']}"):
                                    # Send to concierge for full coordination
                                    messaging_system.add_message(
                                        sender=st.session_state.user_data['username'],
                                        recipient=st.session_state.user_data.get('concierge_name', 'Elite Concierge'),
                                        message=f"Please handle prescription refill for {prescription['name']} at {prescription['pharmacy']}",
                                        message_type="user",
                                        channel='concierge'
                                    )
                                    st.success("Your elite concierge will handle this refill!")
                            with col5:
                                if st.button("Call Pharmacy", key=f"elite_call_{prescription['id']}"):
                                    pharmacy_info = prescription_manager.get_pharmacy_info(prescription['pharmacy'].lower().replace(' ', '_'))
                                    st.success(f"Elite concierge calling {pharmacy_info.get('name', prescription['pharmacy'])} at {pharmacy_info.get('phone', 'N/A')}")
                            st.markdown("---")
                
                # Elite prescription analytics and optimization
                if prescriptions:
                    st.subheader("📊 Elite Prescription Analytics")
                    
                    # Advanced prescription analytics
                    prescription_data = []
                    for prescription in prescriptions:
                        prescription_data.append({
                            'Medication': prescription['name'],
                            'Refills Remaining': prescription['refills_remaining'],
                            'Days Until Refill': (datetime.strptime(prescription['next_refill_due'], '%Y-%m-%d') - datetime.now()).days,
                            'Cost': np.random.randint(20, 200),  # Simulated cost data
                            'Adherence': np.random.randint(85, 100)  # Simulated adherence rate
                        })
                    
                    if prescription_data:
                        df_prescriptions = pd.DataFrame(prescription_data)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            fig = px.bar(df_prescriptions, x='Medication', y='Refills Remaining', 
                                       title="Refills Remaining by Medication")
                            st.plotly_chart(fig, use_container_width=True, key="elite_health_refills_chart")
                        
                        with col2:
                            fig = px.bar(df_prescriptions, x='Medication', y='Days Until Refill', 
                                       title="Days Until Refill")
                            st.plotly_chart(fig, use_container_width=True, key="elite_health_days_chart")
                        
                        # Cost optimization
                        st.subheader("💰 Prescription Cost Optimization")
                        total_cost = df_prescriptions['Cost'].sum()
                        potential_savings = total_cost * 0.15  # 15% potential savings
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Monthly Cost", f"${total_cost}")
                        with col2:
                            st.metric("Potential Savings", f"${potential_savings:.0f}")
                        with col3:
                            st.metric("Optimization Score", "85%")
                        
                        if st.button("🔄 Optimize Prescription Costs"):
                            st.success("Elite concierge analyzing cost optimization opportunities...")
                            st.info("Your concierge will contact you with savings recommendations!")
                
                # Elite prescription management
                st.subheader("➕ Elite Prescription Management")
                st.info("🎯 Your elite concierge can coordinate with doctors, pharmacies, and insurance for complete prescription management!")
                
                with st.form("add_elite_prescription"):
                    col1, col2 = st.columns(2)
                    with col1:
                        name = st.text_input("Medication Name")
                        dosage = st.text_input("Dosage (e.g., 10mg)")
                        frequency = st.selectbox("Frequency", ["Once daily", "Twice daily", "Three times daily", "As needed"])
                    with col2:
                        quantity = st.number_input("Quantity", min_value=1, value=30)
                        refill_date = st.date_input("Next Refill Date", value=datetime.now().date() + timedelta(days=30))
                        pharmacy = st.selectbox("Preferred Pharmacy", ["CVS Pharmacy", "Walgreens", "Rite Aid", "Local Pharmacy", "Fullscript"])
                    
                    doctor = st.text_input("Prescribing Doctor")
                    insurance_coverage = st.checkbox("Check insurance coverage", key="elite_insurance_coverage")
                    concierge_coordinate = st.checkbox("Have concierge coordinate with doctor and pharmacy", key="elite_concierge_coordinate")
                    cost_optimization = st.checkbox("Request cost optimization analysis", key="elite_cost_optimization")
                    
                    # Elite Fullscript-specific options
                    if pharmacy == "Fullscript":
                        st.info("🌿 Elite Fullscript Integration: Complete supplement management with concierge coordination!")
                        col1, col2 = st.columns(2)
                        with col1:
                            supplement_category = st.selectbox("Supplement Category", ["Vitamins", "Minerals", "Omega-3", "Probiotics", "Herbs", "Protein", "Specialty"])
                            delivery_preference = st.selectbox("Delivery Preference", ["Standard (5-7 days)", "Express (2-3 days)", "Next Day", "Same Day"])
                        with col2:
                            auto_refill = st.checkbox("Enable Auto-Refill", key="elite_auto_refill")
                            concierge_monitoring = st.checkbox("Concierge Health Monitoring", key="elite_health_monitoring")
                            cost_analysis = st.checkbox("Fullscript Cost Analysis", key="elite_fullscript_cost")
                    
                    if st.form_submit_button("Add Prescription (Elite)"):
                        if name and dosage and doctor:
                            prescription_manager.add_prescription(
                                name, dosage, frequency, quantity, 
                                refill_date.strftime('%Y-%m-%d'), pharmacy, doctor
                            )
                            st.success(f"Elite prescription management initiated for {name}!")
                            
                            # Elite concierge coordination
                            if concierge_coordinate:
                                messaging_system.add_message(
                                    sender=st.session_state.user_data['username'],
                                    recipient=st.session_state.user_data.get('concierge_name', 'Elite Concierge'),
                                    message=f"ELITE REQUEST: Coordinate prescription {name} {dosage} with {doctor} and {pharmacy}",
                                    message_type="user",
                                    channel='concierge'
                                )
                                st.info("Your elite concierge will coordinate everything!")
                            
                            if insurance_coverage:
                                st.info("Insurance coverage verification in progress...")
                            
                            if cost_optimization:
                                st.info("Cost optimization analysis requested...")
                            
                            st.rerun()
                        else:
                            st.error("Please fill in all required fields")
            
            with elite_health_tab3:
                st.subheader("🏥 Elite Medical Appointments")
                st.write("Complete appointment management with elite concierge coordination")
                
                # Elite appointment overview
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Upcoming Appointments", "3")
                with col2:
                    st.metric("This Month", "2")
                with col3:
                    st.metric("Concierge Managed", "3")
                with col4:
                    st.metric("Elite Priority", "1")
                
                # Elite appointments with full concierge coordination
                appointments = pd.DataFrame({
                    'Date': ['2024-02-15', '2024-02-20', '2024-03-01'],
                    'Time': ['10:00 AM', '2:30 PM', '9:00 AM'],
                    'Doctor': ['Dr. Smith', 'Dr. Johnson', 'Dr. Williams'],
                    'Type': ['Annual Checkup', 'Dermatology', 'Cardiology'],
                    'Status': ['Scheduled', 'Confirmed', 'Pending'],
                    'Concierge': ['Yes', 'Yes', 'Yes'],
                    'Priority': ['Normal', 'High', 'Elite']
                })
                
                st.dataframe(appointments, use_container_width=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("Schedule Elite Appointment"):
                        st.success("Your elite concierge will coordinate the appointment with priority scheduling!")
                with col2:
                    if st.button("Request Elite Health Coordination"):
                        st.success("Elite health coordination requested!")
                with col3:
                    if st.button("Emergency Medical Contact"):
                        st.success("Emergency medical contact initiated!")
            
            with elite_health_tab4:
                st.subheader("🤖 Elite AI Health Command Center")
                st.write("Advanced AI-powered health management and optimization")
                
                # AI health command center
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("🚀 Run Full Health AI Analysis"):
                        st.success("Elite AI agents analyzing complete health profile...")
                        for agent_id in ['medical_agent', 'expense_agent']:
                            ai_system.simulate_ai_task(agent_id, f'Elite {agent_id} health analysis')
                        st.rerun()
                
                with col2:
                    if st.button("💊 Optimize Prescription Schedule"):
                        st.success("AI optimizing prescription schedule for maximum effectiveness!")
                
                with col3:
                    if st.button("🏥 Health Risk Assessment"):
                        st.success("Elite AI conducting comprehensive health risk assessment!")
                
                # Elite AI insights
                st.subheader("🧠 Elite AI Health Insights")
                elite_insights = [
                    "🎯 AI optimized your medication schedule for maximum effectiveness",
                    "📊 Detected 3 potential health optimization opportunities",
                    "💰 Prescription cost optimization could save $240/year",
                    "⏰ 2 appointments need rescheduling for optimal health outcomes",
                    "🔍 AI monitoring for potential drug interactions",
                    "📈 Health score trending upward - excellent progress!"
                ]
                
                for insight in elite_insights:
                    st.write(insight)
            
            with elite_health_tab5:
                st.subheader("📞 Elite Concierge Health Services")
                st.write("Direct access to your elite concierge for all health-related needs")
                
                # Elite concierge health services
                st.subheader("🏆 Available Elite Health Services")
                elite_services = [
                    "📞 Direct concierge coordination with doctors and specialists",
                    "💊 Complete prescription management and refill coordination",
                    "🏥 Priority appointment scheduling with top specialists",
                    "💰 Insurance and cost optimization for all health services",
                    "🚨 24/7 emergency health coordination",
                    "📊 Comprehensive health monitoring and reporting",
                    "🎯 Proactive health optimization recommendations",
                    "📱 Real-time health status updates and alerts"
                ]
                
                for service in elite_services:
                    st.write(service)
                
                # Elite health request form
                st.subheader("📝 Elite Health Request")
                health_request_type = st.selectbox("What do you need help with?", [
                    "Schedule specialist appointment",
                    "Coordinate prescription refill",
                    "Insurance coverage verification",
                    "Health cost optimization",
                    "Emergency medical coordination",
                    "Health monitoring setup",
                    "Doctor communication",
                    "Other health service"
                ])
                
                urgent_health = st.checkbox("This is urgent (within 2 hours)", key="elite_urgent_health")
                health_description = st.text_area("Describe your health request:", placeholder="Please provide details about your health needs...")
                
                if st.button("Submit Elite Health Request"):
                    if health_description:
                        priority = "URGENT" if urgent_health else "Elite"
                        
                        # Send to elite concierge
                        messaging_system.add_message(
                            sender=st.session_state.user_data['username'],
                            recipient=st.session_state.user_data.get('concierge_name', 'Elite Concierge'),
                            message=f"ELITE HEALTH REQUEST ({priority}): {health_request_type} - {health_description}",
                            message_type="user",
                            channel='concierge'
                        )
                        
                        st.success(f"Elite health request submitted ({priority} priority)")
                        st.info("Your elite concierge will respond within 1 hour for urgent requests, 4 hours for normal requests.")
                    else:
                        st.error("Please describe your health request")
        
        with tab2:
            st.subheader("📈 Elite Investment Management")
            st.write("Complete investment oversight with AI-powered insights and optimization")
            
            # Elite investment overview
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Portfolio", "$485,000", "↑ 8.2%")
            with col2:
                st.metric("YTD Return", "15.3%")
            with col3:
                st.metric("Risk Score", "Moderate")
            with col4:
                st.metric("Diversification", "92%")
            
            # AI recommendations
            st.subheader("🤖 AI Investment Recommendations")
            recommendations = [
                "💡 Consider rebalancing portfolio - tech stocks overweight by 5%",
                "📈 Add international exposure - currently only 12%",
                "💳 Review bond allocation - interest rate environment changing"
            ]
            
            for rec in recommendations:
                st.write(rec)
        
        with tab3:
            st.subheader("💰 Elite Expense Management")
            st.write("Complete financial oversight with AI-powered insights and optimization")
            
            # Financial overview
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Net Worth", "$485,000", "↑ 8.2%")
            with col2:
                st.metric("Monthly Income", "$12,500")
            with col3:
                st.metric("Monthly Expenses", "$7,200")
            with col4:
                st.metric("Savings Rate", "42%")
            
            # AI recommendations
            st.subheader("🤖 AI Financial Recommendations")
            recommendations = [
                "💡 Consider refinancing your mortgage - potential savings: $200/month",
                "📈 Max out your 401k contribution to save $2,000 in taxes",
                "💳 Switch to a cashback credit card - earn $150 more annually"
            ]
            
            for rec in recommendations:
                st.write(rec)
        
        with tab4:
            st.subheader("🛡️ Elite Insurance Management")
            st.write("Comprehensive insurance optimization and claim management")
            
            # Insurance optimization
            st.subheader("📊 Insurance Optimization Analysis")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Current Premiums", "$755/month")
                st.metric("Potential Savings", "$180/month")
            with col2:
                st.metric("Coverage Score", "92/100")
                st.metric("Risk Assessment", "Low")
            
            if st.button("Optimize Insurance Portfolio"):
                st.success("Insurance optimization analysis complete!")
            
            # Insurance policies
            st.subheader("📋 Insurance Policies")
            policies = pd.DataFrame({
                'Policy Type': ['Auto', 'Home', 'Health', 'Life', 'Disability'],
                'Provider': ['State Farm', 'Allstate', 'Blue Cross', 'Northwestern', 'Aflac'],
                'Premium': ['$120/month', '$85/month', '$450/month', '$75/month', '$25/month'],
                'Next Due': ['2024-02-15', '2024-02-20', '2024-02-01', '2024-02-10', '2024-02-05']
            })
            
            st.dataframe(policies, use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("File Claim"):
                    st.success("Claim filing process initiated!")
            with col2:
                if st.button("Compare Rates"):
                    st.success("Rate comparison in progress...")
        
        with tab5:
            st.subheader("⚖️ Elite Legal Services")
            st.write("Premium legal services with dedicated legal counsel and law firm integration")
            
            # Elite legal overview
            legal_summary = legal_manager.get_legal_summary()
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Active Cases", legal_summary['active_cases'])
            with col2:
                st.metric("Completed Cases", legal_summary['completed_cases'])
            with col3:
                st.metric("Pending Documents", legal_summary['pending_documents'])
            with col4:
                st.metric("Upcoming Appointments", legal_summary['upcoming_appointments'])
            
            # Elite legal counsel
            st.subheader("👨‍⚖️ Your Dedicated Legal Counsel")
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.write("**Robert Thompson, Esq.**")
                st.write("Senior Legal Advisor")
                st.write("📞 +1 (555) 123-4567")
                st.write("📧 robert.thompson@concierge.com")
                st.write("**Bar Admissions:** NY, CA, IL")
                st.write("**Experience:** 20+ years")
            
            with col2:
                st.write("**Elite Legal Services:**")
                st.write("• Dedicated legal counsel available 24/7")
                st.write("• Direct connections to top law firms")
                st.write("• Priority case management")
                st.write("• Document review and preparation")
                st.write("• Contract negotiation support")
                st.write("• Legal strategy consultation")
                st.write("• Litigation support and coordination")
            
            # Law firm integration
            st.subheader("🏢 Premium Law Firm Integration")
            
            # Major law firms
            st.subheader("🏛️ Elite Law Firm Partners")
            major_firms = ['kirkland_ellis', 'latham_watkins', 'skadden', 'cravath', 'wachtell']
            
            for firm_key in major_firms:
                firm_info = legal_manager.get_firm_info(firm_key)
                
                with st.expander(f"{firm_info['name']} - ⭐ {firm_info['rating']}/5"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Founded:** {firm_info['founded']}")
                        st.write(f"**Size:** {firm_info['size']}")
                        st.write(f"**Contact:** {firm_info['contact']}")
                        st.write(f"**Locations:** {', '.join(firm_info['locations'])}")
                        st.write(f"**Description:** {firm_info['description']}")
                        
                        # Specialties
                        st.write("**Specialties:**")
                        for specialty in firm_info['specialties']:
                            st.write(f"• {specialty}")
                        
                        st.write("**Elite Benefits:**")
                        st.write("• Direct partner access")
                        st.write("• Priority scheduling")
                        st.write("• Discounted rates")
                        st.write("• 24/7 support")
                    
                    with col2:
                        if st.button(f"Connect Premium", key=f"connect_elite_legal_{firm_key}"):
                            st.success(f"Premium connection to {firm_info['name']} initiated!")
                        
                        if st.button(f"Schedule Partner Meeting", key=f"partner_elite_legal_{firm_key}"):
                            st.success(f"Partner meeting scheduled with {firm_info['name']}!")
                        
                        if st.button(f"Import Cases", key=f"import_elite_legal_{firm_key}"):
                            result = legal_manager.sync_with_firm(firm_key, 'import')
                            st.success(result)
                        
                        if st.button(f"Request Proposal", key=f"proposal_elite_legal_{firm_key}"):
                            st.success(f"Proposal requested from {firm_info['name']}!")
            
            # Legal cases
            st.subheader("📋 Current Legal Cases")
            if legal_manager.legal_cases:
                cases_data = []
                for case in legal_manager.legal_cases:
                    cases_data.append({
                        'Case ID': case['id'],
                        'Type': case['case_type'],
                        'Description': case['description'][:50] + '...' if len(case['description']) > 50 else case['description'],
                        'Law Firm': case['law_firm'],
                        'Status': case['status'].title(),
                        'Priority': case['priority'].title(),
                        'Created': case['created_date']
                    })
                
                cases_df = pd.DataFrame(cases_data)
                st.dataframe(cases_df, use_container_width=True)
            else:
                st.info("No legal cases found. Add a new case below.")
            
            # Elite legal case management
            st.subheader("➕ Add New Legal Case")
            with st.form("add_elite_legal_case_form"):
                col1, col2 = st.columns(2)
                with col1:
                    law_firm = st.selectbox("Law Firm", [firm_info['name'] for firm_info in legal_manager.law_firms.values()], key="elite_law_firm_select")
                    case_type = st.selectbox("Case Type", ["Corporate Law", "Litigation", "M&A", "Securities", "Real Estate", "Tax Law", "IP Law", "Employment Law", "Banking", "Other"], key="elite_case_type_select")
                    description = st.text_area("Case Description", placeholder="Describe your legal case...", key="elite_case_description")
                with col2:
                    status = st.selectbox("Status", ["open", "pending", "closed"], key="elite_case_status")
                    priority = st.selectbox("Priority", ["low", "medium", "high", "urgent"], key="elite_case_priority")
                    budget = st.number_input("Case Budget ($)", min_value=0, value=10000, key="elite_case_budget")
                
                if st.form_submit_button("Add Elite Legal Case"):
                    case = legal_manager.add_legal_case(case_type, description, law_firm, status, priority)
                    st.success(f"Elite legal case added successfully! Case ID: {case['id']}")
                    st.info("Your dedicated legal counsel will be notified and will contact you within 2 hours.")
                    st.rerun()
        
        with tab6:
            st.subheader("📊 Elite Tax Management & Optimization")
            st.write("Dedicated CPA support with advanced tax optimization strategies")
            
            # Tax optimization dashboard
            tax_summary = tax_manager.get_tax_summary(2024)
            st.subheader("📈 Elite Tax Optimization Dashboard")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("2024 Tax Liability", "$8,450", "-$1,200")
            with col2:
                st.metric("Optimization Savings", "$1,200", "14%")
            with col3:
                st.metric("Total Deductions", f"${tax_summary['total_deductions']:,.2f}")
            with col4:
                st.metric("Documents", f"{tax_summary['documents_collected']}/{tax_summary['total_documents']}")
            
            # Premium Tax Provider Integration
            st.markdown("---")
            st.subheader("🏆 Elite Tax Software Integration")
            st.write("Premium access to professional-grade tax preparation services")
            
            # Display elite tax providers with special benefits
            providers = tax_manager.get_available_providers()
            
            # Create two columns for provider selection
            col1, col2 = st.columns([1, 1])
            with col1:
                selected_provider = st.selectbox(
                    "Select Tax Provider",
                    options=providers,
                    format_func=lambda x: tax_manager.get_provider_info(x)['name'],
                    key="elite_tax_provider_select"
                )
            
            with col2:
                st.info("💎 Elite members receive priority support and dedicated account managers from all providers")
            
            if selected_provider:
                provider_info = tax_manager.get_provider_info(selected_provider)
                
                # Provider details in expandable sections
                with st.expander(f"📋 {provider_info['name']} Details", expanded=True):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"**{provider_info['name']}** - {provider_info['description']}")
                        st.write(f"⭐ Rating: {provider_info['rating']}/5.0")
                        st.write(f"🌐 {provider_info['website']}")
                        st.write(f"📱 Mobile App: {'Available' if provider_info['mobile_app'] else 'Not Available'}")
                        st.write(f"💬 Support: {provider_info['customer_support']}")
                        
                    with col2:
                        st.write("**Pricing Tiers:**")
                        for tier, price in provider_info['pricing'].items():
                            st.write(f"• {tier.replace('_', ' ').title()}")
                            st.write(f"  {price}")
                    
                    st.write("**Premium Features:**")
                    cols = st.columns(2)
                    for idx, feature in enumerate(provider_info['features']):
                        with cols[idx % 2]:
                            st.write(f"✅ {feature}")
                
                # Elite integration actions
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button("🔗 Connect", key=f"elite_connect_{selected_provider}"):
                        result = tax_manager.sync_with_provider(selected_provider, 'import')
                        st.success(result)
                        st.info("Elite priority integration activated")
                with col2:
                    if st.button("📤 Export", key=f"elite_export_{selected_provider}"):
                        result = tax_manager.sync_with_provider(selected_provider, 'export')
                        st.success(result)
                with col3:
                    if st.button("🔄 Sync", key=f"elite_sync_{selected_provider}"):
                        result = tax_manager.sync_with_provider(selected_provider, 'sync')
                        st.success(result)
                with col4:
                    if st.button("📞 Get Support", key=f"elite_support_{selected_provider}"):
                        st.success(f"Dedicated support representative from {provider_info['name']} will contact you within 1 hour")
            
            # Advanced tax strategies
            st.markdown("---")
            st.subheader("💡 AI-Powered Tax Optimization Strategies")
            strategies = [
                {"strategy": "Maximize HSA contributions", "savings": "$1,200", "impact": "High"},
                {"strategy": "Home office deduction optimization", "savings": "$800", "impact": "Medium"},
                {"strategy": "Tax-loss harvesting opportunity", "savings": "$300", "impact": "Medium"},
                {"strategy": "Charitable giving strategy", "savings": "$500", "impact": "Low"},
                {"strategy": "Retirement contribution timing", "savings": "$650", "impact": "High"}
            ]
            
            for idx, strat in enumerate(strategies, 1):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"{idx}. {strat['strategy']}")
                with col2:
                    st.write(f"💰 {strat['savings']}")
                with col3:
                    impact_color = "🔴" if strat['impact'] == "High" else "🟡" if strat['impact'] == "Medium" else "🟢"
                    st.write(f"{impact_color} {strat['impact']}")
            
            # Elite tax deduction management
            st.markdown("---")
            st.subheader("➕ Elite Tax Deduction Tracking")
            with st.form("add_elite_tax_deduction"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    deduction_category = st.selectbox("Category", [
                        "Charitable Donations", "Medical Expenses", "Home Office", 
                        "Business Expenses", "Education", "State Taxes", 
                        "Investment Expenses", "Professional Fees", "Other"
                    ], key="elite_deduction_category")
                    deduction_amount = st.number_input("Amount ($)", min_value=0.0, step=100.0, key="elite_deduction_amount")
                with col2:
                    deduction_desc = st.text_area("Description", key="elite_deduction_desc")
                    tax_year = st.selectbox("Tax Year", [2024, 2023, 2022, 2021], key="elite_tax_year")
                with col3:
                    st.write("**CPA Review:**")
                    cpa_review = st.checkbox("Request CPA review", value=True)
                    st.write("**AI Analysis:**")
                    ai_optimize = st.checkbox("AI optimization analysis", value=True)
                
                if st.form_submit_button("Add Elite Deduction"):
                    deduction = tax_manager.add_deduction(deduction_category, deduction_desc, deduction_amount, tax_year)
                    st.success(f"Deduction added! Deduction ID: {deduction['id']}")
                    if cpa_review:
                        st.info("📞 Your dedicated CPA will review this deduction within 24 hours")
                    if ai_optimize:
                        st.info("🤖 AI analysis: This deduction may qualify for additional tax benefits")
                    st.rerun()
            
            # Elite services
            st.markdown("---")
            st.subheader("🌟 Elite Tax Services")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📞 Dedicated CPA Call", key="elite_cpa_call"):
                    st.success("Your dedicated CPA will call you within 2 hours")
            with col2:
                if st.button("📊 Tax Planning Session", key="elite_tax_planning"):
                    st.success("Year-round tax planning session scheduled!")
            with col3:
                if st.button("🔍 Audit Protection", key="elite_audit_protection"):
                    st.success("Comprehensive audit protection activated")
        
        with tab7:
            st.subheader("✈️ Elite Travel Planning")
            st.write("Luxury travel planning with personal concierge booking")
            
            # Travel preferences and history
            st.subheader("🎯 Your Travel Profile")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Favorite Destinations:** Paris, Tokyo, London")
                st.write("**Travel Style:** Luxury, Business")
                st.write("**Preferred Airlines:** First Class")
            with col2:
                st.write("**Hotel Preferences:** 5-Star, Suite upgrades")
                st.write("**Travel Frequency:** Monthly")
                st.write("**Budget Range:** $5,000-$15,000")
            
            # Elite travel services
            st.subheader("🌟 Elite Travel Services")
            services = [
                "✈️ Private jet arrangements",
                "🏨 Luxury hotel bookings with upgrades",
                "🍽️ Restaurant reservations at exclusive venues",
                "🎭 Event tickets and experiences",
                "🚗 Private transportation and chauffeur services"
            ]
            
            for service in services:
                st.write(service)
        
        with tab7:
            st.subheader("🎯 Personal Concierge Services")
            st.write("White-glove personal assistance for all life needs")
            
            # Personal services
            st.subheader("🏆 Available Personal Services")
            services = [
                "🛒 Grocery shopping and meal planning",
                "🏠 Home maintenance coordination",
                "📅 Calendar management and scheduling",
                "🎁 Gift shopping and wrapping",
                "📞 Phone and email management",
                "🚗 Car maintenance and registration",
                "🐕 Pet care coordination",
                "👶 Childcare arrangements"
            ]
            
            for service in services:
                st.write(service)
            
            # Request new service
            new_service = st.text_input("Request a new service:")
            if st.button("Submit Request"):
                st.success(f"Service request submitted: {new_service}")
                st.info("Your personal concierge will contact you within 2 hours!")
        
        with tab8:
            st.subheader("💬 Contact Your Concierge")
            st.write("Your personal concierge is here to help with anything you need.")
            
            # Contact methods
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📞 Call Your Concierge")
                st.write(f"**Phone:** {st.session_state.user_data['concierge_phone']}")
                st.write("**Hours:** 24/7 (Elite Plan)")
                if st.button("📞 Call Now"):
                    st.success("Connecting you to your concierge...")
            
            with col2:
                st.subheader("📧 Email Your Concierge")
                st.write(f"**Email:** {st.session_state.user_data['concierge_email']}")
                st.write("**Response Time:** Within 1 hour")
                if st.button("📧 Send Email"):
                    st.success("Opening email client...")
            
            # Quick message form
            st.subheader("💬 Send Quick Message")
            message_type = st.selectbox("What do you need help with?", [
                "Schedule an appointment",
                "Book travel",
                "Handle insurance claim",
                "Manage expenses",
                "Tax preparation",
                "Personal errands",
                "Other"
            ])
            
            urgent = st.checkbox("This is urgent (within 2 hours)", key="elite_contact_urgent")
            message = st.text_area("Your message:", placeholder="Describe what you need help with...")
            
            if st.button("Send Message"):
                if message:
                    priority = "URGENT" if urgent else "Normal"
                    
                    # Add message to messaging system
                    message_id = messaging_system.add_message(
                        sender=st.session_state.user_data['username'],
                        recipient=st.session_state.user_data['concierge_name'],
                        message=message,
                        message_type="user",
                        channel='concierge'
                    )
                    
                    # Generate concierge response
                    concierge_responses = [
                        f"Thank you for your {priority.lower()} request. I'm handling this personally and will provide updates within the hour.",
                        f"I've received your {priority.lower()} message and am prioritizing this for you. Expect a detailed response shortly.",
                        f"Your {priority.lower()} request is being processed. I'll have this resolved for you today."
                    ]
                    concierge_response = random.choice(concierge_responses)
                    
                    messaging_system.add_message(
                        sender=st.session_state.user_data['concierge_name'],
                        recipient=st.session_state.user_data['username'],
                        message=concierge_response,
                        message_type="concierge",
                        channel='concierge'
                    )
                    
                    st.success(f"Message sent to {st.session_state.user_data['concierge_name']} ({priority} priority)")
                    st.info(f"👩‍💼 {st.session_state.user_data['concierge_name']}: {concierge_response}")
                    st.info("Your concierge will respond within 1 hour for urgent requests, 4 hours for normal requests.")
                else:
                    st.error("Please enter a message")
            
            # Quick message templates
            st.subheader("💬 Quick Message Templates")
            
            template_col1, template_col2 = st.columns(2)
            
            with template_col1:
                if st.button("📅 Schedule Appointment"):
                    template_message = "I need to schedule an appointment. Please find the best time for me."
                    st.text_area("Message:", value=template_message, key="template1")
                
                if st.button("✈️ Book Travel"):
                    template_message = "I need help booking travel. Please find the best options for me."
                    st.text_area("Message:", value=template_message, key="template2")
            
            with template_col2:
                if st.button("💰 Expense Help"):
                    template_message = "I need help with my expenses. Please review and provide recommendations."
                    st.text_area("Message:", value=template_message, key="template3")
                
                if st.button("🛡️ Insurance Claim"):
                    template_message = "I need help with an insurance claim. Please assist me with the process."
                    st.text_area("Message:", value=template_message, key="template4")
        
        with tab9:
            st.subheader("🤖 AI Command Center")
            st.write("Advanced AI agent management and automation for your elite concierge service")
            
            # AI Agent Control Panel
            st.subheader("🎛️ AI Agent Control Panel")
            
            agents = ai_system.get_agent_status()
            
            # Agent status grid
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("💰 Financial AI")
                st.write(f"Status: {'🟢 Active' if agents['expense_agent']['status'] == 'active' else '🔴 Inactive'}")
                st.write(f"Tasks: {agents['expense_agent']['tasks_completed']}")
                if st.button("Toggle Financial AI", key="toggle_expense"):
                    st.success("Financial AI toggled!")
            
            with col2:
                st.subheader("✈️ Travel AI")
                st.write(f"Status: {'🟢 Active' if agents['travel_agent']['status'] == 'active' else '🔴 Inactive'}")
                st.write(f"Tasks: {agents['travel_agent']['tasks_completed']}")
                if st.button("Toggle Travel AI", key="toggle_travel"):
                    st.success("Travel AI toggled!")
            
            with col3:
                st.subheader("🏥 Medical AI")
                st.write(f"Status: {'🟢 Active' if agents['medical_agent']['status'] == 'active' else '🔴 Inactive'}")
                st.write(f"Tasks: {agents['medical_agent']['tasks_completed']}")
                if st.button("Toggle Medical AI", key="toggle_medical"):
                    st.success("Medical AI toggled!")
            
            # AI Automation Rules
            st.subheader("⚙️ AI Automation Rules")
            
            automation_rules = [
                "🔄 Auto-schedule recurring appointments",
                "📊 Generate monthly expense reports",
                "✈️ Monitor flight price changes",
                "💊 Send medication reminders",
                "📋 Auto-categorize expenses",
                "🎯 Proactive task suggestions"
            ]
            
            for rule in automation_rules:
                st.write(rule)
            
            # AI Performance Analytics
            st.subheader("📈 AI Performance Analytics")
            
            # Simulate AI performance data
            performance_data = pd.DataFrame({
                'Agent': ['Expense AI', 'Travel AI', 'Medical AI', 'Insurance AI', 'Tax AI', 'Communication AI'],
                'Efficiency': [94, 89, 92, 87, 91, 96],
                'Tasks Completed': [47, 23, 31, 18, 25, 52],
                'User Satisfaction': [4.8, 4.6, 4.9, 4.5, 4.7, 4.9]
            })
            
            fig = px.bar(performance_data, x='Agent', y='Efficiency', 
                        title="AI Agent Efficiency Scores", color='Efficiency')
            st.plotly_chart(fig, use_container_width=True, key="elite_ai_agent_chart")
            
            # AI Task Queue
            st.subheader("📋 AI Task Queue")
            
            task_queue = [
                "🔍 Analyzing spending patterns for optimization",
                "✈️ Monitoring flight prices for upcoming trips",
                "📅 Scheduling quarterly tax review",
                "💊 Setting up prescription refill reminders",
                "🛡️ Reviewing insurance coverage gaps",
                "📊 Generating personalized financial insights"
            ]
            
            for i, task in enumerate(task_queue, 1):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(task)
                with col2:
                    st.write("In Progress")
                with col3:
                    if st.button(f"Complete", key=f"complete_{i}"):
                        st.success("Task completed!")
            
            # AI Insights Summary
            st.subheader("🧠 AI Insights Summary")
            
            insights_summary = {
                "Financial Optimization": "AI identified $2,400 annual savings opportunities",
                "Travel Efficiency": "25% cost reduction on business travel through AI optimization",
                "Health Management": "Proactive health monitoring prevented 3 potential issues",
                "Insurance Coverage": "Gap analysis revealed $50K underinsurance in life coverage",
                "Tax Strategy": "AI tax optimization saved $1,200 in current year"
            }
            
            for category, insight in insights_summary.items():
                st.write(f"**{category}:** {insight}")
            
            # AI Agent Commands
            st.subheader("🎯 AI Agent Commands")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🚀 Run Full AI Analysis"):
                    st.success("All AI agents are running comprehensive analysis...")
                    for agent_id in ai_system.agents.keys():
                        ai_system.simulate_ai_task(agent_id, f'Full {agent_id} analysis')
                    st.rerun()
                
                if st.button("📊 Generate AI Report"):
                    st.success("AI comprehensive report generated!")
                    st.info("Report includes: Financial optimization, Travel insights, Health recommendations, Insurance analysis, Tax strategies")
            
            with col2:
                if st.button("🔄 Reset AI Agents"):
                    st.success("All AI agents reset and ready for new tasks!")
                
                if st.button("📈 Optimize AI Performance"):
                    st.success("AI performance optimization completed!")
                    st.info("All agents now running at 98% efficiency")

# Footer
st.markdown("---")
st.markdown("**Concierge.com** - Your Personal Life Management Platform | [Upgrade Plan](mailto:support@concierge.com) | [Support](mailto:help@concierge.com)")

# Hidden admin access for internal staff (only visible in development)
if st.session_state.get('admin_logged_in', False) or st.query_params.get("debug", None) == "true":
    st.markdown("---")
    st.markdown("🔧 **Internal Staff Access:** [Admin Panel](?admin=internal)")
