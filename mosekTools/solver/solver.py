import numpy as np

from mosek.fusion import Expr

import model.model as mModel
import model.math as mMath
import model.bound as mBound


def __sum_weighted(c1, expr1, c2, expr2):
    return Expr.add(Expr.mul(c1, expr1), Expr.mul(c2, expr2))


def __residual(matrix, rhs, expr):
    """
    Introduce the residual matrix*expr - rhs
    """
    return Expr.sub(mMath.mat_vec_prod(matrix, expr), rhs)


def lsq_pos(matrix, rhs):
    """
    min 2-norm (matrix*w - rhs)^2
    s.t. e'w = 1
           w >= 0
    """
    # define model
    model = mModel.build_model('lsqPos')

    # introduce n non-negative weight variables
    weights = mModel.weights(model, "weights", n=matrix.shape[1], lb=0.0)

    # e'*w = 1
    mBound.equal(model, Expr.sum(weights), 1.0)

    v = mMath.l2_norm(model, "2-norm(res)", expr=__residual(matrix, rhs, weights))

    # minimization of the residual
    mModel.minimise(model=model, expr=v)

    return np.array(weights.level())


def lsq_pos_l1_penalty(matrix, rhs, cost_multiplier, weights_0):
    """
    min 2-norm (matrix*w - rhs)** + 1-norm(cost_multiplier*(w-w0))
    s.t. e'w = 1
           w >= 0
    """
    # define model
    model = mModel.build_model('lsqSparse')

    # introduce n non-negative weight variables
    weights = mModel.weights(model, "weights", n=matrix.shape[1], lb=0.0)

    # e'*w = 1
    mBound.equal(model, Expr.sum(weights), 1.0)

    # sum of squared residuals
    v = mMath.l2_norm_squared(model, "2-norm(res)**", __residual(matrix, rhs, weights))

    # \Gamma*(w - w0), p is an expression
    p = mMath.mat_vec_prod(cost_multiplier, Expr.sub(weights, weights_0))
    t = mMath.l1_norm(model, 'abs(weights)', p)

    # Minimise v + t
    mModel.minimise(model, __sum_weighted(1.0, v, 1.0, t))
    return np.array(weights.level())


def lasso(matrix, rhs, lamb):
    """
    min 2-norm (matrix*w - rhs)^2 + lamb * 1-norm(w)
    """
    # define model	
    model = mModel.build_model('lasso')

    # introduce variables and constraints
    w = mModel.weights(model, "weights", matrix.shape[1])
    v = mMath.l2_norm_squared(model, "2-norm(res)**", __residual(matrix, rhs, w))
    t = mMath.l1_norm(model, "1-norm(w)", w)

    # Minimise 1.0*v + lambda * t
    mModel.minimise(model=model, expr=__sum_weighted(c1=1.0, expr1=v, c2=lamb, expr2=t))

    return np.array(w.level())


def mean_variance(exp_ret, covariance_mat, bound):
    # define model
    model = mModel.build_model("mean_var")

    # set of n weights (unconstrained)
    weights = mModel.weights(model, "weights", n=len(exp_ret))

    # standard deviation induced by covariance matrix
    # note that
    # stdev = sqrt(w'Cw) = sqrt(w'L*L'*w)=sqrt(w'A'*Aw)=2-norm(Aw) if A=L'
    a = np.linalg.cholesky(covariance_mat)
    stdev = mMath.l2_norm(model, "std", expr=mMath.mat_vec_prod(np.transpose(a), weights))

    # impose a bound on this standard deviation
    mBound.upper(model, stdev, bound)

    return {"model": model, "expression": Expr.dot(exp_ret, weights), "variable": weights, "objective": mModel.maximise}
