# -*- coding: utf-8 -*-
from __future__ import annotations

import numpy as np
from mosek.fusion import BaseModel, Domain, Expr, Matrix, Model, ObjectiveSense


def __sum_weighted(c1, expr1, c2, expr2):
    return Expr.add(Expr.mul(c1, expr1), Expr.mul(c2, expr2))


def __residual(matrix, rhs, expr):
    """
    Introduce the residual matrix*expr - rhs
    """
    return Expr.sub(__mat_vec_prod(matrix, expr), rhs)


def __quad_cone(model, expr1, expr2):
    model.constraint(Expr.vstack(expr1, expr2), Domain.inQCone())


def __rotated_quad_cone(model, expr1, expr2, expr3):
    model.constraint(Expr.vstack(expr1, expr2, expr3), Domain.inRotatedQCone())


def __absolute(model, name, expr):
    t = model.variable(name, expr.getShape(), Domain.unbounded())

    # (t_i, w_i) \in Q2
    for i in range(0, int(expr.getShape())):
        __quad_cone(model, t.index(i), expr.index(i))

    return t


def __l1_norm(model, name, expr):
    """
    Given an expression (e.g. a vector) this returns the L1-norm of this vector
    as an expression.
    It also introduces n (where n is the size of the expression) auxiliary
    variables. Mosek requires a name
    for any variable that is added to a model. The user has to specify
    this name explicitly.
    This requirement may disappear in future version of this API.

    ATTENTION: THIS WORKS ONLY IF expr is a VARIABLE
    """
    return Expr.sum(__absolute(model, name, expr))


def __l2_norm(model, name, expr):
    """
    Given an expression (e.g. a vector) this returns the L2-norm of
    this vector as an expression.
    It also introduces an auxiliary variables. Mosek requires a name
    for any variable that is added to a model. The user has to specify
    this name explicitly.
    This requirement may disappear in future version of this API.
    """
    t = model.variable(name, 1, Domain.unbounded())
    __quad_cone(model, t, expr)
    return t


def __l2_norm_squared(model, name, expr):
    """
    Given an expression (e.g. a vector) this returns the squared
    L2-norm of this vector as an expression.
    It also introduces an auxiliary variables.
    Mosek requires a name
    for any variable that is added to a model. The user has to
    specify this name explicitly.
    This requirement may disappear in future version of this API.
    """
    t = model.variable(name, 1, Domain.unbounded())
    __rotated_quad_cone(model, 0.5, t, expr)
    return t


def __linfty_norm(model, name, expr):
    t = model.variable(name, 1, Domain.unbounded())

    # (t, w_i) \in Q2
    for i in range(0, expr.size()):
        __quad_cone(model, t, expr.index(i))

    return t


def __mat_vec_prod(matrix, expr):
    return Expr.mul(Matrix.dense(matrix), expr)


def __stdev(model, name, weights, covar):
    a = np.linalg.cholesky(covar)
    return __l2_norm(model, name, __mat_vec_prod(np.transpose(a), weights))


def __variance(model, name, weights, covar):
    a = np.linalg.cholesky(covar)
    return __l2_norm_squared(model, name, __mat_vec_prod(np.transpose(a), weights))


def lsq_ls(matrix, rhs):
    """
    min 2-norm (matrix*w - rhs)^2
    s.t. e'w = 1
    """
    # define model
    with Model("lsqPos") as model:
        weights = model.variable(
            "weights", matrix.shape[1], Domain.inRange(-np.infty, +np.infty)
        )

        # e'*w = 1
        model.constraint(Expr.sum(weights), Domain.equalsTo(1.0))

        v = __l2_norm(model, "2-norm(res)", expr=__residual(matrix, rhs, weights))

        # minimization of the residual
        model.objective(ObjectiveSense.Minimize, v)
        # solve the problem
        model.solve()

        return np.array(weights.level())


def lsq_pos(matrix, rhs):
    """
    min 2-norm (matrix*w - rhs)^2
    s.t. e'w = 1
           w >= 0
    """
    # define model
    with Model("lsqPos") as model:
        # introduce n non-negative weight variables
        weights = model.variable("weights", matrix.shape[1], Domain.inRange(0.0, 1.0))

        # e'*w = 1
        model.constraint(Expr.sum(weights), Domain.equalsTo(1.0))

        v = __l2_norm(model, "2-norm(res)", expr=__residual(matrix, rhs, weights))

        # minimization of the residual
        model.objective(ObjectiveSense.Minimize, v)
        # solve the problem
        model.solve()

        return np.array(weights.level())


def lsq_pos_l1_penalty(matrix, rhs, cost_multiplier, weights_0):
    """
    min 2-norm (matrix*w - rhs)** + 1-norm(cost_multiplier*(w-w0))
    s.t. e'w = 1
           w >= 0
    """
    # define model
    with Model("lsqSparse") as model:
        # introduce n non-negative weight variables
        weights = model.variable(
            "weights", matrix.shape[1], Domain.inRange(0.0, +np.infty)
        )

        # e'*w = 1
        model.constraint(Expr.sum(weights), Domain.equalsTo(1.0))

        # sum of squared residuals
        v = __l2_norm_squared(model, "2-norm(res)**", __residual(matrix, rhs, weights))

        # \Gamma*(w - w0), p is an expression
        p = Expr.mulElm(cost_multiplier, Expr.sub(weights, weights_0))

        cost = model.variable("cost", matrix.shape[1], Domain.unbounded())
        model.constraint(Expr.sub(cost, p), Domain.equalsTo(0.0))

        t = __l1_norm(model, "abs(weights)", cost)

        # Minimise v + t
        model.objective(ObjectiveSense.Minimize, __sum_weighted(1.0, v, 1.0, t))
        # solve the problem
        model.solve()

        return np.array(weights.level())


def lasso(matrix, rhs, lamb):
    """
    min 2-norm (matrix*w - rhs)^2 + lamb * 1-norm(w)
    """
    # define model
    with Model("lasso") as model:
        weights = model.variable(
            "weights", matrix.shape[1]
        )  # , Domain.inRange(-np.infty, +np.infty))
        # introduce variables and constraints

        v = __l2_norm_squared(model, "2-norm(res)**", __residual(matrix, rhs, weights))
        t = __l1_norm(model, "1-norm(w)", weights)

        model.objective(
            ObjectiveSense.Minimize, __sum_weighted(c1=1.0, expr1=v, c2=lamb, expr2=t)
        )
        # solve the problem
        model.solve()

        return np.array(weights.level())


def markowitz_riskobjective(exp_ret, covariance_mat, bound):
    # define model
    with Model("mean var") as model:
        # set of n weights (unconstrained)
        weights = model.variable("weights", len(exp_ret), Domain.inRange(0.0, 1.0))

        # standard deviation induced by covariance matrix
        stdev = __stdev(model, "std", weights, covariance_mat)

        # impose a bound on this standard deviation
        # mBound.upper(model, stdev, bound)
        model.constraint(stdev, Domain.lessThan(bound))

        # mModel.maximise(model=model, expr=Expr.dot(exp_ret, weights))
        model.objective(ObjectiveSense.Maximize, Expr.dot(exp_ret, weights))
        # solve the problem
        model.solve()

        return np.array(weights.level())


def markowitz(exp_ret, covariance_mat, aversion):
    # define model
    with Model("mean var") as model:
        # set of n weights (unconstrained)
        weights = model.variable(
            "weights", len(exp_ret), Domain.inRange(-np.infty, +np.infty)
        )

        model.constraint(Expr.sum(weights), Domain.equalsTo(1.0))

        # standard deviation induced by covariance matrix
        var = __variance(model, "var", weights, covariance_mat)

        model.objective(
            ObjectiveSense.Maximize,
            Expr.sub(Expr.dot(exp_ret, weights), Expr.mul(aversion, var)),
        )
        model.solve()
        return np.array(weights.level())


def minimum_variance(matrix):
    # Given the matrix of returns a (each column is a series of returns) this method
    # computes the weights for a minimum variance portfolio, e.g.

    # min   2-Norm[a*w]^2
    # s.t.
    #         w >= 0
    #     sum[w] = 1

    # This is the left-most point on the efficiency frontier in the classic
    # Markowitz theory

    # build the model
    with Model("Minimum Variance") as model:
        # introduce the weight variable

        weights = model.variable("weights", matrix.shape[1], Domain.inRange(0.0, 1.0))
        # sum of weights has to be 1
        model.constraint(Expr.sum(weights), Domain.equalsTo(1.0))
        # returns
        r = Expr.mul(Matrix.dense(matrix), weights)
        # compute l2_norm squared of those returns
        # minimize this l2_norm
        model.objective(
            ObjectiveSense.Minimize, __l2_norm_squared(model, "2-norm^2(r)", expr=r)
        )
        # solve the problem
        model.solve()
        # return the series of weights
        return np.array(weights.level())


if __name__ == "__main__":
    # MOSEK (often) requires that the environment variable
    # MOSEKLM_LICENSE_FILE is defined and set to the port on the server
    # that is exposed by the license management program.
    import mosek
    from numpy.random import randn

    A = randn(5, 3)

    print(minimum_variance(matrix=A))

    # please note that the Mosek License may still be in cache which could
    # interfere/block subsequent programs running
    # One way to make sure the license is no longer in cache is to use the trick:
    for feat in mosek.feature.values:
        BaseModel._global_env.checkinlicense(feat)
