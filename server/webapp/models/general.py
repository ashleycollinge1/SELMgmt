"""
This contains all of the 'general' models relating to the flask app
"""
from webapp.database import Base
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy import Column, Integer, String
#from flask.ext.login import LoginManager, UserMixin
from flask_login import LoginManager, UserMixin


class Agents(Base, UserMixin):
    __tablename__ = 'Agents'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hash = Column(String)
    hostname = Column(String)
    windows_user = Column(String)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
