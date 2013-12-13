import datetime as dt

import numpy as np
import pandas as pd
from mosek.fusion import Expr

import mosekTools.data.yahoo as Data
import mosekTools.solver.model.model as mModel
import mosekTools.solver.model.math as mMath
import mosekTools.solver.model.bound as mBound


### DAX ###
#symbols = Data.get_index_components("dax").index
#Data.get_data_yahoo(symbols=symbols, start=dt.datetime(2000, 7, 1)).to_csv("data/dax/data.csv")

### load data from csv files
data = Data.get_index_data("dax")
data = data.truncate(before=dt.datetime(2010, 1, 1))

### compute returns
returns = data.pct_change(fill_method="ffill").fillna(0.0)
mu = returns.mean().values
covariance_mat = returns.cov().values

print "Condition number of covariance matrix"
print np.linalg.cond(covariance_mat)

model = mModel.build_model("PFP")

# set of n weights (unconstrained)
weights = mModel.weights(model, "weights", n=len(mu))

# covariance
eVar = mMath.variance(model, "var", weights, 0.5 * covariance_mat)
eProfit = Expr.dot(mu, weights)

# e'*w = 1
mBound.equal(model, Expr.sum(weights), 1.0)

# model maximise
mModel.maximise(model=model, expr=Expr.sub(eProfit, eVar))

w = pd.Series(index=data.columns, data=np.array(weights.level()))

### Results
print "Weights"
print w

print "Sum of Weights"
print w.sum()

print "1-Norm of Weights"
print w.abs().sum()
