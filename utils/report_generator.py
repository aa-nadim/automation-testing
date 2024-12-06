# utils/report_generator.py
import os
import pandas as pd
from datetime import datetime
from config.config import Config

class ReportGenerator:
    @staticmethod
    def generate_report(test_results):
        """
        Generate or update Excel report with change tracking
        
        Args:
        test_results (list): List of dictionaries containing test results
        
        Returns:
        str: Path to generated/updated report
        """
        try:
            # Ensure the results are not empty
            if not test_results:
                print("No test results to generate report.")
                return None

            # Convert test results to DataFrame
            current_df = pd.DataFrame(test_results)
            
            # Add timestamp column
            current_df['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Ensure reports directory exists
            os.makedirs(os.path.dirname(Config.REPORT_PATH), exist_ok=True)
            
            # Check if report file already exists
            if os.path.exists(Config.REPORT_PATH):
                # Read existing report
                existing_df = pd.read_excel(Config.REPORT_PATH)
                
                # Compare current results with previous results
                def compare_results(row):
                    # Find matching previous test
                    prev_tests = existing_df[
                        (existing_df['page_url'] == row['page_url']) & 
                        (existing_df['testcase'] == row['testcase'])
                    ]
                    
                    # If previous test exists, add change tracking
                    if not prev_tests.empty:
                        prev_test = prev_tests.iloc[0]
                        row['previous_status'] = prev_test['passed']
                        row['status_changed'] = row['passed'] != prev_test['passed']
                    else:
                        row['previous_status'] = 'N/A'
                        row['status_changed'] = True
                    
                    return row

                # Apply comparison
                current_df = current_df.apply(compare_results, axis=1)
                
                # Append new results to existing DataFrame
                final_df = pd.concat([existing_df, current_df], ignore_index=True)
            else:
                # If no existing file, use current results
                final_df = current_df
                
                # Add columns for first run
                final_df['previous_status'] = 'N/A'
                final_df['status_changed'] = True

            # Write to Excel
            final_df.to_excel(Config.REPORT_PATH, index=False)
            print(f"Report updated: {Config.REPORT_PATH}")
            
            # Print summary of changes
            changes = final_df[final_df['status_changed']]
            if not changes.empty:
                print("\n🔍 Changes Detected:")
                for _, change in changes.iterrows():
                    print(f"- {change['testcase']} on {change['page_url']}:")
                    print(f"  Previous Status: {change['previous_status']}")
                    print(f"  Current Status: {change['passed']}")
            
            return Config.REPORT_PATH
        
        except Exception as e:
            print(f"Error generating report: {e}")
            import traceback
            traceback.print_exc()
            return None