# utils/test_utils.py

import os
import csv
from config.config import REPORT_FILE_PATH, SCREENSHOT_DIR  # Import configuration

def create_report_directory():
    """Create the reports directory if it doesn't exist."""
    if not os.path.exists("reports"):
        os.makedirs("reports")

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

    except Exception as e:
        print(f"Error writing to CSV: {e}")

def run_test(driver, url, test_func, test_name):
    """Run a test function and write results to a CSV file."""
    try:
        driver.get(url)
        result, comments = test_func(driver)
        status = 'PASS' if result else 'FAIL'
        write_to_csv([url, test_name, status, comments])
    except Exception as e:
        write_to_csv([url, test_name, 'FAIL', str(e)])
