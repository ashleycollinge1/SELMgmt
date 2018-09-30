"""
This contains all of the 'general' views relating to the flask app
"""
import socket
import getpass
from flask import Blueprint, jsonify, request

AGENT = Blueprint('agent', __name__, url_prefix='/agent')

@AGENT.route('/ping')
def ping():
    """
    ping function, returns pong
    """
    return jsonify({'response': 'pong'})

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
                    'username': '{}'.format(getpass.getuser()),
                    'agent_version': '0.0.1'})

@AGENT.route('/map-network-drive', methods=['POST'])
def map_network_drive():
    """
    map the network drive based on post data
    """
    if request.method == 'POST':
        if not request.get_json()['network_location']:
            return jsonify({'error': 'network_location not present'}), 400
        network_location = request.get_json()['network_location']
        # map network drive here
        import subprocess
        command = 'net use * {} /user:synseal.com\\%username%'.format(network_location)
        subprocess.call(command, shell=True)#net use * \\10.1.23.14\Backup /user:synseal.com\%username%
        return jsonify({'message': {'network_location': network_location}})
