# Automation Testing

This project automates the testing of web properties using Selenium WebDriver. It performs various tests, including HTML validation, URL status checks, and custom data scraping. Results are logged and exported into reports for analysis.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Tests Included](#tests-included)

---

## Features

- Automates browser-based testing using Selenium.
- Executes tests for HTML tag validation, image attributes, URL statuses, and more.
- Logs results to a file for debugging and analysis.
- Generates Excel reports with detailed test results.
- Takes screenshots of test outcomes for reference.

---

## Prerequisites

- Python 3.8+
- Google Chrome Browser
- ChromeDriver (managed by `webdriver-manager`)

---

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/aa-nadim/automation-testing.git
    cd automation-testing
    ```

2. Create a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .venv/Scripts/activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

1. Update the configuration in `config/config.py` as needed:
   - `PROPERTY_URL`: The URL of the property to test.
   - Paths for logs, screenshots, and reports.

2. Run the script:
    ```bash
    python main.py
    ```

3. Check the following for results:
   - **Logs**: `logs/test_logs.log`
   - **Reports**: `reports/test_result.xlsx`
   - **Screenshots**: `screenshots/`

4. In `reports/test_result.xlsx`, you will find the test results presented in a tabular format across six sheets:

   -  **h1_tag_test**
   -  **html_tag_sequence_test**
   -  **image_alt_attribute_test**
   -  **url_status_test**
   -  **currency_filter_test**
   -  **ScrapedData**

---

## Tests Included

- **H1 Tag Test**: Validates the presence and content of `<h1>` tags.
- **HTML Tag Sequence Test**: Ensures proper sequencing of HTML tags.
- **Image Alt Attribute Test**: Checks for missing alt attributes in images.
- **URL Status Test**: Verifies the status of links on the page.
- **Console Data Scraping**: Extracts and logs custom data from the browser console.
- **Currency Filter Test**: Validates currency formatting and filters.
---



