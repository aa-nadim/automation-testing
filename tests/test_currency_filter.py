# tests/test_currency_filter.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from config.config import PROPERTY_URL

from utils.driver_setup import setup_driver
from utils.test_utils import generate_report
import time

def run_currency_filter_test(driver):
    """
    Robust test to ensure property tile currency changes when selecting different currencies.
    
    :param driver: Selenium WebDriver
    :return: List of test results
    """
    test_results = []

    try:
        print(f"Navigating to {PROPERTY_URL}...")
        driver.get(PROPERTY_URL)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "js-price-value"))
        )
        
        try:
            currency_dropdown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "js-currency-sort-footer"))
            )
        except TimeoutException:
            currency_dropdown = driver.find_element(By.CSS_SELECTOR, "#js-currency-sort-footer")
        
        driver.execute_script("arguments[0].scrollIntoView(true);", currency_dropdown)
        time.sleep(2)
        
        try:
            driver.execute_script("arguments[0].click();", currency_dropdown)
        except Exception:
            ActionChains(driver).move_to_element(currency_dropdown).click().perform()
        
        time.sleep(2)
        currency_options = driver.find_elements(By.CSS_SELECTOR, "#js-currency-sort-footer .select-ul li")
        print(f"Found {len(currency_options)} currency options.")
        
        for currency_option in currency_options:
            try:
                currency_code = currency_option.get_attribute("data-currency-country") or "Unknown"
                currency_symbol = currency_option.find_element(By.TAG_NAME, "p").text.strip()
                
                driver.execute_script("arguments[0].click();", currency_option)
                
                WebDriverWait(driver, 10).until(
                    EC.text_to_be_present_in_element(
                        (By.CLASS_NAME, "js-price-value"), currency_symbol
                    )
                )
                
                property_tiles = driver.find_elements(By.CLASS_NAME, "js-price-value")
                updated_prices = [tile.text for tile in property_tiles]
                
                test_passed = all(currency_symbol in price for price in updated_prices)
                
                test_results.append({
                    'Page URL': PROPERTY_URL,
                    'Test Case': f"Currency Change to {currency_code}",
                    'Status': test_passed,
                    'Comments': f"Updated prices: {updated_prices}"
                })
                
                driver.execute_script("arguments[0].click();", currency_dropdown)
                time.sleep(1)
                
            except Exception as e:
                print(f"Error processing currency {currency_code}: {str(e)}")
                test_results.append({
                    'page_url': PROPERTY_URL,
                    'Test Case': f"Currency Change to {currency_code}",
                    'Status': False,
                    'Comments': f"Test failed: {str(e)}"
                })
        
        generate_report(test_results, 'currency_filtering_test')
        print("Currency filtering test completed. Results saved.")
        
    except Exception as e:
        print(f"Critical error during test: {str(e)}")
        test_results.append({
            'Page URL': PROPERTY_URL,
            'Test Case': "Currency Change Test",
            'Status': False,
            'Comments': f"Critical error: {str(e)}"
        })
    
    return test_results
