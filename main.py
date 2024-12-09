# main.py

import logging
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.driver_setup import setup_driver
from utils.test_utils import run_test
from config.config import PROPERTY_URL

from tests.test_h1_tag import test_h1_tag
from tests.test_html_tag_sequence import test_html_tag_sequence
from tests.test_image_alt_attribute import test_image_alt_attribute
from tests.test_url_status import test_url_status
# Import the scraping function
from tests.test_scrape_data import scrape_console_data

logging.basicConfig(
    level=logging.DEBUG,  # Capture all log levels (DEBUG, INFO, WARNING, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/test_logs.log"),
        # logging.StreamHandler()  
    ]
)


def main():
    driver = None
    try:
        print("Starting test execution...")
        logging.info("Setting up WebDriver...")

        logging.info("Setting up WebDriver...")
        driver = setup_driver(headless=False)  
        driver.maximize_window()  

        # Navigate to the test URL
        print(f"Navigating to: {PROPERTY_URL}")
        driver.get(PROPERTY_URL)

        # Wait for page to load
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            print("Page loaded successfully.")
            print("Page Title:", driver.title)
        except Exception as load_error:
            print(f"Error loading page: {load_error}")
            logging.error(f"Traceback: {traceback.format_exc()}")
            return

        # Run individual tests
        # run_test(driver, PROPERTY_URL, test_h1_tag, "H1 tag existence test")
        # run_test(driver, PROPERTY_URL, test_html_tag_sequence, "HTML tag sequence test")
        # run_test(driver, PROPERTY_URL, test_image_alt_attribute, "Image alt attribute test")
        # run_test(driver, PROPERTY_URL, test_url_status, "URL status code test")

        # Run the scraping function and save the data to CSV
        script_to_run = "return window.ScriptData;"  
        scrape_console_data(script_to_run)

        driver.save_screenshot("screenshots/final_test_state.png")
        print("Test execution complete.")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        logging.error(f"Traceback: {traceback.format_exc()}")
    finally:
        if driver:
            logging.info("Closing the WebDriver...")
            driver.quit()
            logging.info("WebDriver closed.")

if __name__ == "__main__":
    main()
