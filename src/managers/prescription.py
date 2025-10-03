"""
Prescription Management System
"""
import json
import uuid
import os
from datetime import datetime, timedelta
from src.config.constants import DATA_FILES


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
            if os.path.exists(DATA_FILES['prescriptions']):
                with open(DATA_FILES['prescriptions'], 'r') as f:
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
            with open(DATA_FILES['prescriptions'], 'w') as f:
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
        if not prescription:
            return None
        
        # Use preferred pharmacy or prescription's current pharmacy
        target_pharmacy = pharmacy_preference or prescription['pharmacy']
        
        # Create refill request
        refill_request = {
            'id': str(uuid.uuid4()),
            'prescription_id': prescription_id,
            'pharmacy': target_pharmacy,
            'request_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'estimated_ready': (datetime.now() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M'),
            'status': 'pending'
        }
        
        self.refill_reminders.append(refill_request)
        self.save_prescriptions()
        
        return refill_request
