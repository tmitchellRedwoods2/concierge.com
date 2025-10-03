"""
Selenium test configuration and fixtures
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@pytest.fixture(scope="session")
def driver():
    """Create and configure Chrome driver"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode for CI/CD
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Use webdriver-manager to automatically download and manage ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Set implicit wait
    driver.implicitly_wait(10)
    
    yield driver
    
    # Cleanup
    driver.quit()


@pytest.fixture
def app_url():
    """Get the application URL"""
    # For local testing
    return "http://localhost:8501"
    # For Streamlit Cloud testing, replace with your actual URL
    # return "https://your-app-name.streamlit.app"


@pytest.fixture
def wait(driver):
    """Create WebDriverWait instance"""
    return WebDriverWait(driver, 20)


class StreamlitAppHelper:
    """Helper class for Streamlit app interactions"""
    
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
    
    def login(self, username="demo", password="demo123"):
        """Login to the application"""
        # Wait for login form to be visible
        username_input = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Username"]'))
        )
        password_input = self.driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Password"]')
        
        # Enter credentials
        username_input.clear()
        username_input.send_keys(username)
        password_input.clear()
        password_input.send_keys(password)
        
        # Click login button
        login_button = self.driver.find_element(By.XPATH, '//button[contains(text(), "Sign In")]')
        login_button.click()
        
        # Wait for dashboard to load
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "Welcome back")]'))
        )
    
    def click_tab(self, tab_name):
        """Click on a specific tab"""
        tab_element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'//button[contains(text(), "{tab_name}")]'))
        )
        tab_element.click()
        time.sleep(1)  # Wait for tab content to load
    
    def get_tab_content(self):
        """Get the content of the current tab"""
        # Wait for content to be visible
        time.sleep(2)
        return self.driver.page_source
    
    def is_element_present(self, xpath):
        """Check if an element is present"""
        try:
            self.driver.find_element(By.XPATH, xpath)
            return True
        except:
            return False
    
    def wait_for_element(self, xpath, timeout=10):
        """Wait for an element to be present"""
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            return True
        except:
            return False


@pytest.fixture
def app_helper(driver, wait):
    """Create StreamlitAppHelper instance"""
    return StreamlitAppHelper(driver, wait)
