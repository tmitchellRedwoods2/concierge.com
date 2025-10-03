"""
Pytest configuration and fixtures
"""
import pytest
import tempfile
import os
import json
from unittest.mock import patch, mock_open


@pytest.fixture
def temp_data_file():
    """Create a temporary data file for testing"""
    temp_dir = tempfile.mkdtemp()
    data_file = os.path.join(temp_dir, 'test_data.json')
    yield data_file
    # Cleanup
    if os.path.exists(data_file):
        os.remove(data_file)


@pytest.fixture
def sample_client_data():
    """Sample client data for testing"""
    return {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '555-1234',
        'age': 35,
        'location': 'New York, NY',
        'net_worth': 500000,
        'annual_income': 100000,
        'employment_status': 'Employed',
        'family_size': 2,
        'goals': ['wealth management', 'tax optimization'],
        'selected_services': ['Investment Management', 'Tax Management']
    }


@pytest.fixture
def mock_file_data():
    """Mock JSON data for file operations"""
    return {
        'clients': [
            {
                'id': 'test-id-1',
                'created_date': '2024-01-01 10:00:00',
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'test@example.com'
            }
        ]
    }


@pytest.fixture
def mock_open_file(mock_file_data):
    """Mock file open for testing file operations"""
    with patch('builtins.open', mock_open(read_data=json.dumps(mock_file_data))):
        yield


@pytest.fixture
def mock_file_exists():
    """Mock os.path.exists to return True"""
    with patch('os.path.exists', return_value=True):
        yield


@pytest.fixture
def mock_file_not_exists():
    """Mock os.path.exists to return False"""
    with patch('os.path.exists', return_value=False):
        yield
