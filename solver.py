import numpy as np
import pandas as pd

from mosek.fusion import Expr

import mosekTools.solver.model.model as mModel
import mosekTools.solver.model.math as mMath
import mosekTools.solver.model.bound as mBound


def report(w):
    rep = dict()
    rep["n"] = len(w)
    rep["sum"] = w.sum()
    rep["leverage"] = w.abs().sum()
    return pd.Series(rep)


def experiment1(returns):
    mu = returns.mean().values
    covariance_mat = returns.cov().values

    print "Condition number of covariance matrix"
    print np.linalg.cond(covariance_mat, 2)

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

    return pd.Series(index=returns.columns, data=np.array(weights.level()))


def experiment2(returns, lev=np.infty):
    mu = returns.mean().values
    covariance_mat = returns.cov().values

    print "Condition number of covariance matrix"
    print np.linalg.cond(covariance_mat, 2)

    model = mModel.build_model("PFP")
    # set of n weights (unconstrained)
    weights = mModel.weights(model, "weights", n=len(mu))
    leverage = mMath.l1_norm(model, "leverage", weights)
    # covariance
    eVar = mMath.variance(model, "var", weights, 0.5 * covariance_mat)
    eProfit = Expr.dot(mu, weights)

    mBound.upper(model, leverage, lev)
    # e'*w = 1
    mBound.equal(model, Expr.sum(weights), 1.0)

    # model maximise
    mModel.maximise(model=model, expr=Expr.sub(eProfit, eVar))

    return pd.Series(index=returns.columns, data=np.array(weights.level()))
