import numpy as np
import numpy.testing as nptest

from mosekTools.solver.solver import lasso, lsq_pos


def get_X():
    return np.array([[2.0, 1.0], [0.0, -1.0], [3.0, -1.0]])


def get_y():
    return np.array([1.9, 0.0, 2.5])


def test_Lasso():
    w = lasso(matrix=get_X(), rhs=get_y(), lamb=0.0)
    nptest.assert_array_almost_equal(w, [0.8763256773171494, 0.09210753016243604], 7)


def test_lsqPosFUllInv():
    w = lsq_pos(matrix=get_X(), rhs=get_y())
    nptest.assert_array_almost_equal(w, [0.88334, 0.116655], 5)