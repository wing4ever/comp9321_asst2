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
import json, os


api = Blueprint('api', __name__)
restplus_api = Api(api)


@restplus_api.route('/login/')
class UserLogin(Resource):
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

@restplus_api.route('/signup/')
class UserSignup(Resource):
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

        token = auth_token.generate_token(username)
        resp = make_response(jsonify({'token': token, 'status': 201}))
        return resp

# show the info of the current user
# basic info + statistical info
@restplus_api.route('/home/user/')
class UserAccount(Resource):
    @cross_origin()
    @requires_auth
    def get(self):
        token = request.headers.get('user_token')
        user = auth_token.validate_token(token)
        resp = make_response(jsonify({'username': str(user), 'status': 200}))
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
    @cross_origin()
    @requires_auth
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

@restplus_api.route('/home/factors/')
class HomeFactor(Resource):
    @cross_origin()
    @requires_auth
    def post(self):
        data = json.loads(request.get_data())
        factor = data.get('factor')
        if not factor:
            redirect(url_for('api.home.factors'))
        else:
            current_path = os.path.abspath(__file__)
            feature_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + '/dataset'),  'feature.csv')
            label_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + '/dataset'),  'label.csv')
            allFeatures = pandas.read_csv(feature_path)
            thisFactor = list(allFeatures[factor])
            popularity = list(pandas.read_csv(label_path)['review_scores_rating'])
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
            resp = make_response(jsonify({"image" : data , 'status': 201}))
            return resp