"""
Unit tests for AIAgentSystem class
"""
import pytest
import sys
import os
sys.path.append('.')
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.managers.ai_agent import AIAgentSystem


class TestAIAgentSystem:
    """Test cases for AIAgentSystem"""
    
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.ai_system = AIAgentSystem()
    
    def test_init_agents(self):
        """Test that AI agents are properly initialized"""
        assert isinstance(self.ai_system.agents, dict)
        assert len(self.ai_system.agents) > 0
        
        # Check that all agents have required keys
        for agent_id, agent_data in self.ai_system.agents.items():
            assert 'name' in agent_data
            assert 'status' in agent_data
            assert 'tasks_completed' in agent_data
    
    def test_get_agent_status(self):
        """Test getting agent status"""
        status = self.ai_system.get_agent_status()
        
        assert isinstance(status, dict)
        assert len(status) > 0
    
    def test_simulate_ai_task(self):
        """Test simulating AI task completion"""
        agent_id = list(self.ai_system.agents.keys())[0]
        initial_tasks = self.ai_system.agents[agent_id]['tasks_completed']
        
        result = self.ai_system.simulate_ai_task(agent_id, "Test task")
        
        assert result.startswith("✅")
        assert self.ai_system.agents[agent_id]['tasks_completed'] == initial_tasks + 1
    
    def test_simulate_ai_task_invalid(self):
        """Test simulating task for invalid agent"""
        result = self.ai_system.simulate_ai_task('invalid_agent', 'test task')
        assert result == "❌ Agent not found"
    
    def test_get_ai_insights(self):
        """Test getting AI insights"""
        insights = self.ai_system.get_ai_insights('expense_patterns')
        
        assert isinstance(insights, list)
        assert len(insights) > 0
    
    def test_get_ai_insights_invalid(self):
        """Test getting insights for invalid category"""
        insights = self.ai_system.get_ai_insights('invalid_category')
        assert insights == []
    
    def test_generate_ai_recommendations(self):
        """Test generating AI recommendations"""
        recommendations = self.ai_system.generate_ai_recommendations('premium', 'expense')
        
        assert isinstance(recommendations, list)
        assert len(recommendations) >= 0


if __name__ == '__main__':
    pytest.main([__file__])
