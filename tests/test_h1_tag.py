# tests/test_h1_tag.py

from selenium.webdriver.common.by import By
from utils.test_utils import generate_report
import logging

def run_h1_tag_test(driver, page_url):
    """
    Test for the existence of the H1 tag on the page and generate an Excel report.
    
    :param driver: Selenium WebDriver
    :param page_url: URL of the page to test
    :return: List of test results
    """
    test_results = []
    
    try:
        logging.info(f"Navigating to {page_url}...")
        driver.get(page_url)
        
        logging.info("Checking for <h1> tag...")
        h1_tags = driver.find_elements(By.TAG_NAME, "h1")
        
        if not h1_tags:
            logging.warning("H1 tag is missing.")
            test_results.append({
                'Page URL': page_url,
                'Test Case': "Check H1 Tag",
                'Status': False,
                'Comments': "Missing <h1> tag"
            })
        else:
            logging.info("H1 tag exists.")
            h1_texts = [tag.text for tag in h1_tags]
            test_results.append({
                'Page URL': page_url,
                'Test Case': "Check H1 Tag",
                'Status': True,
                'Comments': f"<h1> tag exists with text: {', '.join(h1_texts)}"
            })
    
    except Exception as e:
        logging.error(f"Error while checking <h1> tag: {e}")
        test_results.append({
            'Page URL': page_url,
            'Test Case': "Check H1 Tag",
            'Status': False,
            'Comments': f"Error: {str(e)}"
        })
    
    # Generate the Excel report
    generate_report(test_results, 'h1_tag_test')
    logging.info("H1 tag test completed. Results saved.")
    
    return test_results

