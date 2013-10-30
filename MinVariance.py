import os

import pandas as pd
import matplotlib.pyplot as mPlot

from mosekTools.solver import solver as ms


def lsq(matrix, rhs):
    return pd.Series(index=matrix.columns,
                     data=ms.lsq_pos(matrix.values, rhs.values))


def ann_Sharpe_ratio(ts):
    return 16 * ts.mean() / ts.std()


def returns(frame):
    def __compute_return(ts):
        ts = ts.dropna()
        return ts.diff() / ts.shift(1)

    return frame.apply(__compute_return).fillna(value=0.0)


if __name__ == '__main__':
    # load data from csv file
    data = pd.read_csv(os.path.join("data", "data.csv"), index_col=0, parse_dates=True)

    stocks = returns(data[["GOOG", "T", "AAPL", "GS", "IBM"]])
    index = returns(data[["^GSPC"]])["^GSPC"]

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
    print "Annualized Sharpe ratio"
    print frame.apply(ann_Sharpe_ratio)
    print "Standard deviation of returns"
    print frame.std()

    (frame + 1.0).cumprod().plot()
    mPlot.show()