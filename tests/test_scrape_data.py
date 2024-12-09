import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import BASE_URL

# Function to initialize the browser
def init_browser():
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Function to perform the test case
def scrape_console_data(script_to_run):
    # Use BASE_URL from the config
    url = BASE_URL  # Retrieve URL from config
    
    # Initialize the browser
    driver = init_browser()
    
    try:
        # Open the test site URL
        driver.get(url)
        
        # Wait for the page to load completely
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Execute the script in the browser's console and retrieve the result
        console_data = driver.execute_script(script_to_run)

        # Check if console_data is None
        if console_data is None:
            print("No script data found.")
            return
        
        # Extract the relevant data from the console output
        page_data = console_data.get('pageData', {})
        config = console_data.get('config', {})
        user_info = console_data.get('userInfo', {})

        data = {
            "SiteURL": url,
            "CampaignID": page_data.get('CampaignId', 'N/A'),
            "SiteName": config.get('SiteName', 'N/A'),
            "Browser": user_info.get('Browser', 'N/A'),
            "CountryCode": user_info.get('CountryCode', 'N/A'),
            "IP": user_info.get('IP', 'N/A')
        }

        # Create the DataFrame to save the data to Excel
        df = pd.DataFrame([data])

        # Define the Excel file path
        file_path = 'reports/scraped_data.xlsx'

        # Check if the file already exists to decide whether to create a new file or append to the existing one
        if os.path.isfile(file_path):
            # Append to existing Excel file
            with pd.ExcelWriter(file_path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                # Get the current row count to append new rows
                sheet_name = 'ScrapedData'
                start_row = writer.sheets[sheet_name].max_row if sheet_name in writer.sheets else 0
                df.to_excel(writer, index=False, header=start_row == 0, startrow=start_row, sheet_name=sheet_name)
        else:
            # Create a new Excel file and write data
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='ScrapedData')

        print(f"Data saved for {url}")

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Close the browser
        driver.quit()

# Main function to run the tests
def run_tests():
    script_to_run = "return window.ScriptData;"  # Corrected the case to match the console variable
    
    # Perform the scraping and save data to Excel
    scrape_console_data(script_to_run)

# Execute the test
if __name__ == "__main__":
    run_tests()
