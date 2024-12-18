#stl imports
import csv
import joblib

#external library imports
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit

#project imports
import data.datasets as datasets



def pull_training_data(columns):
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


  df["Stock_ID"] = pd.Categorical(df["Stock_ID"])
  stock_df = pd.get_dummies(df["Stock_ID"], prefix="Stock_ID")

  df = pd.concat([df, stock_df], axis=1)
  return df, stock_df


def train_model():
  columns = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
  df, stock_df = pull_training_data(columns)

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


def metrics():
  with open("cols.conf", "r", newline="") as file:
    reader = csv.reader(file, delimiter="|")
    columns = next(reader)
    feature_columns = next(reader)

  df, stock_df = pull_training_data(columns)

  print("loading model")

  model = joblib.load("stock_model.pkl")

  test = df.groupby("Stock_ID", observed=False).tail(30)

  y_test = test["Tomorrow"]
  X_test = test[feature_columns]

  y_pred = model.predict(X_test)

  print()
  print("Efficiency Metrics")
  print(f"MAE: {mean_absolute_error(y_test, y_pred)}")
  print(f"RMSE: {root_mean_squared_error(y_test, y_pred)}")
  print(f"R2: {r2_score(y_test, y_pred)}")


import sys


def train():
  datasets.download_data()

  if (sys.argv[1] == "-metrics"):
    metrics()

  else:
    print("Calling train model")
    train_model()
    print("model trained")


train()