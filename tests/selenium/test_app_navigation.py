"""
Selenium tests for app navigation and tab functionality
"""
import pytest
import time


class TestAppNavigation:
    """Test app navigation and tab functionality"""
    
    def test_login_functionality(self, driver, app_url, app_helper):
        """Test login functionality"""
        # Navigate to app
        driver.get(app_url)
        
        # Verify login page loads
        assert "Concierge.com" in driver.title or "Concierge.com" in driver.page_source
        
        # Test login
        app_helper.login("demo", "demo123")
        
        # Verify dashboard loads
        assert app_helper.is_element_present('//h1[contains(text(), "Welcome back")]')
    
    def test_all_service_tabs_present(self, driver, app_url, app_helper):
        """Test that all service tabs are present and clickable"""
        # Login first
        driver.get(app_url)
        app_helper.login("demo", "demo123")
        
        # Expected tabs
        expected_tabs = [
            "💰 Expenses", "📈 Investments", "🏥 Health", "🛡️ Insurance", 
            "⚖️ Legal", "📊 Tax", "✈️ Travel", "💬 Messages", 
            "🤖 AI Agents", "⚙️ Settings"
        ]
        
        # Check each tab is present and clickable
        for tab in expected_tabs:
            assert app_helper.is_element_present(f'//button[contains(text(), "{tab}")]'), f"Tab {tab} not found"
            
            # Click tab and verify it's active
            app_helper.click_tab(tab)
            time.sleep(1)
            
            # Verify tab content loads (look for subheader or content)
            assert app_helper.wait_for_element('//h2 | //h3 | //div[contains(@class, "stSubheader")]'), f"Tab {tab} content not loading"
    
    def test_expenses_tab_content(self, driver, app_url, app_helper):
        """Test Expenses tab content"""
        driver.get(app_url)
        app_helper.login("demo", "demo123")
        
        # Click Expenses tab
        app_helper.click_tab("💰 Expenses")
        
        # Verify expected content
        expected_content = [
            "Expense Management",
            "Total Expenses",
            "Remaining Budget",
            "Monthly Trend",
            "Add New Expense"
        ]
        
        content = app_helper.get_tab_content()
        for item in expected_content:
            assert item in content, f"Expected content '{item}' not found in Expenses tab"
    
    def test_investments_tab_content(self, driver, app_url, app_helper):
        """Test Investments tab content"""
        driver.get(app_url)
        app_helper.login("demo", "demo123")
        
        # Click Investments tab
        app_helper.click_tab("📈 Investments")
        
        # Verify expected content
        expected_content = [
            "Investment Management",
            "Portfolio Value",
            "Total Investments",
            "Daily Change",
            "Available Brokers"
        ]
        
        content = app_helper.get_tab_content()
        for item in expected_content:
            assert item in content, f"Expected content '{item}' not found in Investments tab"
    
    def test_health_tab_content(self, driver, app_url, app_helper):
        """Test Health tab content"""
        driver.get(app_url)
        app_helper.login("demo", "demo123")
        
        # Click Health tab
        app_helper.click_tab("🏥 Health")
        
        # Verify expected content
        expected_content = [
            "Health Management",
            "Active Prescriptions",
            "Refill Reminders",
            "Add New Prescription"
        ]
        
        content = app_helper.get_tab_content()
        for item in expected_content:
            assert item in content, f"Expected content '{item}' not found in Health tab"
    
    def test_insurance_tab_content(self, driver, app_url, app_helper):
        """Test Insurance tab content"""
        driver.get(app_url)
        app_helper.login("demo", "demo123")
        
        # Click Insurance tab
        app_helper.click_tab("🛡️ Insurance")
        
        # Verify expected content
        expected_content = [
            "Insurance Management",
            "Active Policies",
            "Insurance Companies",
            "Available Insurance Companies"
        ]
        
        content = app_helper.get_tab_content()
        for item in expected_content:
            assert item in content, f"Expected content '{item}' not found in Insurance tab"
    
    def test_legal_tab_content(self, driver, app_url, app_helper):
        """Test Legal tab content"""
        driver.get(app_url)
        app_helper.login("demo", "demo123")
        
        # Click Legal tab
        app_helper.click_tab("⚖️ Legal")
        
        # Verify expected content
        expected_content = [
            "Legal Management",
            "Active Cases",
            "Law Firms",
            "Available Law Firms"
        ]
        
        content = app_helper.get_tab_content()
        for item in expected_content:
            assert item in content, f"Expected content '{item}' not found in Legal tab"
    
    def test_tax_tab_content(self, driver, app_url, app_helper):
        """Test Tax tab content"""
        driver.get(app_url)
        app_helper.login("demo", "demo123")
        
        # Click Tax tab
        app_helper.click_tab("📊 Tax")
        
        # Verify expected content
        expected_content = [
            "Tax Management",
            "Tax Documents",
            "Tax Providers",
            "Available Tax Providers"
        ]
        
        content = app_helper.get_tab_content()
        for item in expected_content:
            assert item in content, f"Expected content '{item}' not found in Tax tab"
    
    def test_travel_tab_content(self, driver, app_url, app_helper):
        """Test Travel tab content"""
        driver.get(app_url)
        app_helper.login("demo", "demo123")
        
        # Click Travel tab
        app_helper.click_tab("✈️ Travel")
        
        # Verify expected content
        expected_content = [
            "Travel Management",
            "Travel Trips",
            "Travel Services",
            "Available Travel Services"
        ]
        
        content = app_helper.get_tab_content()
        for item in expected_content:
            assert item in content, f"Expected content '{item}' not found in Travel tab"
    
    def test_messages_tab_content(self, driver, app_url, app_helper):
        """Test Messages tab content"""
        driver.get(app_url)
        app_helper.login("demo", "demo123")
        
        # Click Messages tab
        app_helper.click_tab("💬 Messages")
        
        # Verify expected content
        expected_content = [
            "Messaging System",
            "Select Channel",
            "Send Message"
        ]
        
        content = app_helper.get_tab_content()
        for item in expected_content:
            assert item in content, f"Expected content '{item}' not found in Messages tab"
    
    def test_ai_agents_tab_content(self, driver, app_url, app_helper):
        """Test AI Agents tab content"""
        driver.get(app_url)
        app_helper.login("demo", "demo123")
        
        # Click AI Agents tab
        app_helper.click_tab("🤖 AI Agents")
        
        # Verify expected content
        expected_content = [
            "AI Agents",
            "Expense AI",
            "Travel AI",
            "Medical AI",
            "Insurance AI",
            "Tax AI",
            "Communication AI"
        ]
        
        content = app_helper.get_tab_content()
        for item in expected_content:
            assert item in content, f"Expected content '{item}' not found in AI Agents tab"
    
    def test_settings_tab_content(self, driver, app_url, app_helper):
        """Test Settings tab content"""
        driver.get(app_url)
        app_helper.login("demo", "demo123")
        
        # Click Settings tab
        app_helper.click_tab("⚙️ Settings")
        
        # Verify expected content
        expected_content = [
            "Settings",
            "Current Plan",
            "Plan Features"
        ]
        
        content = app_helper.get_tab_content()
        for item in expected_content:
            assert item in content, f"Expected content '{item}' not found in Settings tab"
    
    def test_tab_navigation_sequence(self, driver, app_url, app_helper):
        """Test navigating through all tabs in sequence"""
        driver.get(app_url)
        app_helper.login("demo", "demo123")
        
        # Navigate through all tabs
        tabs = [
            "💰 Expenses", "📈 Investments", "🏥 Health", "🛡️ Insurance", 
            "⚖️ Legal", "📊 Tax", "✈️ Travel", "💬 Messages", 
            "🤖 AI Agents", "⚙️ Settings"
        ]
        
        for tab in tabs:
            app_helper.click_tab(tab)
            time.sleep(1)
            
            # Verify tab content loads
            assert app_helper.wait_for_element('//h2 | //h3 | //div[contains(@class, "stSubheader")]'), f"Tab {tab} failed to load content"
    
    def test_dashboard_metrics(self, driver, app_url, app_helper):
        """Test dashboard metrics are displayed"""
        driver.get(app_url)
        app_helper.login("demo", "demo123")
        
        # Verify dashboard metrics are present
        expected_metrics = [
            "AI Tasks Completed",
            "Unread Messages",
            "Active Prescriptions",
            "Portfolio Value"
        ]
        
        for metric in expected_metrics:
            assert app_helper.is_element_present(f'//text()[contains(., "{metric}")]'), f"Metric '{metric}' not found on dashboard"
    
    def test_sidebar_functionality(self, driver, app_url, app_helper):
        """Test sidebar functionality"""
        driver.get(app_url)
        app_helper.login("demo", "demo123")
        
        # Verify sidebar elements
        expected_sidebar = [
            "Concierge.com",
            "Plan:"
        ]
        
        for item in expected_sidebar:
            assert app_helper.is_element_present(f'//text()[contains(., "{item}")]'), f"Sidebar item '{item}' not found"
