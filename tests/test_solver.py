from unittest import TestCase

import numpy as np
import numpy.testing as npTest

import mosekTools.solver.solver as sol


class TestSolver(TestCase):
    def __get_X(self):
        return np.array([[2.0, 1.0], [0.0, -1.0], [3.0, -1.0]])

    def __get_y(self):
        return np.array([1.9, 0.0, 2.5])

    def test_lasso(self):
        a = np.linalg.lstsq(self.__get_X(), self.__get_y())
        w = sol.lasso(matrix=self.__get_X(), rhs=self.__get_y(), lamb=0.0)
        npTest.assert_array_almost_equal(w, a[0], 4)

    def test_xxx(self):
        w = sol.lsq_pos_l1_penalty(matrix=self.__get_X(), rhs=self.__get_y(), cost_multiplier=np.array([1.0, 2.0]),
                                   weights_0=np.array([1.0, 2.0]))

    def test_lsq_pos(self):
        w = sol.lsq_pos(matrix=self.__get_X(), rhs=self.__get_y())
        npTest.assert_array_almost_equal(w, [0.88334, 0.116655], 5)

    def test_mean_var(self):
        covar = np.array([[1.0, 0.3], [0.3, 1.0]])
        mu = np.array([0.2, 0.25])

        bound = 1.0

        w1 = sol.markowitz_riskobjective(mu, covar, bound)
        w2 = sol.markowitz(mu, covar, 1.0)

        npTest.assert_array_almost_equal(w1, [0.486757, 0.7396317], 4)
        npTest.assert_array_almost_equal(w2, [0.48215943, 0.51784057], 4)
