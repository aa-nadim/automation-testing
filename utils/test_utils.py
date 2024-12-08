# utils/test_utils.py

import os
import csv
import logging
from config.config import REPORT_FILE_PATH, SCREENSHOT_DIR  # Import configuration

# Ensure the reports directory exists
def create_report_directory():
    if not os.path.exists("reports"):
        os.makedirs("reports")
        logging.info("Created reports directory.")

def read_existing_reports(filename=REPORT_FILE_PATH):
    """Read the existing CSV file and return a list of rows (test results)."""
    existing_rows = []
    if os.path.isfile(filename):
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            existing_rows = list(reader)
    return existing_rows

def write_to_csv(test_data, filename=REPORT_FILE_PATH):
    create_report_directory()  # Ensure the reports directory exists

    # Read existing reports to check if the test result already exists
    existing_reports = read_existing_reports(filename)
    
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)

            # If the file is empty, write the header
            if not existing_reports:
                writer.writerow(['page_url', 'testcase', 'status', 'comments'])
                logging.info("Created new report file with header.")
            
            updated = False  # Flag to track if we updated an existing test result
            for row in existing_reports:
                # Check if the row matches the test (same URL and test name)
                if row[0] == test_data[0] and row[1] == test_data[1]:
                    writer.writerow(test_data)  # Update the existing test result
                    updated = True
                else:
                    writer.writerow(row)  # Keep existing rows unchanged
            
            # If the test result didn't exist before, append it
            if not updated:
                writer.writerow(test_data)
                logging.info(f"Appended test result for {test_data[1]}.")

    except Exception as e:
        logging.error(f"Error writing to CSV: {e}")
        print(f"Error writing to CSV: {e}")

def run_test(driver, url, test_func, test_name):
    """Run a test function and write results to a CSV file."""
    try:
        logging.info(f"Running test: {test_name} on {url}")
        driver.get(url)
        
        # Log the start of the test
        print(f"Running {test_name} on {url}...")
        
        result, comments = test_func(driver)
        status = 'PASS' if result else 'FAIL'
        
        # Write results to CSV
        write_to_csv([url, test_name, status, comments])

        # Log the result of the test
        logging.info(f"Test result for {test_name}: {status}. Comments: {comments}")
        print(f"Test result for {test_name}: {status}. Comments: {comments}")
    except Exception as e:
        logging.error(f"Error during {test_name}: {e}")
        print(f"Error during {test_name}: {e}")
        write_to_csv([url, test_name, 'FAIL', str(e)])
