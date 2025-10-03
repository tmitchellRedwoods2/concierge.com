"""
Tax Management System
"""
import json
import os
from datetime import datetime
from src.config.constants import DATA_FILES


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
                'features': ['Federal & State Filing', 'Import W-2s', 'Audit Defense', 'Refund Maximizer', 'Prior Year Import', 'Mobile App'],
                'pricing': {
                    'free': '$0 - Simple returns',
                    'deluxe': '$47 - Homeowners',
                    'premium': '$67 - Investments',
                    'self_employed': '$87 - Business owners'
                },
                'rating': 4.2,
                'description': 'Affordable tax software with good features and customer support',
                'mobile_app': True,
                'integration': True,
                'customer_support': 'Phone & Email'
            }
        }
        self.load_data()
    
    def load_data(self):
        """Load tax data from storage"""
        try:
            if os.path.exists('tax_data.json'):
                with open('tax_data.json', 'r') as f:
                    data = json.load(f)
                    self.tax_documents = data.get('documents', [])
                    self.tax_filings = data.get('filings', [])
                    self.deductions = data.get('deductions', [])
        except Exception as e:
            print(f"Error loading tax data: {e}")
    
    def save_data(self):
        """Save tax data to storage"""
        try:
            data = {
                'documents': self.tax_documents,
                'filings': self.tax_filings,
                'deductions': self.deductions
            }
            with open('tax_data.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving tax data: {e}")
    
    def add_tax_document(self, document_type, provider, amount, description):
        """Add a new tax document"""
        document = {
            'id': len(self.tax_documents) + 1,
            'type': document_type,
            'provider': provider,
            'amount': amount,
            'description': description,
            'created_date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'active'
        }
        self.tax_documents.append(document)
        self.save_data()
        return document
    
    def get_documents(self):
        """Get all active tax documents"""
        return [d for d in self.tax_documents if d['status'] == 'active']
    
    def get_provider_info(self, provider_key):
        """Get tax provider information"""
        return self.tax_providers.get(provider_key, {})
    
    def get_available_providers(self):
        """Get list of available tax providers"""
        return list(self.tax_providers.keys())
