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

    def test_the_whoami_route(self):
        """
        test whether the whoami route returns all of the data
        and it's the correct return
        """
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
        reply = self.client.get('/agent/whoami')
        assert {'hostname': socket.gethostname(),
                'ip_address': '{}'.format(IP),
                'agent_version': '0.0.1'}


def main():
    """
    Run the unittests
    """
    unittest.main()

if __name__ == '__main__':
    main()
