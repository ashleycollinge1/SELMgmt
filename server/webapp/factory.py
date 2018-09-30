"""
This module is used to generate flask apps like a factory
"""
from flask import Flask
from webapp.views.general import ADMIN
from webapp.database import init_db, db_session
from webapp.models.general import Agents
from flask_login import LoginManager


def create_app():
    """
    Create instance of Flask, pass config options and return instance
    """
    app = Flask(__name__)
    app.register_blueprint(ADMIN)
    app.config['SECRET_KEY'] = 'agfsgev'
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "admin.login"

    init_db()
    @login_manager.user_loader
    def load_user(id):
        return db_session.query(Agents).get(int(id))
    return app
