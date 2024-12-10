# Automation Testing

This project automates the testing of web properties using Selenium WebDriver. It performs various tests, including HTML validation, URL status checks, and custom data scraping. Results are logged and exported into reports for analysis.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
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
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
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

---

## File Structure

```plaintext
automation-testing/
├── config/
│   └── config.py          
├── logs/                  
├── reports/               
├── screenshots/           
├── tests/  
│   ├── test_h1_tag.py   
│   ├── test_html_tag_sequence.py   
│   ├── test_image_alt_attribute.py  
│   ├── test_url_status.py  
│   ├── test_currency_filter.py  
│   └── test_scrape_data.py              
├── utils/
│   ├── driver_setup.py    
│   └── test_utils.py
├── main.py                
├── .gitignore             
├── README.md              
└── requirements.txt       
```

---

## Tests Included

- **H1 Tag Test**: Validates the presence and content of `<h1>` tags.
- **HTML Tag Sequence Test**: Ensures proper sequencing of HTML tags.
- **Image Alt Attribute Test**: Checks for missing alt attributes in images.
- **URL Status Test**: Verifies the status of links on the page.
- **Console Data Scraping**: Extracts and logs custom data from the browser console.
- **Currency Filter Test**: Validates currency formatting and filters.
---



