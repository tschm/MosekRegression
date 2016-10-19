from datetime import datetime
import pandas_datareader.data as web


if __name__ == '__main__':
    # fetch individual stocks and the S&P index
    symbols = ["GS", "AAPL", "IBM", "GOOG", "T", "^GSPC"]
    f = web.DataReader(symbols, 'yahoo', datetime(2010, 1, 1), datetime(2015, 3, 1))["Adj Close"]
    print(f)
    f.to_csv("data/data.csv")
