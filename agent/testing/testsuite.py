"""
This file contains the entry point to the test suite
"""
import sys
import unittest
from flask import Flask
from webapp.views.general import AGENT


class WebApp(unittest.TestCase):
    """
    Class for tests all relating to the web application
    """
    def setUp(self):
        """
        Set up of Flask app testing instance
        Uses app.test_client()
        """
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.register_blueprint(AGENT)
        self.client = app.test_client()

    def tearDown(self):
        """
        Called at the end of every test
        """
        pass

    def test_the_test_route(self):
        """
        Test whether getting from /admin/test returns the correct
        response
        """
        reply = self.client.get('/agent/test')
        assert b'hello world' in reply.data


def main():
    """
    Run the unittests
    """
    unittest.main()

if __name__ == '__main__':
    main()
