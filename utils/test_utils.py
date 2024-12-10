import os
import pandas as pd
from datetime import datetime

def generate_report(test_results, test_name):
    """
    Generate an Excel report for a specific test with multiple sheets in one file.
    
    :param test_results: List of dictionaries containing test results
    :param test_name: Name of the test for report naming
    """
    # Create reports directory if not exists
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)

    # Create DataFrame from test results
    df = pd.DataFrame(test_results)

    # Generate unique filename with timestamp for the Excel file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{reports_dir}/test_result.xlsx"

    # Check if the file exists
    file_exists = os.path.exists(filename)
    
    # If the file exists, we append data to it
    if file_exists:
        with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='new') as writer:
            df.to_excel(writer, index=False, sheet_name=test_name)
    else:
        # If the file doesn't exist, create it and write the data
        with pd.ExcelWriter(filename, engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, index=False, sheet_name=test_name)

    print(f"Report generated: {filename}")
    return filename