#! /usr/bin/env python
from flask import Flask
import sqlite3
from sqlite3 import Error
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api, Resource
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
class User(db.Model):
    username = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100),nullable=False)
    

#json ma schema
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


@app.route('/testing')
class Testing(Resource):
    def get(self):
        return {'message' : 'testing get'}

#main
if __name__ == '__main__':
    create_db("data.db")
    # db.create_all()
    app.run(debug=True)