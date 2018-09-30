"""
This contains all of the 'general' views relating to the flask app
"""
from flask import Blueprint, request, abort, jsonify
import flask
import flask_login
from webapp.models.general import Agents
#from flask.ext.login import LoginManager, UserMixin, \
 #                               login_required, login_user, logout_user 
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

from webapp.database import db_session as session

ADMIN = Blueprint('admin', __name__, url_prefix='/admin')




@ADMIN.route('/test')
def test():
    """
    test function, returns hello world to the browser/client
    """
    return 'hello world'

 # somewhere to login
@ADMIN.route("/login", methods=["POST"])
def login():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        agent = session.query(Agents).filter_by(username=username).first()
        if agent.verify_password(password):
            flask_login.login_user(agent)
            return jsonify({'login': 'successful'})
        else:
            return abort(401)

# somewhere to logout
@ADMIN.route("/logout")
@flask_login.login_required
def logout():
    logout_user()
    return jsonify({'loggedout': True})

@ADMIN.route('/api/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        return jsonify({'message':'1st'}), 400
    result = Agents.query.filter_by(username = username).first()
    if Agents.query.filter_by(username = username).first() is not None:
        return jsonify({'message': 'username already being used'}), 400
    agent = Agents(username = username)
    agent.hash_password(password)
    session.add(agent)
    session.commit()
    return jsonify({'username': username})


@ADMIN.route('/hello', methods = ['GET'])
@login_required
def hello():
    return jsonify({'user': flask_login.current_user.username})

@ADMIN.route('/api/users', methods = ['GET'])
def get_users():
    results = Agents.query.all()
    accounts = []
    for i in results:
        account = {}
        account['username'] = i.username
        account['password'] = i.password_hash
        accounts.append(account)
    return jsonify(accounts)
