# utils/web_driver.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def setup_chrome_driver():
    """
    Setup Chrome WebDriver using WebDriver Manager
    Automatically downloads and manages ChromeDriver
    """
    # Chrome options for headless and no-gui mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Automatic ChromeDriver management
    service = Service(ChromeDriverManager().install())
    
    # Create WebDriver instance
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver

