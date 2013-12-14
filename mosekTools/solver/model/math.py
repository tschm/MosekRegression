from mosek.fusion import *
import numpy as np


def quad_cone(model, expr1, expr2):
    model.constraint(Expr.vstack(expr1, expr2), Domain.inQCone())


def rotated_quad_cone(model, expr1, expr2, expr3):
    model.constraint(Expr.vstack(expr1, expr2, expr3), Domain.inRotatedQCone())


def absolute(model, name, expr):
    t = model.variable(name, int(expr.size()), Domain.unbounded())

    # (t_i, w_i) \in Q2
    for i in range(0, int(expr.size())):
        quad_cone(model, t.index(i), expr.index(i))

    return t


def l1_norm(model, name, expr):
    """
    Given an expression (e.g. a vector) this returns the L1-norm of this vector as an expression.
    It also introduces n (where n is the size of the expression) auxiliary variables. Mosek requires a name
    for any variable that is added to a model. The user has to specify this name explicitly.
    This requirement may disappear in future version of this API.

    ATTENTION: THIS WORKS ONLY IF expr is a VARIABLE
    """
    return Expr.sum(absolute(model, name, expr))


def l2_norm(model, name, expr):
    """
    Given an expression (e.g. a vector) this returns the L2-norm of this vector as an expression.
    It also introduces an auxiliary variables. Mosek requires a name
    for any variable that is added to a model. The user has to specify this name explicitly.
    This requirement may disappear in future version of this API.
    """
    t = model.variable(name, 1, Domain.unbounded())
    quad_cone(model, t, expr)
    return t


def l2_norm_squared(model, name, expr):
    """
    Given an expression (e.g. a vector) this returns the squared L2-norm of this vector as an expression.
    It also introduces an auxiliary variables. Mosek requires a name
    for any variable that is added to a model. The user has to specify this name explicitly.
    This requirement may disappear in future version of this API.
    """
    t = model.variable(name, 1, Domain.unbounded())
    rotated_quad_cone(model, 0.5, t, expr)
    return t


def linfty_norm(model, name, expr):
    t = model.variable(name, 1, Domain.unbounded())

    # (t, w_i) \in Q2
    for i in range(0, int(expr.size())):
        quad_cone(model, t, expr.index(i))

    return t


def mat_vec_prod(matrix, expr):
    return Expr.mul(DenseMatrix(matrix), expr)


def stdev(model, name, weights, covar):
    a = np.linalg.cholesky(covar)
    return l2_norm(model, name, mat_vec_prod(np.transpose(a), weights))


def variance(model, name, weights, covar):
    a = np.linalg.cholesky(covar)
    return l2_norm_squared(model, name, mat_vec_prod(np.transpose(a), weights))

