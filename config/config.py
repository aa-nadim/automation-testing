# config/config.py
import os

class Config:
    # Base URL for testing
    BASE_URL = "https://www.alojamiento.io/"
    
    # Determine the base directory of the project
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Reports directory
    REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
    
    # Ensure reports directory exists
    os.makedirs(REPORTS_DIR, exist_ok=True)
    
    # Consistent report path
    REPORT_PATH = os.path.join(REPORTS_DIR, 'vacation_rental_test_results.xlsx')
    
    # Screenshots directory
    SCREENSHOTS_DIR = os.path.join(BASE_DIR, 'screenshots')
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    
    # Timeout for web operations
    TIMEOUT = 10