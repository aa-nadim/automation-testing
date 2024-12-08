# tests/test_currency_filter.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time

def test_currency_filter(driver):
    """
    This test checks if property tiles update their prices correctly when the currency filter is changed.
    """
    try:
        logging.info("Performing currency filter test...")

        # Locate the dropdown container
        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "js-currency-sort-footer"))
        )
        logging.info("Currency dropdown located.")

        # Click to open the dropdown
        dropdown.click()
        logging.info("Currency dropdown clicked.")

        # Select a new currency (EUR in this case)
        currency_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "li[data-currency-country='BE']"))
        )
        currency_option.click()
        logging.info("Selected currency: EUR (Euro).")
        time.sleep(3)  # Wait for prices to update

        # Verify that the property tile prices have updated
        property_tile = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "property-tile"))  # Adjust class as needed
        )
        updated_currency_symbol = property_tile.find_element(By.CLASS_NAME, "price-currency").text.strip()  # Adjust class as needed
        logging.debug(f"Updated currency symbol: {updated_currency_symbol}")

        if updated_currency_symbol == "€":
            logging.info("Currency filter test passed.")
            return True, "Property tiles updated to EUR currency."
        else:
            logging.error("Currency filter test failed: Currency did not update.")
            return False, "Currency filter test failed: Currency did not update."

    except Exception as e:
        logging.error(f"Error during currency filter test: {e}")
        return False, f"Error: {e}"
