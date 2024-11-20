from classes.hashmap import *
import yfinance as yf
import pandas as pd
import csv

def download_data():

  url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
  sp500_table = pd.read_html(url)
  sp500_tickers = sp500_table[0]['Symbol'].tolist()
  

  data : pd.DataFrame = yf.download(sp500_tickers, period="max", group_by='ticker')
  # data = yf.download(sp500_tickers, start='2022-01-01', end='2022-01-31', group_by='ticker')

  failed = [stock for stock in sp500_tickers if stock not in data.columns.levels[0]]
  print(failed)

  with open("stock_info.csv", "x", newline='') as file:
    writer = csv.writer(file, delimiter="|")

    for stock in sp500_tickers:
      row_count = sum(1 for _, row in data[stock].iterrows() if not pd.isna(row.iloc[0]))

      if stock in failed or row_count == 0:
        continue

      writer.writerow([stock, row_count])

      for _, row in data[stock].iterrows():
        if pd.isna(row.iloc[0]): #skip row if no data for date exists
          continue

        list = [str(row.name)[:9]]
        list.extend(row)

        writer.writerow(list)

      print(f"{stock} writing finished")


def get_stock_list(name_list : list):
  
  with open("stock_info.csv", mode="r") as file:
    reader = csv.reader(file, delimiter='|')
    for line in reader:

      if (len(line)) == 2:
        name_list.append(line[0])
    



# stocks_list = HashMap(len(sp500_tickers))

# for i in sp500_tickers:
#     data_stock = data[i]
#     size = len(data_stock)
#     stock = HashMap(size)
#     for i,k in enumerate(data_stock.index):
#         value = []
#         date_string = str(k)
#         parsed_date = datetime.fromisoformat(date_string)
#         cleaned_date = parsed_date.strftime('%Y-%m-%d')
#         for j in data_stock.iloc[i]:
#             value.append(j)

#         stock.put(cleaned_date,value)

#     stocks_list.put(i,stock)

# print(stocks_list.get("AAPL"))


