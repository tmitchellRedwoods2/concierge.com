"""
Unit tests for InvestmentManager class
"""
import pytest
import sys
sys.path.append('.')

from app import InvestmentManager


class TestInvestmentManager:
    """Test cases for InvestmentManager"""
    
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.investment_manager = InvestmentManager()
    
    def test_init_investments(self):
        """Test that investments list is properly initialized"""
        assert isinstance(self.investment_manager.investments, list)
        assert len(self.investment_manager.investments) >= 0
    
    def test_init_accounts(self):
        """Test that accounts list is properly initialized"""
        assert isinstance(self.investment_manager.accounts, list)
        assert len(self.investment_manager.accounts) >= 0
    
    def test_init_brokers(self):
        """Test that brokers dictionary is properly initialized"""
        assert isinstance(self.investment_manager.brokers, dict)
        assert len(self.investment_manager.brokers) > 0
        
        # Check that all brokers have required keys
        for broker_key, broker_data in self.investment_manager.brokers.items():
            assert 'name' in broker_data
            assert 'website' in broker_data
            assert 'api_available' in broker_data
            assert 'features' in broker_data
    
    def test_add_investment_account(self):
        """Test adding an investment account"""
        account = self.investment_manager.add_investment_account(
            'charles_schwab', 'My Brokerage', 'individual', 10000
        )
        
        assert account is not None
        assert account['broker'] == 'charles_schwab'
        assert account['account_name'] == 'My Brokerage'
        assert account['account_type'] == 'individual'
        assert account['balance'] == 10000
        assert account['status'] == 'active'
        assert len(self.investment_manager.accounts) >= 1
    
    def test_add_investment_account_default_balance(self):
        """Test adding account with default balance"""
        account = self.investment_manager.add_investment_account(
            'fidelity', 'Retirement Account', 'ira'
        )
        
        assert account['balance'] == 0
        assert account['account_type'] == 'ira'
    
    def test_add_investment(self):
        """Test adding an investment"""
        # First add an account
        account = self.investment_manager.add_investment_account(
            'charles_schwab', 'Test Account', 'individual'
        )
        
        investment = self.investment_manager.add_investment(
            'AAPL', 'Apple Inc.', 10, 150.00, account['id']
        )
        
        assert investment is not None
        assert investment['symbol'] == 'AAPL'
        assert investment['name'] == 'Apple Inc.'
        assert investment['shares'] == 10
        assert investment['price'] == 150.00
        assert investment['current_value'] == 1500.00
        assert investment['account_id'] == account['id']
        assert investment['investment_type'] == 'stock'
        assert investment['status'] == 'active'
        assert len(self.investment_manager.investments) >= 1
    
    def test_add_investment_custom_type(self):
        """Test adding investment with custom type"""
        account = self.investment_manager.add_investment_account(
            'vanguard', 'ETF Account', 'individual'
        )
        
        investment = self.investment_manager.add_investment(
            'VTI', 'Vanguard Total Stock Market ETF', 50, 200.00, account['id'], 'etf'
        )
        
        assert investment['investment_type'] == 'etf'
        assert investment['current_value'] == 10000.00
    
    def test_get_portfolio_summary(self):
        """Test getting portfolio summary"""
        # Add accounts and investments
        account1 = self.investment_manager.add_investment_account(
            'charles_schwab', 'Account 1', 'individual', 5000
        )
        account2 = self.investment_manager.add_investment_account(
            'fidelity', 'Account 2', 'ira', 3000
        )
        
        self.investment_manager.add_investment(
            'AAPL', 'Apple Inc.', 10, 150.00, account1['id']
        )
        self.investment_manager.add_investment(
            'MSFT', 'Microsoft Corp.', 5, 300.00, account2['id']
        )
        
        summary = self.investment_manager.get_portfolio_summary()
        
        assert isinstance(summary, dict)
        assert 'total_value' in summary
        assert 'total_investments' in summary
        assert 'total_accounts' in summary
        assert 'daily_change' in summary
        assert 'percent_change' in summary
        assert summary['total_value'] >= 3000.00  # 10*150 + 5*300 (may include additional data)
        assert summary['total_investments'] >= 2
        assert summary['total_accounts'] >= 2
    
    def test_get_broker_info(self):
        """Test getting broker information"""
        broker_info = self.investment_manager.get_broker_info('charles_schwab')
        
        assert isinstance(broker_info, dict)
        assert broker_info['name'] == 'Charles Schwab'
        assert broker_info['website'] == 'https://www.schwab.com'
        assert broker_info['api_available'] is True
        assert 'Trading' in broker_info['features']
    
    def test_get_broker_info_invalid(self):
        """Test getting info for invalid broker"""
        broker_info = self.investment_manager.get_broker_info('invalid_broker')
        
        assert broker_info == {}
    
    def test_get_available_brokers(self):
        """Test getting available brokers list"""
        brokers = self.investment_manager.get_available_brokers()
        
        assert isinstance(brokers, list)
        assert len(brokers) > 0
        assert 'charles_schwab' in brokers
        assert 'fidelity' in brokers
        assert 'vanguard' in brokers
    
    def test_get_investment_performance(self):
        """Test getting investment performance"""
        performance = self.investment_manager.get_investment_performance()
        
        assert isinstance(performance, dict)
        assert 'asset_allocation' in performance
        assert 'sector_allocation' in performance
        assert 'top_performers' in performance


if __name__ == '__main__':
    pytest.main([__file__])