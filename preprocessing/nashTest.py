import joblib
import pandas as pd
import numpy as np
from tabulate import tabulate
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score

def loadData(dataFeature,dataLabel):
    #this function is used to load data and divide it into train and test class
    
    dfFeature = pd.read_csv(dataFeature,index_col=False ).to_numpy()
    dfLabel = pd.read_csv(dataLabel,index_col=False ).to_numpy()
    return train_test_split(dfFeature,dfLabel,test_size=0.3,random_state=0)
    

def trainModel(train_x, test_x, train_y, test_y):
    #this function is used to train different models with data
    
    print("linear regression model")
    #create linear regression model
    regr = linear_model.LinearRegression()
    #train the model
    regr.fit(train_x,train_y)
    #predict the results
    predicted_y = regr.predict(test_x) 
    #transform input data
    train_x_ = PolynomialFeatures(degree=2, include_bias=False).fit_transform(train_x)
    test_x_ = PolynomialFeatures(degree=2, include_bias=False).fit_transform(test_x)
    #create linear regression model
    regr = linear_model.LinearRegression()
    #train the model
    regr.fit(train_x_,train_y)
    #predict the results
    predicted_y = regr.predict(test_x_)
    joblib.dump(regr, 'linearRegression.pkl')
    
    return predicted_y
    
if __name__ == "__main__":
    #load data from csv files
    train_x, test_x, train_y, test_y = loadData("feature.csv","label.csv")
    #train the model
    trainModel(train_x, test_x, train_y, test_y)