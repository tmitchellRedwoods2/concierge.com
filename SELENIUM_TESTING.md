# 🧪 Selenium Testing Guide

## 📋 Overview

This guide covers the Selenium test suite for Concierge.com, which provides automated browser testing to verify that all functionality works correctly in a real browser environment.

## 🎯 Test Coverage

### **Navigation Tests** (`test_app_navigation.py`)
- ✅ Login functionality
- ✅ All 10 service tabs present and clickable
- ✅ Tab content rendering verification
- ✅ Dashboard metrics display
- ✅ Sidebar functionality

### **Signup Flow Tests** (`test_signup_flow.py`)
- ✅ Signup tab access
- ✅ Multi-step form navigation
- ✅ Form validation
- ✅ Progress indicator updates
- ✅ Previous/Next button functionality

### **Admin Functionality Tests** (`test_admin_functionality.py`)
- ✅ Admin login access
- ✅ Admin dashboard elements
- ✅ System metrics display
- ✅ User management features
- ✅ Logout functionality

## 🚀 Quick Start

### **Prerequisites**
```bash
# Install dependencies
pip install -r requirements-selenium.txt
```

### **Run All Tests**
```bash
# Run against local app
python run_selenium_tests.py

# Run against Streamlit Cloud
python run_selenium_tests.py --url "https://your-app.streamlit.app"

# Run with visible browser
python run_selenium_tests.py --no-headless

# Install dependencies and run
python run_selenium_tests.py --install-deps
```

### **Run Smoke Tests Only**
```bash
# Quick smoke test
python run_selenium_tests.py --smoke-only
```

## 🔧 Test Configuration

### **Browser Settings**
- **Default**: Headless Chrome
- **Window Size**: 1920x1080
- **Implicit Wait**: 10 seconds
- **Explicit Wait**: 20 seconds

### **Test Data**
- **Username**: `demo`
- **Password**: `demo123`
- **Admin Username**: `admin`
- **Admin Password**: `SecureAdmin2024!`

## 📊 Test Reports

### **HTML Report**
- **Location**: `reports/selenium_report.html`
- **Features**: Detailed test results, screenshots, timings
- **Format**: Self-contained HTML file

### **JUnit XML**
- **Location**: `reports/selenium_junit.xml`
- **Features**: CI/CD integration, test metrics
- **Format**: Standard JUnit XML

## 🎯 Test Scenarios

### **1. Login Flow**
```python
def test_login_functionality(self, driver, app_url, app_helper):
    # Navigate to app
    driver.get(app_url)
    
    # Verify login page loads
    assert "Concierge.com" in driver.title
    
    # Test login
    app_helper.login("demo", "demo123")
    
    # Verify dashboard loads
    assert app_helper.is_element_present('//h1[contains(text(), "Welcome back")]')
```

### **2. Tab Navigation**
```python
def test_all_service_tabs_present(self, driver, app_url, app_helper):
    # Login first
    driver.get(app_url)
    app_helper.login("demo", "demo123")
    
    # Expected tabs
    expected_tabs = [
        "💰 Expenses", "📈 Investments", "🏥 Health", "🛡️ Insurance", 
        "⚖️ Legal", "📊 Tax", "✈️ Travel", "💬 Messages", 
        "🤖 AI Agents", "⚙️ Settings"
    ]
    
    # Check each tab
    for tab in expected_tabs:
        assert app_helper.is_element_present(f'//button[contains(text(), "{tab}")]')
        app_helper.click_tab(tab)
        assert app_helper.wait_for_element('//h2 | //h3 | //div[contains(@class, "stSubheader")]')
```

### **3. Content Verification**
```python
def test_expenses_tab_content(self, driver, app_url, app_helper):
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
        assert item in content
```

## 🔍 Troubleshooting

### **Common Issues**

#### **1. Element Not Found**
```python
# Use explicit waits
wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

# Check if element is present
app_helper.is_element_present(xpath)
```

#### **2. Timing Issues**
```python
# Add explicit waits
time.sleep(2)

# Wait for specific conditions
wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
```

#### **3. Headless Mode Issues**
```bash
# Run with visible browser
python run_selenium_tests.py --no-headless
```

### **Debug Mode**
```python
# Add debug prints
print(f"Current URL: {driver.current_url}")
print(f"Page source: {driver.page_source[:500]}")

# Take screenshots
driver.save_screenshot("debug.png")
```

## 🚀 CI/CD Integration

### **GitHub Actions**
```yaml
- name: Run Selenium Tests
  run: |
    python run_selenium_tests.py --url ${{ secrets.APP_URL }} --install-deps
```

### **Local Development**
```bash
# Start app locally
streamlit run app_modular.py --server.port=8501

# Run tests
python run_selenium_tests.py --url "http://localhost:8501"
```

## 📈 Best Practices

### **1. Test Isolation**
- Each test should be independent
- Clean up after each test
- Use fresh browser instances

### **2. Robust Selectors**
- Prefer stable selectors (IDs, classes)
- Use explicit waits over implicit waits
- Handle dynamic content gracefully

### **3. Error Handling**
- Use try-catch blocks for optional elements
- Provide meaningful error messages
- Take screenshots on failures

### **4. Performance**
- Run tests in parallel when possible
- Use headless mode for CI/CD
- Optimize wait times

## 🎯 Expected Results

### **Successful Test Run**
```
🧪 Concierge.com Selenium Test Runner
==================================================
🚀 Running Selenium tests against: http://localhost:8501
✅ All Selenium tests passed!
🎉 Test execution completed successfully!
📊 Check reports/ directory for detailed results
```

### **Test Coverage**
- **Navigation Tests**: 15 test cases
- **Signup Flow Tests**: 8 test cases
- **Admin Functionality Tests**: 7 test cases
- **Total**: 30 test cases

## 🔧 Customization

### **Adding New Tests**
1. Create new test file in `tests/selenium/`
2. Follow naming convention: `test_*.py`
3. Use `Test*` class names
4. Add to test runner if needed

### **Modifying Test Data**
1. Update `conftest.py` for global changes
2. Modify individual test methods for specific cases
3. Use environment variables for configuration

### **Extending Test Coverage**
1. Add new test methods to existing classes
2. Create new test classes for new functionality
3. Update test runner and documentation

## 📞 Support

If you encounter issues with Selenium tests:

1. **Check Dependencies**: Ensure all packages are installed
2. **Verify App URL**: Make sure the app is accessible
3. **Review Logs**: Check test output and error messages
4. **Debug Mode**: Run with `--no-headless` for visibility
5. **Screenshots**: Check `reports/` directory for failure screenshots

## 🎉 Conclusion

The Selenium test suite provides comprehensive coverage of Concierge.com functionality, ensuring that all features work correctly in a real browser environment. Regular execution of these tests helps maintain code quality and catch regressions early.

**Happy Testing! 🚀**
