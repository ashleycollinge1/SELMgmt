"""
This file contains the entry point to the test suite
"""
import sys
import unittest
from webapp.factory import create_app


class WebApp(unittest.TestCase):
    """
    Class for tests all relating to the web application
    """
    def setUp(self):
        flask_app = create_app()

    def tearDown(self):
        pass

    def test_the_test_route(self):
        pass


def main():
    """
    Run the unittests
    """
    unittest.main()

if __name__ == '__main__':
    main()
