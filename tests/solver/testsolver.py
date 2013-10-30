import numpy as np
import numpy.testing as npTest

import mosekTools.solver.solver as sol


def get_X():
    return np.array([[2.0, 1.0], [0.0, -1.0], [3.0, -1.0]])


def get_y():
    return np.array([1.9, 0.0, 2.5])


def test_lasso():
    w = sol.lasso(matrix=get_X(), rhs=get_y(), lamb=0.0)
    npTest.assert_array_almost_equal(w, [0.8763256773171494, 0.09210753016243604], 7)


def test_lsq_pos():
    w = sol.lsq_pos(matrix=get_X(), rhs=get_y())
    npTest.assert_array_almost_equal(w, [0.88334, 0.116655], 5)


def test_mean_var():
    covar = np.array([[1.0, 0.3], [0.3, 1.0]])
    mu = np.array([0.2, 0.25])

    bound = 1.0

    w1 = sol.markowitz_riskobjective(mu, covar, bound)
    w2 = sol.markowitz(mu, covar, 1.0)

    npTest.assert_array_almost_equal(w1, [0.486757, 0.7396317], 7)
    npTest.assert_array_almost_equal(w2, [0.48215943, 0.51784057], 7)
