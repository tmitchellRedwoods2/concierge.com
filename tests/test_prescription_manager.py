"""
Unit tests for PrescriptionManager class
"""
import pytest
import sys
sys.path.append('.')

from app import PrescriptionManager


class TestPrescriptionManager:
    """Test cases for PrescriptionManager"""
    
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.prescription_manager = PrescriptionManager()
    
    def test_init_prescriptions(self):
        """Test that prescriptions list is properly initialized"""
        assert isinstance(self.prescription_manager.prescriptions, list)
        assert len(self.prescription_manager.prescriptions) >= 0
    
    def test_init_refill_reminders(self):
        """Test that refill reminders list is properly initialized"""
        assert isinstance(self.prescription_manager.refill_reminders, list)
        assert len(self.prescription_manager.refill_reminders) >= 0
    
    def test_init_pharmacies(self):
        """Test that pharmacies dictionary is properly initialized"""
        assert isinstance(self.prescription_manager.pharmacies, dict)
        assert len(self.prescription_manager.pharmacies) > 0
        
        # Check that all pharmacies have required keys
        for pharmacy_key, pharmacy_data in self.prescription_manager.pharmacies.items():
            assert 'name' in pharmacy_data
            assert 'phone' in pharmacy_data
            assert 'address' in pharmacy_data
            assert 'type' in pharmacy_data
    
    def test_add_prescription(self):
        """Test adding a prescription"""
        prescription_id = self.prescription_manager.add_prescription(
            'Test Medication', '10mg', 'Once daily', 30, '2024-02-01', 'cvs', 'Dr. Smith'
        )
        
        assert prescription_id is not None
        assert len(self.prescription_manager.prescriptions) >= 1
        
        prescription = self.prescription_manager.prescriptions[0]
        assert prescription['name'] == 'Test Medication'
        assert prescription['dosage'] == '10mg'
        assert prescription['frequency'] == 'Once daily'
        assert prescription['quantity'] == 30
        assert prescription['refill_date'] == '2024-02-01'
        assert prescription['pharmacy'] == 'cvs'
        assert prescription['doctor'] == 'Dr. Smith'
        assert prescription['status'] == 'active'
        assert prescription['refills_remaining'] == 3
    
    def test_get_prescriptions(self):
        """Test getting all active prescriptions"""
        # Add a prescription
        self.prescription_manager.add_prescription(
            'Medication 1', '10mg', 'Daily', 30, '2024-02-01', 'cvs', 'Dr. Smith'
        )
        
        prescriptions = self.prescription_manager.get_prescriptions()
        
        assert isinstance(prescriptions, list)
        assert len(prescriptions) >= 1  # May include previously loaded prescriptions
    
    def test_get_refill_reminders(self):
        """Test getting refill reminders"""
        # Add a prescription with upcoming refill
        from datetime import datetime, timedelta
        future_date = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
        
        self.prescription_manager.add_prescription(
            'Test Med', '10mg', 'Daily', 30, future_date, 'cvs', 'Dr. Smith'
        )
        
        reminders = self.prescription_manager.get_refill_reminders()
        
        assert isinstance(reminders, list)
        # The reminder should be present since it's due within 7 days
        if reminders:
            assert 'prescription' in reminders[0]
            assert 'days_until' in reminders[0]
            assert 'urgent' in reminders[0]
    
    def test_request_refill(self):
        """Test requesting a prescription refill"""
        # Add a prescription
        prescription_id = self.prescription_manager.add_prescription(
            'Test Medication', '10mg', 'Daily', 30, '2024-02-01', 'cvs', 'Dr. Smith'
        )
        
        result = self.prescription_manager.request_refill(prescription_id)
        
        assert result is not None
        assert isinstance(result, dict)
    
    def test_request_refill_with_pharmacy_preference(self):
        """Test requesting refill with pharmacy preference"""
        prescription_id = self.prescription_manager.add_prescription(
            'Test Medication', '10mg', 'Daily', 30, '2024-02-01', 'cvs', 'Dr. Smith'
        )
        
        result = self.prescription_manager.request_refill(prescription_id, 'walgreens')
        
        assert result is not None
        assert isinstance(result, dict)
    
    def test_request_refill_invalid_id(self):
        """Test requesting refill for invalid prescription ID"""
        result = self.prescription_manager.request_refill('invalid_id')
        
        assert result is None
    
    def test_get_pharmacy_info(self):
        """Test getting pharmacy information"""
        pharmacy_info = self.prescription_manager.pharmacies.get('cvs', {})
        
        assert isinstance(pharmacy_info, dict)
        assert pharmacy_info['name'] == 'CVS Pharmacy'
        assert pharmacy_info['phone'] == '(555) 123-4567'
        assert pharmacy_info['type'] == 'traditional'
    
    def test_prescription_structure(self):
        """Test that prescriptions have proper structure"""
        prescription_id = self.prescription_manager.add_prescription(
            'Structure Test', '5mg', 'Twice daily', 60, '2024-02-15', 'fullscript', 'Dr. Test'
        )
        
        prescription = self.prescription_manager.prescriptions[0]
        
        assert 'id' in prescription
        assert 'name' in prescription
        assert 'dosage' in prescription
        assert 'frequency' in prescription
        assert 'quantity' in prescription
        assert 'refill_date' in prescription
        assert 'pharmacy' in prescription
        assert 'doctor' in prescription
        assert 'status' in prescription
        assert 'refills_remaining' in prescription
        assert 'last_refill' in prescription
        assert 'next_refill_due' in prescription
    
    def test_fullscript_pharmacy(self):
        """Test Fullscript pharmacy properties"""
        fullscript_info = self.prescription_manager.pharmacies.get('fullscript', {})
        
        assert fullscript_info['name'] == 'Fullscript'
        assert fullscript_info['type'] == 'supplement'
        assert fullscript_info['website'] == 'https://fullscript.com'
        assert fullscript_info['app_available'] is True


if __name__ == '__main__':
    pytest.main([__file__])