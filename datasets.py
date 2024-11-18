from classes.hashmap import *
from datetime import datetime
# write in terminal pip install yfinance
import yfinance as yf

data = yf.download('AAPL', start='2013-01-01', end='2013-01-31')

apple = HashMap()
for i,k in enumerate(data.index):
    value = []
    date_string = str(k)
    parsed_date = datetime.fromisoformat(date_string)
    cleaned_date = parsed_date.strftime('%Y-%m-%d')
    for j in data.iloc[i]:
        value.append(j)

    apple.put(cleaned_date,value)

print(len(apple))
print(apple.get('2013-01-02'))

stock = {"APPL": [[]], "TSLA": [[]]}


