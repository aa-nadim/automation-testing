# main.py
import sys
import logging
from tests.test_vacation_rental import VacationRentalTests
from config.config import Config
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('logs/test_logs.log'),  # Log to file
        logging.StreamHandler(sys.stdout)  # Log to console
    ]
)
logger = logging.getLogger(__name__)

def run_tests():
    """
    Comprehensive test execution with detailed logging
    """
    # Track overall test status
    all_tests_passed = True
    
    try:
        # Clear previous log if needed
        open('logs/test_logs.log', 'w').close()
        
        logger.info("🚀 Starting Vacation Rental Website Automation Tests")
        logger.info("=" * 50)
        
        # Initialize tests
        rental_tests = VacationRentalTests()
        
        # List of tests to run
        test_methods = [
            ('H1 Tag Test', rental_tests.test_h1_existence),
        ]
        
        # Run each test and log results
        for test_name, test_method in test_methods:
            logger.info(f"\n📋 Running Test: {test_name}")
            try:
                result = test_method(Config.BASE_URL)
                
                # Determine test status
                status = "✅ PASSED" if result['passed'] else "❌ FAILED"
                logger.info(f"{status}: {test_name}")
                logger.info(f"Comments: {result['comments']}")
                
                # Update overall test status
                if not result['passed']:
                    all_tests_passed = False
            
            except Exception as test_error:
                logger.error(f"❌ Error in {test_name}: {test_error}")
                logger.error(traceback.format_exc())
                all_tests_passed = False
        
        # Generate final report
        logger.info("\n📊 Generating Test Report...")
        report_path = rental_tests.generate_report()
        logger.info(f"✨ Test Report Generated: {report_path}")
        
        # Final status
        if all_tests_passed:
            logger.info("\n🎉 All Tests Completed Successfully!")
        else:
            logger.warning("\n⚠️ Some Tests Failed. Check the report for details.")
    
    except Exception as e:
        logger.error(f"❌ Critical Error during test execution: {e}")
        logger.error(traceback.format_exc())
        all_tests_passed = False
    
    finally:
        # Always close the driver
        try:
            rental_tests.close()
        except:
            pass
    
    return all_tests_passed

def main():
    try:
        # Run tests and get result
        test_result = run_tests()
        
        # Set exit code based on test results
        sys.exit(0 if test_result else 1)
    
    except KeyboardInterrupt:
        logger.info("\n🛑 Test execution interrupted by user.")
        sys.exit(1)

if __name__ == "__main__":
    main()