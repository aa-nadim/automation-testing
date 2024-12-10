import requests
from selenium.webdriver.common.by import By
from utils.test_utils import generate_report
import logging

def run_url_status_test(driver, page_url):
    """
    This test checks the status code of all URLs on the page.
    If any URL returns a 404 status code, the test fails.
    
    :param driver: Selenium WebDriver
    :param page_url: URL of the page to test
    :return: List of test results
    """
    test_results = []

    try:
        logging.info(f"Navigating to {page_url}...")
        driver.get(page_url)

        logging.info("Checking status codes for all URLs on the page...")

        # Find all anchor tags (<a>) with 'href' attributes
        links = driver.find_elements(By.TAG_NAME, "a")
        broken_links = []

        # Iterate through each link and check its status code
        for link in links:
            url = link.get_attribute("href")
            if url:  # Ensure that the href attribute is not empty
                # Filter out unwanted links
                if "redirect-partner" in url or "placeholder" in url:
                    logging.info(f"Skipping URL: {url}")
                    continue

                if "www.alojamiento.io" not in url:
                    logging.info(f"Skipping external URL: {url}")
                    continue

                try:
                    response = requests.get(url, allow_redirects=True, timeout=10)
                    logging.debug(f"Checked URL: {url} - Status Code: {response.status_code} - Response Time: {response.elapsed.total_seconds()}s")

                    # Check for 404 status code
                    if response.status_code == 404:
                        broken_links.append(url)
                        logging.debug(f"Broken link found: {url} (404)")

                except requests.RequestException as e:
                    logging.error(f"Error checking URL: {url} - {e}")
                    broken_links.append(url)

        # Record the test result for the page
        if broken_links:
            logging.error(f"{len(broken_links)} broken link(s) found: {broken_links}")
            test_results.append({
                'Page URL': page_url,
                'Test Case': "Check URL Status",
                'Status': False,
                'Comments': f"{len(broken_links)} broken link(s) found: {', '.join(broken_links)}"
            })
        else:
            logging.info("All URLs are valid (no 404 errors).")
            test_results.append({
                'Page URL': page_url,
                'Test Case': "Check URL Status",
                'Status': True,
                'Comments': "All URLs returned valid status codes."
            })

    except Exception as e:
        logging.error(f"Error while checking URL status: {e}")
        test_results.append({
            'Page URL': page_url,
            'Test Case': "Check URL Status",
            'Status': False,
            'Comments': f"Error: {str(e)}"
        })

    # Generate the Excel report
    generate_report(test_results, 'url_status_test')
    logging.info("URL status test completed. Results saved.")

    return test_results
