#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 14:55:44 2019

@author: blueberry

"""
import numpy as np
import pandas as pd
import torch
import matplotlib.pyplot as plt
from torch import nn, optim
import xgboost as xgb
import pickle
import torch.nn.functional as F
from tabulate import tabulate
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn import linear_model
from sklearn.preprocessing import MinMaxScaler, scale
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
from sklearn.feature_selection import VarianceThreshold
import warnings
warnings.filterwarnings("ignore")


def preprocessing_data(datafile):
    
    data_train = pd.read_csv(datafile)
    columnNeedDrop = [
        'id', 'amenities', 'description', 'first_review', 'host_since', 'last_review','latitude', 'longitude',
        'name', 'neighbourhood', 'thumbnail_url', 'zipcode',
        ]
    data_train.drop(columnNeedDrop, axis=1, inplace=True)
    data_train['host_response_rate'] = data_train['host_response_rate'].str.replace('%', '').astype(float)
    
#    columns_string = ['property_type','room_type','bed_type','cancellation_policy','city', 'host_has_profile_pic',
#        'host_identity_verified','instant_bookable'
#        ]
    
    columns_number = ['log_price','accommodates','bathrooms','cleaning_fee','number_of_reviews','review_scores_rating','bedrooms','beds']
    
#    clean the data which contain number
    for i in columns_number:
        data_train[i].fillna(0, axis = 0,inplace=True)
        data_train[i] = data_train[i].astype(float)
    
#   drop the null rows
    data_train.dropna(axis=0, inplace=True)
#    print(data_train.isnull().values.any()) 
    
#   one hot coding conbine with the label
    data = pd.get_dummies(data_train,drop_first = True)
    
    columns = data.columns
    labels = pd.DataFrame(data['review_scores_rating']/10,columns=['review_scores_rating'])
    
#   normolization which use stander scaler keep the distribution this can be change to minmax
    scaler = scale
    data = pd.DataFrame(scaler(data), columns = columns)
    
#    scaler = MinMaxScaler()
#    data = pd.DataFrame(scaler.fit_transform(data), columns = columns)
    
#   generate the data for train and text
    X_train, X_val, y_train, y_val = train_test_split(data.drop('review_scores_rating', axis=1), labels, test_size=0.2, random_state=42)
#    print(X_train.shape)
    return X_train, X_val, y_train, y_val

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
    
    
def KnnModel(train_x, test_x, train_y, test_y , n_neighbors):
    #this function is used to train different models with data
    train_x, test_x, train_y, test_y = train_x.to_numpy(), test_x.to_numpy(), train_y.to_numpy(), test_y.to_numpy()
    
    #create linear regression model
    knn = KNeighborsRegressor(algorithm='brute')
    #train the model
    model = knn.fit(train_x,train_y)

    #predict the results
    predicted_y = model.predict(test_x)

    print(tabulate([['mean_absolute_error', mean_absolute_error(test_y,predicted_y)], \
      ['mean_squared_error', mean_squared_error(test_y,predicted_y)],['r2_score',knn.score(test_x, test_y)]], headers=['Metric', 'Value'], tablefmt='orgtbl'))
    print()
    return predicted_y    

def XGBRegressor(X_train,X_val,y_train,y_val):
    
    X_train,X_val,y_train,y_val = X_train.to_numpy(),X_val.to_numpy(),y_train.to_numpy(),y_val.to_numpy()
#    print(X_train.shape)
   
    #train the model
    xgb_reg = xgb.XGBRegressor(objective ='reg:squarederror')
    xgb_reg.fit(X_train, y_train)
    training_preds_xgb_reg = xgb_reg.predict(X_train)
    val_preds_xgb_reg = xgb_reg.predict(X_val)
    
    # Printing the results
    print(tabulate([["Training MSE", round(mean_squared_error(y_train, training_preds_xgb_reg),4)], \
      ["Validation MSE", round(mean_squared_error(y_val, val_preds_xgb_reg),4)],["Training r2", round(r2_score(y_train, training_preds_xgb_reg),4)],["Validation r2", round(r2_score(y_val, val_preds_xgb_reg),4)]], headers=['Metric', 'Value'], tablefmt='orgtbl'))
        
    with open('XGBRegressor.pickle','wb') as f:
        pickle.dump(xgb_reg,f)
        
    
    print('\nSave the XGBRegressor model\n')
    return val_preds_xgb_reg, y_val


def Liner(X_train,X_val,y_train,y_val):
    
    X_train,X_val,y_train,y_val = X_train.to_numpy(),X_val.to_numpy(),y_train.to_numpy(),y_val.to_numpy()
    regr = linear_model.LinearRegression()
    #train the model
    regr.fit(X_train,y_train)
    #predict the results
    predictions = regr.predict(X_val)
    
    print(tabulate([['mean_absolute_error', mean_absolute_error(y_val,predictions)], \
      ['mean_squared_error', mean_squared_error(y_val,predictions)],['r2_score',r2_score(y_val,predictions)]], headers=['Metric', 'Value'], tablefmt='orgtbl'))
    
    print()
    return predictions

def Neural_Network(X_train, X_val, y_train, y_val):
#    print(X_train.shape)
#    print(X_val.shape)
    
#    drop the columns that data not balanced
    x_columns = X_train.columns
    sel = VarianceThreshold(threshold=0.05)
    X_train = sel.fit_transform(X_train)
    index = sel.get_support(indices=False)
    for i in range(len(index)):
        if index[i] == False:
            X_val.drop([x_columns[i]],axis=1, inplace=True)
#    print(X_train.shape)
#    print(X_val.shape)
    
#   create data batch 
    train_batch = np.array_split(X_train, 50)
    label_batch = np.array_split(y_train, 50)
    
    
    for i in range(len(train_batch)):
        train_batch[i] = torch.from_numpy(train_batch[i]).float()
    for i in range(len(label_batch)):
        label_batch[i] = torch.from_numpy(label_batch[i].values).float().view(-1, 1)
    
#    print(train_batch[0].shape)
#    print(label_batch[0].shape)
    X_val = torch.from_numpy(X_val.values).float()
    y_val = torch.from_numpy(y_val.values).float().view(-1, 1)
#    print(X_val.shape)
#    print(y_val.shape)

#  training the model 
    model = FeedForward()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)  # Minimise the loss using the Adam algorithm.
    
    train_losses, test_losses ,r2_scores= [], [], []
    epochs = 1000
    for e in range(epochs):
        model.train()
        train_loss = 0
        for i in range(len(train_batch)):
            optimizer.zero_grad()

            output = model(train_batch[i])
#            print(output)
            loss = criterion(output, label_batch[i])
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            
            
#       record the loss for display and display graph       
        test_loss = 0
        with torch.no_grad():
            model.eval()
            predictions = model(X_val)
            test_loss += criterion(predictions, y_val)
        r2score = r2_score(y_val,predictions)    
            
        train_losses.append(train_loss/len(train_batch))
        test_losses.append(test_loss)
        r2_scores.append(r2score)
        print("Epoch: {}/{}.. ".format(e+1, epochs),
              "Training Loss: {:.3f}.. ".format(train_loss/len(train_batch)),
              "Test Loss: {:.3f}.. ".format(test_loss),
              "r2_score: {:.3f}..".format(r2score))
        
#    plot the graph show the results       
    plt.plot(train_losses, label='Training loss')
    plt.plot(test_losses, label='Validation loss')
    plt.plot(np.array(r2_scores)*20, label='r2_score')
    plt.legend(frameon=False)
    plt.show()
    
    torch.save(model.state_dict(), "./model.pth")
    print("Saved nural network model\n")
    
    results = []
    for i in predictions:
        if abs(i) >10:
            results.append(10.0000)
        else:
            results.append(round(abs(float(i)),4))
    
    return results,y_val

def main():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("Using device: " + str(device))
    
    #X_train, X_val, y_train, y_val = preprocessing_data('test.csv')
    X_train, X_val, y_train, y_val = preprocessing_data('train.csv')
    
    #using neural_network model to predicte
    print('1.Neural_Network model:\n')
    neual_results, true_results = Neural_Network(X_train, X_val, y_train, y_val)
    
    X_train, X_val, y_train, y_val = preprocessing_data('train.csv')
    #using XGB Regression to predicte
    print('2.XGB Regression model:\n')
    reg_results, _ = XGBRegressor(X_train, X_val, y_train, y_val)
    
     #using Normal Regression to predicte
    print('3.Normal Regression model:\n')
    nor_reg_results = Liner(X_train,X_val,y_train,y_val)
    
    print('4.Knn Model:\n')
    knn_results = KnnModel(X_train,X_val,y_train,y_val, 5)
    
    return neual_results, true_results , abs(reg_results), nor_reg_results, knn_results 

if __name__ == "__main__":
    neual_results,true_results ,reg_results, nor_reg_results, knn_results = main()    
    