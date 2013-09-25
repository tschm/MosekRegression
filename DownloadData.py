import pandas.io.data as web
import datetime as dt
import pandas as pd

def fetchDataFromYahoo(symbols):
    s = dt.datetime(2010,  1,  1)
    e = dt.datetime(2012, 12, 31)
    return pd.DataFrame(
        {symb: web.get_data_yahoo(symb, s, e)["Adj Close"]
         for symb in symbols})

if __name__ == '__main__':
    # fetch individual stocks and the S&P index
    symbols = ["GS", "AAPL", "IBM", "GOOG", "T", "^GSPC"]
    fetchDataFromYahoo(symbols).to_csv("data.csv")


