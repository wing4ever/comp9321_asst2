#! /usr/bin/env python
from flask import Flask
import sqlite3
from sqlite3 import Error
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api
from flask_marshmallow import Marshmallow


def create_db(db_file):
    '''
    uase this function to create a db, don't change the name of this function.
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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
class Property(db.Model):
    neighbourhood = db.Column(db.String(100))
    name = db.Column(db.String(100), primary_key=True)
    latitude = db.Column(db.Float(),nullable=False)
    longtitude = db.Column(db.Float(),nullable=False)
    property_type = db.Column(db.String(100))
    room_type = db.Column(db.String(100))

class Facility(db.Model): #missing primary key !!!
    accommodations = db.Column(db.Integer)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    beds = db.Column(db.Integer)
    bed_types = db.Column(db.String(100))
    amenities = db.Column(db.String(100))
    description = db.Column(db.String(100))

class Host(db.Model): #should have name or id as primary key?
    since = db.Column(db.String(100))
    profile_picture = db.Column(db.Integer,nullable=False) #boolean
    identity_verified = db.Column(db.Integer,nullable=False) #boolean
    response_rate =db.Column(db.Float())

class Policy(db.Model): #forgeign key to preperty and primary key?
    cancellation = db.Column(db.String(100))
    free_cleaning = db.Column(db.Integer,nullable=False) #boolean
    instant_bookable = db.Column(db.Integer,nullable=False) #boolean

class Review(db.Model):
    first = db.Column(db.String(100))
    last = db.Column(db.String(100))
    total = db.Column(db.Integer)
    rating = db.Column(db.Integer)

#json ma schema
class PropertySchema(ma.ModelSchema):
    class Meta:
        model = Property

class FacilitySchema(ma.ModelSchema):
    class Meta:
        model = Facility

class HostSchema(ma.ModelSchema):
    class Meta:
        model = Host

class PolicySchema(ma.ModelSchema):
    class Meta:
        model = Policy

class ReviewSchema(ma.ModelSchema):
    class Meta:
        model = Review

@app.route('/')
def get():
    return "Hello World!"

#main
if __name__ == '__main__':
    create_db("data.db")
    app.run(debug=True)