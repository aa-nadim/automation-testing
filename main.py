# main.py
import os
import logging
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.driver_setup import setup_driver
from config.config import PROPERTY_URL
from tests.test_h1_tag import run_h1_tag_test
from tests.test_html_tag_sequence import run_html_tag_sequence_test
from tests.test_image_alt_attribute import run_image_alt_attribute_test
from tests.test_url_status import run_url_status_test
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

        driver = setup_driver(headless=True)
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


        run_h1_tag_test(driver, PROPERTY_URL)
        run_html_tag_sequence_test(driver, PROPERTY_URL)
        run_image_alt_attribute_test(driver, PROPERTY_URL)
        run_url_status_test(driver, PROPERTY_URL)
        run_currency_filter_test(driver, PROPERTY_URL)

        script_to_run = "return window.ScriptData;"  
        scrape_console_data(script_to_run)
        

        screenshot_path = "screenshots/after_test_state.png"
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
