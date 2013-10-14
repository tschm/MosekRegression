import pandas as pd
import pandas.io.data as Web


def get_data_yahoo(symbols, start, end, series="Adj Close"):
    return pd.DataFrame(
        {symb: Web.get_data_yahoo(symb, start, end)[series] for symb in symbols}
    )
