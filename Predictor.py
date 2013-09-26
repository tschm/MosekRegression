import pandas


def computeReturn(ts):
    ts = ts.dropna()
    return ts.diff() / ts.shift(1)

if __name__ == '__main__':
    # load data from csv files
    data = pandas.read_csv("data.csv", index_col=0, parse_dates=True)

    apple = data["AAPL"]
    r = computeReturn(apple)

    d = dict()
    for c in [3, 5, 8, 13, 21, 34, 55]:
        d["m" + str(c)] = pandas.ewma(r, com=c, min_periods=15)

    X = pandas.DataFrame(d)
    # shift returns as we are trying to predict the next day return...
    y = r.shift(-1)

    X = X.truncate(before="01-02-2010").fillna(0.0)
    y = y.truncate(before="01-02-2010").fillna(0.0)

