from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import sqlite3
from flask_cors import CORS

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)
    # database
    app.config['SECRET_KEY'] = 'thisissecret'
    app.config['CORSE_HEADERS'] = 'Content-Type'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    CORS(app, resources=r'/*')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .model import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
