from mosek.fusion import *


def upper(model, expr, bound):
    model.constraint(expr, Domain.lessThan(bound))


def lower(model, expr, bound):
    model.constraint(expr, Domain.greaterThan(bound))


def range(model, expr, lower, upper):
    model.constraint(expr, Domain.inRange(lower, upper))


def equal(model, expr, bound):
    model.constraint(expr, Domain.equalsTo(bound))
