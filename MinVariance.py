import os

import pandas as pd

from mosekTools.solver import solver as ms


def computeReturn(ts):
    ts = ts.dropna()
    return ts.diff() / ts.shift(1)

def lsq(X, y):
    return pd.Series(index=X.columns,
                     data=ms.lsqPosFullInv(X.values, y.values))

def AnnualizedSharpeRatio(ts):
    return 16*ts.mean()/ts.std()

if __name__ == '__main__':
    # load data from csv file
    data = pd.read_csv(os.path.join("data", "data.csv"), index_col=0,
                       parse_dates=True)

    stocks = data[["GOOG", "T", "AAPL", "GS", "IBM"]]
    index = data["^GSPC"]

    retStocks = stocks.apply(computeReturn).fillna(value=0.0)
    retIndex = computeReturn(index).fillna(value=0.0)
    # construct a rhs
    rhsZero = pd.TimeSeries(index=retStocks.index, data=0.0)
    
    wMin = lsq(X=retStocks, y=rhsZero)
    wTrack = lsq(X=retStocks, y=retIndex)

    d = dict()
    d["Min Variance"] = (retStocks * wMin).sum(axis=1)
    d["Index"] = retIndex
    d["1/N"] = retStocks.mean(axis=1)
    d["Tracking"] = (retStocks * wTrack).sum(axis=1)
    frame = pd.DataFrame(d)

    # apply some simple diagnostics
    print "Annualized Sharpe ratio"
    print frame.apply(AnnualizedSharpeRatio)
    print "Standard deviation of returns"
    print frame.std()

    import matplotlib.pyplot as plt

    (frame + 1.0).cumprod().plot()
    plt.show()

