"""
Unit tests for plan recommendation logic
"""
import pytest
import sys
sys.path.append('.')

from app import ClientIntakeManager


class TestPlanRecommendation:
    """Test cases for plan recommendation logic"""
    
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.manager = ClientIntakeManager()
    
    def test_basic_plan_recommendation(self):
        """Test basic plan recommendation for simple cases"""
        # Low net worth, simple goals, few services
        test_cases = [
            (50000, ['health management'], ['Health Management']),
            (100000, ['expense tracking'], ['Expense Tracking']),
            (75000, ['travel'], ['Travel Planning']),
        ]
        
        for net_worth, goals, services in test_cases:
            plan, score = self.manager.recommend_plan(net_worth, goals, services)
            assert plan == 'basic', f"Should recommend basic for net_worth={net_worth}, goals={goals}, services={services}"
            assert 0 <= score <= 10
    
    def test_premium_plan_recommendation(self):
        """Test premium plan recommendation for moderate complexity"""
        # Medium net worth, moderate goals, several services
        test_cases = [
            (500000, ['wealth management', 'tax optimization'], ['Investment Management', 'Tax Management']),
            (750000, ['health', 'investment'], ['Health Management', 'Investment Management', 'Expense Tracking']),
            (750000, ['legal planning', 'insurance'], ['Legal Services', 'Insurance Management']),  # Increased net worth and services
        ]
        
        for net_worth, goals, services in test_cases:
            plan, score = self.manager.recommend_plan(net_worth, goals, services)
            assert plan == 'premium', f"Should recommend premium for net_worth={net_worth}, goals={goals}, services={services}"
            assert 0 <= score <= 10
    
    def test_elite_plan_recommendation(self):
        """Test elite plan recommendation for high complexity"""
        # High net worth, complex goals, many services
        test_cases = [
            (2000000, ['wealth management', 'tax optimization', 'legal planning'], 
             ['Investment Management', 'Tax Management', 'Legal Services', 'Personal Assistant']),
            (5000000, ['business management', 'estate planning', 'investment'], 
             ['Investment Management', 'Legal Services', 'Tax Management', 'Travel Planning', 'Personal Assistant']),
            (10000000, ['wealth', 'tax', 'legal', 'business'], 
             ['Investment Management', 'Legal Services', 'Tax Management', 'Personal Assistant', 'Travel Planning', 'Insurance Management']),
        ]
        
        for net_worth, goals, services in test_cases:
            plan, score = self.manager.recommend_plan(net_worth, goals, services)
            assert plan == 'elite', f"Should recommend elite for net_worth={net_worth}, goals={goals}, services={services}"
            assert 0 <= score <= 10
    
    def test_net_worth_scoring(self):
        """Test that net worth affects complexity score"""
        goals = ['wealth management']
        services = ['Investment Management']
        
        # Test different net worth levels
        test_cases = [
            (100000, 1),    # $100K should add 1 point
            (500000, 2),    # $500K should add 2 points
            (2000000, 3),   # $2M should add 3 points
        ]
        
        for net_worth, expected_additional_score in test_cases:
            plan, score = self.manager.recommend_plan(net_worth, goals, services)
            assert score >= expected_additional_score, \
                f"Net worth {net_worth} should contribute at least {expected_additional_score} points"
    
    def test_goal_complexity_scoring(self):
        """Test that complex goals increase score"""
        net_worth = 100000
        services = ['Investment Management']
        
        # High-value goals should increase score
        high_value_goals = [
            ['wealth management'],
            ['tax optimization'],
            ['legal planning'],
            ['investment'],
            ['business'],
        ]
        
        simple_goals = ['health management']
        
        simple_plan, simple_score = self.manager.recommend_plan(net_worth, simple_goals, services)
        
        for goals in high_value_goals:
            plan, score = self.manager.recommend_plan(net_worth, goals, services)
            assert score >= simple_score, \
                f"Goals {goals} should have higher score than {simple_goals}"
    
    def test_service_count_scoring(self):
        """Test that more services increase complexity score"""
        net_worth = 100000
        goals = ['health management']
        
        # More services should increase score
        few_services = ['Health Management']
        many_services = ['Health Management', 'Investment Management', 'Legal Services', 'Tax Management', 'Travel Planning']
        
        few_plan, few_score = self.manager.recommend_plan(net_worth, goals, few_services)
        many_plan, many_score = self.manager.recommend_plan(net_worth, goals, many_services)
        
        assert many_score > few_score, "More services should increase complexity score"
    
    def test_premium_services_scoring(self):
        """Test that premium services increase score"""
        net_worth = 100000
        goals = ['health management']
        
        # Premium services should increase score
        basic_services = ['Health Management', 'Expense Tracking']
        premium_services = ['Legal Services', 'Tax Management', 'Investment Management']
        
        basic_plan, basic_score = self.manager.recommend_plan(net_worth, goals, basic_services)
        premium_plan, premium_score = self.manager.recommend_plan(net_worth, goals, premium_services)
        
        assert premium_score > basic_score, "Premium services should increase complexity score"
    
    def test_edge_case_empty_inputs(self):
        """Test plan recommendation with empty inputs"""
        plan, score = self.manager.recommend_plan(0, [], [])
        
        assert plan == 'basic'  # Should default to basic
        assert score >= 0
    
    def test_edge_case_very_high_values(self):
        """Test plan recommendation with very high values"""
        plan, score = self.manager.recommend_plan(
            100000000,  # Very high net worth
            ['wealth management', 'tax optimization', 'legal planning', 'business management', 'estate planning'],
            ['Investment Management', 'Legal Services', 'Tax Management', 'Personal Assistant', 'Travel Planning', 'Insurance Management', 'Expense Tracking']
        )
        
        assert plan == 'elite'
        assert score >= 7  # Should be high complexity
    
    def test_score_consistency(self):
        """Test that similar inputs produce consistent scores"""
        net_worth = 500000
        goals = ['wealth management', 'tax optimization']
        services = ['Investment Management', 'Tax Management']
        
        # Run multiple times to ensure consistency
        scores = []
        for _ in range(5):
            plan, score = self.manager.recommend_plan(net_worth, goals, services)
            scores.append(score)
        
        # All scores should be the same
        assert all(score == scores[0] for score in scores), "Scores should be consistent"
    
    def test_plan_thresholds(self):
        """Test plan recommendation thresholds"""
        # Test boundary conditions
        test_cases = [
            # (net_worth, goals, services, expected_plan)
            (100000, ['health'], ['Health Management'], 'basic'),
            (500000, ['wealth', 'tax'], ['Investment Management', 'Tax Management'], 'premium'),
            (2000000, ['wealth', 'tax', 'legal', 'business'], 
             ['Investment Management', 'Legal Services', 'Tax Management', 'Personal Assistant'], 'elite'),
        ]
        
        for net_worth, goals, services, expected_plan in test_cases:
            plan, score = self.manager.recommend_plan(net_worth, goals, services)
            assert plan == expected_plan, \
                f"Expected {expected_plan} for net_worth={net_worth}, goals={goals}, services={services}, got {plan}"


if __name__ == '__main__':
    pytest.main([__file__])
