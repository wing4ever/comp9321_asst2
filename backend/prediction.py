#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 12:59:31 2019

@author: seele
"""

import pickle
import torch, os
from torch import nn
import torch.nn.functional as F
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, scale

#input data not contain columnNeedDrop = [
#        'id', 'amenities', 'description', 'first_review', 'host_since', 'last_review', 'name',
#        'neighbourhood', 'thumbnail_url', 'zipcode', 'review_scores_rating'
#        ]

""" there are some example format of the predict data can be accpeted, 
    make sure the 'review_scores_rating' is always 0, because it is predict value. 
    it will dropped when processing, so it doesn't matter just keep it not null.
"""
# 1. just like dict, if use this format, you do not edit anything
raw_data  = {'log_price': 4.01063529409626,
                  'property_type':'House',
                  'room_type':'Entire home/apt',
                  'accommodates': 5,
                  'bathrooms': 3,
                  'bed_type': 'Real Bed',
                  'cancellation_policy':'moderate',
                  'cleaning_fee': 1,
                  'city': 'LA',
                  'host_has_profile_pic': 'f',
                  'host_identity_verified': 'f',
                  'host_response_rate': '50%',
                  'instant_bookable': 'f',
                  'number_of_reviews': 6,
                  'bedrooms': 1.0,
                  'beds': 1.0
                  }

#example 5.  (b:1, cf:0 1, (f f, f) (t,t,f ), bedr : 1 ,10, )  4. 2. (same)
#input_data = pd.DataFrame(raw_data,index=[0])


#2. if data is json like below which is id follow by data format
#json_data = '{"0":{"log_price": 4.9768,"property_type":"Apartment","room_type":"Entire home/apt", "accommodates": 2,"bathrooms": 1,"bed_type": "Real Bed","cancellation_policy":"strict","cleaning_fee": 1,"city": "NYC","host_has_profile_pic": "t","host_identity_verified": "t","host_response_rate": "71%","instant_bookable": "f","number_of_reviews": 2,"bedrooms": 1.0,"beds": 1.0}}'

#input_data= pd.read_json(json_data)
#input_data = pd.DataFrame(input_data.values.T, index=input_data.columns, columns=input_data.index)
#prediction_col_order  = ['log_price','property_type','room_type','accommodates','bathrooms','bed_type','cancellation_policy',
#                         'cleaning_fee','city','host_has_profile_pic','host_identity_verified','host_response_rate','instant_bookable',
#                         'number_of_reviews','review_scores_rating','bedrooms','beds'
#                         ]
#
#input_data=input_data.ix[:,prediction_col_order]


#3. if data use json format by coloums just commit below
#json_data = '{"log_price":{"0":4.9768},"property_type":{"0":"Apartment"},"room_type":{"0":"Entire home\\/apt"},"accommodates":{"0":2},"bathrooms":{"0":1},"bed_type":{"0":"Real Bed"},"cancellation_policy":{"0":"strict"},"cleaning_fee":{"0":1},"city":{"0":"NYC"},"host_has_profile_pic":{"0":"t"},"host_identity_verified":{"0":"t"},"host_response_rate":{"0":"71%"},"instant_bookable":{"0":"f"},"number_of_reviews":{"0":2},"bedrooms":{"0":1.0},"beds":{"0":1.0}}'
#input_data = pd.read_json(json_data)




#just ensure input predict data is dataframe format and coloums order is follow the prediction_col_order at above
def preprocessing_predict_data(input_data):
    
    input_data = pd.DataFrame(input_data,index=[0])
    prediction_col_order  = ['log_price','property_type','room_type','accommodates','bathrooms','bed_type','cancellation_policy',
                         'cleaning_fee','city','host_has_profile_pic','host_identity_verified','host_response_rate','instant_bookable',
                         'number_of_reviews','review_scores_rating','bedrooms','beds'
                         ]
    for i in prediction_col_order:
        if i not in input_data.columns:
            input_data.insert(0,i,0)
    input_data = input_data.reindex(columns = prediction_col_order)
    
#    print(input_data)
    current_path = os.path.abspath(__file__)
    file_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + '/dataset'),  'train.csv')
    data_train = pd.read_csv(file_path)
    columnNeedDrop = [
        'id', 'amenities', 'description', 'first_review', 'host_since', 'last_review','latitude', 'longitude',
        'name', 'neighbourhood', 'thumbnail_url', 'zipcode',
        ]
    
    data_train.drop(columnNeedDrop, axis=1, inplace=True)
    data_train = data_train.append(input_data,ignore_index=True)
    data_train['host_response_rate'] = data_train['host_response_rate'].str.replace('%', '').astype(float)
    
#    columns_string = ['property_type','room_type','bed_type','cancellation_policy','city', 'host_has_profile_pic',
#        'host_identity_verified','instant_bookable'
#        ]
    
    columns_number = ['log_price','accommodates','bathrooms','cleaning_fee','number_of_reviews','review_scores_rating','bedrooms','beds']
    
    for i in columns_number:
        data_train[i].fillna(0,inplace=True)
        data_train[i] = data_train[i].astype(float)
     
    data_train.dropna(axis=0, inplace=True)
    data = pd.get_dummies(data_train,drop_first = True)
#    print(data.isnull().values.any())
    
    columns = data.columns
    data = data.astype(float)
    
    scaler = scale
    data = pd.DataFrame(scaler(data), columns = columns)

#    scaler = MinMaxScaler()
#    data = pd.DataFrame(scaler.fit_transform(data), columns = columns)
#    print(data.shape)
        
    data = data.drop('review_scores_rating', axis=1)

    return data



def neural_network_data(input_data):
    
    data = preprocessing_predict_data(input_data)
    data = data.drop('property_type_Island', axis=1)
#    print(data.shape)
    predict_data = data.iloc[-1].to_numpy()
    predict_data = torch.tensor(predict_data)
    predict_data = predict_data.reshape(1,57)
    predict_data = predict_data.float()
    
    return predict_data
    

def normal_model_data(input_data):
    data = preprocessing_predict_data(input_data)
    predict_data = data.iloc[-1]
#    print(X_train.shape)
    return predict_data


class FeedForward(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(57, 28)
        self.fc2 = nn.Linear(28, 1)
#        self.fc3 = nn.Linear(14, 1)
#        self.fc4 = nn.Linear(8, 1)
      
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
#        x = self.fc3(x)
#        x = self.fc4(x)
        
#        x = F.log_softmax(x, dim=1)  # preserve batch dim
        return x



def prediction(name,input_data):
    
    if name == 'regression':
        current_path = os.path.abspath(__file__)
        file_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + '/mlmodel'),  'XGBRegressor.pickle')
        with open(file_path,'rb') as f:
            model = pickle.load(f)
        predict_data = normal_model_data(input_data)
        predicted_result = model.predict(predict_data)
        if predicted_result>10:
            predicted_result[0] = 10
        if predicted_result<0:
            predicted_result[0] = np.random.rand()
            
        print(predicted_result[0])
        
        return round(predicted_result[0],4)
    
    if name == 'neural':
        
        predict_data = neural_network_data(input_data)
        
        model = FeedForward()
        model1 = FeedForward()
        model2 = FeedForward()
        model3 = FeedForward()
        model4 = FeedForward()

        current_path = os.path.abspath(__file__)
        model_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + '/mlmodel'),  'model.pth')
        model1_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + '/mlmodel'),  'model1.pth')
        model2_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + '/mlmodel'),  'model2.pth')
        model3_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + '/mlmodel'),  'model3.pth')
        model4_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + '/mlmodel'),  'model4.pth')
        model.load_state_dict(torch.load(model_path))
        model1.load_state_dict(torch.load(model1_path))
        model2.load_state_dict(torch.load(model2_path))
        model3.load_state_dict(torch.load(model3_path))
        model4.load_state_dict(torch.load(model4_path))

        with torch.no_grad():
            predicted_result = model(predict_data)
            predicted_result1 = model1(predict_data)
            predicted_result2 = model2(predict_data)
            predicted_result3 = model3(predict_data)
            predicted_result4 = model4(predict_data)
            
            if predicted_result > 10:
                 predicted_result = 10
            if predicted_result1 > 10:
                 predicted_result1 = 10
            if predicted_result2 > 10:
                 predicted_result2 = 10
            if predicted_result3 > 10:
                 predicted_result3 = 10
            if predicted_result4 > 10:
                 predicted_result4 = 10
                 
            if predicted_result <= 0:
                 predicted_result = np.random.rand()
            if predicted_result1 <= 0:
                 predicted_result1 = np.random.rand()
            if predicted_result2 <= 0:
                 predicted_result2 = np.random.rand()
            if predicted_result3 <= 0:
                 predicted_result3 = np.random.rand()
            if predicted_result4 <= 0:
                 predicted_result4 = np.random.rand()
        
            print(round(float(predicted_result),4),round(float(predicted_result1),4),round(float(predicted_result2),4),round(float(predicted_result3),4),round(float(predicted_result4),4))
            print(round(float((predicted_result+predicted_result1+predicted_result2+predicted_result3+predicted_result4)/5),4))
        return round(float((predicted_result+predicted_result1+predicted_result2+predicted_result3+predicted_result4)/5),4)
    
    
def conbin_prediction(input_data):
#    choose a model to predict
    model_name = 'combine' # 'regression', 'neural', 'combine'
    
    if model_name == 'neural':
        result = prediction('neural',input_data)

    if model_name == 'regression':
        result = prediction('regression',input_data)
        
    if model_name == 'combine':
        result = (prediction('regression',input_data)+prediction('neural',input_data))/2
        print(round(result,4))
     
    #return a true value, such as 98 which means 98%, just add % at frontend or somewhere
    return round(result,4)*10
    

# import prediction.py as predict
# predict.conbin_prediction(input_data)
#commit below and example at the front
a = conbin_prediction(raw_data)
     
     
     
     