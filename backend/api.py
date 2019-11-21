from flask import Blueprint, make_response, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required
import json
import joblib, pandas
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from .model import User
from .authentication_token import auth_token, requires_auth

api = Blueprint('api', __name__)

# show the info of the current user
# basic info + statistical info
@api.route('/home/user/', methods=['GET'])
@requires_auth
def get_info_curuser():

    token = request.headers.get('user_token')
    user = auth_token.validate_token(token)

    resp = make_response(jsonify({'username': str(user), 'status': 200}))
    return resp

# # this service is also not good
# @api.route('/home/user/', methods=['POST'])
# def create_user():
#     # get json data from user's request
#     data = json.loads(request.get_data())
#     username, password = data['username'].strip(), data['password'].strip()
#     # username and password should be valid and username is unique
#     if username and password:
#         # hash the password and store into db
#         hashed_password = generate_password_hash(password, method='sha256')
#         newUser = User(public_id=str(uuid.uuid4()), username=username, password=hashed_password)
#         # check the username if already exist or not
#         alreadyExit = 0
#         for user in User.query.all():
#             if user.username == newUser.username:
#                 alreadyExit = 1
#         if not alreadyExit:
#             db.session.add(newUser)
#             db.session.commit()
#             return jsonify({'message': 'user create success', 'status': 201})
#         else:
#             return jsonify({'message':'user already exit-->need redirct to logon page'})
#     else:
#         return jsonify({'message':'username or password is empty-->need redirct logon page'})

# this part is used to provide the service of prediction
# totally speaking, there are two methods one is GET which
# provide the relationship between some features and the output
# another is POST which make prediction according the features
# from user
linearRegression = joblib.load('backend/pkl/linearRegression.pkl')

@api.route('/home/prediction/', methods=['POST'])
@requires_auth
def get_prediction():

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
        'property_type', 'room_type', 'bed_type', 'cancellation_policy',\
        'cleaning_fee', 'instant_bookable'
        ]
    # the values for these features should be float
    floatFeatures = [
        'log_price', 'accommodates','bathrooms', 'host_response_rate',\
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

    resp = make_response(jsonify({"prediction_result" : prediction_result[0][0], 'status': 201}))
    return resp

@api.route('/home/factors/', methods=['POST'])
@requires_auth
def get_relationship():
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
