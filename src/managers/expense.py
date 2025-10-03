"""
Expense Management System
"""
import json
import os
from datetime import datetime
from src.config.constants import DATA_FILES


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
                'features': ['Subscription tracking', 'Bill negotiation', 'Credit monitoring', 'Budgeting'],
                'cost': 'Free to $12/month',
                'rating': 4.1,
                'description': 'Focuses on subscription management and bill negotiation'
            },
            'mint': {
                'name': 'Mint',
                'website': 'https://www.mint.com',
                'api_available': True,
                'features': ['Budget tracking', 'Bill reminders', 'Credit score', 'Investment tracking'],
                'cost': 'Free',
                'rating': 4.0,
                'description': 'Comprehensive free budgeting and expense tracking'
            }
        }
        self.load_expenses()
    
    def load_expenses(self):
        """Load expenses from storage"""
        try:
            if os.path.exists(DATA_FILES['expenses']):
                with open(DATA_FILES['expenses'], 'r') as f:
                    data = json.load(f)
                    self.expenses = data.get('expenses', [])
                    self.budgets = data.get('budgets', [])
        except Exception as e:
            print(f"Error loading expenses: {e}")
    
    def save_expenses(self):
        """Save expenses to storage"""
        try:
            data = {
                'expenses': self.expenses,
                'budgets': self.budgets
            }
            with open(DATA_FILES['expenses'], 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving expenses: {e}")
    
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
