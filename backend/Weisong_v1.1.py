#save data in the separate csv files
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, MinMaxScaler

def normalization(dfDataset):
    """this function is used to do normalization for the dataset"""

    for col in dfDataset.columns:        
        MIN = min(dfDataset[col])
        MAX = max(dfDataset[col])
        newCol = dfDataset[col].apply(lambda x: (x - MIN) / (MAX - MIN))
        dfDataset = dfDataset.drop(col, axis=1)
        dfDataset[col] = newCol

    return dfDataset

def preProcessDataSet():
    """this function is uesed to pre process the dataset for modelling"""

    dataSetTrain = 'dataset.csv'
    dfDataset = pd.read_csv(dataSetTrain)
    # these columns are hard to use for KNN, so I just drop provisonally
    columnNeedDrop = [
        'latitude', 'longitude', 'thumbnail_url', 'neighbourhood', 'host_has_profile_pic',
        'host_identity_verified', 'zipcode', 'host_since', 'id', 'last_review', 'first_review',
        'city', 'description', 'name', 'amenities'
    ]

    dfDataset.drop(columnNeedDrop, axis=1, inplace=True)
    # map property type as number, the rule is {Apartment: 0.0, House: 1.0}
    dfDataset['property_type'] = LabelEncoder().fit_transform(dfDataset['property_type'])
    # map room type as number, the rule is {Entire home/apt: 0, Private room: 1, Shared room: 3}
    dfDataset['room_type'] = LabelEncoder().fit_transform(dfDataset['room_type'])
    # map bed type as number, the rule is {Real Bed: 0, Futon: 1, Airbed:2, Pull-out Sofa: 3}
    dfDataset['bed_type'] = LabelEncoder().fit_transform(dfDataset['bed_type'])
    # map cancellation_policy
    dfDataset['cancellation_policy'] = LabelEncoder().fit_transform(dfDataset['cancellation_policy'])
    # map cleaning_fee
    dfDataset['cleaning_fee'] = LabelEncoder().fit_transform(dfDataset['cleaning_fee'])
    # map host_has_profile_pic
    # dfDataset['host_has_profile_pic'] = dfDataset['host_has_profile_pic'].apply(mapHostHasProfilePic)
    # # map host_identity_verified
    # dfDataset['host_identity_verified'] = dfDataset['host_identity_verified'].apply(mapHostIdentityVerified)
    # map instant_bookable
    dfDataset['instant_bookable'] = LabelEncoder().fit_transform(dfDataset['instant_bookable'])

    # cityLabel = LabelEncoder().fit_transform(dfDataset['city'])
    # dfDataset['city'] = OneHotEncoder(categories='auto').fit_transform(cityLabel.reshape(-1, 1))
    #
    # amenitiesLabel = LabelEncoder().fit_transform(dfDataset['amenities'])
    # dfDataset['amenities'] = OneHotEncoder(categories='auto').fit_transform(amenitiesLabel.reshape(-1, 1))
    #
    # nameLabel = LabelEncoder().fit_transform(dfDataset['name'])
    # dfDataset['name'] = OneHotEncoder(categories='auto').fit_transform(nameLabel.reshape(-1, 1))
    #
    # descriptionLabel = LabelEncoder().fit_transform(dfDataset['description'])
    # dfDataset['description'] = OneHotEncoder(categories='auto').fit_transform(descriptionLabel.reshape(-1, 1))
 
    print('before dropna')
    print(dfDataset.shape[1], dfDataset.shape[0])
    dfDataset.dropna(axis=0, inplace=True)
    print('after dropna')
    print(dfDataset.shape[1], dfDataset.shape[0])
    

    dfDataset['host_response_rate'] = dfDataset['host_response_rate'].str.replace('%', '').astype(float)
    # finally, you get the data you can use for modelling
    dfDataset = normalization(dfDataset)
    # we use review_scores_rating as y
    allLabelData = pd.DataFrame(dfDataset['review_scores_rating'],columns=['review_scores_rating'])
    # and left are our features
    allFeatureData = dfDataset.drop('review_scores_rating', axis=1)
    print(dfDataset.dtypes)
    #save data in the separate csv files
    createFeature = 'feature.csv'
    createLabel = 'label.csv'
    allLabelData.to_csv(createLabel,index=False)
    allFeatureData.to_csv(createFeature,index=False)

def main():
    preProcessDataSet()

if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', 1000)
    main()
