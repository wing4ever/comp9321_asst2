from flask import Blueprint, make_response, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required
from flask_cors import cross_origin
import joblib, pandas
import matplotlib.pyplot as plt
import base64
from PIL import Image
from io import BytesIO
from . import db
from .model import User, Activity
from .authentication_token import auth_token, requires_auth
from .prediction import conbin_prediction
from flask_restplus import Api, Resource, fields
import json, os

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
                                  description="Shows user authentication process"
                                  )
signup_api = restplus_api.namespace('signup',
                                  description="Shows user authentication process"   
                                  )
user_api = restplus_api.namespace('user',
                                  description="Shows user account information"
                                  )

admin_api = restplus_api.namespace('admin',
                                   description="Summary of service usage"
                                   )

home_api = restplus_api.namespace('home/prediction',
                                  description="Predict Airbnb Home popularity"
                                  )
home_factor_api = restplus_api.namespace('home/factors',
                                  description="Relationship between Airbnb Home features and popularity"
                                  )

user_login_model = user_api.model('User', {
    'username': fields.String,
    'password': fields.String
})

home_prediction_model = home_api.model('HomePrediction', {
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

home_factor_model = home_factor_api.model('HomeFactor', {
    "factor": fields.String,
    "AUTH_TOKEN": fields.String
})

@restplus_api.route('/login/')
class UserLogin(Resource):
    @login_api.doc(description="Login in to the API with username & password to receive API token")
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
            resp = make_response(jsonify({'API_TOKEN':token, 'status': 201}))
            return resp

@restplus_api.route('/signup/')
class UserSignup(Resource):
    @signup_api.doc(description="Sign in to the API with username & password to receive API token")
    @login_api.expect(user_login_model)
    @cross_origin()
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
        resp = make_response(jsonify({'API_TOKEN': token, 'status': 201}))
        return resp

# show the info of the current user
# basic info + statistical info
@restplus_api.route('/home/user/')
class UserAccount(Resource):
    @user_api.doc(security="TOKEN-BASED", description="Get information of current user account")
    @cross_origin()
    @requires_auth
    def get(self):
        token = request.headers.get('API_TOKEN')
        my_info = auth_token.validate_token(token)
        my_username = str(my_info['username'])

        resp = make_response(jsonify({'username': my_username, 'status': 200}))
        return resp

@restplus_api.route('/home/summary/')
class ServiceUsageSummary(Resource):
    @home_api.doc(security="TOKEN-BASED",
                   description="Summary of frequency of service usage (Which service is more popular?)")
    @cross_origin()
    @requires_auth
    def get(self):
        data = Activity.get_service_usage_summary()
        services, numbers = ['prediction', 'factors', 'summary'], [0, 0, 0]
        for service in data:
            if 'prediction' in service['service-url']:
                numbers[0] = service['visit-count']
            elif 'factors' in service['service-url']:
                numbers[1] = service['visit-count']
            elif 'summary' in service['service-url']:
                numbers[2] = service['visit-count']

        plt.bar(services, numbers)
        plt.title('API services usage statistics')
        sio = BytesIO()
        plt.savefig(sio, format='png')
        data = base64.encodebytes(sio.getvalue()).decode()

        resp = make_response(jsonify({'image': data, 'status':200}))
        return resp

# this part is used to provide the service of prediction
# totally speaking, there are two methods one is GET which
# provide the relationship between some features and the output
# another is POST which make prediction according the features
# from user
current_path = os.path.abspath(__file__)
model_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + '/mlmodel'),  'linearRegression.pkl')
linearRegression = joblib.load(model_path)

@restplus_api.route('/home/prediction/')
class HomePrediction(Resource):
    @home_api.doc(security="TOKEN-BASED", description="Get Prediction of popularity of the house base on its features")
    @home_api.expect(home_prediction_model)
    @cross_origin()
    @requires_auth
    def post(self):

        # below is input example WEISONG
        # ==============================
        # {
        #     "log_price": 4.01063529409626,
        #     "property_type":"House",
        #     "room_type":"Entire home/apt",
        #     "accommodates": 5,
        #     "bathrooms": 3,
        #     "bed_type": "Real Bed",
        #     "cancellation_policy":"moderate",
        #     "cleaning_fee": 1,
        #     "city": "LA",
        #     "host_has_profile_pic": "f",
        #     "host_identity_verified": "f",
        #     "host_response_rate": "50%",
        #     "instant_bookable": "f",
        #     "number_of_reviews": 6,
        #     "bedrooms": 1.0,
        #     "beds": 1.0
        # }   
        # ===============================

        allFeatures = json.loads(request.get_data())
        prediction_result = conbin_prediction(allFeatures)
        resp = make_response(jsonify({"prediction_result" : prediction_result, "status" : 201}))
        return resp

@restplus_api.route('/home/factors/')
class HomeFactor(Resource):
    @home_factor_api.doc(security="TOKEN-BASED", description="Get relationship of any feature with its popularity")
    @home_factor_api.expect(home_factor_model)
    @cross_origin()
    @requires_auth
    def post(self):
        data = json.loads(request.get_data())
        factor = data.get('factor')
        current_path = os.path.abspath(__file__)
        feature_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + '/dataset'),  'feature.csv')
        label_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + '/dataset'),  'label.csv')
        allFeatures = pandas.read_csv(feature_path)
        thisFactor = list(allFeatures[factor])
        popularity = list(pandas.read_csv(label_path)['review_scores_rating'])
        data = {}
        data['factor'], data['popularity'] = thisFactor, popularity

        plt.title(f'relationship of {factor} and popularity')
        plt.xlabel(f'{factor}')
        plt.ylabel('popularity level')
        plt.scatter(thisFactor, popularity)
        sio = BytesIO()
        plt.savefig(sio, format='png')
        data = base64.encodebytes(sio.getvalue()).decode()
        plt.close()

        resp = make_response(jsonify({'image':data, 'status':201}))
        return resp
    
    @home_factor_api.doc(security="TOKEN-BASED", description="Get top eight features that affect popularity")
    @cross_origin()
    @requires_auth
    def get(self):
        current_path = os.path.abspath(__file__)
        graph_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + '/importance'),  'importance.png')
        byteImageIO = BytesIO()
        byteImage = Image.open(graph_path)
        byteImage.save(byteImageIO, 'png')
        data = base64.encodebytes(byteImageIO.getvalue()).decode()
        
        resp = make_response(jsonify({'image' : data, 'status': 200}))
        return resp