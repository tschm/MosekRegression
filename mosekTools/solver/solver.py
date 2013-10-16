import numpy as np

import mosekTools.util.util as Util
import finance as fin


def lsq_pos(matrix, rhs):
    """
    min 2-norm (matrix*w - rhs)^2
    s.t. e'w = 1
           w >= 0
    """
    # define model
    model = Util.build_model('lsqPos')
    # weight-variables
    w = fin.weights_long_only(model, matrix.shape[1])

    # e'*w = 1
    fin.fully_invested(model, w)

    # minimization of the residual
    Util.minimise(model=model,
                  expr=Util.l2_norm(model=model,
                                    name="2-norm(res)",
                                    expr=Util.residual(matrix, rhs, w)))

    return np.array(w.level())


def lsq_pos_l1_penalty(matrix, rhs, cost_multiplier, weights_0):
    """
    min 2-norm (matrix*w - rhs)** + 1-norm(cost_multiplier*(w-w0))
    s.t. e'w = 1
           w >= 0
    """
    # define model
    model = Util.build_model('lsqSparse')
    # introduce variable and constraints
    weights = fin.weights_long_only(model, matrix.shape[1])

    # e'*w = 1
    fin.fully_invested(model, weights)

    # sum of squared residuals
    res = Util.residual(matrix, rhs, weights)
    v = Util.l2_norm_squared(model, "2-norm(res)**", res)

    # \Gamma*(w - w0), p is an expression
    p = fin.cost(cost_multiplier, weights, weights_0)
    t = Util.l1_norm(model, 'abs(weights)', p)

    # Minimise v + lambda * t
    Util.minimise(model, Util.sum_weighted(1.0, v, 1.0, t))
    return np.array(weights.level())


def lasso(matrix, rhs, lamb):
    """
    min 2-norm (matrix*w - rhs)^2 + lamb * 1-norm(w)
    """
    # define model	
    model = Util.build_model('lasso')

    # introduce variables and constraints
    w = fin.weights_long_short(model, matrix.shape[1])
    v = Util.l2_norm_squared(model, "2-norm(res)", Util.residual(matrix, rhs, w))
    t = Util.l1_norm(model, "1-norm(w)", w)

    # Minimise v + lambda * t
    Util.minimise(model=model,
                  expr=Util.sum_weighted(c1=1.0, expr1=v, c2=lamb, expr2=t))

    return np.array(w.level())
