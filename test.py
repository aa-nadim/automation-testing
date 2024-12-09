# test.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from config.config import PROPERTY_URL
from utils.test_utils2 import write_to_csv
from utils.driver_setup2 import setup_driver
import time

def run_currency_filter_test(driver):
    """
    Robust test to ensure property tile currency changes when selecting different currencies.
    
    :param driver: Selenium WebDriver
    :return: List of test results
    """
    test_results = []
    base_url = PROPERTY_URL
    page_url = PROPERTY_URL

    try:
        # Navigate to the test URL
        print(f"Navigating to {base_url}...")
        driver.get(base_url)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "js-price-value"))
        )
        
        # Find currency dropdown using multiple strategies
        try:
            currency_dropdown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "js-currency-sort-footer"))
            )
        except TimeoutException:
            # Fallback to finding by CSS selector
            currency_dropdown = driver.find_element(By.CSS_SELECTOR, "#js-currency-sort-footer")
        
        # Force scroll and click using JavaScript
        driver.execute_script("arguments[0].scrollIntoView(true);", currency_dropdown)
        time.sleep(2)  # Allow time for scroll
        
        # Try multiple ways to open dropdown
        try:
            driver.execute_script("arguments[0].click();", currency_dropdown)
        except Exception:
            ActionChains(driver).move_to_element(currency_dropdown).click().perform()
        
        # Wait and get currency options
        time.sleep(2)  # Additional wait for dropdown to populate
        currency_options = driver.find_elements(By.CSS_SELECTOR, "#js-currency-sort-footer .select-ul li")
        print(f"Found {len(currency_options)} currency options.")
        
        # Iterate through currency options
        for currency_option in currency_options:
            try:
                # Extract currency details
                currency_code = currency_option.get_attribute("data-currency-country") or "Unknown"
                currency_symbol = currency_option.find_element(By.TAG_NAME, "p").text.strip()
                
                # Force click using JavaScript
                driver.execute_script("arguments[0].click();", currency_option)
                
                # Wait for price update
                WebDriverWait(driver, 10).until(
                    EC.text_to_be_present_in_element(
                        (By.CLASS_NAME, "js-price-value"), currency_symbol
                    )
                )
                
                # Get all price elements (property tiles) on the page
                property_tiles = driver.find_elements(By.CLASS_NAME, "js-price-value")
                
                # Get updated price for each property tile
                updated_prices = [tile.text for tile in property_tiles]
                
                # Check if all property tiles have the correct currency symbol
                test_passed = all(currency_symbol in price for price in updated_prices)
                
                # Append test result
                test_results.append({
                    'page_url': page_url,
                    'testcase': f"Currency Change to {currency_code}",
                    'status': 'PASS' if test_passed else 'FAIL',
                    'comments': f"Updated prices: {updated_prices}"
                })
                
                # Reopen dropdown to change to next currency
                driver.execute_script("arguments[0].click();", currency_dropdown)
                time.sleep(1)
                
            except Exception as e:
                print(f"Error processing currency {currency_code}: {str(e)}")
                test_results.append({
                    'page_url': page_url,
                    'testcase': f"Currency Change to {currency_code}",
                    'status': 'FAIL',
                    'comments': f"Test failed: {str(e)}"
                })
        
        # Save the results to a CSV file
        write_to_csv(test_results, 'currency_filtering_test')
        print("Currency filtering test completed. Results saved.")
        
    except Exception as e:
        print(f"Critical error during test: {str(e)}")
        test_results.append({
            'page_url': page_url,
            'testcase': "Currency Change Test",
            'status': 'FAIL',
            'comments': f"Critical error: {str(e)}"
        })
    
    return test_results


if __name__ == "__main__":
    driver = setup_driver()
    try:
        results = run_currency_filter_test(driver)
    finally:
        driver.quit()
