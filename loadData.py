from datetime import datetime
import mosekTools.data.Data as Data

if __name__ == '__main__':
    # fetch individual stocks and the S&P index
    s = datetime(2010, 1, 1)
    e = datetime(2015, 3, 1)
    symbols = ["GS", "AAPL", "IBM", "GOOG", "T", "^GSPC"]
    Data.get_data_yahoo(symbols=symbols, start=s, end=e).to_csv("data/data.csv")
