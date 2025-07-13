# Stock Predictor

## Table of Contents
1. [Overview](#overview)
2. [Metrics](#metrics-from-model-trained-december-2024)
3. [Usage](#usage)
4. [Training/Testing](#trainingtesting)
5. [Issues](#known-issues)
6. [Dependencies](#dependencies)
7. [Authors](#authors)
8. [License](#license)


# Overview
Basic Random Forest Regression stock predictor using Python and scikit-learn.
Uses a Grid Search Cross Validator with 16 possible configurations to find the best fit model.


# Metrics (From model trained December 2024)
- Mean Average Error (MAE):      1.3335
- Root Mean Square Error (RMSE): 4.6514
- R Squared:                     99.991%


# Usage
If importing a model or data manually, rename the files to stock_model.pkl and stock_info.csv respectively and place them in the root directory

If no stock_info.csv file is present, running either training.py or main.py will automatically pull the data.
The unmodified program will pull all tickers from the Wikipedia S&P500 list and get all YFinance data from 01/01/2010 to the present day. To modify this, edit lines 22-24 of datasets.py

Use `python main.py` to run the main GUI program.


# Training/Testing
Use `python training.py`
  Unmodified, the training process uses 4 cores and approx. 32GB of RAM. 
  The RAM usage can be lowered by either changing n_jobs=4 on line 70 of training.py or narrowing the dataset.

After training, the Efficiency Metrics will be printed to the console.
To view the metrics without retraining, use 
'''shell
python training.py -metrics
'''


# Known Issues
- Selecting a stock may cause an incorrect historical graph to show
- The frontend may have certain moments where callbacks may seem unresponsive
- Pressing predict with no stock_model.pkl file will throw an error


# Dependencies
- [pandas](https://pandas.pydata.org/)
- [numpy](https://numpy.org/)
- [dearpygui](https://github.com/hoffstadt/DearPyGui)
- [yfinance](https://pypi.org/project/yfinance/)
- [scikit-learn](https://scikit-learn.org/stable/)


# Authors
- **Sandro Mocevic**
- **Aimar Murua**
- **Nouri Clarke**


# License
This repository has a 'Do Whatever You Want With It' License. This project was created as a challenge for the authors' own learning within a classroom environment, and may have oversights that come as a result of class deadlines.