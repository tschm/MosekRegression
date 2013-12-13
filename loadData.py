import datetime as dt
import mosekTools.data.Data as Data

if __name__ == '__main__':
    # fetch individual stocks and the S&P index
    s = dt.datetime(2010, 1, 1)
    e = dt.datetime(2012, 12, 31)
    symbols = ["GS", "AAPL", "IBM", "GOOG", "T", "^GSPC"]
    Data.get_data_yahoo(symbols=symbols, start=s, end=e).to_csv("data/data.csv")
