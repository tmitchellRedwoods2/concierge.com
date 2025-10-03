"""
Investment Management System
"""
import json
import os
from datetime import datetime
from src.config.constants import DATA_FILES


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
                'features': ['Low-cost funds', 'ETFs', 'Advisory', 'Retirement'],
                'min_deposit': 1000,
                'commission': 'Low-cost investing'
            }
        }
        self.load_investments()
    
    def load_investments(self):
        """Load investments from storage"""
        try:
            if os.path.exists(DATA_FILES['investments']):
                with open(DATA_FILES['investments'], 'r') as f:
                    data = json.load(f)
                    self.investments = data.get('investments', [])
                    self.accounts = data.get('accounts', [])
        except Exception as e:
            print(f"Error loading investments: {e}")
    
    def save_investments(self):
        """Save investments to storage"""
        try:
            data = {
                'investments': self.investments,
                'accounts': self.accounts
            }
            with open(DATA_FILES['investments'], 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving investments: {e}")
    
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
            'asset_allocation': {
                'Stocks': 70.0,
                'Bonds': 20.0,
                'Cash': 5.0,
                'Alternatives': 5.0
            },
            'sector_allocation': {
                'Technology': 25.3,
                'Healthcare': 20.1,
                'Financial': 15.8,
                'Consumer': 10.5,
                'Industrial': 8.9,
                'Energy': 7.2,
                'Utilities': 5.1,
                'Materials': 4.8,
                'Real Estate': 2.3,
                'Other': 8.4
            },
            'top_performers': [
                {'symbol': 'AAPL', 'name': 'Apple Inc.', 'return': 15.2, 'value': 25000},
                {'symbol': 'MSFT', 'name': 'Microsoft Corp.', 'return': 12.8, 'value': 18000},
                {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'return': 8.5, 'value': 12000}
            ]
        }
