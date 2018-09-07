"""
This contains all of the 'general' views relating to the flask app
"""
from flask import Blueprint

AGENT = Blueprint('agent', __name__, url_prefix='/agent')

@AGENT.route('/test')
def test():
    """
    test function, returns hello world to the browser/client
    """
    return 'hello world'
