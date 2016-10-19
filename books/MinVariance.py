import os
import pandas as pd
from mosekTools.solver import solver as ms


def lsq(matrix, rhs):
    return pd.Series(index=matrix.columns,
                     data=ms.lsq_pos(matrix.values, rhs.values))


def Sharpe_Ratio(ts):
    return 16 * ts.mean() / ts.std()


if __name__ == '__main__':
    # load data from csv file
    data = pd.read_csv(os.path.join("data", "data.csv"), index_col=0, parse_dates=True)

    returns = data.pct_change(fill_method="ffill").fillna(0.0)

    print(returns)

    stocks = returns[["GOOG", "T", "AAPL", "GS", "IBM"]]
    print(stocks)
    index = returns["^GSPC"]
    print(type(index))
    # construct a rhs
    rhsZero = pd.TimeSeries(index=stocks.index, data=0.0)

    wMin = lsq(matrix=stocks, rhs=rhsZero)
    wTrack = lsq(matrix=stocks.cumsum(), rhs=index.cumsum())

    d = dict()
    d["Min Variance"] = (stocks * wMin).sum(axis=1)
    d["Index"] = index
    d["1/N"] = stocks.mean(axis=1)
    d["Tracking"] = (stocks * wTrack).sum(axis=1)
    frame = pd.DataFrame(d)

    # apply some simple diagnostics
    print("Annualized Sharpe ratio")
    print(frame.apply(Sharpe_Ratio))
    print("Standard deviation of returns")
    print(frame.std())



