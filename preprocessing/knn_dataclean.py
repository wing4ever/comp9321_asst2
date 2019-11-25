#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 7 21:37:55 2019

@author: blueberry

"""


import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, MinMaxScaler, scale

def normalization(dfDataset):
    """this function is used to do normalization for the dataset"""

    for col in dfDataset.columns:
        dfDataset[col]= dfDataset[col].astype(float)
#        MIN = min(dfDataset[col])
#        MAX = max(dfDataset[col])
#        newCol = dfDataset[col].apply(lambda x: (x - MIN) / (MAX - MIN))
#        dfDataset = dfDataset.drop(col, axis=1)
#        dfDataset[col] = newCol
    
    return dfDataset

def preProcessDataSet(Dataset):
    """this function is uesed to pre process the dataset for knn training model"""
    
    dfDataset = pd.read_csv(Dataset)
    
    # The most of  these columns is not useful for prediction. At first, we drop these.
    columnNeedDrop = [
        'id', 'amenities', 'city', 'description', 'first_review', 'host_since', 'last_review', 
        'latitude', 'longitude', 'name', 'neighbourhood', 'thumbnail_url', 'zipcode'
        ]
    dfDataset.drop(columnNeedDrop, axis=1, inplace=True)
    
    print('before dropna')
    print(dfDataset.shape)
    dfDataset.dropna(axis=0, inplace=True)
    print('after dropna')
    print(dfDataset.shape)
    
     # log_price label coder 
    print(min(dfDataset['log_price']),max(dfDataset['log_price']))
    
   # 'property_type' label coder 
    dfDataset['property_type'] = scale((LabelEncoder().fit_transform(dfDataset['property_type'])).astype(float))
    print(min(dfDataset['property_type']),max(dfDataset['property_type']))
    
    # 'room_type' label coder
    dfDataset['room_type'] = scale((LabelEncoder().fit_transform(dfDataset['room_type'])).astype(float))
    print(min(dfDataset['room_type']),max(dfDataset['room_type']))
    
    # 'bed_type' label coder
    dfDataset['bed_type'] = scale((LabelEncoder().fit_transform(dfDataset['bed_type'])).astype(float))
    print(min(dfDataset['bed_type']),max(dfDataset['bed_type']))
    
    # 'cancellation_policy' label coder
    dfDataset['cancellation_policy'] = scale((LabelEncoder().fit_transform(dfDataset['cancellation_policy'])).astype(float))
    print(min(dfDataset['cancellation_policy']),max(dfDataset['cancellation_policy']))

    # 'cleaning_fee' label coder
    dfDataset['cleaning_fee'] = LabelEncoder().fit_transform(dfDataset['cleaning_fee'])
    print(min(dfDataset['cleaning_fee']),max(dfDataset['cleaning_fee']))
    
    # 'cleaning_fee' label coder
    dfDataset['host_has_profile_pic'] = LabelEncoder().fit_transform(dfDataset['host_has_profile_pic'])
    print(min(dfDataset['host_has_profile_pic']),max(dfDataset['host_has_profile_pic']))
     
    # 'cleaning_fee' label coder
    dfDataset['host_identity_verified'] = LabelEncoder().fit_transform(dfDataset['host_identity_verified'])
    print(min(dfDataset['host_identity_verified']),max(dfDataset['host_identity_verified']))
    
    # 'cleaning_fee' label coder
    dfDataset['host_response_rate'] = dfDataset['host_response_rate'].str.replace('%', '').astype(float)
    dfDataset['host_response_rate'] = dfDataset['host_response_rate']/10
    print(min(dfDataset['host_response_rate']),max(dfDataset['host_response_rate']))
    
    # 'instant_bookable' label coder
    dfDataset['instant_bookable'] = LabelEncoder().fit_transform(dfDataset['instant_bookable'])
    print(min(dfDataset['instant_bookable']),max(dfDataset['instant_bookable']))
    
    dfDataset['number_of_reviews'] = scale(dfDataset['number_of_reviews'].astype(float))
    print(min(dfDataset['number_of_reviews']),max(dfDataset['number_of_reviews']))
    
    # finally, you get the data you can use for modelling
    dfDataset = normalization(dfDataset)
    
    # we use review_scores_rating as y
    allLabelData = pd.DataFrame(dfDataset['review_scores_rating']/100,columns=['review_scores_rating'])
    # and left are our features
    allFeatureData = dfDataset.drop('review_scores_rating', axis=1)
    print(dfDataset.dtypes)
    #save data in the separate csv files
    createFeature = 'knn_feature.csv'
    createLabel = 'knn_label.csv'
    allLabelData.to_csv(createLabel,index=False)
    allFeatureData.to_csv(createFeature,index=False)

def main():
    preProcessDataSet('train.csv')

if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', 500)
    main()

