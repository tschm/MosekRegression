import datetime as dt
import pandas as pd
import pandas.io.data as pw


def get_data_yahoo(symbols, start=dt.datetime(2000, 1, 1), end=dt.datetime.today(), series="Adj Close"):
    return pd.DataFrame(
        {s: pw.get_data_yahoo(s, start, end)[series] for s in symbols}
    )

