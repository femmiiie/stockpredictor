from os import path
from classes.hashmap import *
import pandas as pd
import data.datasets as datasets
import globals
import asyncio
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit, cross_val_score
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
import matplotlib.pyplot as plt
from datetime import timedelta, datetime
import joblib

def train_model(stock_data: HashMap):
   extracted_data = {key: value for key, value in stock_data.items()}
   columns = ["Open", "High", "Low", "Close", "Volume"]
   try:
     df = pd.DataFrame.from_dict(extracted_data, orient="index", columns=columns)
   except ValueError as e:
     print("err creating df")
     raise
   
   df.index = pd.to_datetime(df.index)
   df.sort_index(inplace=True)

   df["Tomorrow"] = df["Close"].shift(-1) 
   for lag in range(1, 6):
     df[f"Close_lag_{lag}"] = df["Close"].shift(lag)
   df = df.dropna() 

   train = df.iloc[:-100]
   test = df.iloc[-100:]

   feature_columns = columns + [f"Close_lag_{lag}" for lag in range(1, 6)]
   X_train, y_train = train[feature_columns], train["Tomorrow"]
   X_test, y_test = test[feature_columns], test["Tomorrow"]

   param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
   
   grid_search = GridSearchCV(RandomForestRegressor(random_state=1), param_grid, n_jobs=-1, cv=TimeSeriesSplit(n_splits=5), verbose=1)
   grid_search.fit(X_train, y_train)
   model = grid_search.best_estimator_

  #  model = RandomForestRegressor(n_estimators=200, random_state=1)
  #  model.fit(train[columns], train["Tomorrow"])

   tscv = TimeSeriesSplit(n_splits=5)
   scores = cross_val_score(model, X_train, y_train, cv=tscv, scoring="neg_mean_squared_error")
  #  print(f"Cross-Val RMSE: {-scores.mean() ** 0.5}")

   model.fit(X_train, y_train)

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

   #prediction quality assessment
   ypred = model.predict(test[feature_columns])
   print(f"MAE: {mean_absolute_error(test['Tomorrow'], ypred)}")
   print(f"RMSE: {root_mean_squared_error(test["Tomorrow"], ypred)}")
   print(f"R2: {r2_score(test["Tomorrow"], ypred)}")

   joblib.dump(model, "stock_model.pkl")

  # Plot with future predictions
   plt.figure(figsize=(10, 6))
   plt.plot(future_df.index, future_df["Close"], label="Predicted Prices", color="orange")
   plt.title("Predicted Future Stock Prices (Next 30 Days)")
   plt.xlabel("Date")
   plt.ylabel("Price")
   plt.legend()
   plt.grid()
   plt.show()


def train_test():
    # Simplified for testing
    if not path.exists("stock_info.csv"):
        print("Error: stock_info.csv not found. Run datasets.download_data() first.")
        return

    # Get stock list and choose a stock for testing
    print(f"getting stocks")
    stock_list = datasets.get_stock_list()
    print(f"Available stocks: {stock_list}")
    print(f"got stocks")

    stock_name = stock_list[0]  # Replace with desired stock or user input
    print(f"Testing stock: {stock_name}")

    # Load stock data
    asyncio.run(datasets.pull_stock_info(stock_name))

    # Test the train_model function
    if globals.current_stock_data is not None:
        print("Calling train model")
        train_model(globals.current_stock_data)
        print("model trained")
    else:
        print("Error: No stock data loaded.")

train_test()