from datetime import datetime
import pandas.io.data as pw

if __name__ == '__main__':
    # fetch individual stocks and the S&P index
    s = datetime(2010, 1, 1)
    e = datetime(2015, 3, 1)
    symbols = ["GS", "AAPL", "IBM", "GOOG", "T", "^GSPC"]

    pw.get_data_yahoo(symbols, s, e)["Adj Close"].to_csv("data/data.csv")
