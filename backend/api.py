from flask import Blueprint, make_response, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import cross_origin
import joblib, pandas
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from .model import User, Activity
from .authentication_token import auth_token, requires_auth, requires_admin
from flask_restplus import Api, Resource, fields
import json
from . import db

api = Blueprint('api', __name__)
restplus_api = Api(api,
                   authorizations= {
                       "TOKEN-BASED": {
                           "type": "apiKey",
                           "name": "API-TOKEN",
                           "in": "header"
                       }
                   },
                   title="Airbnb Home Popularity Prediction", # Documentation title
                   )
login_api = restplus_api.namespace('login',
                                   description="User authentication process"
                                   )
user_api = restplus_api.namespace('user',
                                  description="User registration, and user account information"
                                  )

admin_api = restplus_api.namespace('admin',
                                   description="Admin Interface for Service Usage information"
                                   )

summary_api = restplus_api.namespace('summary',
                                   description="Summary of service usage"
                                   )

home_api = restplus_api.namespace('home',
                                  security="TOKEN-BASED",
                                  description="Relationship between Airbnb Home features and popularity, & popularity prediction"
                                  )

user_login_model = user_api.model('User', {
    'username': fields.String,
    'password': fields.String
})

home_prediction_model = home_api.model('Home', {
    'log_price': fields.Float,
    'property_type': fields.String,
    'room_type': fields.String,
    'accommodates': fields.Integer,
    'bathrooms': fields.Integer,
    'bed_type': fields.String,
    'cancellation_policy': fields.String,
    'cleaning_fee': fields.Integer,
    'city': fields.String,
    'host_has_profile_pic': fields.String,
    'host_identity_verified': fields.String,
    'host_response_rate': fields.String,
    'instant_bookable': fields.String,
    'number_of_reviews': fields.Integer,
    'bedrooms': fields.Float,
    'beds': fields.Float
})

@login_api.route('/')
class UserLogin(Resource):
    @login_api.doc(description="Sign in to the API with username & password to receive API token")
    @login_api.expect(user_login_model)
    @cross_origin()
    def post(self):
        data = json.loads(request.get_data())
        username, password = data['username'].strip(), data['password'].strip()

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            resp = make_response(jsonify({'error':'Validation Failed', 'status': 400}))
            return resp
        else:
            token = auth_token.generate_token(user.id, user.username)
            resp = make_response(jsonify({'token': token, 'status': 201}))
            return resp


# show the info of the current user
# basic info + statistical info
@user_api.route('/')
class UserAccount(Resource):
    @user_api.doc(description="Register new user account")
    @user_api.expect(user_login_model)
    @cross_origin()
    # signup or register new user account
    def post(self):
        data = json.loads(request.get_data())
        username, password = data['username'].strip(), data['password'].strip()

        if not username or not password:
            resp = make_response(jsonify({'error': 'Invalid username or password', 'status': 400}))
            return resp

        user = User.query.filter_by(username=username).first()

        if user:
            resp = make_response(jsonify({'error': 'user already exit', 'status': 400}))
            return resp

        new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()

        token = auth_token.generate_token(new_user.id, new_user.username)
        resp = make_response(jsonify({'token': token, 'status': 201}))
        return resp

    @requires_auth
    @user_api.doc(security="TOKEN-BASED", description="Get information of current user account and activities")
    @cross_origin()
    def get(self):
        token = request.headers.get('API-TOKEN')
        my_info = auth_token.validate_token(token)
        my_username = str(my_info['username'])
        my_user_obj = User.get_user(my_username)
        my_activities = Activity.get_activity_summary(my_user_obj.id)
        resp = make_response(jsonify({'username': my_username, 'activities': my_activities, 'status': 200}))
        return resp


@summary_api.route('/service-usage/')
class ServiceUsageSummary(Resource):
    @requires_auth
    @admin_api.doc(security="TOKEN-BASED",
                   description="Summary of frequency of service usage (Which service is more popular?)")
    def get(self):
        return Activity.get_service_usage_summary()

@admin_api.route('/users-activities/summary/')
class UsersActivitiesSummary(Resource):
    @requires_auth
    @requires_admin
    @admin_api.doc(security="TOKEN-BASED",
                   description="Summary of user-service interaction")
    def get(self):
        return Activity.get_all_activities_summary()

@admin_api.route('/users-activities/')
class ActivitiesLog(Resource):
    @requires_auth
    @requires_admin
    @admin_api.doc(security="TOKEN-BASED",
                   description="All Users Activities Log: Lists all users-interactions with the services")
    def get(self):
        return Activity.get_all_activities()



# this part is used to provide the service of prediction
# totally speaking, there are two methods one is GET which
# provide the relationship between some features and the output
# another is POST which make prediction according the features
# from user
linearRegression = joblib.load('backend/pkl/linearRegression.pkl')

@home_api.route('/prediction/')
class HomePrediction(Resource):
    @requires_auth
    @home_api.doc(security="TOKEN-BASED", description="Get Prediction of popularity of the house base on its features")
    @home_api.expect(home_prediction_model)
    @cross_origin()
    def post(self):

        # below is input example WEISONG
        # ==============================
        # {
        #     "accommodates": "1.0",
        #     "bathrooms": "1.0",
        #     "bed_type": "1.0",
        #     "bedrooms": "1.0",
        #     "beds": "1.0",
        #     "cancellation_policy": "1",
        #     "cleaning_fee": "0",
        #     "host_response_rate": "1.0",
        #     "instant_bookable": "1",
        #     "log_price": "0.301",
        #     "number_of_reviews": "0.8",
        #     "property_type": "1.0",
        #     "room_type": "1.0"
        # }
        # ===============================

        allFeatures = json.loads(request.get_data())
        # the values for these features should be int
        intFeatures = [
            'property_type', 'room_type', 'bed_type', 'cancellation_policy', \
            'cleaning_fee', 'instant_bookable'
        ]
        # the values for these features should be float
        floatFeatures = [
            'log_price', 'accommodates','bathrooms', 'host_response_rate', \
            'number_of_reviews', 'bedrooms', 'beds'
        ]

        prepareFeatures = {}
        for key in allFeatures.keys():
            if key in intFeatures:
                prepareFeatures[key] = [int(allFeatures[key])]
            else:
                prepareFeatures[key] = [float(allFeatures[key])]

        featuresFromUser = pandas.DataFrame(prepareFeatures)
        prediction_result = linearRegression.predict(featuresFromUser)

        resp = make_response(jsonify({"prediction_result": prediction_result[0][0], 'status': 201}))
        return resp

@home_api.route('/factors/')
class HomeFactor(Resource):
    @requires_auth
    @home_api.doc(security="TOKEN-BASED", description="Get relationship of any feature with its popularity")
    @cross_origin()
    def post(self):
        data = json.loads(request.get_data())
        factor = data.get('factor')
        if not factor:
            redirect(url_for('api.home.factors'))
        else:
            allFeatures = pandas.read_csv('feature.csv')
            thisFactor = list(allFeatures[factor])
            popularity = list(pandas.read_csv('label.csv')['review_scores_rating'])
            data = {}
            data['factor'], data['popularity'] = thisFactor, popularity

            plt.title(f'relationship of {factor} and popularity')
            plt.xlabel('property type')
            plt.ylabel('popularity level')
            plt.scatter(thisFactor, popularity)
            sio = BytesIO()
            plt.savefig(sio, format='png')
            data = base64.encodebytes(sio.getvalue()).decode()
            plt.close()
            return data