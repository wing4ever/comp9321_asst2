from flask import Blueprint, render_template, redirect, url_for, request, jsonify, make_response, json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired
import uuid, datetime
from flask_cors import cross_origin
from .model import User
from . import db
from .authentication_token import auth_token, requires_auth

auth = Blueprint('auth', __name__)

@auth.route('/login/', methods=['POST'])
def login():

    data = json.loads(request.get_data())
    username, password = data['username'].strip(), data['password'].strip()

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        resp = make_response(jsonify({'error':'Validation Failed', 'status': 400}))
        return resp
    else:
        token = auth_token.generate_token(username)
        resp = make_response(jsonify({'token':token, 'status': 201}))
        return resp

# signup, pleae remember the URL is '/signup/'
@auth.route('/signup/', methods=['POST'])
def post():

    data = json.loads(request.get_data())
    username, password = data['username'].strip(), data['password'].strip()

    if not username or not password:
        resp = make_response(jsonify({'error':'Invalid username or password', 'status': 400}))
        return resp
    
    user = User.query.filter_by(username=username).first()

    if user:
        resp = make_response(jsonify({'error':'user already exit', 'status': 400}))
        return resp
    
    new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    token = auth_token.generate_token(username)
    resp = make_response(jsonify({'token':token, 'status': 201}))
    return resp