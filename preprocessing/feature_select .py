#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 17:23:49 2019

@author: seele
"""

import pandas as pd

def find_feature_values(datafile):
    data = pd.read_csv(datafile)
    columnNeedDrop = [
        'id', 'amenities', 'description', 'first_review', 'host_since', 'last_review','latitude', 'longitude',
        'name', 'neighbourhood', 'thumbnail_url', 'zipcode',
        ]
    data.drop(columnNeedDrop, axis=1, inplace=True)
    data['host_response_rate'] = data['host_response_rate'].str.replace('%', '').astype(float)
    
    
    columns_string = ['property_type','room_type','bed_type','cancellation_policy','city', 'host_has_profile_pic',
        'host_identity_verified','instant_bookable'
        ]
#    columns_number = ['log_price','accommodates','bathrooms','cleaning_fee','number_of_reviews','review_scores_rating','bedrooms','beds']
#    
#    columns = data.columns
    data.fillna('NaN', axis = 0,inplace=True)
    values = {}
    for i in columns_string:
        values[i] = set(data[i].values)
    
    return values

if __name__ == "__main__":
    
    #generate the fearture_type that user can choose (only for string)
    fearture_type = find_feature_values('train.csv')
    
    with open('fearture_type_for_choosing.txt','w') as f:
        f.write('\n')
        for i in fearture_type:
            f.write(i+': ')
            for s in fearture_type[i]:
                f.write(s + ', ')
            f.write('\n')
            f.write('\n')
    f.close()