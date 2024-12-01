#stl imports
import csv
from datetime import timedelta, datetime
import joblib
from os import path

#external library imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.preprocessing import OneHotEncoder

#project imports
from classes.hashmap import *
import data.datasets as datasets
import data.globals as globals


from itertools import islice

def train_model():
  columns = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
  all_stocks = []

  print("processing stock info")
  for stock, data in datasets.stock_info_iter():
    try:
      df = pd.DataFrame.from_dict(data, orient="index", columns=columns)
    except ValueError as e:
      print("error creating frame")
      raise
   
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)
    df["Stock_ID"] = stock

    df["Tomorrow"] = df["Close"].shift(-1) 
    for lag in range(1, 4):
      df[f"Close_lag_{lag}"] = df["Close"].shift(lag)
  
    df = df.dropna()
    all_stocks.append(df) 

    print(f"done processing {stock}")

  df = pd.concat(all_stocks, axis=0)
  df[["Open", "High", "Low", "Close", "Adj Close", "Volume"]] = df[["Open", "High", "Low", "Close", "Adj Close", "Volume"]].astype("float32")


  encoder = OneHotEncoder(sparse_output=False)
  stock_id = encoder.fit_transform(df[["Stock_ID"]])
  stock_df = pd.DataFrame(stock_id, index=df.index, columns=encoder.get_feature_names_out(["Stock_ID"]))

  df["Stock_ID"] = pd.Categorical(df["Stock_ID"])
  stock_df = pd.get_dummies(df["Stock_ID"], prefix="Stock_ID")

  df = pd.concat([df, stock_df], axis=1)

  # feature_columns = columns + [f"Close_lag_{lag}" for lag in range(1, 6)] + ["Stock_ID"] + list(stock_df.columns)
  feature_columns = columns + [f"Close_lag_{lag}" for lag in range(1, 4)] + list(stock_df.columns)


  train = df.iloc[:-100]
  test = df.iloc[1::2] #get every other column to better estimate efficacy

  X_train, y_train = train[feature_columns], train["Tomorrow"]

  param_grid = {
    'n_estimators': [200, 300],
    'max_depth': [20, None],
    'min_samples_split': [5, 10],
    'min_samples_leaf': [2, 4]
  }
   
  grid_search = GridSearchCV(RandomForestRegressor(random_state=1, n_jobs=-1, verbose=2), param_grid, n_jobs=4, cv=TimeSeriesSplit(n_splits=5), verbose=2)
  grid_search.fit(X_train, y_train)

  print("best model found")

  model = grid_search.best_estimator_
  model.fit(X_train, y_train)

  print("model trained")

  #prediction quality assessment
  y_test = test["Tomorrow"]
  y_pred = model.predict(test[feature_columns])

  print()
  print("Efficiency Metrics")
  print(f"MAE: {mean_absolute_error(y_test, y_pred)}")
  print(f"RMSE: {root_mean_squared_error(y_test, y_pred)}")
  print(f"R2: {r2_score(y_test, y_pred)}")

  with open("cols.conf", "w", newline="") as file:
    writer = csv.writer(file, delimiter='|')
    writer.writerow(columns)
    writer.writerow(feature_columns)

  joblib.dump(model, "stock_model.pkl")


def visualize_model():
  current_date = pd.Timestamp(datetime.now()) 
  start_date = max(df.index[-1], current_date)
  future_dates = pd.date_range(start=start_date + timedelta(days=1), periods=30)  # 30 days

  future_df = pd.DataFrame(index=future_dates)
  future_df["Close"] = None

  # "Predict future prices"
  last_row = df.iloc[-1][feature_columns].to_frame().T
  for i in range(len(future_df)):
    predicted_close = model.predict(last_row)[0]

    if i > 0:
      historical_volatility = df["Close"].pct_change().std()
      predicted_close = max(predicted_close, future_df.iloc[i - 1]["Close"] * (1-historical_volatility))  
      predicted_close = min(predicted_close, future_df.iloc[i - 1]["Close"] * (1+historical_volatility))  

    future_df.iloc[i, future_df.columns.get_loc("Close")] = predicted_close

    last_row = pd.DataFrame([[
      predicted_close,
      last_row.iloc[0]["Volume"] * np.random.uniform(0.98, 1.02),
      predicted_close * np.random.uniform(0.99, 1.01),
      predicted_close * np.random.uniform(1.00, 1.02),
      predicted_close * np.random.uniform(0.98, 1.00), 
      *last_row.iloc[0][[f"Close_lag_{lag}" for lag in range(1, 6)]].values.tolist(),
    ]], columns=feature_columns)

  #Plot with future predictions
  plt.figure(figsize=(10, 6))
  plt.plot(future_df.index, future_df["Close"], label="Predicted Prices", color="orange")
  plt.title("Predicted Future Stock Prices (Next 30 Days)")
  plt.xlabel("Date")
  plt.ylabel("Price")
  plt.legend()
  plt.grid()
  plt.show()


def train_test():
  datasets.download_data()

  print("Calling train model")
  train_model()
  print("model trained")


train_test()