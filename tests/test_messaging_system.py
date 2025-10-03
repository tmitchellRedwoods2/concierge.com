"""
Unit tests for MessagingSystem class
"""
import pytest
import sys
sys.path.append('.')

from app import MessagingSystem


class TestMessagingSystem:
    """Test cases for MessagingSystem"""
    
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.messaging = MessagingSystem()
    
    def test_init_messages(self):
        """Test that messages list is properly initialized"""
        assert isinstance(self.messaging.messages, list)
        assert isinstance(self.messaging.conversations, dict)
    
    def test_add_message(self):
        """Test adding a message"""
        message_id = self.messaging.add_message('user', 'concierge', 'Test message')
        
        assert message_id is not None
        assert len(self.messaging.messages) == 1
        assert self.messaging.messages[0]['message'] == 'Test message'
        assert self.messaging.messages[0]['sender'] == 'user'
        assert self.messaging.messages[0]['recipient'] == 'concierge'
    
    def test_get_messages(self):
        """Test getting messages for a channel"""
        # Add test messages
        self.messaging.add_message('user', 'concierge', 'Test 1')
        self.messaging.add_message('concierge', 'user', 'Test 2')
        
        messages = self.messaging.get_messages('concierge')
        
        assert len(messages) == 2
        assert messages[0]['message'] == 'Test 1'
        assert messages[1]['message'] == 'Test 2'
    
    def test_get_messages_with_limit(self):
        """Test getting messages with limit"""
        # Add multiple messages
        for i in range(5):
            self.messaging.add_message('user', 'concierge', f'Test {i}')
        
        # Get only 3 messages
        messages = self.messaging.get_messages('concierge', limit=3)
        
        assert len(messages) == 3
    
    def test_get_messages_empty(self):
        """Test getting messages when none exist"""
        messages = self.messaging.get_messages('concierge')
        assert len(messages) == 0
    
    def test_get_unread_count(self):
        """Test getting unread message count"""
        # Add messages
        self.messaging.add_message('user', 'concierge', 'Test 1')
        self.messaging.add_message('user', 'concierge', 'Test 2')
        
        unread_count = self.messaging.get_unread_count('concierge')
        
        assert unread_count == 2
    
    def test_mark_message_read(self):
        """Test marking a message as read"""
        message_id = self.messaging.add_message('user', 'concierge', 'Test message')
        
        # Find the message and manually mark it as read
        message = next((m for m in self.messaging.messages if m['id'] == message_id), None)
        message['read'] = True
        
        assert message['read'] is True
    
    def test_message_structure(self):
        """Test that messages have proper structure"""
        message_id = self.messaging.add_message('user', 'concierge', 'Test message')
        
        message = self.messaging.messages[0]
        
        assert 'id' in message
        assert 'sender' in message
        assert 'recipient' in message
        assert 'message' in message
        assert 'timestamp' in message
        assert 'message_type' in message
        assert 'channel' in message
        assert 'read' in message
    
    def test_conversation_threading(self):
        """Test that messages are added to conversation threads"""
        self.messaging.add_message('user', 'concierge', 'Test 1', channel='concierge')
        self.messaging.add_message('concierge', 'user', 'Test 2', channel='concierge')
        
        assert 'concierge' in self.messaging.conversations
        assert len(self.messaging.conversations['concierge']) == 2
    
    def test_different_channels(self):
        """Test messages in different channels"""
        self.messaging.add_message('user', 'concierge', 'Concierge message', channel='concierge')
        self.messaging.add_message('user', 'support', 'Support message', channel='support')
        
        concierge_messages = self.messaging.get_messages('concierge')
        support_messages = self.messaging.get_messages('support')
        
        assert len(concierge_messages) == 1
        assert len(support_messages) == 1
        assert concierge_messages[0]['message'] == 'Concierge message'
        assert support_messages[0]['message'] == 'Support message'


if __name__ == '__main__':
    pytest.main([__file__])