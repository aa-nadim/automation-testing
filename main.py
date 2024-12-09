import os
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
from tests.test_scrape_data import scrape_console_data
from tests.test_currency_filter import run_currency_filter_test  

os.makedirs("logs", exist_ok=True)

# Configure logging to save to file only
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/test_logs.log"),
    ]
)

def main():
    driver = None
    try:
        logging.info("Starting test execution...")

        driver = setup_driver(headless=False)
        driver.maximize_window()

        # Navigate to the test URL
        logging.info(f"Navigating to: {PROPERTY_URL}")
        driver.get(PROPERTY_URL)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            logging.info("Page loaded successfully.")
            logging.info(f"Page Title: {driver.title}")
        except Exception as load_error:
            logging.error(f"Error loading page: {load_error}")
            logging.error(f"Traceback: {traceback.format_exc()}")
            return

        # Run individual tests
        run_test(driver, PROPERTY_URL, test_h1_tag, "H1 tag existence test")
        run_test(driver, PROPERTY_URL, test_html_tag_sequence, "HTML tag sequence test")
        run_test(driver, PROPERTY_URL, test_image_alt_attribute, "Image alt attribute test")
        run_test(driver, PROPERTY_URL, test_url_status, "URL status code test")

        # Run the scraping function and save the data to CSV
        script_to_run = "return window.ScriptData;"  # Adjust script based on requirements
        scrape_console_data(script_to_run)

        # Run the test from test_currency_filter
        results = run_currency_filter_test(driver)
        logging.info(f"Currency filter test results: {results}")

        # Save a screenshot at the end of the tests
        screenshot_path = "screenshots/final_test_state.png"
        os.makedirs("screenshots", exist_ok=True)
        driver.save_screenshot(screenshot_path)
        logging.info(f"Screenshot saved at {screenshot_path}")

        logging.info("Test execution complete.")

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
