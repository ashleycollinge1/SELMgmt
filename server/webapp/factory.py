"""
This module is used to generate flask apps like a factory
"""
from flask import Flask
from webapp.views.general import ADMIN


def create_app():
    """
    Create instance of Flask, pass config options and return instance
    """
    app = Flask(__name__)
    app.register_blueprint(ADMIN)
    return app

def create_app_testing():
	"""
	Create instance of Flask, but with testing=True
	Allows test_client() to be used
	"""
	app = Flask(__name__)
	app.config['TESTING'] = True
	app.register_blueprint(ADMIN)
	return app
