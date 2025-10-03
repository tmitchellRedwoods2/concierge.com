"""
Client Intake Management System
"""
import json
import uuid
import os
from datetime import datetime
from src.config.constants import SERVICE_PRICING, NET_WORTH_MULTIPLIERS, SERVICE_PLANS, DATA_FILES


class ClientIntakeManager:
    def __init__(self):
        self.clients = []
        self.load_client_data()
    
    def load_client_data(self):
        """Load client intake data from storage"""
        try:
            if os.path.exists(DATA_FILES['client_intakes']):
                with open(DATA_FILES['client_intakes'], 'r') as f:
                    data = json.load(f)
                    self.clients = data.get('clients', [])
        except Exception as e:
            print(f"Error loading client data: {e}")
    
    def save_client_data(self):
        """Save client intake data to storage"""
        try:
            data = {'clients': self.clients}
            with open(DATA_FILES['client_intakes'], 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving client data: {e}")
    
    def add_client(self, intake_data):
        """Add a new client intake"""
        client = {
            'id': str(uuid.uuid4()),
            'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            **intake_data
        }
        self.clients.append(client)
        self.save_client_data()
        return client
    
    def calculate_pricing(self, net_worth, selected_services, recommended_plan):
        """Calculate dynamic pricing based on net worth and services"""
        # Base pricing by plan
        base_prices = {
            'basic': 29,
            'premium': 99,
            'elite': 299
        }
        
        base_price = base_prices.get(recommended_plan, 99)
        
        # Net worth multiplier (for premium/elite plans)
        net_worth_multiplier = 1.0
        if net_worth > 10000000:  # $10M+
            net_worth_multiplier = 2.5
        elif net_worth > 5000000:  # $5M+
            net_worth_multiplier = 2.0
        elif net_worth > 2000000:  # $2M+
            net_worth_multiplier = 1.7
        elif net_worth > 1000000:  # $1M+
            net_worth_multiplier = 1.4
        elif net_worth > 500000:  # $500K+
            net_worth_multiplier = 1.2
        
        # Service add-ons
        service_cost = sum(SERVICE_PRICING.get(service, 0) for service in selected_services)
        
        # Calculate final price
        if recommended_plan == 'basic':
            final_price = base_price + service_cost
        else:
            final_price = (base_price * net_worth_multiplier) + service_cost
        
        return {
            'base_price': base_price,
            'net_worth_multiplier': net_worth_multiplier,
            'service_cost': service_cost,
            'monthly_price': round(final_price, 2),
            'annual_price': round(final_price * 12 * 0.85, 2),  # 15% annual discount
            'annual_savings': round(final_price * 12 * 0.15, 2)
        }
    
    def recommend_plan(self, net_worth, goals, selected_services):
        """Recommend appropriate plan based on client profile"""
        # Calculate complexity score
        complexity_score = 0
        
        # Net worth influence
        if net_worth > 2000000:
            complexity_score += 3
        elif net_worth > 500000:
            complexity_score += 2
        elif net_worth > 100000:
            complexity_score += 1
        
        # Goal complexity
        high_value_goals = ['wealth management', 'tax optimization', 'legal planning', 'investment', 'business']
        goal_text = ' '.join(goals).lower()
        for goal in high_value_goals:
            if goal in goal_text:
                complexity_score += 1
        
        # Service count
        if len(selected_services) >= 6:
            complexity_score += 3
        elif len(selected_services) >= 4:
            complexity_score += 2
        elif len(selected_services) >= 2:
            complexity_score += 1
        
        # Premium services check
        premium_services = ['Legal Services', 'Tax Management', 'Investment Management']
        premium_service_count = sum(1 for service in selected_services if service in premium_services)
        if premium_service_count >= 2:
            complexity_score += 2
        
        # Recommend based on score
        if complexity_score >= 7:
            return 'elite', complexity_score
        elif complexity_score >= 4:
            return 'premium', complexity_score
        else:
            return 'basic', complexity_score
    
    def get_plan_features(self, plan):
        """Get features for each plan"""
        return SERVICE_PLANS.get(plan, {}).get('features', [])
