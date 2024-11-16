# write in terminal pip install yfinance
import yfinance as yf

# Fetch stock data for a specific ticker (e.g., AAPL)
data = yf.download('AAPL', start='2013-01-01', end='2023-12-31')

# Print the data
print(data.head())

