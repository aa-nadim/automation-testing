# tests/test_html_tag_sequence.py

from selenium.webdriver.common.by import By
import logging

def test_html_tag_sequence(driver):
    """
    This test checks if HTML tags <h1> to <h6> are present and in the correct sequence.
    The sequence must be <h1>, <h2>, <h3>, <h4>, <h5>, <h6>.
    If any tag is missing or the sequence is broken, it fails.
    """
    try:
        logging.info("Checking HTML tag sequence from <h1> to <h6>...")

        # Find all H1 to H6 tags in order
        tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        tag_present = {}

        # Check if each tag is present
        for tag in tags:
            tag_present[tag] = len(driver.find_elements(By.TAG_NAME, tag)) > 0
            logging.debug(f"Found <{tag}> tag: {tag_present[tag]}")

        # Check for missing tags or broken sequence
        for i in range(len(tags)):
            # If a tag is missing but a tag before it exists, the sequence is broken
            if tag_present[tags[i]] == False:
                # Check if the previous tag exists
                if any(tag_present[tags[j]] for j in range(i)):
                    logging.error(f"Sequence broken: <{tags[i]}> is missing.")
                    return False, f"Sequence broken: <{tags[i]}> is missing"
                else:
                    logging.error(f"<{tags[i]}> tag is missing.")
                    return False, f"<{tags[i]}> tag is missing"

        logging.info("HTML tag sequence is correct.")
        return True, "HTML tag sequence is correct"
    
    except Exception as e:
        logging.error(f"Error while checking HTML tag sequence: {e}")
        return False, f"Error: {e}"
