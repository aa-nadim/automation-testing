import os
import pandas as pd
from datetime import datetime
from openpyxl import load_workbook

def generate_report(test_results, test_name):
    """
    Generate an Excel report for a specific test. If the sheet exists, append the data;
    otherwise, create a new sheet.
    
    :param test_results: List of dictionaries containing test results
    :param test_name: Name of the test for the sheet in the Excel report
    """
    # Define reports directory and ensure it exists
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)

    # Define the report filename
    filename = f"{reports_dir}/test_result.xlsx"

    # Convert test results to a DataFrame
    df = pd.DataFrame(test_results)

    if os.path.exists(filename):
        # Load the existing workbook
        workbook = load_workbook(filename)

        # Check if the sheet exists
        if test_name in workbook.sheetnames:
            # Append data to the existing sheet
            sheet = workbook[test_name]
            for row in df.itertuples(index=False, name=None):
                sheet.append(row)
            workbook.save(filename)
            print(f"Data appended to existing sheet: {test_name}")
        else:
            # Add a new sheet and write data
            with pd.ExcelWriter(filename, engine='openpyxl', mode='a') as writer:
                df.to_excel(writer, index=False, sheet_name=test_name)
            print(f"New sheet created and data written: {test_name}")
    else:
        # Create a new file and write data
        with pd.ExcelWriter(filename, engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, index=False, sheet_name=test_name)
        print(f"New file created with sheet: {test_name}")

    return filename
