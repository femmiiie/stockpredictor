Ready to make more money than you could ever imagine?
Welcome to the world's best stock predictor out there!

How to Run:
if you are importing data/a model manually, rename them to stock_info.csv and stock_model.pkl respectively and place them in the root directory

if no stock_info.csv file is present, running either file below will automatically pull the data if needed
  -which data you want to pull can be changed by editing lines 22-24 of datasets.py

to train the model run 'python training.py'
  -it is currently configured to use 4 cores abd uses approx. 32GB of RAM
  -by narrowing the stock count/time period this can be lowered

to run the main program run 'python main.py'

Known Issues:
  -selecting a stock may cause an incorrect historical graph to show
  -the frontend may have certain moments where callbacks may seem unresponsive
  -pressing predict with no stock_model.pkl file will throw an error

Dependencies:
pandas
numpy
dearpygui
yfinance
scikit-learn

Created by:
Sandro Mocevic
Aimar Murua
Nouri Clarke