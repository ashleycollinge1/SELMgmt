"""
This module is used to generate flask apps like a factory
"""
from flask import Flask
from webapp.views.general import AGENT


def create_app():
    """
    Create instance of Flask, pass config options and return instance
    """
    app = Flask(__name__)
    app.register_blueprint(AGENT)
    return app
