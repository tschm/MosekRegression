import datetime as dt

import pandas as pd

import solver as sl
import mosekTools.data.Data as Data
import mosekTools.util.Model as Model


### load data from csv files
data = Data.get_index_data("dax")

### compute returns
returns = data.pct_change(fill_method="ffill").fillna(0.0)

### compute portfolio weights (for a set of portfolios)
w = dict()
w["a"] = sl.experiment1(returns.truncate(before=dt.datetime(2010, 1, 1), after=dt.datetime(2012, 1, 1)))
w["b"] = sl.experiment2(returns.truncate(before=dt.datetime(2010, 1, 1), after=dt.datetime(2012, 1, 1)), lev=1.5)
w = pd.DataFrame(w)

### weights
print w
print w.apply(sl.report)

### profit per strategy
profit = pd.DataFrame(
    {key: (returns.truncate(before=dt.datetime(2012, 1, 1)) * w[key]).sum(axis=1) for key in w.keys()})
print profit.apply(Model.summary)

### plot profits
Model.plot(profit["b"], title="Leverage Experiment", bins=20)

import matplotlib.pyplot as mPlot

mPlot.show()


