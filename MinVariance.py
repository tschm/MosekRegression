import os

import pandas as pd
import matplotlib.pyplot as mPlot

from mosekTools.solver import solver as ms


def compute_return(ts):
    ts = ts.dropna()
    return ts.diff() / ts.shift(1)


def lsq(X, y):
    return pd.Series(index=X.columns,
                     data=ms.lsq_pos(X.values, y.values))


def ann_Sharpe_ratio(ts):
    return 16 * ts.mean() / ts.std()


if __name__ == '__main__':
    # load data from csv file
    data = pd.read_csv(os.path.join("data", "data.csv"), index_col=0,
                       parse_dates=True)

    stocks = data[["GOOG", "T", "AAPL", "GS", "IBM"]]
    index = data["^GSPC"]

    retStocks = stocks.apply(compute_return).fillna(value=0.0)
    retIndex = compute_return(index).fillna(value=0.0)
    # construct a rhs
    rhsZero = pd.TimeSeries(index=retStocks.index, data=0.0)

    wMin = lsq(X=retStocks, y=rhsZero)
    wTrack = lsq(X=retStocks.cumsum(), y=retIndex.cumsum())

    d = dict()
    d["Min Variance"] = (retStocks * wMin).sum(axis=1)
    d["Index"] = retIndex
    d["1/N"] = retStocks.mean(axis=1)
    d["Tracking"] = (retStocks * wTrack).sum(axis=1)
    frame = pd.DataFrame(d)

    # apply some simple diagnostics
    print "Annualized Sharpe ratio"
    print frame.apply(ann_Sharpe_ratio)
    print "Standard deviation of returns"
    print frame.std()

    (frame + 1.0).cumprod().plot()
    mPlot.show()

