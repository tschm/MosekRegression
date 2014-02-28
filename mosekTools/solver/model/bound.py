from mosek.fusion import *


def upper(model, expr, bound):
    """
    upper bound for an expression in a model
    """
    model.constraint(expr, Domain.lessThan(bound))


def lower(model, expr, bound):
    """
    lower bound for an expression in a model
    """
    model.constraint(expr, Domain.greaterThan(bound))


def range(model, expr, lower, upper):
    """
    range bound for an expression in a model
    """
    model.constraint(expr, Domain.inRange(lower, upper))


def equal(model, expr, bound):
    """
    assigned value for an expression in a model
    """
    model.constraint(expr, Domain.equalsTo(bound))
