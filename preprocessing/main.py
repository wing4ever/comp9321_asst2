#! /usr/bin/env python
from flask import Flask
import sqlite3
from sqlite3 import Error
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api, Resource
from flask_marshmallow import Marshmallow
import pandas as pd

def create_db(db_file):
    '''
    use this function to create a db, don't change the name of this function.
    db_file: Your database's name.
    '''
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()
    pass

#set up
app = Flask(__name__)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

#database model
"""
QUESTION:
should there be a foreign key between property and facility?
not sure what would be the primary key & data type for each model?
specify format for date string?
"""
class User(db.Model):
    username = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100),nullable=False)
    #may be add property ID that belong to this user?

class Airbnb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    log_price = db.Column(db.Float) #db.Float() ???
    property_type = db.Column(db.Integer)
    room_type = db.Column(db.Integer)
    accommodates = db.Column(db.Integer)
    bathrooms = db.Column(db.Float)
    bed_type = db.Column(db.Integer)
    cancellation_policy = db.Column(db.Integer)
    cleaning_fee = db.Column(db.Integer)
    host_response_rate = db.Column(db.Float)
    instant_bookable = db.Column(db.Integer)
    number_of_reviews= db.Column(db.Integer)
    bedrooms = db.Column(db.Float)
    beds = db.Column(db.Float)
    review_scores_rating = db.Column(db.Float)


#json ma schema
class UserSchema(ma.Schema):
    class Meta:
        model = User

class AirbnbSchema(ma.Schema):
    class Meta:
        model = Airbnb


@app.route('/testing')
class Testing(Resource):
    def get(self):
        airbnb_schema = AirbnbSchema(many=False)
        allAirbnb = Airbnb.query.limit(10).all()
        returnData = []
        for ab in allAirbnb:
            item = airbnb_schema.dump(ab).data
            print(item)
            to_return = {
                'log_price':item['log_price'],
                'review_scores_rating':item['review_scores_rating']
            }
            returnData.append(to_return)
        return returnData

#main
if __name__ == '__main__':
    create_db("data.db")
    db.create_all()
    db.session.commit()
    #import data from csv
    features = pd.read_csv('feature.csv')
    label = pd.read_csv('label.csv')
    df = pd.concat([features,label],axis=1)
    df.to_sql(name='airbnb', con=db.engine,if_exists='replace',index=False)
    app.run(debug=True)