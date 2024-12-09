# utils/test_utils2.py

import os
import csv
import logging
from config.config import REPORT_FILE_PATH, SCREENSHOT_DIR

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
