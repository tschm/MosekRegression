import datetime as dt
import os

import pandas as pd
import pandas.io.data as pw
import numpy as np


def get_index_components(index="dax"):
    x = pd.read_csv("data/" + index + "/symbols.csv", header=0, index_col=0)
    return x


def get_data_yahoo(symbols, start=dt.datetime(2000, 1, 1), end=dt.datetime.today(), series="Adj Close"):
    return pd.DataFrame(
        {symb: pw.get_data_yahoo(symb, start, end)[series] for symb in symbols}
    )


def get_index_data(index="dax"):
    return pd.read_csv(os.path.join("data", index, "data.csv"), index_col=0, parse_dates=True)


def get_random_covariance_Matrix(eigenvalues):
    n = len(eigenvalues)
    Q, R = np.linalg.qr(np.random.randn(n, n), 'full')
    return np.dot(np.dot(Q, np.diag(eigenvalues)), np.transpose(Q))


def get_random_data(covariance_matrix, n):
    cc = np.linalg.cholesky(covariance_matrix)

    m = np.size(covariance_matrix, 0)
    Q = np.linalg.qr(np.random.randn(n, m))[0]

    A = np.dot(Q, np.transpose(cc))

    return pd.DataFrame(np.sqrt(n) * A)

