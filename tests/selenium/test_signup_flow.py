"""
Selenium tests for signup flow and client intake
"""
import pytest
import time


class TestSignupFlow:
    """Test signup flow and client intake process"""
    
    def test_signup_tab_access(self, driver, app_url, wait):
        """Test access to signup tab"""
        driver.get(app_url)
        
        # Wait for page to load
        wait.until(lambda driver: "Concierge.com" in driver.page_source)
        
        # Click on Sign Up tab
        signup_tab = wait.until(
            lambda driver: driver.find_element("xpath", '//button[contains(text(), "Sign Up")]')
        )
        signup_tab.click()
        
        # Verify signup form loads
        assert wait.until(
            lambda driver: "Join Concierge.com" in driver.page_source
        ), "Signup form not loaded"
    
    def test_signup_form_steps(self, driver, app_url, wait):
        """Test multi-step signup form"""
        driver.get(app_url)
        
        # Navigate to signup tab
        signup_tab = wait.until(
            lambda driver: driver.find_element("xpath", '//button[contains(text(), "Sign Up")]')
        )
        signup_tab.click()
        
        # Step 1: Account Information
        step1_content = [
            "Step 1 of 5",
            "Account Information",
            "Choose Username",
            "Email Address",
            "Create Password",
            "First Name",
            "Last Name",
            "Confirm Password"
        ]
        
        for content in step1_content:
            assert content in driver.page_source, f"Step 1 content '{content}' not found"
        
        # Test form fields are present
        form_fields = [
            'input[aria-label="Choose Username"]',
            'input[aria-label="Email Address"]',
            'input[aria-label="Create Password"]',
            'input[aria-label="First Name"]',
            'input[aria-label="Last Name"]',
            'input[aria-label="Confirm Password"]'
        ]
        
        for field in form_fields:
            assert wait.until(
                lambda driver: driver.find_element("css selector", field)
            ), f"Form field {field} not found"
    
    def test_signup_form_validation(self, driver, app_url, wait):
        """Test signup form validation"""
        driver.get(app_url)
        
        # Navigate to signup tab
        signup_tab = wait.until(
            lambda driver: driver.find_element("xpath", '//button[contains(text(), "Sign Up")]')
        )
        signup_tab.click()
        
        # Try to submit empty form
        next_button = wait.until(
            lambda driver: driver.find_element("xpath", '//button[contains(text(), "Next →")]')
        )
        next_button.click()
        
        # Should show validation error
        time.sleep(1)
        assert "Please fill in all required fields" in driver.page_source or "error" in driver.page_source.lower()
    
    def test_signup_form_fill_and_navigate(self, driver, app_url, wait):
        """Test filling signup form and navigating through steps"""
        driver.get(app_url)
        
        # Navigate to signup tab
        signup_tab = wait.until(
            lambda driver: driver.find_element("xpath", '//button[contains(text(), "Sign Up")]')
        )
        signup_tab.click()
        
        # Fill Step 1: Account Information
        username_input = wait.until(
            lambda driver: driver.find_element("css selector", 'input[aria-label="Choose Username"]')
        )
        username_input.send_keys("testuser")
        
        email_input = driver.find_element("css selector", 'input[aria-label="Email Address"]')
        email_input.send_keys("test@example.com")
        
        password_input = driver.find_element("css selector", 'input[aria-label="Create Password"]')
        password_input.send_keys("testpassword123")
        
        first_name_input = driver.find_element("css selector", 'input[aria-label="First Name"]')
        first_name_input.send_keys("Test")
        
        last_name_input = driver.find_element("css selector", 'input[aria-label="Last Name"]')
        last_name_input.send_keys("User")
        
        confirm_password_input = driver.find_element("css selector", 'input[aria-label="Confirm Password"]')
        confirm_password_input.send_keys("testpassword123")
        
        # Click Next
        next_button = driver.find_element("xpath", '//button[contains(text(), "Next →")]')
        next_button.click()
        
        # Verify Step 2 loads
        time.sleep(2)
        assert "Step 2 of 5" in driver.page_source, "Step 2 not loaded"
        assert "Financial Profile" in driver.page_source, "Financial Profile step not found"
    
    def test_signup_form_all_steps(self, driver, app_url, wait):
        """Test all signup form steps"""
        driver.get(app_url)
        
        # Navigate to signup tab
        signup_tab = wait.until(
            lambda driver: driver.find_element("xpath", '//button[contains(text(), "Sign Up")]')
        )
        signup_tab.click()
        
        # Step 1: Account Information
        self._fill_step1_form(driver, wait)
        
        # Step 2: Financial Profile
        self._fill_step2_form(driver, wait)
        
        # Step 3: Goals and Objectives
        self._fill_step3_form(driver, wait)
        
        # Step 4: Service Selection
        self._fill_step4_form(driver, wait)
        
        # Step 5: Plan Recommendation
        self._verify_step5_form(driver, wait)
    
    def _fill_step1_form(self, driver, wait):
        """Fill Step 1 form"""
        username_input = wait.until(
            lambda driver: driver.find_element("css selector", 'input[aria-label="Choose Username"]')
        )
        username_input.send_keys("testuser")
        
        email_input = driver.find_element("css selector", 'input[aria-label="Email Address"]')
        email_input.send_keys("test@example.com")
        
        password_input = driver.find_element("css selector", 'input[aria-label="Create Password"]')
        password_input.send_keys("testpassword123")
        
        first_name_input = driver.find_element("css selector", 'input[aria-label="First Name"]')
        first_name_input.send_keys("Test")
        
        last_name_input = driver.find_element("css selector", 'input[aria-label="Last Name"]')
        last_name_input.send_keys("User")
        
        confirm_password_input = driver.find_element("css selector", 'input[aria-label="Confirm Password"]')
        confirm_password_input.send_keys("testpassword123")
        
        next_button = driver.find_element("xpath", '//button[contains(text(), "Next →")]')
        next_button.click()
        time.sleep(2)
    
    def _fill_step2_form(self, driver, wait):
        """Fill Step 2 form"""
        # Verify Step 2 is loaded
        assert "Step 2 of 5" in driver.page_source
        
        # Fill financial information
        net_worth_input = wait.until(
            lambda driver: driver.find_element("css selector", 'input[aria-label="Estimated Net Worth ($)"]')
        )
        net_worth_input.clear()
        net_worth_input.send_keys("500000")
        
        annual_income_input = driver.find_element("css selector", 'input[aria-label="Annual Income ($)"]')
        annual_income_input.clear()
        annual_income_input.send_keys("100000")
        
        # Click Next
        next_button = driver.find_element("xpath", '//button[contains(text(), "Next →")]')
        next_button.click()
        time.sleep(2)
    
    def _fill_step3_form(self, driver, wait):
        """Fill Step 3 form"""
        # Verify Step 3 is loaded
        assert "Step 3 of 5" in driver.page_source
        
        # Select goals (this might be a multiselect)
        # For now, just click Next
        next_button = wait.until(
            lambda driver: driver.find_element("xpath", '//button[contains(text(), "Next →")]')
        )
        next_button.click()
        time.sleep(2)
    
    def _fill_step4_form(self, driver, wait):
        """Fill Step 4 form"""
        # Verify Step 4 is loaded
        assert "Step 4 of 5" in driver.page_source
        
        # Select services (this might be a multiselect)
        # For now, just click Next
        next_button = wait.until(
            lambda driver: driver.find_element("xpath", '//button[contains(text(), "Next →")]')
        )
        next_button.click()
        time.sleep(2)
    
    def _verify_step5_form(self, driver, wait):
        """Verify Step 5 form"""
        # Verify Step 5 is loaded
        assert "Step 5 of 5" in driver.page_source
        
        # Verify plan recommendation is shown
        expected_content = [
            "Your Personalized Plan",
            "Recommended Plan",
            "Pricing",
            "Account Summary"
        ]
        
        for content in expected_content:
            assert content in driver.page_source, f"Step 5 content '{content}' not found"
    
    def test_signup_form_previous_navigation(self, driver, app_url, wait):
        """Test Previous button navigation"""
        driver.get(app_url)
        
        # Navigate to signup tab
        signup_tab = wait.until(
            lambda driver: driver.find_element("xpath", '//button[contains(text(), "Sign Up")]')
        )
        signup_tab.click()
        
        # Fill Step 1 and go to Step 2
        self._fill_step1_form(driver, wait)
        
        # Click Previous button
        previous_button = wait.until(
            lambda driver: driver.find_element("xpath", '//button[contains(text(), "← Previous")]')
        )
        previous_button.click()
        time.sleep(2)
        
        # Verify we're back to Step 1
        assert "Step 1 of 5" in driver.page_source, "Previous navigation failed"
    
    def test_signup_form_progress_indicator(self, driver, app_url, wait):
        """Test progress indicator updates"""
        driver.get(app_url)
        
        # Navigate to signup tab
        signup_tab = wait.until(
            lambda driver: driver.find_element("xpath", '//button[contains(text(), "Sign Up")]')
        )
        signup_tab.click()
        
        # Verify initial progress
        assert "Step 1 of 5" in driver.page_source
        
        # Navigate through steps and verify progress updates
        self._fill_step1_form(driver, wait)
        assert "Step 2 of 5" in driver.page_source
        
        self._fill_step2_form(driver, wait)
        assert "Step 3 of 5" in driver.page_source
        
        self._fill_step3_form(driver, wait)
        assert "Step 4 of 5" in driver.page_source
        
        self._fill_step4_form(driver, wait)
        assert "Step 5 of 5" in driver.page_source
