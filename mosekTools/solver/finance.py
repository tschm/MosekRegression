from mosek.fusion import *
import mosekTools.util.util as Util


def fully_invested(model, weights):
    """
    Enforce that the sum of weights is 1.0
    """
    model.constraint(Expr.sum(weights), Domain.equalsTo(1.0))


def market_neutral(model, weights):
    """
    Enforce that the sum of weights is 0.0
    """
    model.constraint(Expr.sum(weights), Domain.equalsTo(0.0))


def max_leverage(model, weights, bound):
    """
    This is a bound for the 1-norm of the weights
    """
    t = Util.l1_norm(model, "leverage", weights)
    model.constraint(t, Domain.lessThan(bound))


def weights_long_only(model, n):
    """
    Introduce n positive weights for the portfolio
    """
    return model.variable("weights", n, Domain.greaterThan(0.0))


def weights_long_short(model, n):
    """
    Introduce n unbounded weights for the portfolio
    """
    return model.variable("weights", n, Domain.unbounded())


def cost(matrix, weights, weights_0):
    """
     Cost term matrix*(weights - weights_0)
    """
    return Expr.mul(DenseMatrix(matrix), Expr.sub(weights, weights_0))