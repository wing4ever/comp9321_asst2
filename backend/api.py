from flask import Blueprint, make_response, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required
from flask_cors import cross_origin
import joblib, pandas
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from .model import User
from .authentication_token import auth_token, requires_auth
from flask_restplus import Api, Resource
import json

api = Blueprint('api', __name__)
restplus_api = Api(api,
                   title="Airbnb Home Popularity Prediction", # Documentation title
                   )
login_api = restplus_api.namespace('login',
                                  description="Shows user authentication process"
                                  )
user_api = restplus_api.namespace('user',
                                  description="Shows user registration, and user account information"
                                  )

home_api = restplus_api.namespace('home',
                                  description="Relationship between Airbnb Home features and popularity, & popularity prediction"
                                  )

@login_api.route('/')
class UserLogin(Resource):
    @user_api.doc(description="Sign in to the API with username & password to receive API token")
    @cross_origin()
    def post(self):
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


# show the info of the current user
# basic info + statistical info
@user_api.route('/')
class UserAccount(Resource):
    @requires_auth
    @user_api.doc(description="Get information of current user account")
    @cross_origin()
    def get(self):
        token = request.headers.get('user_token')
        user = auth_token.validate_token(token)
        resp = make_response(jsonify({'username': str(user), 'status': 200}))
        return resp

    @user_api.doc(description="Register new user account")
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

        token = auth_token.generate_token(username)
        resp = make_response(jsonify({'token': token, 'status': 201}))
        return resp

# this part is used to provide the service of prediction
# totally speaking, there are two methods one is GET which
# provide the relationship between some features and the output
# another is POST which make prediction according the features
# from user
linearRegression = joblib.load('backend/pkl/linearRegression.pkl')

@home_api.route('/prediction/')
class HomePrediction(Resource):
    @requires_auth
    @home_api.doc(description="Get Prediction of popularity of the house base on its features")
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
    @home_api.doc(description="Get relationship of any feature with its popularity")
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