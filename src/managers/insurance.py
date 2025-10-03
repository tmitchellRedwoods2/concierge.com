"""
Insurance Management System
"""
import json
import os
from datetime import datetime
from src.config.constants import DATA_FILES


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
                'features': ['Auto Insurance', 'Home Insurance', 'Commercial Insurance', 'Motorcycle Insurance', 'RV Insurance'],
                'rating': 4.1,
                'description': 'Progressive makes it easy to compare and save',
                'contact': '1-800-PROGRESSIVE',
                'mobile_app': True,
                'online_portal': True
            }
        }
        self.load_data()
    
    def load_data(self):
        """Load insurance data from storage"""
        try:
            if os.path.exists('insurance_data.json'):
                with open('insurance_data.json', 'r') as f:
                    data = json.load(f)
                    self.policies = data.get('policies', [])
                    self.claims = data.get('claims', [])
        except Exception as e:
            print(f"Error loading insurance data: {e}")
    
    def save_data(self):
        """Save insurance data to storage"""
        try:
            data = {
                'policies': self.policies,
                'claims': self.claims
            }
            with open('insurance_data.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving insurance data: {e}")
    
    def add_policy(self, policy_type, company, policy_number, premium, coverage_amount):
        """Add a new insurance policy"""
        policy = {
            'id': len(self.policies) + 1,
            'type': policy_type,
            'company': company,
            'policy_number': policy_number,
            'premium': premium,
            'coverage_amount': coverage_amount,
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'active'
        }
        self.policies.append(policy)
        self.save_data()
        return policy
    
    def get_policies(self):
        """Get all active policies"""
        return [p for p in self.policies if p['status'] == 'active']
    
    def get_company_info(self, company_key):
        """Get insurance company information"""
        return self.insurance_companies.get(company_key, {})
    
    def get_available_companies(self):
        """Get list of available insurance companies"""
        return list(self.insurance_companies.keys())
