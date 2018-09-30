"""
This file contains the entry point to the test suite
"""
import sys
import json
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
        Test whether getting from /admin/ping returns the correct
        response
        """
        reply = self.client.get('/agent/ping')
        json_data = json.loads(reply.data)
        assert 'response' in json_data
        assert 'pong' in json_data['response']

    def test_the_whoami_route(self):
        """
        test whether the whoami route returns all of the data
        """
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
        reply = self.client.get('/agent/whoami')
        json_data = json.loads(reply.data)
        assert 'hostname' in json_data
        assert 'ip_address' in json_data
        assert 'agent_version' in json_data

    def test_the_network_drive(self):
        """
        test whether the map network drive
        endpoint works
        """
        response=self.client.post('/agent/map-network-drive', 
                       data=json.dumps({'network_location': '\\\\10.1.23.14\\Backup'}),
                       content_type='application/json')
        #reply = self.client.post('/agent/map-network-drive', data={'network_location': '\\\\10.1.23.14\\Backup'})
        json_data = json.loads(response.data)
        assert 'message' in json_data
        assert 'network_location' in json_data['message']


def main():
    """
    Run the unittests
    """
    unittest.main()

if __name__ == '__main__':
    main()
