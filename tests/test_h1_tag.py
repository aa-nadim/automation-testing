# tests/test_h1_tag.py

from selenium.webdriver.common.by import By
import logging

def test_h1_tag(driver):
    """Test for the existence of the H1 tag on the page."""
    try:
        logging.info("Checking for <h1> tag...")
        h1_tags = driver.find_elements(By.TAG_NAME, "h1")
        
        if not h1_tags:
            logging.warning("H1 tag is missing.")
            return False, "Missing <h1> tag"
        
        logging.info("H1 tag exists.")
        return True, "H1 tag exists"
    
    except Exception as e:
        logging.error(f"Error while checking <h1> tag: {e}")
        return False, f"Error: {e}"
