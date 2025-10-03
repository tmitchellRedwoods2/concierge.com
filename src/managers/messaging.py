"""
Messaging System for Concierge Communication
"""
import json
import uuid
import os
from datetime import datetime
from src.config.constants import DATA_FILES


class MessagingSystem:
    def __init__(self):
        self.messages = []
        self.conversations = {}
        self.storage_file = DATA_FILES['chat_history']
        self.load_messages()
        self.ai_responses = {
            'expense': [
                "I've analyzed your spending patterns and found 3 optimization opportunities.",
                "Your dining expenses increased 15% this month. Would you like me to suggest alternatives?",
                "I've identified $200 in potential monthly savings from subscription optimization."
            ],
            'travel': [
                "I found 25% cheaper flights for your upcoming trip to Paris.",
                "Your preferred hotel has a special rate available. Should I book it?",
                "I've optimized your travel itinerary to save 3 hours of travel time."
            ],
            'medical': [
                "Your annual checkup is due next month. I've scheduled it for Tuesday at 2 PM.",
                "I've set up prescription refill reminders for your medications.",
                "Your insurance claim for $450 has been approved and processed.",
                "I've identified 2 prescriptions due for refill in the next 5 days.",
                "Your prescription adherence rate is excellent at 94%.",
                "I found potential cost savings of $120/year on your medications.",
                "I've coordinated with your pharmacy for the refill of your blood pressure medication.",
                "Your prescription schedule has been optimized for maximum effectiveness."
            ],
            'insurance': [
                "I've reviewed your insurance policies and found potential savings of $300/year.",
                "Your claim for $1,200 has been processed and approved.",
                "I've scheduled your policy review for next month.",
                "I found a better health insurance plan that could save you $200/month.",
                "Your auto insurance premium decreased by 15% this year.",
                "I've coordinated with your insurance provider for faster claim processing."
            ],
            'tax': [
                "I've organized your tax documents and identified $2,500 in potential deductions.",
                "Your quarterly tax estimate is ready for review.",
                "I've scheduled your tax preparation appointment for next week.",
                "I found additional business expense deductions worth $1,800.",
                "Your tax optimization strategy could save you $3,200 this year."
            ],
            'communication': [
                "I've prioritized your messages and will respond within 2 hours.",
                "Your communication preferences have been updated successfully.",
                "I've set up automated reminders for your important appointments.",
                "Your message history has been organized and archived."
            ]
        }
    
    def load_messages(self):
        """Load messages from persistent storage"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    # Convert timestamp strings back to datetime objects
                    for message in data.get('messages', []):
                        if isinstance(message.get('timestamp'), str):
                            message['timestamp'] = datetime.fromisoformat(message['timestamp'])
                    self.messages = data.get('messages', [])
                    self.conversations = data.get('conversations', {})
            else:
                self.messages = []
                self.conversations = {}
        except Exception as e:
            print(f"Error loading messages: {e}")
            self.messages = []
            self.conversations = {}
    
    def save_messages(self):
        """Save messages to persistent storage"""
        try:
            # Convert datetime objects to strings for JSON serialization
            messages_to_save = []
            for message in self.messages:
                message_copy = message.copy()
                if isinstance(message_copy.get('timestamp'), datetime):
                    message_copy['timestamp'] = message_copy['timestamp'].isoformat()
                messages_to_save.append(message_copy)
            
            data = {
                'messages': messages_to_save,
                'conversations': self.conversations
            }
            
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving messages: {e}")
    
    def add_message(self, sender, recipient, message, message_type="user", channel="concierge"):
        """Add a new message to the system"""
        message_id = str(uuid.uuid4())
        new_message = {
            'id': message_id,
            'sender': sender,
            'recipient': recipient,
            'message': message,
            'timestamp': datetime.now(),
            'message_type': message_type,  # 'user', 'concierge', 'ai_agent'
            'channel': channel,  # 'concierge', 'ai_agent', 'support'
            'read': False
        }
        self.messages.append(new_message)
        
        # Add to conversation thread
        if channel not in self.conversations:
            self.conversations[channel] = []
        self.conversations[channel].append(new_message)
        
        # Save messages to persistent storage
        self.save_messages()
        
        return message_id
    
    def get_messages(self, channel="concierge", limit=50):
        """Get messages for a specific channel"""
        if channel not in self.conversations:
            return []
        return self.conversations[channel][-limit:]
    
    def get_unread_count(self, channel="concierge"):
        """Get count of unread messages"""
        if channel not in self.conversations:
            return 0
        return sum(1 for msg in self.conversations[channel] if not msg.get('read', False))
