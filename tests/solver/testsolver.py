import numpy as np
import numpy.testing as npTest

from mosekTools.solver.solver import lasso, lsq_pos

#Contents:
#
#.. toctree::
#   :maxdepth: 3

def get_X():
    return np.array([[2.0, 1.0], [0.0, -1.0], [3.0, -1.0]])


def get_y():
    return np.array([1.9, 0.0, 2.5])


def test_lasso():
    w = lasso(matrix=get_X(), rhs=get_y(), lamb=0.0)
    npTest.assert_array_almost_equal(w, [0.8763256773171494, 0.09210753016243604], 7)


def test_lsq_pos():
    w = lsq_pos(matrix=get_X(), rhs=get_y())
    npTest.assert_array_almost_equal(w, [0.88334, 0.116655], 5)