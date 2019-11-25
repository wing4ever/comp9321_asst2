from itsdangerous import SignatureExpired, JSONWebSignatureSerializer, BadSignature
from flask_restplus import abort
from functools import wraps
from time import time
import datetime
from flask import jsonify, request, make_response
from .model import *

class AuthenticationToken:
    def __init__(self, secret_key, expires_in):
        self.secret_key = secret_key
        self.expires_in = expires_in
        self.serializer = JSONWebSignatureSerializer(secret_key)

    def generate_token(self, user_id, username):

        info = {
            'username': username,
            'id': user_id,
            'creation_time': time()
        }

        token = self.serializer.dumps(info)
        return token.decode()
    
    def validate_token(self, token):
        info = self.serializer.loads(token.encode())

        if time() - info['creation_time'] > self.expires_in:
            raise SignatureExpired("The token has been expired, please get a new token")

        return {'id': info['id'], 'username': info['username']}
    
SECRET_KEY = "THIS IS SECRET YOU CAN NEVER GUSS WHAT AM I TALKING"
expires_in = 6000
auth_token = AuthenticationToken(SECRET_KEY, expires_in)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get('API_TOKEN')
        if not token:
            return jsonify({'error': 'Authentication token is missing', 'status': 401})

        try:
            user_info = auth_token.validate_token(token)
            Activity.log(user_info['id'], request.path)
        except SignatureExpired as e:
            return jsonify({'error':'token expired', 'status': 401})
        except BadSignature as e:
            return jsonify({'error':'invalid token', 'status': 401})

        return f(*args, **kwargs)

    return decorated