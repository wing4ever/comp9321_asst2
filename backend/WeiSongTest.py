import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

def mapPropertyType(propertyType):
    """this function is used to handle the property_tyoe column"""

    if propertyType == 'Apartment':
        return 0
    elif propertyType == 'House':
        return 1

def mapRoomType(roomType):
    """this function is used to handle the room type column"""

    if roomType == 'Entire home/apt':
        return 0
    elif roomType == 'Private room':
        return 1
    elif roomType == 'Shared room':
        return 2

def mapBedType(bedType):
    """this function is used to handle the bed type column"""

    if bedType == 'Real Bed':
        return 0
    elif bedType == 'Futon':
        return 1
    elif bedType == 'Airbed':
        return 2
    elif bedType == 'Pull-out Sofa':
        return 3

def mapCancellationPolicy(policy):
    if policy == 'strict':
        return 3
    elif policy == 'moderate':
        return 2
    elif policy == 'flexible':
        return 1

def mapCleaningFee(value):
    if value:
        return 1
    else:
        return 0

def mapHostHasProfilePic(value):
    if value == 't':
        return 1
    else:
        return 0

def mapHostIdentityVerified(value):
    if value == 't':
        return 1
    else:
        return 0

def mapInstanceBookable(value):
    if value == 't':
        return 1
    else:
        return 0

def preProcessDataSet():

    dataSetTrain = 'dataset.csv'
    dfDataset = pd.read_csv(dataSetTrain)

    # these columns are hard to use for KNN, so I just drop provisonally
    columnNeedDrop = [
        'latitude', 'longitude', 'thumbnail_url', 'neighbourhood'
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
    dfDataset['host_has_profile_pic'] = dfDataset['host_has_profile_pic'].apply(mapHostHasProfilePic)
    # map host_identity_verified
    dfDataset['host_identity_verified'] = dfDataset['host_identity_verified'].apply(mapHostIdentityVerified)
    # map instant_bookable
    dfDataset['instant_bookable'] = LabelEncoder().fit_transform(dfDataset['instant_bookable'])
    cityLabel = LabelEncoder().fit_transform(dfDataset['city'])
    dfDataset['city'] = OneHotEncoder(categories='auto').fit_transform(cityLabel.reshape(-1, 1))
    amenitiesLabel = LabelEncoder().fit_transform(dfDataset['amenities'])
    dfDataset['amenities'] = OneHotEncoder(categories='auto').fit_transform(amenitiesLabel.reshape(-1, 1))
    nameLabel = LabelEncoder().fit_transform(dfDataset['name'])
    dfDataset['name'] = OneHotEncoder(categories='auto').fit_transform(nameLabel.reshape(-1, 1))
    descriptionLabel = LabelEncoder().fit_transform(dfDataset['description'])
    dfDataset['description'] = OneHotEncoder(categories='auto').fit_transform(descriptionLabel.reshape(-1, 1))

    print(dfDataset.shape[1], dfDataset.shape[0])
    dfDataset.dropna(axis=0, inplace=True)
    print(dfDataset.shape[1], dfDataset.shape[0])
    print(dfDataset.head(10))


def main():
    preProcessDataSet()

if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', 1000)
    main()