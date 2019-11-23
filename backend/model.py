from datetime import datetime
from sqlalchemy import func
from . import db
from flask_login import UserMixin
import json


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), unique=True)
    activities = db.relationship('Activity', backref='account', lazy=True)

    def get_user(_username):
        return User.query.filter_by(username=_username).first()

    def __repr__(self):
        user_obj = {
            'id': self.id,
            'username': self.username
        }
        return json.dumps(user_obj)


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    service_route = db.Column(db.String(100), nullable=False)
    recorded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    account_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        user_obj = {
            'id': self.id,
            'user': self.account.username,
            'url-visited': self.service_route,
            'visited-at': self.recorded_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        return json.dumps(user_obj)

    def log(account_id, url):
        activity = Activity(account_id=account_id, service_route=url, recorded_at=datetime.now())
        db.session.add(activity)
        db.session.commit()

    def get_all_activities(limit_num=50):
        '''Logs of all activities'''
        return [Activity.json_details(activity) for activity in Activity.query.limit(limit_num).all()]

    def json_details(self):
        return {'id': self.id, 'account_id': self.account_id, 'url-visited': self.service_route, 'visited-at': self.recorded_at.strftime("%Y-%m-%d %H:%M:%S")}