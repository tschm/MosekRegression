import datetime as dt
import os

import pandas as pd
import pandas.io.data as pw


def get_index_components(index="dax"):
    x = pd.read_csv("data/" + index + "/symbols.csv", header=0, index_col=0)
    return x


def get_data_yahoo(symbols, start=dt.datetime(2000, 1, 1), end=dt.datetime.today(), series="Adj Close"):
    return pd.DataFrame(
        {symb: pw.get_data_yahoo(symb, start, end)[series] for symb in symbols}
    )


def get_index_data(index="dax"):
    return pd.read_csv(os.path.join("data", index, "data.csv"), index_col=0, parse_dates=True)

