"""
Admin Management System
"""
import json
import os
from src.config.constants import DEFAULT_ADMIN_USERS, ADMIN_ROLES, DEFAULT_SYSTEM_METRICS, DATA_FILES


class AdminSystem:
    def __init__(self):
        self.admin_users = DEFAULT_ADMIN_USERS.copy()
        self.user_sessions = []
        self.system_metrics = DEFAULT_SYSTEM_METRICS.copy()
        self.load_admin_data()
    
    def load_admin_data(self):
        """Load admin data from storage"""
        try:
            if os.path.exists(DATA_FILES['admin_data']):
                with open(DATA_FILES['admin_data'], 'r') as f:
                    data = json.load(f)
                    self.user_sessions = data.get('user_sessions', [])
                    self.system_metrics = data.get('system_metrics', self.system_metrics)
        except Exception as e:
            print(f"Error loading admin data: {e}")
    
    def save_admin_data(self):
        """Save admin data to storage"""
        try:
            data = {
                'user_sessions': self.user_sessions,
                'system_metrics': self.system_metrics
            }
            with open(DATA_FILES['admin_data'], 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving admin data: {e}")
    
    def authenticate_admin(self, username, password):
        """Authenticate admin user"""
        if username in self.admin_users:
            if self.admin_users[username]['password'] == password:
                return {
                    'authenticated': True,
                    'role': self.admin_users[username]['role'],
                    'name': self.admin_users[username]['name']
                }
        return {'authenticated': False}
    
    def get_admin_permissions(self, role):
        """Get permissions for admin role"""
        return ADMIN_ROLES.get(role, [])
    
    def get_system_metrics(self):
        """Get current system metrics"""
        return self.system_metrics
    
    def update_metrics(self, metric_type, value):
        """Update system metrics"""
        if metric_type in self.system_metrics:
            self.system_metrics[metric_type] += value
            self.save_admin_data()
    
    def get_user_analytics(self):
        """Get user analytics for admin dashboard"""
        return {
            'total_users': self.system_metrics['total_users'],
            'active_sessions': self.system_metrics['active_sessions'],
            'messages_sent': self.system_metrics['messages_sent'],
            'prescriptions_managed': self.system_metrics['prescriptions_managed'],
            'ai_tasks_completed': self.system_metrics['ai_tasks_completed']
        }
    
    def get_staff_members(self):
        """Get all staff members"""
        return self.admin_users
    
    def add_staff_member(self, username, password, role, name, email=None, phone=None, department=None):
        """Add a new staff member"""
        if username in self.admin_users:
            return False, "Username already exists"
        
        self.admin_users[username] = {
            'password': password,
            'role': role,
            'name': name,
            'email': email,
            'phone': phone,
            'department': department
        }
        
        return True, "Staff member added successfully"
    
    def get_staff_performance_metrics(self):
        """Get staff performance metrics"""
        return {
            'total_staff': len(self.admin_users),
            'active_staff': len([u for u in self.admin_users.values() if u.get('status') == 'active']),
            'tasks_completed_today': 156
        }
