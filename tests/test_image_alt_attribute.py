from selenium.webdriver.common.by import By
from utils.test_utils import generate_report
import logging

def run_image_alt_attribute_test(driver, page_url):
    """
    This test checks if all <img> tags on the page have an alt attribute.
    If any <img> tag is missing the alt attribute, the test fails.
    
    :param driver: Selenium WebDriver
    :param page_url: URL of the page to test
    :return: List of test results
    """
    test_results = []

    try:
        logging.info(f"Navigating to {page_url}...")
        driver.get(page_url)

        logging.info("Checking for missing alt attributes on <img> tags...")
        
        # Find all <img> elements
        images = driver.find_elements(By.TAG_NAME, "img")
        missing_alt = []

        # Check if each image has an 'alt' attribute
        for image in images:
            alt = image.get_attribute("alt")
            if not alt:
                missing_alt.append(image)
                logging.debug("Image without alt attribute found.")

        if missing_alt:
            # If there are images without alt attributes, the test fails
            logging.error(f"{len(missing_alt)} image(s) missing alt attribute.")
            test_results.append({
                'Page URL': page_url,
                'Test Case': "Check Image Alt Attribute",
                'Status': False,
                'Comments': f"{len(missing_alt)} image(s) missing alt attribute."
            })
        else:
            logging.info("All images have alt attributes.")
            test_results.append({
                'Page URL': page_url,
                'Test Case': "Check Image Alt Attribute",
                'Status': True,
                'Comments': "All images have alt attributes."
            })

    except Exception as e:
        logging.error(f"Error while checking image alt attributes: {e}")
        test_results.append({
            'Page URL': page_url,
            'Test Case': "Check Image Alt Attribute",
            'Status': False,
            'Comments': f"Error: {str(e)}"
        })

    # Generate the Excel report
    generate_report(test_results, 'image_alt_attribute_test')
    logging.info("Image alt attribute test completed. Results saved.")

    return test_results
