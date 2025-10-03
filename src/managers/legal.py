"""
Legal Management System
"""
import json
import os
from datetime import datetime
from src.config.constants import DATA_FILES


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
                'specialties': ['Corporate Law', 'Mergers & Acquisitions', 'Securities', 'Litigation', 'Tax Law'],
                'rating': 4.6,
                'description': 'Premier law firm specializing in complex transactions',
                'contact': '+1 (212) 735-3000',
                'locations': ['New York', 'Los Angeles', 'Chicago', 'London', 'Hong Kong'],
                'founded': 1948,
                'size': 'Large Firm (1500+ lawyers)'
            }
        }
        self.load_data()
    
    def load_data(self):
        """Load legal data from storage"""
        try:
            if os.path.exists('legal_data.json'):
                with open('legal_data.json', 'r') as f:
                    data = json.load(f)
                    self.legal_cases = data.get('cases', [])
                    self.documents = data.get('documents', [])
                    self.appointments = data.get('appointments', [])
        except Exception as e:
            print(f"Error loading legal data: {e}")
    
    def save_data(self):
        """Save legal data to storage"""
        try:
            data = {
                'cases': self.legal_cases,
                'documents': self.documents,
                'appointments': self.appointments
            }
            with open('legal_data.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving legal data: {e}")
    
    def add_case(self, case_title, case_type, law_firm, description):
        """Add a new legal case"""
        case = {
            'id': len(self.legal_cases) + 1,
            'title': case_title,
            'type': case_type,
            'law_firm': law_firm,
            'description': description,
            'status': 'active',
            'created_date': datetime.now().strftime('%Y-%m-%d'),
            'last_updated': datetime.now().strftime('%Y-%m-%d')
        }
        self.legal_cases.append(case)
        self.save_data()
        return case
    
    def get_cases(self):
        """Get all active legal cases"""
        return [c for c in self.legal_cases if c['status'] == 'active']
    
    def get_firm_info(self, firm_key):
        """Get law firm information"""
        return self.law_firms.get(firm_key, {})
    
    def get_available_firms(self):
        """Get list of available law firms"""
        return list(self.law_firms.keys())
