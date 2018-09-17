"""
Run all of the tests from here
"""
import unittest
import xmlrunner
from testing.testsuite import WebApp

def main():
    """
    Run the unittests
    """
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))

if __name__ == '__main__':
    main()
