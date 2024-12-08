# tests/test_url_status.py

import requests
from selenium.webdriver.common.by import By
import logging

def test_url_status(driver):
    """
    This test checks the status code of all URLs on the page.
    If any URL returns a 404 status code, the test fails.
    """
    try:
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

        # If there are broken links, fail the test
        if broken_links:
            logging.error(f"{len(broken_links)} broken link(s) found: {broken_links}")
            return False, f"{len(broken_links)} broken link(s) found: {', '.join(broken_links)}"
        
        logging.info("All URLs are valid (no 404 errors).")
        return True, "All URLs returned valid status codes."

    except Exception as e:
        logging.error(f"Error while checking URL status: {e}")
        return False, f"Error: {e}"
