"""
This contains all of the 'general' views relating to the flask app
"""
import socket
from flask import Blueprint, jsonify

AGENT = Blueprint('agent', __name__, url_prefix='/agent')

@AGENT.route('/test')
def test():
    """
    test function, returns hello world to the browser/client
    """
    return 'hello world'

@AGENT.route('/whoami', methods=['GET'])
def whoami():
    """
    Returns the version of agent, primary ip address, and the
    hostname of the machine
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('10.255.255.255', 1))
    IP = s.getsockname()[0]
    return jsonify({'hostname': '{}'.format(socket.gethostname()),
                    'ip_address': '{}'.format(IP),
                    'agent_version': '0.0.1'})
