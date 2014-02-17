from mosek.fusion import *
import numpy as np


def weights(model, name, n, lb=-np.infty, ub=np.infty):
    """
    Introduce n positive weights for the portfolio
    """
    return model.variable(name, int(n), Domain.inRange(lb, ub))


def build_model(name):
    """
    build a mosek.fusion model
    """
    return Model(name)


def minimise(model, expr):
    """
    minimise the expr
    """
    model.objective(ObjectiveSense.Minimize, expr)
    model.solve()


def maximise(model, expr):
    """
    maximise the expr
    """
    model.objective(ObjectiveSense.Maximize, expr)
    model.solve()

