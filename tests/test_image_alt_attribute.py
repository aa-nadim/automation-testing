# tests/test_image_alt_attribute.py

from selenium.webdriver.common.by import By
import logging

def test_image_alt_attribute(driver):
    """
    This test checks if all <img> tags on the page have an alt attribute.
    If any <img> tag is missing the alt attribute, the test fails.
    """
    try:
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
            return False, f"{len(missing_alt)} image(s) missing alt attribute."

        logging.info("All images have alt attributes.")
        return True, "All images have alt attributes."
    
    except Exception as e:
        logging.error(f"Error while checking image alt attributes: {e}")
        return False, f"Error: {e}"
