# -*- coding: utf-8 -*-
"""Stock Price Prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/118mcodc_NMK6AALxdhu3dbKCaw5d56ZY
"""

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15, 6

from google.colab import drive
drive.mount('/content/drive')

display (os.getcwd())

os.chdir ('/content/drive/MyDrive/Stock_Market')
display (os.getcwd())

df =pd.read_csv("prices.csv", header=0)
display (df)

print(df.shape)

print(df.columns)

df.symbol.value_counts()

df.symbol.unique()

display(df.symbol.unique().shape)

df.symbol.unique()[0:20]

print(len(df.symbol.values))

df.info()

df.describe()

df.isnull().sum()

df.date.unique()

pd.DataFrame(df.date.unique())

df.duplicated().sum()

comp_info = pd.read_csv('securities.csv')
comp_info

comp_info["Ticker symbol"].nunique()

comp_info.info()

comp_info.isnull().sum()

comp_info.describe()

comp_info.loc[comp_info.Security.str.startswith('Face') , :]

comp_info.loc[comp_info.Security.str.startswith('Acc') , :]

comp_plot = comp_info.loc[(comp_info["Security"] == 'Yahoo Inc.') | (comp_info["Security"] == 'Xerox Corp.') | (comp_info["Security"] == 'Adobe Systems Inc')
              | (comp_info["Security"] == 'Microsoft Corp.') | (comp_info["Security"] == 'Adobe Systems Inc')
              | (comp_info["Security"] == 'Facebook') | (comp_info["Security"] == 'Goldman Sachs Group') , ["Ticker symbol"] ]["Ticker symbol"]
print(comp_plot)

for i in comp_plot:
    print (i)

def plotter(code):
    global closing_stock ,opening_stock
    f, axs = plt.subplots(2,2,figsize=(15,8))
    plt.subplot(212)
    company = df[df['symbol']==code]
    company = company.open.values.astype('float32')
    company = company.reshape(-1, 1)
    opening_stock = company


    plt.grid(True)
    plt.xlabel('Time')
    plt.ylabel(code + " open stock prices")
    plt.title('prices Vs Time')
    plt.plot(company , 'r')


    plt.subplot(211)
    company_close = df[df['symbol']==code]
    company_close = company_close.close.values.astype('float32')
    company_close = company_close.reshape(-1, 1)
    closing_stock = company_close
    plt.xlabel('Time')
    plt.ylabel(code + " close stock prices")
    plt.title('prices Vs Time')
    plt.grid(True)
    plt.plot(company_close , 'b')
    plt.show()

for i in comp_plot:
    plotter(i)

stocks= np.array (df[df.symbol.isin (['FB'])].close)
print(stocks)

display (stocks.shape)

stocks = stocks.reshape(len(stocks) , 1)
print (stocks.shape)
print(stocks)

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))
stocks = scaler.fit_transform(stocks)
display (stocks)

print (stocks.shape)

train = int(len(stocks) * 0.80)
print (train)

test = len(stocks) - train
print (test)

train = stocks[0:train]
display (train.shape)
print(train)

test = stocks[len(train) : ]
display(test.shape)
display (test)

def process_data(data , n_features):
    dataX, dataY = [], []
    for i in range(len(data)-n_features):
        a = data[i:(i+n_features), 0]
        dataX.append(a)
        dataY.append(data[i + n_features, 0])
    return np.array(dataX), np.array(dataY)

n_features = 2
trainX, trainY = process_data(train, n_features)
print(trainX.shape , trainY.shape)

testX, testY = process_data(test, n_features)
print (testX.shape , testY.shape)

stocksX, stocksY = process_data(stocks, n_features)
print (stocksX.shape , stocksY.shape)

display (trainX[:10])

display (trainY[:10])

trainX = trainX.reshape(trainX.shape[0] , 1 ,trainX.shape[1])
display (trainX.shape)

testX = testX.reshape(testX.shape[0] , 1 ,testX.shape[1])
display (testX.shape)

stocksX= stocksX.reshape(stocksX.shape[0] , 1 ,stocksX.shape[1])
display (stocksX.shape)

import math
from keras.models import Sequential
from keras.layers import Dense , BatchNormalization , Dropout , Activation
from keras.layers import LSTM , GRU
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.optimizers import Adam , SGD , RMSprop

filepath = "stock_weights1.keras"
from keras.callbacks import ReduceLROnPlateau, ModelCheckpoint
lr_reduce = ReduceLROnPlateau(monitor='val_loss', factor=0.1, min_delta=0.0001, patience=10, verbose=1)
checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='max')

model = Sequential()
model.add(GRU(256 , input_shape = (1 , n_features) , return_sequences=True))
model.add(Dropout(0.4))
model.add(LSTM(256))
model.add(Dropout(0.4))
model.add(Dense(64 ,  activation = 'relu'))
model.add(Dense(1))
print(model.summary())

model.compile(loss='mean_squared_error', optimizer=Adam(learning_rate=0.0005), metrics=['mean_squared_error'])

history = model.fit(trainX, trainY, epochs=100 , batch_size = 128 ,
          callbacks = [checkpoint , lr_reduce] , validation_data = (testX,testY))

test_pred = model.predict(testX)
display (test_pred [:10])

test_pred = scaler.inverse_transform(test_pred)
display (test_pred [:10])

testY = testY.reshape(testY.shape[0] , 1)
testY = scaler.inverse_transform(testY)
display (testY[:10])

from sklearn.metrics import r2_score
r2_score(testY,test_pred)

print("Red - Predicted Stock Prices  ,  Blue - Actual Stock Prices")
plt.rcParams["figure.figsize"] = (15,7)
plt.plot(testY , 'b')
plt.plot(test_pred , 'r')
plt.xlabel('Time')
plt.ylabel('Stock Prices')
plt.title('Check the accuracy of the model with time')
plt.grid(True)
plt.show()

train_pred = model.predict(trainX)
train_pred = scaler.inverse_transform(train_pred)
trainY = trainY.reshape(trainY.shape[0] , 1)
trainY = scaler.inverse_transform(trainY)
print ('Display Accuracy Training Data')
display (r2_score(trainY,train_pred))

stocks_pred = model.predict(stocksX)
stocks_pred = scaler.inverse_transform(stocks_pred)
stocksY = stocksY.reshape(stocksY.shape[0] , 1)
stocksY = scaler.inverse_transform(stocksY)
print ('Display Accuracy Training Data')
display (r2_score(stocksY,stocks_pred))

stocks_open = np.array(df[df.symbol.isin(['FB'])].open)
print("Open prices shape:", stocks_open.shape)

stocks_open = stocks_open.reshape(len(stocks_open), 1)
scaler_open = MinMaxScaler(feature_range=(0, 1))
stocks_open_scaled = scaler_open.fit_transform(stocks_open)

train_open = stocks_open_scaled[0:train_size]
test_open = stocks_open_scaled[train_size:]

print(f"Train open shape: {train_open.shape}")
print(f"Test open shape: {test_open.shape}")

trainX_open, trainY_open = process_data(train_open, n_features)
testX_open, testY_open = process_data(test_open, n_features)
stocksX_open, stocksY_open = process_data(stocks_open_scaled, n_features)

trainX_open = trainX_open.reshape(trainX_open.shape[0], 1, trainX_open.shape[1])
testX_open = testX_open.reshape(testX_open.shape[0], 1, testX_open.shape[1])
stocksX_open = stocksX_open.reshape(stocksX_open.shape[0], 1, stocksX_open.shape[1])

model_open = Sequential()
model_open.add(GRU(256, input_shape=(1, n_features), return_sequences=True))
model_open.add(Dropout(0.4))
model_open.add(LSTM(256))
model_open.add(Dropout(0.4))
model_open.add(Dense(64, activation='relu'))
model_open.add(Dense(1))
model_open.compile(loss='mean_squared_error', optimizer=Adam(learning_rate=0.0005), metrics=['mean_squared_error'])

history_open = model_open.fit(trainX_open, trainY_open, epochs=100, batch_size=128,
                             callbacks=[checkpoint, lr_reduce], validation_data=(testX_open, testY_open))

test_pred_open = model_open.predict(testX_open)
test_pred_open = scaler_open.inverse_transform(test_pred_open)
testY_open = testY_open.reshape(testY_open.shape[0], 1)
testY_open = scaler_open.inverse_transform(testY_open)

print("Open Price R2 Score:", r2_score(testY_open, test_pred_open))

print("Red - Predicted Open Prices, Blue - Actual Open Prices")
plt.rcParams["figure.figsize"] = (15,7)
plt.plot(testY_open, 'b')
plt.plot(test_pred_open, 'r')
plt.xlabel('Time')
plt.ylabel('Stock Open Prices')
plt.title('Open Price Prediction Accuracy')
plt.grid(True)
plt.show()

stocks_pred_open = model_open.predict(stocksX_open)
stocks_pred_open = scaler_open.inverse_transform(stocks_pred_open)
stocksY_open = stocksY_open.reshape(stocksY_open.shape[0], 1)
stocksY_open = scaler_open.inverse_transform(stocksY_open)
print('Open Price Full Dataset R2 Score:', r2_score(stocksY_open, stocks_pred_open))

results = df[df.symbol.isin(['FB'])]
results = results[2:]
results = results.reset_index(drop=True)

df_stocks_pred = pd.DataFrame(stocks_pred, columns=['Close_Prediction'])
df_stocks_pred_open = pd.DataFrame(stocks_pred_open, columns=['Open_Prediction'])

results = pd.concat([results, df_stocks_pred, df_stocks_pred_open], axis=1)

results.to_excel('results_with_both_predictions.xlsx')
display(results)