import datetime as dt
import mosekTools.data.Data as Data

### DAX ###
symbols = Data.get_index_components("dax").index
Data.get_data_yahoo(symbols=symbols, start=dt.datetime(2000, 7, 1)).to_csv("data/dax/data.csv")