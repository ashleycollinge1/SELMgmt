"""
This module is used to generate flask apps like a factory
"""
from flask import Flask
from webapp.views.general import ADMIN
from webapp.database import init_db


def create_app():
    """
    Create instance of Flask, pass config options and return instance
    """
    app = Flask(__name__)
    app.register_blueprint(ADMIN)
    init_db()
    return app
