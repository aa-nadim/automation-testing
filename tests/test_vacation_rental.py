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
    
    def test_image_alt_attributes(self, url):
        """
        Test images for alt attributes
        
        Args:
        url (str): Page URL to test
        
        Returns:
        dict: Test result
        """
        try:
            self.driver.get(url)
            images = self.driver.find_elements(By.TAG_NAME, 'img')
            
            images_without_alt = [img for img in images if not img.get_attribute('alt')]
            
            result = {
                'page_url': url,
                'testcase': 'Image Alt Attributes',
                'passed': len(images_without_alt) == 0,
                'comments': f'{len(images_without_alt)} images missing alt attributes' 
                            if images_without_alt else 'All images have alt attributes'
            }
        except Exception as e:
            result = {
                'page_url': url,
                'testcase': 'Image Alt Attributes',
                'passed': False,
                'comments': f'Error checking image alt attributes: {str(e)}'
            }
        
        self.test_results.append(result)
        return result
    
    def test_url_availability(self, url):
        """
        Test if URLs on the page are accessible
        
        Args:
        url (str): Page URL to test
        
        Returns:
        dict: Test result
        """
        try:
            self.driver.get(url)
            links = self.driver.find_elements(By.TAG_NAME, 'a')
            
            broken_links = []
            for link in links:
                href = link.get_attribute('href')
                if href and href.startswith('http'):
                    try:
                        response = requests.head(href, timeout=5)
                        if response.status_code >= 400:
                            broken_links.append(href)
                    except requests.RequestException:
                        broken_links.append(href)
            
            result = {
                'page_url': url,
                'testcase': 'URL Availability',
                'passed': len(broken_links) == 0,
                'comments': f'{len(broken_links)} broken URLs found: {", ".join(broken_links)}'
                            if broken_links else 'All URLs are accessible'
            }
        except Exception as e:
            result = {
                'page_url': url,
                'testcase': 'URL Availability',
                'passed': False,
                'comments': f'Error checking URL availability: {str(e)}'
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