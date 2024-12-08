# main.py

from utils.driver_setup import setup_driver
from utils.test_utils import run_test
from tests.test_h1_tag import test_h1_tag
from config.config import PROPERTY_URL  # Import the property URL from config

if __name__ == "__main__":
    driver = setup_driver()
    
    # Run the H1 tag existence test on the specified URL
    run_test(driver, PROPERTY_URL, test_h1_tag, "H1 tag existence test")

    driver.quit()
