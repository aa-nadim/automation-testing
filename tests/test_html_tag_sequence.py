# tests/test_html_tag_sequence.py
from selenium.webdriver.common.by import By
from utils.test_utils import generate_report
import logging

def run_html_tag_sequence_test(driver, page_url):
    """
    This test checks if HTML tags <h1> to <h6> are present and in the correct sequence.
    The sequence must be <h1>, <h2>, <h3>, <h4>, <h5>, <h6>.
    If any tag is missing or the sequence is broken, it fails.
    
    :param driver: Selenium WebDriver
    :param page_url: URL of the page to test
    :return: List of test results
    """
    test_results = []

    try:
        logging.info(f"Navigating to {page_url}...")
        driver.get(page_url)
        
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
                    test_results.append({
                        'Page URL': page_url,
                        'Test Case': f"HTML Tag Sequence Test",
                        'Status': False,
                        'Comments': f"Sequence broken: <{tags[i]}> is missing"
                    })
                    break
                else:
                    logging.error(f"<{tags[i]}> tag is missing.")
                    test_results.append({
                        'Page URL': page_url,
                        'Test Case': f"HTML Tag Sequence Test",
                        'Status': False,
                        'Comments': f"<{tags[i]}> tag is missing"
                    })
                    break
        else:
            logging.info("HTML tag sequence is correct.")
            test_results.append({
                'Page URL': page_url,
                'Test Case': "HTML Tag Sequence Test",
                'Status': True,
                'Comments': "HTML tag sequence is correct"
            })
    
    except Exception as e:
        logging.error(f"Error while checking HTML tag sequence: {e}")
        test_results.append({
            'Page URL': page_url,
            'Test Case': "HTML Tag Sequence Test",
            'Status': False,
            'Comments': f"Error: {str(e)}"
        })
    
    # Generate the Excel report
    generate_report(test_results, 'html_tag_sequence_test')
    logging.info("HTML tag sequence test completed. Results saved.")
    
    return test_results
