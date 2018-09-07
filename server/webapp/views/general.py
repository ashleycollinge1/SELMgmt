"""
This contains all of the 'general' views relating to the flask app
"""
from flask import Blueprint

ADMIN = Blueprint('admin', __name__, url_prefix='/admin')

@ADMIN.route('/test')
def test():
    """
    test function, returns hello world to the browser/client
    """
    return 'hello world'
