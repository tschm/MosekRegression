import pandas as pd
import pandas.io.data as Web


def get_data_yahoo(symbols, start, end, type="Adj Close"):
    return pd.DataFrame(
        {symb: Web.get_data_yahoo(symb, start, end)[type] for symb in symbols}
    )


