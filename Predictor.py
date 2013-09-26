import pandas as pd
import numpy as np
import MosekSolver as mp

def computeReturn(ts):
    ts = ts.dropna()
    return ts.diff() / ts.shift(1)

def normalize(ts):
    return ts/np.linalg.norm(ts.values,2)

def lasso(X, y, lamb):
    e = np.eye(X.shape[1])
    print e
    return pd.Series(index=X.columns,
                     data=mp.lsqSparse(X.values, y.values, e, lamb, np.zeros(len(y))))


if __name__ == '__main__':
    # load data from csv files
    data = pd.read_csv("data.csv", index_col=0, 
                                   parse_dates=True)

    apple = data["AAPL"]
    r = computeReturn(apple)

    d = dict()
    for c in [3, 5, 8, 13, 21, 34, 55]:
        d["m" + str(c)] = pd.ewma(r, com=c, min_periods=15)

    X = pd.DataFrame(d)
    # shift returns as we are trying to predict the next day return...
    y = r.shift(-1)

    X = X.truncate(before="01-02-2010").fillna(0.0)
    y = y.truncate(before="01-02-2010").fillna(0.0)

    X = X.apply(normalize)
    y = normalize(y)
    print lasso(X,y,0.0)
    
    
    
    