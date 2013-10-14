import pandas as pd
import numpy as np
from mosekTools.solver import solver as mp


def computeReturn(ts):
    ts = ts.dropna()
    return ts.diff() / ts.shift(1)

def normalize(ts):
    return ts/np.linalg.norm(ts.values,2)

def lasso(X, y, lamb):
    return pd.Series(index=X.columns,
                     data=mp.lasso(X.values, y.values, lamb))


if __name__ == '__main__':
    # load data from csv files
    data = pd.read_csv("data/data.csv", index_col=0,
                       parse_dates=True)

    stock = data["GS"]
    r = computeReturn(stock)
    
    d = dict()
    for c in [2,3,5,8,13, 21, 34, 55, 89]:
        d[str(c)] = pd.ewma(r, com=c, min_periods=30)

    X = pd.DataFrame(d)
    # shift returns as we are trying to predict the next day return...
    y = r.shift(-1)

    X = X.truncate(before="01-02-2010").fillna(0.0)
    y = y.truncate(before="01-02-2010").fillna(0.0)

    X = X.apply(normalize)
    y = normalize(y)
    w = lasso(X,y,0.005)
    
    print w
    print np.corrcoef((X*w).sum(axis=1), y)
    
    #position = 1000000*(X*w).sum(axis=1)
    #profit = position*y
    #print position.mean()
    #print profit.mean()
    #profit.cumsum().plot()
    #plt.show()
    