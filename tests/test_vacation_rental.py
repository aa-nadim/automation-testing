# tests/test_vacation_rental.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.web_driver import setup_chrome_driver
from config.config import Config
import requests
import os

class VacationRentalTests:
    def __init__(self):
        self.driver = setup_chrome_driver()
        self.test_results = []
    
    def test_h1_existence(self, url):
        """
        Test if H1 tag exists on the page
        
        Args:
        url (str): Page URL to test
        
        Returns:
        dict: Test result
        """
        try:
            self.driver.get(url)
            h1_elements = self.driver.find_elements(By.TAG_NAME, 'h1')
            
            result = {
                'page_url': url,
                'testcase': 'H1 Tag Existence',
                'passed': len(h1_elements) > 0,
                'comments': 'H1 tag found' if h1_elements else 'No H1 tag present'
            }
        except Exception as e:
            result = {
                'page_url': url,
                'testcase': 'H1 Tag Existence',
                'passed': False,
                'comments': f'Error checking H1: {str(e)}'
            }
        
        self.test_results.append(result)
        return result
    
    def test_html_tag_sequence(self, url):
        """
        Test HTML tag sequence for SEO best practices
        
        Args:
        url (str): Page URL to test
        
        Returns:
        dict: Test result
        """
        try:
            self.driver.get(url)
            
            # Check for proper heading hierarchy
            headings = self.driver.find_elements(By.CSS_SELECTOR, 'h1, h2, h3, h4, h5, h6')
            heading_tags = [h.tag_name for h in headings]
            
            # Basic sequence check
            is_valid_sequence = all(
                int(tag[1]) <= int(next_tag[1]) 
                for tag, next_tag in zip(heading_tags, heading_tags[1:])
            )
            
            result = {
                'page_url': url,
                'testcase': 'HTML Tag Sequence',
                'passed': is_valid_sequence,
                'comments': 'Valid heading sequence' if is_valid_sequence else 'Improper heading hierarchy'
            }
        except Exception as e:
            result = {
                'page_url': url,
                'testcase': 'HTML Tag Sequence',
                'passed': False,
                'comments': f'Error checking tag sequence: {str(e)}'
            }
        
        self.test_results.append(result)
        return result
    
    def generate_report(self):
        """
        Generate Excel report from collected test results
        
        Returns:
        str: Path to generated report
        """
        from utils.report_generator import ReportGenerator
        return ReportGenerator.generate_report(self.test_results)
    
    def close(self):
        """
        Close the WebDriver
        """
        if self.driver:
            self.driver.quit()