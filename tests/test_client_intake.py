"""
Unit tests for ClientIntakeManager class
"""
import pytest
import json
import os
import tempfile
from datetime import datetime
from unittest.mock import patch, mock_open
import sys
sys.path.append('.')

from app import ClientIntakeManager


class TestClientIntakeManager:
    """Test cases for ClientIntakeManager"""
    
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_data_file = os.path.join(self.temp_dir, 'test_client_intakes.json')
        
        # Create manager with test data file
        with patch('app.ClientIntakeManager.__init__', return_value=None):
            self.manager = ClientIntakeManager()
            self.manager.clients = []
            self.manager.data_file = self.test_data_file
    
    def teardown_method(self):
        """Clean up after each test method"""
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)
    
    def test_init_empty_clients_list(self):
        """Test that manager initializes with empty clients list"""
        # Mock the file loading to avoid loading real data
        with patch('os.path.exists', return_value=False):
            manager = ClientIntakeManager()
            assert isinstance(manager.clients, list)
            assert len(manager.clients) == 0
    
    def test_load_client_data_file_not_exists(self):
        """Test loading data when file doesn't exist"""
        # Mock the file loading to avoid loading real data
        with patch('os.path.exists', return_value=False):
            manager = ClientIntakeManager()
            # Should not raise exception when file doesn't exist
            assert len(manager.clients) == 0
    
    def test_load_client_data_valid_file(self):
        """Test loading data from valid JSON file"""
        test_data = {
            'clients': [
                {
                    'id': 'test-id-1',
                    'created_date': '2024-01-01 10:00:00',
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'email': 'john@example.com'
                }
            ]
        }
        
        with patch('builtins.open', mock_open(read_data=json.dumps(test_data))):
            with patch('os.path.exists', return_value=True):
                manager = ClientIntakeManager()
                assert len(manager.clients) == 1
                assert manager.clients[0]['first_name'] == 'John'
    
    def test_load_client_data_invalid_json(self):
        """Test loading data from invalid JSON file"""
        with patch('builtins.open', mock_open(read_data='invalid json')):
            with patch('os.path.exists', return_value=True):
                manager = ClientIntakeManager()
                # Should handle invalid JSON gracefully
                assert len(manager.clients) == 0
    
    def test_add_client(self):
        """Test adding a new client"""
        manager = ClientIntakeManager()
        manager.clients = []
        
        client_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane@example.com',
            'net_worth': 500000
        }
        
        with patch.object(manager, 'save_client_data'):
            client = manager.add_client(client_data)
            
            assert 'id' in client
            assert 'created_date' in client
            assert client['first_name'] == 'Jane'
            assert client['last_name'] == 'Smith'
            assert client['email'] == 'jane@example.com'
            assert client['net_worth'] == 500000
            assert len(manager.clients) == 1
    
    def test_recommend_plan_basic(self):
        """Test plan recommendation for basic tier"""
        manager = ClientIntakeManager()
        
        # Low net worth, simple goals, few services
        net_worth = 50000
        goals = ['health management']
        services = ['Health Management']
        
        plan, score = manager.recommend_plan(net_worth, goals, services)
        
        assert plan == 'basic'
        assert score >= 0
        assert score <= 10
    
    def test_recommend_plan_premium(self):
        """Test plan recommendation for premium tier"""
        manager = ClientIntakeManager()
        
        # Medium net worth, moderate complexity
        net_worth = 500000
        goals = ['wealth management', 'tax optimization']
        services = ['Investment Management', 'Tax Management', 'Health Management']
        
        plan, score = manager.recommend_plan(net_worth, goals, services)
        
        assert plan == 'premium'
        assert score >= 0
        assert score <= 10
    
    def test_recommend_plan_elite(self):
        """Test plan recommendation for elite tier"""
        manager = ClientIntakeManager()
        
        # High net worth, complex goals, many services
        net_worth = 2000000
        goals = ['wealth management', 'tax optimization', 'legal planning', 'business management']
        services = ['Investment Management', 'Tax Management', 'Legal Services', 'Personal Assistant', 'Travel Planning']
        
        plan, score = manager.recommend_plan(net_worth, goals, services)
        
        assert plan == 'elite'
        assert score >= 0
        assert score <= 10
    
    def test_calculate_pricing_basic(self):
        """Test pricing calculation for basic plan"""
        manager = ClientIntakeManager()
        
        net_worth = 100000
        services = ['Health Management', 'Expense Tracking']
        plan = 'basic'
        
        pricing = manager.calculate_pricing(net_worth, services, plan)
        
        assert pricing['base_price'] == 29
        assert pricing['net_worth_multiplier'] == 1.0
        assert pricing['service_cost'] == 35  # 20 + 15
        assert pricing['monthly_price'] == 64  # 29 + 35
        assert pricing['annual_price'] == 652.8  # 64 * 12 * 0.85
        assert pricing['annual_savings'] == 115.2  # 64 * 12 * 0.15
    
    def test_calculate_pricing_premium_high_net_worth(self):
        """Test pricing calculation for premium plan with high net worth"""
        manager = ClientIntakeManager()
        
        net_worth = 1500000  # Changed to match implementation threshold
        services = ['Investment Management', 'Legal Services']
        plan = 'premium'
        
        pricing = manager.calculate_pricing(net_worth, services, plan)
        
        assert pricing['base_price'] == 99
        assert pricing['net_worth_multiplier'] == 1.4
        assert pricing['service_cost'] == 125  # 50 + 75
        assert pricing['monthly_price'] == 263.6  # (99 * 1.4) + 125
        assert pricing['annual_price'] == 2688.72  # 263.6 * 12 * 0.85
        assert pricing['annual_savings'] == 474.48  # 263.6 * 12 * 0.15
    
    def test_calculate_pricing_elite_very_high_net_worth(self):
        """Test pricing calculation for elite plan with very high net worth"""
        manager = ClientIntakeManager()
        
        net_worth = 15000000  # Changed to match implementation threshold
        services = ['Investment Management', 'Legal Services', 'Personal Assistant']
        plan = 'elite'
        
        pricing = manager.calculate_pricing(net_worth, services, plan)
        
        assert pricing['base_price'] == 299
        assert pricing['net_worth_multiplier'] == 2.5
        assert pricing['service_cost'] == 225  # 50 + 75 + 100
        assert pricing['monthly_price'] == 972.5  # (299 * 2.5) + 225
        assert pricing['annual_price'] == 9919.5  # 972.5 * 12 * 0.85
        assert pricing['annual_savings'] == 1750.5  # 972.5 * 12 * 0.15 (rounded)
    
    def test_get_plan_features_basic(self):
        """Test getting features for basic plan"""
        manager = ClientIntakeManager()
        
        features = manager.get_plan_features('basic')
        
        assert len(features) > 0
        assert any('Core service management' in feature for feature in features)
        assert any('Up to 3 services' in feature for feature in features)
        assert any('No AI assistance' in feature for feature in features)
    
    def test_get_plan_features_premium(self):
        """Test getting features for premium plan"""
        manager = ClientIntakeManager()
        
        features = manager.get_plan_features('premium')
        
        assert len(features) > 0
        assert any('AI-powered recommendations' in feature for feature in features)
        assert any('Up to 6 services' in feature for feature in features)
        assert any('Priority support' in feature for feature in features)
    
    def test_get_plan_features_elite(self):
        """Test getting features for elite plan"""
        manager = ClientIntakeManager()
        
        features = manager.get_plan_features('elite')
        
        assert len(features) > 0
        assert any('Dedicated personal concierge' in feature for feature in features)
        assert any('Unlimited services' in feature for feature in features)
        assert any('24/7 priority support' in feature for feature in features)
    
    def test_get_plan_features_invalid(self):
        """Test getting features for invalid plan"""
        manager = ClientIntakeManager()
        
        features = manager.get_plan_features('invalid')
        
        assert features == []
    
    def test_save_client_data(self):
        """Test saving client data to file"""
        manager = ClientIntakeManager()
        manager.clients = [
            {
                'id': 'test-id',
                'created_date': '2024-01-01 10:00:00',
                'first_name': 'Test',
                'last_name': 'User'
            }
        ]
        
        with patch('builtins.open', mock_open()) as mock_file:
            manager.save_client_data()
            
            # Verify file was opened for writing
            mock_file.assert_called_once_with('client_intakes.json', 'w')
            
            # Verify JSON data was written
            written_data = ''.join(call.args[0] for call in mock_file().write.call_args_list)
            parsed_data = json.loads(written_data)
            assert 'clients' in parsed_data
            assert len(parsed_data['clients']) == 1
            assert parsed_data['clients'][0]['first_name'] == 'Test'


if __name__ == '__main__':
    pytest.main([__file__])
