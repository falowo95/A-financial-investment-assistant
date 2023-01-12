# importation of needed packages
import numpy as np
import pandas as pd
import pandas_datareader as web
import datetime as dt
import json
# koko

#importation of needed packages
import numpy as np
import pandas as pd
import pandas_datareader as web
import datetime as dt
import json
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, LSTM

# [17]K.  Willems, "Algorithmic Trading", Datacamp, 2019.
# [Online]. Available: https://www.datacamp.com/community/tutorials/finance-python-trading.
# [Accessed: 13- May- 2022].


def closing_prices(choice, start_date, end_date):
    data = web.DataReader(choice, 'yahoo', start_date, end_date)["Close"]
    data = data.to_json()
    return json.loads(data)


def daily_percentage_change(choice, start_date, end_date):
    data = web.DataReader(choice, 'yahoo', start_date, end_date)['Adj Close']

    for col in data.columns:
        data[f'{col} daily_pct_change'] = data[col].pct_change()
        data[f'{col} daily_pct_change'].fillna(0, inplace=True)
        data = data.drop(columns=col)
    data = data.to_json()
    return json.loads(data)


def simple_moving_averages(choice, start_date, end_date):
    data = web.DataReader(choice, 'yahoo', start_date, end_date)['Adj Close']

    for col in data.columns:
        # 20 days to represent the 22 trading days in a month
        data[f'{col} 20_day'] = data[col].rolling(20).mean()

        # 250 days to represent the 250 trading days in a year
        data[f'{col} 200_day'] = data[col].rolling(200).mean()

        data = data.drop(columns=col)
    data = data.to_json()
    return json.loads(data)


def bollinger_bands(choice, start_date, end_date):
    data = web.DataReader(choice, 'yahoo', start_date, end_date)

    # 20 days to represent the 22 trading days in a month
    data['20_day'] = data['Adj Close'].rolling(20).mean()

    data["std"] = data['Adj Close'].rolling(20).std()

    data["bollinger_up"] = data["20_day"] + data["std"] * 2  # Calculate top band

    data["bollinger_down"] = data['20_day'] - data["std"] * 2  # Calculate bottom band

    data = data.drop(columns=['High', 'Low', 'Open', 'Close', 'Volume', '20_day', 'std'])

    data = data.to_json()
    return json.loads(data)
    

def cumulative_daily_returns(choice, start_date, end_date):
    data = None
    data = web.DataReader(choice, 'yahoo', start_date, end_date)['Adj Close']


    for col in data.columns:

        data[f'{col} daily_pct_change'] = data[col].pct_change()
        data[f'{col} daily_pct_change'].fillna(0, inplace=True)

        data[f'{col} cum_daily_returns'] = (1 + data[f'{col} daily_pct_change']).cumprod()
        data = data.drop(columns=[col,f'{col} daily_pct_change'])
    data = data.to_json()
    return json.loads(data)

def cumulative_monthly_returns(choice, start_date, end_date):

    data = web.DataReader(choice, 'yahoo', start_date, end_date)['Adj Close']
    for col in data.columns:
        data[f'{col} daily_pct_change'] = data[col].pct_change()
        data[f'{col} daily_pct_change'].fillna(0, inplace=True)

        data[f'{col} cum_daily_returns'] = (1 + data[f'{col} daily_pct_change']).cumprod()
        data[f'{col} cum_monthly_returns'] = data[f'{col} cum_daily_returns'].resample('M').mean()

        data = data.drop(columns=[col, f'{col} daily_pct_change', f'{col} cum_daily_returns'])

    data = data.to_json()
    return json.loads(data)


def daily_log_returns(choice, start_date, end_date):
    data = None
    data = web.DataReader(choice, 'yahoo', start_date, end_date)

    data['daily_pct_change'] = data['Adj Close'].pct_change()
    data['daily_pct_change'].fillna(0, inplace=True)
    # Daily log returns
    data['daily_log_returns'] = np.log(data['daily_pct_change'] + 1)
    data = data.drop(columns=['High', 'Low', 'Open', 'Close', 'Volume', 'Adj Close', 'daily_pct_change'])


    data = data.to_json()
    return json.loads(data)



def volatility_info(choice, start_date, end_date):
    data = web.DataReader(choice, 'yahoo', start_date, end_date)['Adj Close'].pct_change()
    min_periods = 75

    for col in data.columns:
        data[f"{col} volaltility"] = data[col].rolling(min_periods).std() * np.sqrt(min_periods)

    data = data.drop(columns=choice)

    data = data.to_json()
    return json.loads(data)


def sharpe_ratio(choice, start_date, end_date):

    data = None
    data = web.DataReader(choice, 'yahoo', start_date, end_date)['Adj Close']

    TRADING_DAYS = 252

    for col in data.columns:

        data[f"{col} returns"] = np.log(data[col] / data[col].shift(1))
        data[f"{col} returns"].fillna(0, inplace=True)

        data[f"{col} volatility"] = data[f"{col} returns"].rolling(window=TRADING_DAYS).std() * np.sqrt(TRADING_DAYS)
        data[f"{col} sharpe_ratio"] = data[f"{col} returns"].mean() / data[f"{col} volatility"]


        data = data.drop(columns=[col,f"{col} volatility",f"{col} returns"])

    data = data.to_json()
    return json.loads(data)


def prediction(i):
    # [36] N. Nine, Youtube.com, 2021. [Online].
    # Available: https://www.youtube.com/watch?v=PuZY9q-aKLw&t=1274s.
    #         [Accessed: 19- Mar- 2022].
    # above reference in the dissertaion is a reference to the tutorial video researched for my implementation
    model = load_model(f"trained_models/{i}_predictive_model.h5")
    start_date = dt.datetime(2012, 1, 1)
    end_date = dt.datetime(2020, 1, 1)
    data = web.DataReader(i, 'yahoo', start_date, end_date)

    # now we will see how well the model will perfom on past data data we already have
    # testing the model accuracy on existing data data the model has not seen before
    test_start_date = dt.datetime(2020, 1, 1)
    test_end_date = dt.datetime.now()
    test_data = web.DataReader(i, 'yahoo', test_start_date, test_end_date)

    prediction_days = 60
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_DATA = scaler.fit_transform(data.Close.values.reshape(-1, 1))
    actual_prices = test_data.Close.values

    # data containing both the training data and the test data
    total_dataset = pd.concat((data.Close, test_data.Close), axis=0)

    # this is what the model will take in as input
    model_inputs = total_dataset[len(total_dataset) - len(test_data) - prediction_days:].values

    # we now have to reshape the model inputs from the new dataframe
    model_inputs = model_inputs.reshape(-1, 1)

    # now we have to scale it down with the existing scaler
    model_inputs = scaler.transform(model_inputs)

    # now we will predict based on the data we have not seen before (test data)
    # here we evaluate how well our model performs on test data
    x_test = []
    for x in range(prediction_days, len(model_inputs) + 1):
        x_test.append(model_inputs[x - prediction_days:x, 0])

    # we dont need ytest here because we already have the actual stock prices
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    predicted_prices = model.predict(x_test)
    # because the prices were scaled before we now rescale them back to the actual prices
    predicted_prices = scaler.inverse_transform(predicted_prices)

    # predict next day
    real_data = [model_inputs[len(model_inputs) - prediction_days:len(model_inputs + 1), 0]]
    #converting real data into a np array
    real_data = np.array(real_data)
    real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))

    prediction = model.predict(real_data)
    prediction = scaler.inverse_transform(prediction)
    response = f"{i.upper()} Price Prediction for tomorrow is  : {prediction}"
    return response
