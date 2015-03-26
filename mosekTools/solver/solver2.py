# minimum variance portfolio
import mosek
from mosekTools.solver.model.math import l2_norm_squared
import numpy as np

from mosek.fusion import Model, Expr, Domain, DenseMatrix, ObjectiveSense, BaseModel


def minimum_variance(a):
    # Given the matrix of returns a (each column is a series of returns) this method
    # computes the weights for a minimum variance portfolio, e.g.

    # min   2-Norm[a*w]^2
    # s.t.
    #         w >= 0
    #     sum[w] = 1

    # build the model
    with Model("Minimum Variance") as model:
        # introduce the weight variable
        weights = model.variable("weights", int(a.shape[1]), Domain.inRange(0.0, 1.0))
        # sum of weights have to be 1
        model.constraint(Expr.sum(weights), Domain.equalsTo(1.0))
        # returns
        r = Expr.mul(DenseMatrix(a), weights)
        # compute l2_norm squared of those returns
        v = l2_norm_squared(model, "2-norm^2(r)", expr=r)
        # minimize this l2_norm
        model.objective(ObjectiveSense.Minimize, v)
        # solve the problem
        model.solve()
        # return the series of weights
        return np.array(weights.level())


if __name__ == '__main__':
    # MOSEK (often) requires that the environment variable MOSEKLM_LICENSE_FILE is defined and set to the port on the server
    # that is exposed by the license management program.
    import os
    os.environ["MOSEKLM_LICENSE_FILE"] = "27000@quantsrv"

    from numpy.random import randn

    A = randn(5, 3)

    print minimum_variance(a=A)


    # please note that the Mosek License may still be in cache which could interfere/block subsequent programs running
    # One way to make sure the license is no longer in cache is to use the trick:
    for feat in mosek.feature.values:
        BaseModel._global_env.checkinlicense(feat)
