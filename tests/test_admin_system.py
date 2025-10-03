"""
Unit tests for AdminSystem class
"""
import pytest
import sys
sys.path.append('.')

from app import AdminSystem


class TestAdminSystem:
    """Test cases for AdminSystem"""
    
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.admin_system = AdminSystem()
    
    def test_init_admin_users(self):
        """Test that admin users are properly initialized"""
        assert isinstance(self.admin_system.admin_users, dict)
        assert len(self.admin_system.admin_users) > 0
        
        # Check that all admin users have required keys
        for username, user_data in self.admin_system.admin_users.items():
            assert 'password' in user_data
            assert 'role' in user_data
            assert 'name' in user_data
    
    def test_init_system_metrics(self):
        """Test that system metrics are properly initialized"""
        assert isinstance(self.admin_system.system_metrics, dict)
        assert 'total_users' in self.admin_system.system_metrics
        assert 'active_sessions' in self.admin_system.system_metrics
        assert 'messages_sent' in self.admin_system.system_metrics
        assert 'prescriptions_managed' in self.admin_system.system_metrics
        assert 'ai_tasks_completed' in self.admin_system.system_metrics
    
    def test_init_user_sessions(self):
        """Test that user sessions list is properly initialized"""
        assert isinstance(self.admin_system.user_sessions, list)
    
    def test_authenticate_admin_valid(self):
        """Test authenticating valid admin user"""
        result = self.admin_system.authenticate_admin('admin', 'SecureAdmin2024!')
        
        assert result['authenticated'] is True
        assert result['role'] == 'super_admin'
        assert result['name'] == 'System Administrator'
    
    def test_authenticate_admin_invalid_username(self):
        """Test authenticating with invalid username"""
        result = self.admin_system.authenticate_admin('invalid_user', 'password')
        
        assert result['authenticated'] is False
    
    def test_authenticate_admin_invalid_password(self):
        """Test authenticating with invalid password"""
        result = self.admin_system.authenticate_admin('admin', 'wrong_password')
        
        assert result['authenticated'] is False
    
    def test_get_admin_permissions(self):
        """Test getting admin permissions by role"""
        permissions = self.admin_system.get_admin_permissions('super_admin')
        
        assert isinstance(permissions, list)
        assert 'user_management' in permissions
        assert 'system_monitoring' in permissions
        assert 'analytics' in permissions
        assert 'settings' in permissions
        assert 'logs' in permissions
    
    def test_get_admin_permissions_invalid_role(self):
        """Test getting permissions for invalid role"""
        permissions = self.admin_system.get_admin_permissions('invalid_role')
        
        assert permissions == []
    
    def test_get_system_metrics(self):
        """Test getting system metrics"""
        metrics = self.admin_system.get_system_metrics()
        
        assert isinstance(metrics, dict)
        assert 'total_users' in metrics
        assert 'active_sessions' in metrics
        assert 'messages_sent' in metrics
        assert 'prescriptions_managed' in metrics
        assert 'ai_tasks_completed' in metrics
    
    def test_update_metrics(self):
        """Test updating system metrics"""
        initial_value = self.admin_system.system_metrics['total_users']
        
        self.admin_system.update_metrics('total_users', 5)
        
        assert self.admin_system.system_metrics['total_users'] == initial_value + 5
    
    def test_update_metrics_invalid(self):
        """Test updating invalid metric"""
        initial_metrics = self.admin_system.system_metrics.copy()
        
        self.admin_system.update_metrics('invalid_metric', 5)
        
        # Metrics should remain unchanged
        assert self.admin_system.system_metrics == initial_metrics
    
    def test_get_user_analytics(self):
        """Test getting user analytics"""
        analytics = self.admin_system.get_user_analytics()
        
        assert isinstance(analytics, dict)
        assert 'total_users' in analytics
        assert 'active_sessions' in analytics
        assert 'messages_sent' in analytics
        assert 'prescriptions_managed' in analytics
        assert 'ai_tasks_completed' in analytics
    
    def test_get_staff_members(self):
        """Test getting staff members"""
        staff = self.admin_system.get_staff_members()
        
        assert isinstance(staff, dict)
        assert staff == self.admin_system.admin_users
    
    def test_add_staff_member(self):
        """Test adding a staff member"""
        result = self.admin_system.add_staff_member(
            'new_staff', 'password123', 'support', 'New Staff Member'
        )
        
        assert result[0] is True
        assert 'new_staff' in self.admin_system.admin_users
        assert self.admin_system.admin_users['new_staff']['name'] == 'New Staff Member'
        assert self.admin_system.admin_users['new_staff']['role'] == 'support'
    
    def test_add_staff_member_optional_params(self):
        """Test adding staff member with optional parameters"""
        result = self.admin_system.add_staff_member(
            'staff_with_details', 'password123', 'manager', 'Staff Member',
            email='staff@example.com', phone='555-1234', department='Operations'
        )
        
        assert result[0] is True
        assert 'staff_with_details' in self.admin_system.admin_users
    
    def test_get_staff_performance_metrics(self):
        """Test getting staff performance metrics"""
        metrics = self.admin_system.get_staff_performance_metrics()
        
        assert isinstance(metrics, dict)
        assert 'total_staff' in metrics
        assert 'active_staff' in metrics
        assert 'tasks_completed_today' in metrics


if __name__ == '__main__':
    pytest.main([__file__])