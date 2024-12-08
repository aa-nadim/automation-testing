# main.py

import logging
from utils.driver_setup import setup_driver
from utils.test_utils import run_test

from tests.test_h1_tag import test_h1_tag
from tests.test_html_tag_sequence import test_html_tag_sequence
from tests.test_image_alt_attribute import test_image_alt_attribute
from tests.test_url_status import test_url_status 

from config.config import PROPERTY_URL  # Import the property URL from config

# Configure logging for better visibility
logging.basicConfig(
    level=logging.DEBUG,  # Capture all levels of logs (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Timestamp, level, and message
    handlers=[
        logging.FileHandler("logs/test_logs.log"),  # Write logs to a file
        logging.StreamHandler()  # Also print logs to the console
    ]
)

def main():
    try:
        # Print starting message
        print("Starting the test execution...")

        # Set up the WebDriver
        logging.info("Setting up WebDriver...")
        driver = setup_driver()
        print("WebDriver setup complete.")

        # Run the H1 tag existence test
        print(f"Running test on URL: {PROPERTY_URL}")

        # Run the H1 tag existence test
        run_test(driver, PROPERTY_URL, test_h1_tag, "H1 tag existence test")
        # Run the HTML tag sequence test
        run_test(driver, PROPERTY_URL, test_html_tag_sequence, "HTML tag sequence test")
        # Run the Image alt attribute test
        run_test(driver, PROPERTY_URL, test_image_alt_attribute, "Image alt attribute test")
        # Run the URL status test
        run_test(driver, PROPERTY_URL, test_url_status, "URL status code test")

        print("Test execution complete.")

    except Exception as e:
        # Log and print any error that occurs during execution
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
    finally:
        # Ensure the WebDriver quits gracefully
        if 'driver' in locals():
            logging.info("Closing the WebDriver...")
            driver.quit()
            print("WebDriver closed.")
        else:
            logging.warning("WebDriver was not initialized, skipping quit.")

if __name__ == "__main__":
    main()
